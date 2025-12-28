# Cricket APIs

This project includes two APIs:

1. **Shot Classification API** - Provides cricket shot classification functionality using a TensorFlow model
2. **Stadiums API** - Provides access to stadium data from the database

## Setup Instructions

1. Install the required dependencies:
   ```
   pip install -r requirements-api.txt
   ```

2. Make sure you have the `model_weights.h5` file in the same directory as `api.py`.

3. Run the API server:
   ```
   python api.py
   ```

4. The API will be available at `http://localhost:8000`

## API Endpoints

### Shot Classification API

#### POST `/classify-video/`

Upload a cricket video for shot classification.

**Request:**
- Form data with a `file` field containing the video file

**Response:**
```json
{
  "shotType": "Cover Drive",
  "confidence": 95.5,
  "shotsDetected": ["Cover Drive"],
  "footworkQuality": 85,
  "timingClassification": "Excellent",
  "shotTypeRecognition": ["Cover Drive: 100%"],
  "balanceAnalysis": 78,
  "keyFrames": ["/placeholder.svg", "/placeholder.svg", ...],
  "recommendations": [
    "Focus on improving your cover drive technique",
    "Maintain proper body alignment during shots",
    "Practice consistent footwork for better balance"
  ]
}
```

### Stadiums API

#### GET `/stadiums`

Fetch all stadiums from the database.

**Response:**
```json
[
  {
    "id": 1,
    "ground_name": "Melbourne Cricket Ground",
    "pitch_type": "Batting",
    "pitch_description": "Known for high scores and batting friendly pitches",
    "url": "https://pitch-report.com/melbourne-cricket-ground-pitch-report/",
    "scraped_at": "2024-01-15T10:30:19.123456"
  }
]
```

#### GET `/stadiums/{id}`

Fetch a specific stadium by ID.

**Response:**
```json
{
  "id": 1,
  "ground_name": "Melbourne Cricket Ground",
  "pitch_type": "Batting",
  "pitch_description": "Known for high scores and batting friendly pitches",
  "url": "https://pitch-report.com/melbourne-cricket-ground-pitch-report/",
  "scraped_at": "2024-01-15T10:30:19.123456"
}
```

## Integration with Frontend

The frontend application should:
1. Send a POST request to `http://localhost:8000/classify-video/` with the video file in the request body as form data.
2. Send a GET request to `http://localhost:8001/stadiums` to fetch stadium data.

CORS is enabled for all origins in development, but this should be restricted in production.