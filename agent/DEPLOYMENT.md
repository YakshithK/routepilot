# Deployment Guide for Route Pilot Agent

This guide covers deploying the Flask app to various cloud platforms.

## Prerequisites

1. **Amadeus API Credentials**: Sign up at [Amadeus for Developers](https://developers.amadeus.com/) to get your API key and secret.
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Quick Deploy Options

### 🚀 Option 1: Render (Recommended - Easiest)

**Best for**: Quick deployment with free tier

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub/GitLab repository
4. Configure:
   - **Name**: `routepilot-agent` (or your choice)
   - **Root Directory**: `agent`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Add Environment Variables:
   - `AMADEUS_API_KEY`: Your Amadeus API key
   - `AMADEUS_SECRET`: Your Amadeus secret
   - `PORT`: (auto-set by Render, but you can leave it)
6. Click "Create Web Service"
7. Wait for deployment (2-3 minutes)

**Free Tier**: 750 hours/month, sleeps after 15 min inactivity

---

### 🚂 Option 2: Railway

**Best for**: Simple deployment with good free tier

1. Go to [railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and use `railway.json`
5. Add Environment Variables in the Variables tab:
   - `AMADEUS_API_KEY`: Your Amadeus API key
   - `AMADEUS_SECRET`: Your Amadeus secret
6. Railway will automatically deploy

**Free Tier**: $5 credit/month, pay-as-you-go after

---

### ✈️ Option 3: Fly.io

**Best for**: Global edge deployment

1. Install Fly CLI: `powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"`
2. Login: `fly auth login`
3. In the `agent` directory, run: `fly launch`
4. Follow prompts (use `fly.toml` config)
5. Set secrets:
   ```powershell
   fly secrets set AMADEUS_API_KEY=your_key
   fly secrets set AMADEUS_SECRET=your_secret
   ```
6. Deploy: `fly deploy`

**Free Tier**: 3 shared-cpu VMs, 3GB persistent storage

---

### 🐍 Option 4: PythonAnywhere

**Best for**: Python-focused hosting

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Go to "Web" tab → "Add a new web app"
3. Choose Flask and Python 3.10+
4. Upload your code or clone from Git
5. Set working directory to `/home/yourusername/routepilot/agent`
6. Set source code to `/home/yourusername/routepilot/agent/app.py`
7. In "Web" → "Environment variables", add:
   - `AMADEUS_API_KEY`
   - `AMADEUS_SECRET`
8. Reload web app

**Free Tier**: Limited, but good for testing

---

### ☁️ Option 5: Heroku

**Best for**: Traditional PaaS (now paid)

1. Install Heroku CLI
2. Login: `heroku login`
3. In `agent` directory: `heroku create your-app-name`
4. Set config vars:
   ```powershell
   heroku config:set AMADEUS_API_KEY=your_key
   heroku config:set AMADEUS_SECRET=your_secret
   ```
5. Deploy: `git push heroku main`

**Note**: Heroku no longer has a free tier

---

## Environment Variables

All platforms require these environment variables:

- `AMADEUS_API_KEY`: Your Amadeus API key
- `AMADEUS_SECRET`: Your Amadeus secret
- `PORT`: Usually auto-set by platform (don't set manually unless needed)

## Testing Your Deployment

Once deployed, test your endpoints:

```powershell
# Health check
curl https://your-app-url.com/_health

# Flight search (example)
curl -X POST https://your-app-url.com/flightsearch `
  -H "Content-Type: application/json" `
  -d '{
    "origin": "NYC",
    "destination": "LAX",
    "departure_date": "2024-06-01",
    "adults": 1,
    "currency_code": "USD",
    "max_results": 5
  }'
```

## Production Considerations

1. **Security**: Never commit `.env` files. Use platform environment variables.
2. **HTTPS**: Most platforms provide HTTPS automatically.
3. **Scaling**: Adjust worker count in gunicorn command based on traffic.
4. **Monitoring**: Set up health check monitoring on your platform.
5. **Logs**: Check platform logs if issues occur.

## Troubleshooting

- **Port errors**: Ensure app listens on `0.0.0.0` and uses `$PORT` env var
- **Import errors**: Verify all dependencies in `requirements.txt`
- **API errors**: Check Amadeus credentials are set correctly
- **Timeout errors**: Increase timeout in gunicorn command (currently 120s)

## Recommended Platform

**For beginners**: **Render** - easiest setup, good free tier
**For production**: **Railway** or **Fly.io** - better performance and scaling

