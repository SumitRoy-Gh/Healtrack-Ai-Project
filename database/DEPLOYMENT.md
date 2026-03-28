# HealTrack AI - Deployment Guide

This guide covers deploying HealTrack AI to production environments.

## Table of Contents
1. [Supabase Setup](#supabase-setup)
2. [Backend Deployment (Render)](#backend-deployment-render)
3. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
4. [Environment Variables](#environment-variables)
5. [Post-Deployment Verification](#post-deployment-verification)

---

## Supabase Setup

### 1. Create Supabase Project

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click "New Project"
3. Enter project name: `healtrack-ai`
4. Choose region closest to your users
5. Create project

### 2. Run Database Schema

1. In Supabase Dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy contents from `docs/database_schema.sql`
4. Run the query

### 3. Set Up Storage Bucket

1. Go to **Storage** in the sidebar
2. Click **New Bucket**
3. Name: `wound-images`
4. Enable **Public bucket**
5. Create bucket

### 4. Configure Storage Policies

In Storage > Policies, add these policies:

```sql
-- Allow authenticated uploads
CREATE POLICY "Allow authenticated uploads" ON storage.objects
    FOR INSERT TO authenticated WITH CHECK (bucket_id = 'wound-images');

-- Allow authenticated reads
CREATE POLICY "Allow authenticated reads" ON storage.objects
    FOR SELECT TO authenticated USING (bucket_id = 'wound-images');

-- Allow authenticated deletes
CREATE POLICY "Allow authenticated deletes" ON storage.objects
    FOR DELETE TO authenticated USING (bucket_id = 'wound-images');
```

### 5. Get API Credentials

1. Go to **Project Settings** > **API**
2. Copy:
   - `URL` (Supabase URL)
   - `anon public` (Supabase Key)
   - `JWT Secret` (from Settings > API > JWT Settings)

---

## Backend Deployment (Render)

### 1. Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

### 2. Create Render Account

1. Go to [Render](https://render.com)
2. Sign up with GitHub
3. Complete onboarding

### 3. Create Web Service

1. Click **New** > **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `healtrack-ai-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4. Set Environment Variables

In Render dashboard, add these environment variables:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
OPENAI_API_KEY=sk-your-openai-key
APP_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
```

### 5. Deploy

Click **Create Web Service**

Render will automatically deploy your backend.

---

## Frontend Deployment (Vercel)

### 1. Prepare Frontend

Ensure `vite.config.ts` has correct base URL:

```typescript
export default defineConfig({
  base: './',
  // ... rest of config
});
```

### 2. Create Vercel Account

1. Go to [Vercel](https://vercel.com)
2. Sign up with GitHub

### 3. Import Project

1. Click **Add New Project**
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 4. Set Environment Variables

Add these environment variables:

```
VITE_API_URL=https://your-backend.onrender.com/api
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### 5. Deploy

Click **Deploy**

Vercel will build and deploy your frontend.

---

## Environment Variables

### Backend (.env)

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIs...
SUPABASE_JWT_SECRET=your-jwt-secret

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# App
APP_ENV=production
DEBUG=false
CORS_ORIGINS=https://your-frontend.vercel.app

# Storage
STORAGE_BUCKET=wound-images
MAX_FILE_SIZE=10485760
```

### Frontend (.env)

```env
VITE_API_URL=https://your-backend.onrender.com/api
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
```

---

## Post-Deployment Verification

### 1. Test Backend Health

```bash
curl https://your-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "HealTrack AI API",
  "version": "1.0.0"
}
```

### 2. Test API Endpoints

```bash
# Test auth
curl https://your-backend.onrender.com/api/auth/register \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### 3. Test Frontend

1. Open your Vercel deployment URL
2. Verify login page loads
3. Test registration flow
4. Upload a test image

### 4. Common Issues

#### CORS Errors
- Verify `CORS_ORIGINS` includes your frontend URL
- Check for trailing slashes

#### Database Connection
- Verify Supabase credentials
- Check database schema is applied
- Verify RLS policies

#### Image Upload Fails
- Check storage bucket exists
- Verify storage policies
- Check file size limits

#### OpenAI Errors
- Verify API key is valid
- Check API key has available credits

---

## Monitoring

### Backend Logs (Render)

1. Go to Render Dashboard
2. Select your web service
3. Click **Logs** tab

### Frontend Analytics (Vercel)

1. Go to Vercel Dashboard
2. Select your project
3. Click **Analytics** tab

### Database Monitoring (Supabase)

1. Go to Supabase Dashboard
2. Check **Database** > **Logs**
3. Monitor **Auth** > **Logs**

---

## Updating Deployment

### Backend Update

```bash
git add .
git commit -m "Update backend"
git push origin main
```

Render will automatically redeploy.

### Frontend Update

```bash
git add .
git commit -m "Update frontend"
git push origin main
```

Vercel will automatically redeploy.

---

## Custom Domain (Optional)

### Vercel Custom Domain

1. Go to Vercel Dashboard
2. Select project
3. Click **Settings** > **Domains**
4. Add your domain

### Render Custom Domain

1. Go to Render Dashboard
2. Select web service
3. Click **Settings** > **Custom Domain**
4. Add your domain

---

## Security Checklist

- [ ] Environment variables are set (not in code)
- [ ] Supabase RLS policies are enabled
- [ ] Storage bucket is private with proper policies
- [ ] CORS origins are restricted
- [ ] DEBUG mode is off in production
- [ ] API keys are rotated regularly

---

## Support

For deployment issues:
1. Check service logs
2. Verify environment variables
3. Test API endpoints directly
4. Review CORS configuration

---

**Your HealTrack AI app should now be live! 🚀**
