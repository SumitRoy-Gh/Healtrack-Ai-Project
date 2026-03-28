# HealTrack AI - Quick Start Guide

Get your hackathon project running in 5 minutes!

## Prerequisites
- Python 3.10+
- Node.js 20+
- GitHub account
- Supabase account (free)
- OpenAI API key

## Step 1: Setup Supabase (2 minutes)

1. Go to [supabase.com](https://supabase.com) and create a free project
2. Once created, go to **SQL Editor** → **New Query**
3. Copy and paste the contents of `docs/database_schema.sql`
4. Click **Run**
5. Go to **Storage** → **New Bucket**
   - Name: `wound-images`
   - Check: **Public bucket**
6. Go to **Project Settings** → **API** and copy:
   - `URL`
   - `anon public` key
   - `JWT Secret` (under JWT Settings)

## Step 2: Configure Backend (1 minute)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `.env` with your credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
OPENAI_API_KEY=sk-your-openai-key
```

## Step 3: Run Backend (30 seconds)

```bash
uvicorn app.main:app --reload
```

Backend is running at: `http://localhost:8000`

Test it: `http://localhost:8000/health`

## Step 4: Configure Frontend (1 minute)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
```

Edit `.env`:
```env
VITE_API_URL=http://localhost:8000/api
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

## Step 5: Run Frontend (30 seconds)

```bash
npm run dev
```

Frontend is running at: `http://localhost:5173`

## You're Ready! 🎉

Open `http://localhost:5173` in your browser and:
1. Create an account
2. Add a patient
3. Create a wound case
4. Upload a wound photo
5. See the AI analysis!

## Demo Checklist

Before your hackathon demo:

- [ ] Backend running locally
- [ ] Frontend running locally
- [ ] Test image upload
- [ ] Test analysis results
- [ ] Test report generation
- [ ] Test future simulation
- [ ] Have backup screenshots ready

## Common Issues

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
npm install
```

### CORS errors
- Make sure backend `.env` has `CORS_ORIGINS` with your frontend URL
- Default: `http://localhost:5173`

## Need Help?

Check these files:
- `docs/IMPLEMENTATION_GUIDE.md` - Full technical guide
- `docs/DEPLOYMENT.md` - Production deployment
- `docs/PITCH_SCRIPT.md` - Demo presentation script

---

**Good luck with your hackathon! 🚀**
