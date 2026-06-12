# 🎵 Music Party

<div align="center">

A collaborative music playlist management platform that brings people together through shared music experiences. Create parties, invite friends, and add songs from all major music streaming services in real-time.

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## ✨ Key Features

- 👥 **User Authentication** - Secure registration and login with JWT tokens
- 🎉 **Party Management** - Create shared parties with unique codes for easy invitations
- 🎵 **Multi-Streaming Support** - Add songs from:
  - 🎵 Spotify
  - 🎥 YouTube
  - 🍎 Apple Music
  - 🎼 SoundCloud
- 🌐 **Real-Time Collaboration** - WebSocket support for instant playlist updates
- ☁️ **Cloud Storage** - AWS S3 integration for reliable audio file storage
- 🗺️ **Location Services** - Google Maps, Leaflet, and Mapbox integration
- 🎨 **Modern UI** - Beautiful responsive interface with Vue 3 and TailwindCSS
- 🔐 **Secure** - JWT authentication with bcrypt password hashing

## 🏗️ Technical Architecture

### Backend Stack
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Modern, fast web framework for building APIs |
| **SQLAlchemy** | Powerful ORM for database operations |
| **PostgreSQL** | Reliable relational database |
| **Alembic** | Database migration management |
| **Uvicorn** | Lightning-fast ASGI server |
| **PyJWT & bcrypt** | Authentication and password security |
| **boto3** | AWS S3 integration |
| **yt-dlp** | YouTube video downloading |

### Frontend Stack
| Technology | Purpose |
|-----------|---------|
| **Vue 3** | Progressive JavaScript framework |
| **Vite** | Next-generation build tool |
| **TailwindCSS** | Utility-first CSS framework |
| **Axios** | Promise-based HTTP client |
| **Socket.io** | Real-time bidirectional communication |
| **Leaflet & Mapbox** | Interactive mapping |

## 📂 Project Structure

```
PartyFY/
│
├── 🐍 Backend (Python/FastAPI)
│   └── app/
│       ├── backend/
│       │   ├── routes/              # API endpoints (auth, party, items, users)
│       │   ├── service/             # Business logic layer
│       │   ├── repository/          # Database abstraction layer
│       │   ├── schemas/             # Request/response validation (Pydantic)
│       │   ├── dependencies/        # Dependency injection
│       │   ├── exceptions/          # Custom exception handling
│       │   ├── FactoryService/      # Factory pattern implementation
│       │   └── ws/                  # WebSocket connection manager
│       │
│       ├── core/
│       │   ├── constants.py         # Service domain mappings
│       │   └── security.py          # Auth utilities
│       │
│       ├── db/
│       │   ├── models/              # SQLAlchemy ORM models
│       │   │   ├── user.py          # User model
│       │   │   ├── party.py         # Party model
│       │   │   └── item.py          # Music item model
│       │   ├── session/             # Database session management
│       │   ├── config/              # Database connection config
│       │   └── migrations/          # Alembic version control
│       │
│       └── ExternalServices/        # Third-party integrations
│           ├── spotifyAPI/          # Spotify track parser
│           ├── youtube/             # YouTube downloader
│           ├── applemusic/          # Apple Music integration
│           └── s3/                  # AWS S3 client
│
├── 🎨 Frontend (Vue 3/Vite)
│   └── frontend/
│       ├── src/
│       │   ├── components/          # Reusable Vue components
│       │   │   ├── header.vue
│       │   │   ├── login.vue
│       │   │   ├── parties.vue
│       │   │   ├── PartyItems.vue
│       │   │   ├── AddSongPopup.vue
│       │   │   └── ...
│       │   ├── router/              # Vue Router configuration
│       │   ├── api/                 # API client module
│       │   ├── assets/              # Styles, fonts, images
│       │   └── App.vue              # Root component
│       │
│       ├── public/                  # Static assets
│       ├── package.json
│       ├── vite.config.js
│       └── tailwind.config.js
│
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── alembic.ini                      # Migration configuration
└── README.md                        # This file

```

## 🚀 Quick Start

### Prerequisites
- **Python** 3.10 or higher
- **Node.js** 20.19.0 or 22.12.0+
- **PostgreSQL** database
- **AWS S3** bucket (for audio storage)
- Git

### Backend Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/musicparty1.git
   cd musicparty1
   ```

2. **Create Python Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Create `.env` file in project root:
   ```env
   # Database
   DATABASE_URL=postgresql://user:password@localhost:5432/musicparty
   
   # Security
   SECRET_KEY=your-super-secret-jwt-key-change-this
   
   # AWS S3
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_REGION=us-east-1
   
   # API Keys
   SPOTIFY_CLIENT_ID=your-spotify-id
   SPOTIFY_CLIENT_SECRET=your-spotify-secret
   YOUTUBE_API_KEY=your-youtube-key
   ```

5. **Initialize Database**
   ```bash
   alembic upgrade head
   ```

6. **Start Backend Server**
   ```bash
   python main.py
   ```
   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```
   Application will be available at `http://127.0.0.1:5173`

4. **Build for Production**
   ```bash
   npm run build
   ```
   Output will be in `dist/` directory

## 📚 API Documentation

### Interactive Documentation
Access Swagger UI while the backend is running:
- **Swagger**: http://127.0.0.1:8000/swagger
- **ReDoc**: http://127.0.0.1:8000/redoc

### API Endpoints Overview

#### 🔐 Authentication
```
POST   /auth/register              - Create new user account
POST   /auth/login                 - User login
POST   /auth/refresh               - Refresh access token
```

#### 🎉 Parties
```
POST   /party/create_party         - Create new party
GET    /party/get_parties          - Get user's parties
GET    /party/get_full_party       - Get party with all songs
```

#### 🎵 Music Items
```
POST   /items/add_item             - Add song to party
GET    /items/get_items            - Get party songs
DELETE /items/delete_item/{id}     - Remove song
```

#### 👤 Users
```
GET    /user/profile               - Get user information
PUT    /user/update                - Update profile
```

#### 🌐 WebSockets
```
WS     /ws/items/{party_uuid}      - Real-time playlist updates
```

## 🎵 Music Streaming Integration

### Supported Services

#### Spotify
- Parse track information from Spotify links
- Retrieve metadata (artist, album, duration)
- Support for playlist and album sharing

#### YouTube
- Download audio from YouTube videos
- Store in cloud (S3)
- Support for playlists and channels

#### Apple Music
- Access track metadata
- Artist and album information
- Playlist support

#### SoundCloud
- Parse SoundCloud tracks
- Extract audio information
- Direct link sharing

## 🔒 Security Architecture

- **JWT Authentication** - Token-based stateless authentication
- **Password Hashing** - bcrypt with configurable cost factors
- **CORS Protection** - Whitelist allowed origins
- **Role-Based Access** - User and Guest access levels
- **Token Refresh** - Automatic token rotation mechanism
- **Input Validation** - Pydantic schema validation
- **Error Handling** - Custom exception classes with proper HTTP status codes

## 🛠️ Development Guide

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new feature"

# Apply pending migrations
alembic upgrade head

# Show current revision
alembic current

# Rollback one migration
alembic downgrade -1
```

### Project Architecture Patterns

#### Service Layer
Business logic implementation separated from routes for better testability.

#### Repository Pattern
Database operations abstraction allowing easy switching between database implementations.

#### Dependency Injection
FastAPI's `Depends()` for clean, testable code structure.

#### Factory Pattern
Dynamic service instantiation in `FactoryService/` for flexible service creation.

#### Schema Validation
Pydantic models for request/response validation and serialization.

## 📦 Key Dependencies

### Python Packages
- **fastapi (0.128.0)** - Web framework
- **sqlalchemy (2.0.45)** - ORM
- **pydantic (2.12.5)** - Data validation
- **PyJWT (2.10.1)** - JWT handling
- **bcrypt (5.0.0)** - Password hashing
- **boto3 (1.42.27)** - AWS SDK
- **yt-dlp (2025.12.8)** - YouTube downloading
- **asyncpg (0.31.0)** - Async PostgreSQL driver
- **uvicorn (0.40.0)** - ASGI server

### JavaScript Packages
- **vue (3.5.18)** - Frontend framework
- **vite (7.0.6)** - Build tool
- **tailwindcss (4.1.12)** - CSS framework
- **axios (1.11.0)** - HTTP client
- **socket.io-client (4.8.1)** - WebSocket client
- **leaflet (1.9.4)** - Mapping library

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋 Support

- **Issues** - Please use GitHub Issues for bug reports and feature requests
- **Discussions** - Start a discussion for questions and ideas
- **Email** - Contact the development team directly

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Collaborative music queue sorting
- [ ] Party statistics and history
- [ ] Integration with more music services
- [ ] Advanced search and filtering
- [ ] Dark mode theme
- [ ] Offline mode support

## 👨‍💻 Author

Created with ❤️ by Volodymyr

---

<div align="center">

### 🎉 Enjoying Music Party? Give us a ⭐ on GitHub!

**Made with ❤️ for music lovers who want to share the vibe!** 🎵🎸🎹

</div>

