import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import re
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CricketStadiumScraper:
    def __init__(self, db_config):
        self.db_config = db_config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_db_connection(self):
        """Create database connection"""
        try:
            conn = psycopg2.connect(
                host=self.db_config['host'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                port=self.db_config['port']
            )
            return conn
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return None
    
    def create_table(self):
        """Create the stadiums table if it doesn't exist"""
        conn = self.get_db_connection()
        if not conn:
            return False
            
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS stadiums (
                        id SERIAL PRIMARY KEY,
                        ground_name VARCHAR(255) NOT NULL,
                        pitch_type VARCHAR(50),
                        pitch_description TEXT,
                        url VARCHAR(500),
                        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("Table created successfully")
                return True
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            return False
        finally:
            conn.close()
    
    def extract_stadium_urls(self, main_url):
        """Extract stadium URLs from the main page"""
        try:
            response = self.session.get(main_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for links that contain stadium names
            # These are typically in the format: /stadium-name-pitch-report/
            stadium_urls = []
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href')
                if href and 'pitch-report' in href and href != main_url:
                    # Convert relative URLs to absolute URLs
                    full_url = urljoin(main_url, href)
                    stadium_urls.append(full_url)
            
            # Remove duplicates
            stadium_urls = list(set(stadium_urls))
            logger.info(f"Found {len(stadium_urls)} stadium URLs")
            
            return stadium_urls
            
        except Exception as e:
            logger.error(f"Error extracting stadium URLs: {e}")
            return []
    
    def extract_pitch_info(self, stadium_url):
        """Extract pitch information from individual stadium page"""
        try:
            response = self.session.get(stadium_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract ground name from URL or page title
            ground_name = self.extract_ground_name(stadium_url, soup)
            
            # Look for the "Batting Pitch Or Bowling Pitch?" section
            pitch_type = None
            pitch_description = None
            
            # Find the heading that contains "Batting Pitch Or Bowling Pitch?"
            heading = soup.find(text=re.compile(r'Batting Pitch Or Bowling Pitch\?', re.IGNORECASE))
            
            if heading:
                # Find the parent element and look for the next paragraph
                parent = heading.parent
                if parent:
                    # Look for the next paragraph or div containing the description
                    next_element = parent.find_next(['p', 'div'])
                    if next_element:
                        pitch_description = next_element.get_text(strip=True)
                        
                        # Determine pitch type based on description
                        description_lower = pitch_description.lower()
                        if 'batting' in description_lower and 'bowling' not in description_lower:
                            pitch_type = 'Batting'
                        elif 'bowling' in description_lower and 'batting' not in description_lower:
                            pitch_type = 'Bowling'
                        elif 'batting' in description_lower and 'bowling' in description_lower:
                            # Check which one is emphasized more
                            batting_count = description_lower.count('batting')
                            bowling_count = description_lower.count('bowling')
                            pitch_type = 'Batting' if batting_count > bowling_count else 'Bowling'
                        else:
                            pitch_type = 'Mixed'
            
            return {
                'ground_name': ground_name,
                'pitch_type': pitch_type,
                'pitch_description': pitch_description,
                'url': stadium_url
            }
            
        except Exception as e:
            logger.error(f"Error extracting pitch info from {stadium_url}: {e}")
            return None
    
    def extract_ground_name(self, url, soup):
        """Extract ground name from URL or page content"""
        try:
            # Try to extract from URL first
            url_path = urlparse(url).path
            if url_path:
                # Remove /pitch-report/ and replace hyphens with spaces
                name_part = url_path.replace('/pitch-report/', '').replace('/', '')
                if name_part:
                    ground_name = name_part.replace('-', ' ').title()
                    return ground_name
            
            # Fallback to page title
            title = soup.find('title')
            if title:
                title_text = title.get_text(strip=True)
                # Extract stadium name from title
                if 'Pitch Report' in title_text:
                    ground_name = title_text.replace('Pitch Report', '').strip()
                    return ground_name
            
            return "Unknown Stadium"
            
        except Exception as e:
            logger.error(f"Error extracting ground name: {e}")
            return "Unknown Stadium"
    
    def save_to_database(self, stadium_data):
        """Save stadium data to database"""
        conn = self.get_db_connection()
        if not conn:
            return False
            
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO stadiums (ground_name, pitch_type, pitch_description, url)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    stadium_data['ground_name'],
                    stadium_data['pitch_type'],
                    stadium_data['pitch_description'],
                    stadium_data['url']
                ))
                conn.commit()
                logger.info(f"Saved data for {stadium_data['ground_name']}")
                return True
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            return False
        finally:
            conn.close()
    
    def scrape_all_stadiums(self, main_url):
        """Main method to scrape all stadiums"""
        logger.info("Starting stadium scraping process...")
        
        # Create table
        if not self.create_table():
            logger.error("Failed to create table")
            return False
        
        # Extract stadium URLs
        stadium_urls = self.extract_stadium_urls(main_url)
        if not stadium_urls:
            logger.error("No stadium URLs found")
            return False
        
        # Process each stadium
        success_count = 0
        for i, url in enumerate(stadium_urls, 1):
            logger.info(f"Processing stadium {i}/{len(stadium_urls)}: {url}")
            
            stadium_data = self.extract_pitch_info(url)
            if stadium_data:
                if self.save_to_database(stadium_data):
                    success_count += 1
                else:
                    logger.error(f"Failed to save data for {url}")
            else:
                logger.error(f"Failed to extract data from {url}")
            
            # Add delay to be respectful to the server
            time.sleep(2)
        
        logger.info(f"Scraping completed. Successfully processed {success_count}/{len(stadium_urls)} stadiums")
        return True

def main():
    # Database configuration
    db_config = {
        'host': 'localhost',
        'database': 'cricket_db',
        'user': 'postgres',
        'password': 'admin123',
        'port': 5432
    }
    
    # Main URL to scrape
    main_url = "https://pitch-report.com/"
    
    # Create scraper instance
    scraper = CricketStadiumScraper(db_config)
    
    # Start scraping
    scraper.scrape_all_stadiums(main_url)

if __name__ == "__main__":
    main()
