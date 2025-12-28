# Cricket Stadium Pitch Scraper

This project scrapes cricket stadium pitch information from pitch-report.com and stores it in a PostgreSQL database.

## Features

- Scrapes stadium URLs from the main pitch-report.com page
- Extracts pitch information from individual stadium pages
- Determines if a pitch is batting-friendly, bowling-friendly, or mixed
- Stores data in PostgreSQL database with proper schema
- Includes error handling and logging
- Respectful scraping with delays between requests

## Setup

### Prerequisites

1. Python 3.7+
2. PostgreSQL database
3. Internet connection

### Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database:
```sql
CREATE DATABASE cricket_db;
```

3. Ensure PostgreSQL is running and accessible with the credentials:
   - Host: localhost
   - Database: cricket_db
   - Username: postgres
   - Password: admin123
   - Port: 5432

## Usage

### Run the complete scraper:
```bash
python cricket_scraper.py
```

### Test the scraper:
```bash
python test_scraper.py
```

## Database Schema

The scraper creates a table called `stadiums` with the following structure:

```sql
CREATE TABLE stadiums (
    id SERIAL PRIMARY KEY,
    ground_name VARCHAR(255) NOT NULL,
    pitch_type VARCHAR(50),
    pitch_description TEXT,
    url VARCHAR(500),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## How it Works

1. **URL Extraction**: The scraper visits the main pitch-report.com page and extracts all stadium URLs
2. **Data Extraction**: For each stadium URL, it:
   - Extracts the ground name from the URL
   - Searches for "Batting Pitch Or Bowling Pitch?" section
   - Extracts the description paragraph below this heading
   - Determines pitch type based on the description content
3. **Database Storage**: Saves the extracted information to PostgreSQL

## Configuration

You can modify the database configuration in the `main()` function of `cricket_scraper.py`:

```python
db_config = {
    'host': 'localhost',
    'database': 'cricket_db',
    'user': 'postgres',
    'password': 'admin123',
    'port': 5432
}
```

## Error Handling

The scraper includes comprehensive error handling:
- Database connection errors
- Network request failures
- HTML parsing errors
- Missing data scenarios

All errors are logged with timestamps for debugging.

## Notes

- The scraper includes a 2-second delay between requests to be respectful to the server
- Uses proper User-Agent headers to avoid being blocked
- Handles both relative and absolute URLs
- Removes duplicate URLs automatically
- Uses ON CONFLICT DO NOTHING to avoid duplicate entries

## Troubleshooting

1. **Database Connection Issues**: Ensure PostgreSQL is running and the database exists
2. **Network Issues**: Check internet connection and firewall settings
3. **Parsing Issues**: The website structure might have changed, check the HTML structure
4. **Permission Issues**: Ensure the database user has proper permissions

## Example Output

The scraper will log progress and save data like:

```
2024-01-15 10:30:15 - INFO - Found 25 stadium URLs
2024-01-15 10:30:17 - INFO - Processing stadium 1/25: https://pitch-report.com/rajiv-gandhi-international-stadium-pitch-report/
2024-01-15 10:30:19 - INFO - Saved data for Rajiv Gandhi International Stadium
...
2024-01-15 10:35:45 - INFO - Scraping completed. Successfully processed 23/25 stadiums
```
This is for Ground Pitch Scraping
python cricket_scraper.py
python view_data.py
python summary.py
## Pakistan Squad Scraper

Use the Sportskeeda scraper to capture Pakistan squad information (T20I, TEST, ODI) and store it in the `team_squad_players` table.

### Run the squad scraper
- `python pakistan_squad_scraper.py`

### Verify squad data
Run simple checks in PostgreSQL, for example:
- `SELECT format, COUNT(*) FROM team_squad_players WHERE team_name = 'Pakistan' GROUP BY format ORDER BY format;`
- `SELECT player_name, player_info FROM team_squad_players WHERE team_name = 'Pakistan' AND format = 'T20I' LIMIT 5;`

### Table schema
The scraper ensures the following columns exist in `team_squad_players`:
- `id SERIAL PRIMARY KEY`
- `team_name VARCHAR(100)`
- `format VARCHAR(20)`
- `player_name VARCHAR(255)`
- `player_info TEXT`
- `additional_info TEXT`
- `player_link VARCHAR(500)`
- `image_url VARCHAR(500)`
- `scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- `UNIQUE (team_name, format, player_name)`

## Player Profile Scraper

Use `player_profile_scraper.py` to enrich each squad player with personal information plus aggregate batting and bowling statistics.

### Run the profile scraper
- `python player_profile_scraper.py`

### What gets stored
- Personal information stored as key/value JSON (e.g., Full Name, Date of Birth, Height).
- Batting and bowling stats saved as JSON arrays (one entry per game type).
- Data lands in the `player_profiles` table.

### Verify profile data
- `SELECT COUNT(*) FROM player_profiles;`
- `SELECT player_name, jsonb_array_length(batting_stats) FROM player_profiles ORDER BY player_name LIMIT 5;`

### Table schema (`player_profiles`)
- `id SERIAL PRIMARY KEY`
- `player_name VARCHAR(255)`
- `profile_url VARCHAR(500) UNIQUE`
- `personal_info JSONB`
- `batting_stats JSONB`
- `bowling_stats JSONB`
- `scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`

## Embeddings + FAISS Vector DB

Create row-wise embeddings from your PostgreSQL tables and store them in FAISS.

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the embeddings pipeline
```bash
python embeddings_pipeline.py --tables team_squad_player stadium_patch_info player_profile --model all-MiniLM-L6-v2 --out faiss_indexes
```

Notes:
- Aliases are resolved automatically:
  - `team_squad_player` -> `team_squad_players`
  - `stadium_patch_info` -> `stadiums`
  - `player_profile` -> `player_profiles`
- Defaults use the database config shown above (localhost, `cricket_db`).
- The pipeline builds separate FAISS indexes per table in `faiss_indexes/` and also writes JSONL metadata and a manifest for each table.

### Output artifacts per table
- `faiss_indexes/<table>.index` — FAISS index with normalized embeddings (cosine similarity).
- `faiss_indexes/<table>_meta.jsonl` — one line per vector: `{vector_id, pk, table, text}`.
- `faiss_indexes/<table>_manifest.json` — summary including model, dimension, and counts.

### Customization
- Pick a different model via `--model` (e.g., `all-mpnet-base-v2`).
- Limit to specific tables by passing `--tables` with only those names.
- If your DB uses different table names, pass them directly (the pipeline falls back to generic text rendering).

## Cricket AI Squad - Video Classification

This repository also includes the Cricket AI Squad web application with video classification functionality.

### Components

1. **Frontend**: React/Vite application in `cricket-ai-squad-main/`
2. **Backend**: FastAPI server in `api.py` for video classification
3. **Stadiums API**: FastAPI server in `stadiums_api.py` for stadium data

### Setup

1. Install frontend dependencies:
   ```bash
   cd cricket-ai-squad-main
   npm install
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. The requirements now include `psycopg2-binary` for database connectivity

### Running the Application

#### Method 1: Using the Batch Script (Windows)

Double-click `start-dev.bat` to automatically:
1. Install backend dependencies
2. Start the backend API server
3. Start the stadiums API server
4. Start the frontend development server

#### Method 2: Manual Start

1. **Start the Backend API**:
   ```bash
   python api.py
   ```

2. **Start the Stadiums API**:
   ```bash
   python stadiums_api.py
   ```

3. **Start the Frontend**:
   ```bash
   cd cricket-ai-squad-main
   npm run dev
   ```

### Accessing the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Stadiums API**: http://localhost:8001
- **API Documentation**: http://localhost:8000/docs

For more detailed information about the integration, see `INTEGRATION-GUIDE.md`.

If you encounter any issues, please refer to `TROUBLESHOOTING.md` for common solutions.
