import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin

import psycopg2
from psycopg2.extras import execute_batch
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PakistanSquadScraper:
    BASE_URL = 'https://www.sportskeeda.com'
    TEAM_PATH = '/team/pakistan-cricket-team'
    TEAM_NAME = 'Pakistan'
    FORMAT_MAP = {
        't20i': 'T20I',
        'test': 'TEST',
        'odi': 'ODI',
    }

    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self.session = requests.Session()
        self.session.headers.update(
            {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/123.0 Safari/537.36'
                )
            }
        )

    def get_db_connection(self):
        try:
            return psycopg2.connect(
                host=self.db_config['host'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                port=self.db_config['port'],
            )
        except Exception as exc:
            logger.error('Database connection failed: %s', exc)
            return None

    def create_table(self) -> bool:
        conn = self.get_db_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS team_squad_players ('
                    ' id SERIAL PRIMARY KEY,'
                    ' team_name VARCHAR(100) NOT NULL,'
                    ' format VARCHAR(20) NOT NULL,'
                    ' player_name VARCHAR(255) NOT NULL,'
                    ' player_info TEXT,'
                    ' additional_info TEXT,'
                    ' player_link VARCHAR(500),'
                    ' image_url VARCHAR(500),'
                    ' scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                    ' UNIQUE (team_name, format, player_name)'
                    ')'
                )
            conn.commit()
            logger.info('Ensured team_squad_players table exists')
            return True
        except Exception as exc:
            conn.rollback()
            logger.error('Error creating team_squad_players table: %s', exc)
            return False
        finally:
            conn.close()

    def fetch_page(self) -> Optional[str]:
        try:
            url = f'{self.BASE_URL}{self.TEAM_PATH}'
            logger.info('Fetching squad page: %s', url)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as exc:
            logger.error('Failed to fetch squad page: %s', exc)
            return None

    def parse_squad(self, html: str) -> Dict[str, List[Dict[str, Optional[str]]]]:
        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find('div', class_='team-squad-container')
        if not container:
            logger.error('Unable to locate squad container on page')
            return {}

        squads: Dict[str, List[Dict[str, Optional[str]]]] = {}
        sections = container.find_all('div', class_='team-squads-detail')

        for section in sections:
            section_id = section.get('id', '')
            format_key = section_id.rsplit('-', 1)[-1].lower() if section_id else ''
            format_name = self.FORMAT_MAP.get(format_key)
            if not format_name:
                logger.debug('Skipping unknown squad section with id: %s', section_id)
                continue

            players = self.parse_players(section)
            logger.info('Parsed %d players for %s squad', len(players), format_name)
            squads[format_name] = players

        return squads

    def parse_players(self, section) -> List[Dict[str, Optional[str]]]:
        player_map: Dict[str, Dict[str, Optional[str]]] = {}
        order: List[str] = []
        for block in section.find_all('div', class_='squad-players'):
            name_tag = block.select_one('.team-squad-player--name')
            if not name_tag:
                continue

            player_name = name_tag.get_text(strip=True)
            if not player_name:
                continue

            info_tag = block.select_one('.team-squad-player--batting-style')
            player_info = info_tag.get_text(strip=True) if info_tag else None

            info_parts: List[str] = []
            info_container = block.select_one('.team-squad-info')
            if info_container:
                extra_text = info_container.get_text(' ', strip=True)
                if extra_text:
                    info_parts.append(extra_text)

            title_tag = block.select_one('.captain-title')
            if title_tag:
                title_text = title_tag.get_text(strip=True)
                if title_text:
                    info_parts.append(title_text)

            additional_info = self._normalize_info_parts(info_parts)

            link_tag = block.find('a', class_='team-player-link')
            player_link = urljoin(self.BASE_URL, link_tag['href']) if link_tag and link_tag.get('href') else None

            image_tag = block.select_one('.team-player-img img')
            image_url = self.extract_image_url(image_tag)

            existing = player_map.get(player_name)
            if existing:
                if not existing.get('player_info') and player_info:
                    existing['player_info'] = player_info
                existing['additional_info'] = self._merge_info_strings(
                    existing.get('additional_info'), additional_info
                )
                if not existing.get('player_link') and player_link:
                    existing['player_link'] = player_link
                if not existing.get('image_url') and image_url:
                    existing['image_url'] = image_url
            else:
                player_map[player_name] = {
                    'player_name': player_name,
                    'player_info': player_info,
                    'additional_info': additional_info,
                    'player_link': player_link,
                    'image_url': image_url,
                }
                order.append(player_name)

        return [player_map[name] for name in order]

    def _normalize_info_parts(self, parts: List[str]) -> Optional[str]:
        unique: List[str] = []
        for part in parts:
            cleaned = part.strip()
            if cleaned and cleaned not in unique:
                unique.append(cleaned)
        return '; '.join(unique) if unique else None

    def _merge_info_strings(self, current: Optional[str], new_value: Optional[str]) -> Optional[str]:
        values: List[str] = []
        for source in (current, new_value):
            if not source:
                continue
            for item in source.split(';'):
                cleaned = item.strip()
                if cleaned and cleaned not in values:
                    values.append(cleaned)
        return '; '.join(values) if values else None

    def extract_image_url(self, img_tag) -> Optional[str]:
        if not img_tag:
            return None

        candidates: List[str] = []
        fallback = img_tag.get('data-img-fallbacks')
        if fallback:
            candidates.extend([val.strip() for val in fallback.split('|:|:|') if val.strip()])

        src = img_tag.get('src')
        if src:
            candidates.append(src.strip())

        for candidate in candidates:
            if not candidate or candidate.startswith('data:'):
                continue
            if candidate.startswith('//'):
                return f'https:{candidate}'
            if candidate.startswith('/'):
                return urljoin(self.BASE_URL, candidate)
            return candidate

        return None

    def save_to_database(self, squads: Dict[str, List[Dict[str, Optional[str]]]]) -> bool:
        if not squads:
            logger.error('No squad data to persist')
            return False

        conn = self.get_db_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                upsert_query = (
                    'INSERT INTO team_squad_players (team_name, format, player_name, player_info, additional_info, '
                    'player_link, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s) '
                    'ON CONFLICT (team_name, format, player_name) DO UPDATE SET '
                    'player_info = EXCLUDED.player_info, '
                    'additional_info = EXCLUDED.additional_info, '
                    'player_link = EXCLUDED.player_link, '
                    'image_url = EXCLUDED.image_url, '
                    'scraped_at = NOW()'
                )

                for format_name, players in squads.items():
                    logger.info('Persisting %d players for %s', len(players), format_name)
                    cursor.execute(
                        'DELETE FROM team_squad_players WHERE team_name = %s AND format = %s',
                        (self.TEAM_NAME, format_name),
                    )

                    if not players:
                        continue

                    values = [
                        (
                            self.TEAM_NAME,
                            format_name,
                            player['player_name'],
                            player.get('player_info'),
                            player.get('additional_info'),
                            player.get('player_link'),
                            player.get('image_url'),
                        )
                        for player in players
                    ]

                    execute_batch(cursor, upsert_query, values)

            conn.commit()
            logger.info('Squad data saved successfully')
            return True
        except Exception as exc:
            conn.rollback()
            logger.error('Error saving squad data: %s', exc)
            return False
        finally:
            conn.close()

    def scrape_and_store(self) -> bool:
        if not self.create_table():
            return False

        html = self.fetch_page()
        if not html:
            return False

        squads = self.parse_squad(html)
        if not squads:
            logger.error('Parsed squad data is empty')
            return False

        return self.save_to_database(squads)


def main():
    db_config = {
        'host': 'localhost',
        'database': 'cricket_db',
        'user': 'postgres',
        'password': 'admin123',
        'port': 5432,
    }

    scraper = PakistanSquadScraper(db_config)
    success = scraper.scrape_and_store()

    if success:
        logger.info('Pakistan squad scraping completed successfully')
    else:
        logger.error('Pakistan squad scraping failed')


if __name__ == '__main__':
    main()
