# Deployment Guide - Vehicle Damage Assessment

This guide explains how to deploy the Vehicle Damage Assessment application to DigitalOcean App Platform.

## Prerequisites

1. **DigitalOcean Account**: Sign up at [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. **GitHub Repository**: Push your code to a GitHub repository
3. **Gemini API Key**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Deployment Options

### Option 1: DigitalOcean App Platform (Recommended)

#### Step 1: Prepare Your Repository

1. Push your code to GitHub:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### Step 2: Create App on DigitalOcean

1. Login to [DigitalOcean](https://cloud.digitalocean.com)
2. Go to **Apps** section
3. Click **Create App**
4. Choose **GitHub** as source
5. Select your repository and branch (`main`)
6. DigitalOcean will auto-detect your app structure

#### Step 3: Configure Services

**Backend Service:**
- **Name**: `backend`
- **Source Directory**: `/` (root)
- **Build Command**: (leave empty)
- **Run Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment**: Python
- **Plan**: Basic ($5/month)

**Frontend Service:**
- **Name**: `frontend`
- **Source Directory**: `/frontend`
- **Build Command**: `npm ci && npm run build`
- **Run Command**: `npx serve -s build -p $PORT`
- **Environment**: Node.js
- **Plan**: Basic ($5/month)

#### Step 4: Set Environment Variables

Add these environment variables to the **backend** service:

| Key | Value | Type |
|-----|-------|------|
| `GEMINI_API_KEY` | `your_actual_api_key_here` | Secret |
| `PORT` | `8000` | Regular |

Add these environment variables to the **frontend** service:

| Key | Value | Type |
|-----|-------|------|
| `REACT_APP_API_URL` | `${backend.PUBLIC_URL}` | Build Time |
| `PORT` | `3000` | Regular |

#### Step 5: Configure Routes

- **Frontend**: Route `/` to frontend service
- **Backend**: Route `/api` to backend service

#### Step 6: Deploy

1. Click **Create Resources**
2. Wait for deployment (5-10 minutes)
3. Your app will be available at the provided URL

### Option 2: Docker Deployment

If you prefer Docker deployment:

```bash
# Build and run locally
docker build -t vehicle-damage-backend .
docker run -p 8000:8000 --env-file .env vehicle-damage-backend
```

## Environment Variables

Create a `.env` file with:

```env
GEMINI_API_KEY=your_actual_api_key_here
PORT=8000
```

## Monitoring and Logs

- **DigitalOcean Console**: View logs and metrics in the Apps dashboard
- **Health Check**: The app includes a `/health` endpoint for monitoring
- **Error Handling**: All errors are logged and returned as JSON responses

## Scaling

- **Horizontal Scaling**: Increase instance count in DigitalOcean
- **Vertical Scaling**: Upgrade to higher-tier plans
- **Auto-scaling**: Available on Professional plans

## Security Considerations

1. **API Keys**: Always use environment variables, never hardcode
2. **CORS**: Update CORS origins in production (currently set to `*`)
3. **File Upload**: 10MB limit is enforced
4. **HTTPS**: Automatically provided by DigitalOcean

## Troubleshooting

### Common Issues

1. **Build Failures**: Check logs in DigitalOcean console
2. **API Key Issues**: Verify GEMINI_API_KEY is set correctly
3. **CORS Errors**: Check frontend is calling correct backend URL
4. **Memory Issues**: Upgrade to higher-tier plan if needed

### Useful Commands

```bash
# Check backend health
curl https://your-app-url.ondigitalocean.app/health

# View logs
# Use DigitalOcean console or CLI

# Redeploy
git push origin main  # Auto-deploys if connected to GitHub
```

## Cost Estimation

- **Basic Plan**: ~$10/month (Backend + Frontend)
- **Professional Plan**: ~$25/month (includes auto-scaling)
- **Bandwidth**: Included in plan
- **Storage**: Minimal (stateless application)

## Support

- **DigitalOcean Docs**: [docs.digitalocean.com/products/app-platform](https://docs.digitalocean.com/products/app-platform/)
- **Community**: [DigitalOcean Community](https://www.digitalocean.com/community)
- **Support**: Available through DigitalOcean dashboard
