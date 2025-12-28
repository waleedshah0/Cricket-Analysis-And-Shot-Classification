 # Cricket AI Squad & Shot Classification System

A comprehensive AI-powered cricket analysis platform that combines squad generation with advanced video-based shot classification. Built with React, FastAPI, and TensorFlow.

## 🎯 Features

### Squad Generation
- **Real-time Player Database Integration**: Fetch players from PostgreSQL database
- **Format-based Selection**: Generate squads for Test, ODI, and T20I formats
- **Player Profiles**: View complete player statistics and performance metrics
- **Stadium Selection**: Choose from real cricket grounds

### Video Analysis
- **AI Shot Classification**: Classify cricket shots using deep learning
- **Top 3 Predictions**: Get the top 3 most likely shot types with confidence scores
- **Video Playback**: Review uploaded videos with playback controls
- **Real-time Analysis**: Instant feedback with AI recommendations

### Player Management
- **Squad Database**: 52 players with comprehensive statistics
- **Player Profiles**: 34 players with complete profile data
- **Statistics Extraction**: JSON-based batting and bowling statistics
- **Smart Matching**: Intelligent player lookup by name

## 🏗️ Architecture

```
├── Frontend (React + TypeScript + Vite)
│   ├── Squad Generator
│   ├── Batting Analysis (Video Classification)
│   ├── Player Details
│   └── Dark-themed UI with Tailwind CSS
│
├── Backend APIs
│   ├── Video Classification API (FastAPI) - Port 8000
│   ├── Stadium & Player API (FastAPI) - Port 8001
│   └── Database Integration (PostgreSQL)
│
└── Data Processing
    ├── Video Frame Extraction
    ├── Model Inference (EfficientNetB0 + GRU)
    └── Statistics Parsing from JSON
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Git

### Backend Setup

```powershell
# Navigate to project directory
cd d:\cricket

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Start Video Classification API (Port 8000)
python api.py

# In a new terminal, start Stadium/Player API (Port 8001)
python stadiums_api.py
```

### Frontend Setup

```powershell
# Navigate to frontend directory
cd cricket-ai-squad-main

# Install dependencies
npm install

# Start development server (Port 8081)
npm run dev
```

## 📊 API Endpoints

### Video Classification API (Port 8000)
- **POST `/classify-video/`** - Upload and classify cricket shot video
  - Request: Video file (.mp4, .avi, .mov)
  - Response: Shot type, confidence, top 3 predictions, recommendations

### Stadium & Player API (Port 8001)
- **GET `/stadiums`** - List all stadiums
- **GET `/players/{format}`** - Get players by format (Test/ODI/T20I)
- **GET `/player-profile/{player_name}`** - Get player detailed profile

## 🎬 Video Classification Model

- **Architecture**: EfficientNetB0 + GRU + Dense Layers
- **Input**: 30 frames at 224x224 resolution
- **Output**: 10 cricket shot classes with confidence scores
  - Cover Drive, Defense, Flick Shot, Hook Shot, Late Cut
  - Lofted Shot, Pull Shot, Square Cut, Straight Drive, Sweep Shot

### Model Features
- Pre-trained EfficientNetB0 for feature extraction
- Temporal modeling with GRU layers
- Top 3 predictions for user guidance
- Real-time preprocessing with proper normalization

## 📦 Shot Types Recognized

1. **Cover Drive** - Defensive shot played towards cover
2. **Defense** - Defensive/blocking shot
3. **Flick Shot** - Off-side flick shot
4. **Hook Shot** - Aggressive horizontal bat shot
5. **Late Cut** - Cut shot played late
6. **Lofted Shot** - Shot with elevation
7. **Pull Shot** - Horizontal aggressive shot
8. **Square Cut** - Cut shot towards point/square
9. **Straight Drive** - Straight bat shot
10. **Sweep Shot** - Horizontal bat sweep

## 🗄️ Database Schema

### Teams & Players
- `team_squad_players` - 52 players in squad format (Test/ODI/T20I)
- `player_profiles` - 34 players with complete profile data
- Columns include:
  - player_name, player_info, image_url
  - batting_stats (JSON), bowling_stats (JSON)
  - personal_info (Full Name, Age, Nationality, Playing Role)

### Stadiums
- `stadiums` - Cricket ground information
- Columns: id, ground_name, pitch_type, pitch_description

## 🎨 Frontend Features

### Pages
1. **Squad Generator** - Create squads by format
2. **Batting Analysis** - Upload and analyze batting videos
3. **Bowling Analysis** - Bowling-specific analysis (expandable)
4. **Player Details** - View player statistics and profiles

### UI Components
- Dark theme with slate/cyan/violet color scheme
- Responsive design for mobile/tablet/desktop
- Real-time toast notifications
- Loading states and error handling
- Animated transitions with Framer Motion

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```
DATABASE_HOST=localhost
DATABASE_NAME=cricket_db
DATABASE_USER=postgres
DATABASE_PASSWORD=admin123
DATABASE_PORT=5432
```

### Model Configuration
The model loads from `model_weights.h5` on each API request for:
- Latest model weights
- Proper resource isolation
- Easy model updates

## 📝 Project Structure

```
d:\cricket/
├── api.py                          # Video classification API
├── stadiums_api.py                 # Stadium/Player API
├── requirements.txt                # Python dependencies
├── model_weights.h5                # Trained model weights
│
├── cricket-ai-squad-main/          # Frontend React project
│   ├── src/
│   │   ├── pages/
│   │   │   ├── BattingAnalysis.tsx
│   │   │   ├── SquadGenerator.tsx
│   │   │   ├── PlayerDetails.tsx
│   │   │   └── ...
│   │   ├── components/
│   │   └── lib/
│   ├── package.json
│   └── vite.config.ts
│
├── faiss_indexes/                  # Vector search indexes
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Kill Python processes and restart
Get-Process python | Stop-Process -Force
```

### Model Loading Error
- Ensure `model_weights.h5` exists in the project root
- Check file size is reasonable (100MB+)
- Verify model weights match architecture

### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure `cricket_db` database exists

## 📚 API Response Examples

### Video Classification Response
```json
{
  "shotType": "Late Cut",
  "confidence": 99.95,
  "top3Predictions": [
    {
      "shotType": "Late Cut",
      "confidence": 99.95
    },
    {
      "shotType": "Square Cut",
      "confidence": 0.04
    },
    {
      "shotType": "Sweep Shot",
      "confidence": 0.01
    }
  ],
  "shotsDetected": ["Late Cut"],
  "recommendations": [
    "Focus on improving your Late Cut technique",
    "Maintain proper body alignment during shots",
    "Practice consistent footwork for better balance"
  ]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact & Support

For issues, questions, or contributions, please open an issue on GitHub.

## 🙏 Acknowledgments

- EfficientNetB0 for robust feature extraction
- FastAPI for high-performance APIs
- React & TypeScript for modern frontend
- PostgreSQL for reliable data storage
- TensorFlow/Keras for deep learning

---

**Note**: Model weights file (`model_weights.h5`) should be downloaded/trained separately and placed in the project root directory.
