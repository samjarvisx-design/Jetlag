# Jetlag Sleep Calculator API

A FastAPI-based web service that calculates optimal sleep schedules to minimize jetlag based on travel details.

## Features

- Calculate sleep recommendations based on origin and destination timezones
- Pre-flight sleep schedule adjustments (3 days before)
- Post-flight sleep recommendations
- Personalized tips based on travel direction and time difference

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload
```

3. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### GET `/`
Returns API information and available endpoints.

### GET `/timezones`
Returns a list of common timezones.

### POST `/calculate`
Calculate jetlag sleep recommendations.

**Request Body:**
```json
{
  "origin_tz": "America/New_York",
  "dest_tz": "Europe/London",
  "departure_time": "2024-12-15 14:30",
  "flight_duration_hours": 7.5
}
```

**Response:**
```json
{
  "time_difference_hours": 5.0,
  "arrival_time_dest": "2024-12-15 22:00 GMT",
  "is_eastward": true,
  "pre_flight_sleep": [...],
  "post_flight_sleep": [...],
  "tips": [...],
  "origin_tz_abbrev": "EST/EDT",
  "dest_tz_abbrev": "GMT/BST"
}
```

## Deployment Options

### Option 1: Render (Recommended for beginners)

1. Push your code to GitHub
2. Go to https://render.com
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
6. Deploy!

### Option 2: Railway

1. Push your code to GitHub
2. Go to https://railway.app
3. Create new project from GitHub repo
4. Railway auto-detects FastAPI and deploys
5. Your API will be live at `https://your-app.railway.app`

### Option 3: Fly.io

1. Install flyctl: https://fly.io/docs/getting-started/installing-flyctl/
2. Login: `fly auth login`
3. Initialize: `fly launch` (in the Jet_Lag directory)
4. Deploy: `fly deploy`

### Option 4: Docker + Any Platform

1. Build: `docker build -t jetlag-api .`
2. Run: `docker run -p 8000:8000 jetlag-api`
3. Deploy the Docker image to:
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances
   - DigitalOcean App Platform

### Option 5: Heroku

1. Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Environment Variables

No environment variables required for basic operation.

## Testing

Test the API with curl:

```bash
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "origin_tz": "America/New_York",
    "dest_tz": "Europe/London",
    "departure_time": "2024-12-15 14:30",
    "flight_duration_hours": 7.5
  }'
```

## License

MIT

