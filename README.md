# BigTime Bugs Assistant

A FastAPI-powered assistant for analyzing BTIQ repository issues and bugs.

## Running Locally with Docker

1. Create a `.env` file (see template below)
2. Run with Docker Compose:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## Swagger Documentation

Access the interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`

## Making Requests to `/assistant/ask`

Send a POST request to ask the assistant questions about BigTime bugs:

```bash
curl -X POST "http://localhost:8000/assistant/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the recent bugs in the authentication module?"}'
```

The endpoint returns streaming NDJSON responses with assistant messages.

## Environment Configuration

Create a `.env` file in the root directory with your credentials:

```env
# Azure DevOps Git Credentials
# Generate these from your ADO profile settings
GIT_USERNAME=your-ado-username
GIT_PASSWORD=your-ado-personal-access-token

# Claude API Key
# Get your API key from https://console.anthropic.com/
ANTHROPIC_API_KEY=your-anthropic-api-key
```

