# Bizzz Backend API

Multi-platform messaging integration with AI-powered chat capabilities using FastAPI, LangChain, and Google Gemini.

## Features

- 🔐 **OAuth Authentication** - Secure user authentication with JWT tokens
- 💬 **Multi-Platform Integration** - WhatsApp, Telegram, Messenger, Instagram, Facebook Pages
- 🤖 **AI-Powered Chat** - LangChain with Google Gemini for intelligent responses
- 📊 **Database Management** - PostgreSQL with SQLAlchemy and Alembic migrations
- 🧠 **Vector Search** - PGVector-backed RAG with FastEmbed embeddings
- 🔄 **Webhook Handling** - Automated message processing and responses
- 📡 **Streaming Chat** - Real-time AI responses
- 🛠️ **RAG & Tools** - Context-aware responses with database queries

## Technology Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Async ORM
- **PostgreSQL** - Primary database
- **PGVector** - Vector storage for retrieval-augmented generation
- **Alembic** - Database migrations
- **LangChain** - AI orchestration
- **FastEmbed** - Lightweight local embeddings
- **DeepSeek** - LLM provider
- **OAuth 2.0** - Authentication

## Project Structure

```
bizzz-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── ai_service.py        # AI/LangChain service
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── store.py         # Store CRUD
│   │   ├── users.py         # User CRUD
│   │   ├── chat.py          # Chat endpoints
│   │   ├── setup.py         # Platform setup
│   │   └── webhooks.py      # Webhook handlers
│   └── services/
│       └── message_processor.py  # Message processing
├── alembic/                 # Database migrations
├── requirements.txt
├── .env.example
├── V1.0.md                  # Project requirements
└── README.md
```


## PostgreSql Notes
To list your databases:
```bash
sudo -u postgres psql -c "\l"
```
Reset Password:
```bash
sudo -u postgres psql
# then inside psql:
ALTER USER postgres PASSWORD 'newpassword';
# or for a specific user:
ALTER USER saikat PASSWORD 'newpassword';
\q
```
Bypass Password temporally:
```bash
sudo -u postgres psql  # no password needed as root
```
Connecting String:
```bash
postgresql://USER:PASSWORD@localhost:5432/DBNAME
# or
postgresql://saikat:password@localhost:5432/mydb
```
Creating a new database:
```bash
sudo -u postgres psql
CREATE DATABASE sellervai;
CREATE USER saikat WITH PASSWORD 'saikat'; // if not created earlier
GRANT ALL PRIVILEGES ON DATABASE sellervai TO saikat;
ALTER DATABASE sellervai OWNER TO saikat;
\q
// before quit, to list all db
\l *
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Virtual environment

### 2. Installation

```bash
# Clone the repository
cd /home/saikat/projects/bizzz-backend

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Application secret key
- `GEMINI_API_KEY` - Google Gemini API key
- Platform-specific API keys and tokens

### 4. Database Setup

```bash
# Create database
createdb bizzz_db

# Run migrations
alembic upgrade head
```

### 5. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/api/auth/`)
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/session` - Get user profile

### Store (`/api/store/`)
- `GET /api/store/` - List stores
- `POST /api/store/` - Create store
- `GET /api/store/{id}` - Get store
- `PUT /api/store/{id}` - Update store
- `DELETE /api/store/{id}` - Delete store

### Users (`/api/users/`)
- `GET /api/users/` - List users
- `GET /api/users/{id}` - Get user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Chat (`/api/chat/`)
- `POST /api/chat/` - Chat with AI
- `POST /api/chat/stream` - Stream chat responses

### Setup (`/api/setup/`)
- `POST /api/setup/{platform}/{store_id}/api-key` - Configure API key
- `POST /api/setup/{platform}/{store_id}/webhook` - Setup webhook

Platforms: `messenger`, `whatsapp`, `telegram`, `instagram`

### Webhooks (`/api/webhooks/`)
- `GET/POST /api/webhooks/{platform}/{store_id}` - Platform webhooks

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## AI Features

The AI service includes:
- **Product queries** - "How many products do you have?"
- **Product search** - "Show me products with 'shirt'"
- **Store info** - "Tell me about the store"
- **Streaming responses** - Real-time chat
- **Context awareness** - RAG-based responses

## Webhook Configuration

### Messenger/Instagram
1. Configure API key via `/api/setup/messenger/{store_id}/api-key`
2. Set webhook URL in Facebook Developer Console
3. Verify webhook via `/api/setup/messenger/{store_id}/webhook`

### WhatsApp
1. Configure API key via `/api/setup/whatsapp/{store_id}/api-key`
2. Set webhook URL in WhatsApp Business API settings
3. Verify webhook via `/api/setup/whatsapp/{store_id}/webhook`

### Telegram
1. Configure bot token via `/api/setup/telegram/{store_id}/api-key`
2. Set webhook using Telegram Bot API
3. Verify webhook via `/api/setup/telegram/{store_id}/webhook`

## Security

- API keys are encrypted before storage
- JWT-based authentication
- CORS configuration
- Environment-based secrets
- Webhook verification

## Development

```bash
# Run tests
pytest

# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up SSL/TLS certificates
4. Configure reverse proxy (Nginx)
5. Set up monitoring and logging
6. Use environment secrets management

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
