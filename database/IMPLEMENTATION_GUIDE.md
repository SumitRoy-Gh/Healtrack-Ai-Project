# HealTrack AI - Complete Hackathon Implementation Guide

## Project Overview
**HealTrack AI** is a predictive wound recovery assistant that helps patients track healing progress, predicts infection risk, generates doctor reports, and provides care suggestions.

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Tech Stack](#tech-stack)
3. [Phase 1: Project Setup](#phase-1-project-setup)
4. [Phase 2: Backend (FastAPI)](#phase-2-backend-fastapi)
5. [Phase 3: AI/ML Module](#phase-3-aiml-module)
6. [Phase 4: Frontend (React)](#phase-4-frontend-react)
7. [Phase 5: Integration](#phase-5-integration)
8. [Phase 6: Deployment](#phase-6-deployment)
9. [Demo Script](#demo-script)

---

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Frontend │────▶│  FastAPI Backend │────▶│   Supabase DB   │
│                 │     │                 │     │                 │
│ • Dashboard     │     │ • Image Upload  │     │ • Patient Data  │
│ • Timeline      │◀────│ • AI Analysis   │◀────│ • Wound Scans   │
│ • Reports       │     │ • Report Gen    │     │ • Reports       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   AI Services   │
                        │                 │
                        │ • OpenCV        │
                        │ • PyTorch       │
                        │ • OpenAI API    │
                        └─────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React + TypeScript + Vite | UI Framework |
| Styling | Tailwind CSS + shadcn/ui | Styling & Components |
| Charts | Recharts + Plotly | Data Visualization |
| Backend | FastAPI | API Server |
| Database | Supabase (PostgreSQL) | Data Storage |
| Storage | Supabase Storage | Image Files |
| Auth | Supabase Auth | User Authentication |
| AI/ML | OpenCV + PyTorch + scikit-learn | Image Analysis |
| LLM | OpenAI Responses API | Report Generation |
| Deployment | Vercel + Render | Hosting |

---

## Phase 1: Project Setup

### 1.1 Create Project Structure

```bash
# Create main project directory
mkdir healtrack-ai
cd healtrack-ai

# Create subdirectories
mkdir -p backend/app/{routers,models,services,utils}
mkdir -p frontend/src/{components,pages,hooks,services,types,lib}
mkdir -p docs
mkdir -p assets
```

### 1.2 Environment Variables

Create `.env` files for both frontend and backend:

**Backend `.env`:**
```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_JWT_SECRET=your_jwt_secret

# OpenAI
OPENAI_API_KEY=your_openai_key

# App
APP_ENV=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Frontend `.env`:**
```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

---

## Phase 2: Backend (FastAPI)

### 2.1 Setup FastAPI Project

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Create requirements.txt
pip install fastapi uvicorn python-multipart supabase pyjwt openai opencv-python-headless torch torchvision pillow scikit-learn numpy python-dotenv pydantic
```

### 2.2 Backend File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration settings
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── wounds.py        # Wound analysis routes
│   │   ├── reports.py       # Report generation routes
│   │   └── patients.py      # Patient management routes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py       # Pydantic models
│   │   └── database.py      # Database models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── image_processor.py   # OpenCV image processing
│   │   ├── wound_analyzer.py    # AI analysis logic
│   │   ├── report_generator.py  # OpenAI report generation
│   │   └── prediction_engine.py # Risk prediction
│   └── utils/
│       ├── __init__.py
│       ├── supabase.py      # Supabase client
│       └── helpers.py       # Utility functions
├── requirements.txt
└── .env
```

### 2.3 Core Backend Files

**main.py** - FastAPI entry point
**config.py** - Configuration
**schemas.py** - Pydantic models
**image_processor.py** - OpenCV wound analysis
**wound_analyzer.py** - AI scoring engine
**report_generator.py** - OpenAI integration
**prediction_engine.py** - Risk prediction

### 2.4 Supabase Database Schema

```sql
-- Enable RLS
alter table auth.users enable row level security;

-- Patients table
create table patients (
    id uuid default gen_random_uuid() primary key,
    user_id uuid references auth.users(id),
    name text not null,
    email text,
    phone text,
    age integer,
    medical_conditions text[],
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Wound cases table
create table wound_cases (
    id uuid default gen_random_uuid() primary key,
    patient_id uuid references patients(id),
    wound_type text,
    location text,
    description text,
    start_date date default current_date,
    status text default 'active',
    created_at timestamp with time zone default now()
);

-- Wound scans table (daily uploads)
create table wound_scans (
    id uuid default gen_random_uuid() primary key,
    case_id uuid references wound_cases(id),
    image_url text not null,
    pain_level integer check (pain_level between 0 and 10),
    notes text,
    healing_score integer check (healing_score between 0 and 100),
    infection_risk numeric(5,2),
    redness_score numeric(5,2),
    size_mm2 numeric(10,2),
    texture_stability numeric(5,2),
    analyzed_at timestamp with time zone,
    created_at timestamp with time zone default now()
);

-- Reports table
create table reports (
    id uuid default gen_random_uuid() primary key,
    case_id uuid references wound_cases(id),
    scan_id uuid references wound_scans(id),
    report_type text,
    content jsonb,
    care_suggestions text[],
    generated_at timestamp with time zone default now()
);

-- Enable RLS policies
alter table patients enable row level security;
alter table wound_cases enable row level security;
alter table wound_scans enable row level security;
alter table reports enable row level security;

-- RLS Policies
create policy "Users can view own patients" on patients
    for select using (auth.uid() = user_id);
    
create policy "Users can insert own patients" on patients
    for insert with check (auth.uid() = user_id);
```

---

## Phase 3: AI/ML Module

### 3.1 Image Processing Pipeline

1. **Preprocessing**
   - Resize image to standard size (512x512)
   - Convert to RGB if needed
   - Apply noise reduction

2. **Feature Extraction**
   - Wound segmentation using color thresholding
   - Redness analysis (HSV color space)
   - Edge detection for size estimation
   - Texture analysis using GLCM

3. **Scoring Algorithm**
   - Redness score (0-100): Lower is better
   - Size trend: Decreasing is positive
   - Texture stability: Consistent is positive
   - Combined healing score (0-100)

### 3.2 Infection Risk Prediction

Uses trend analysis:
- Rising redness over 3+ days = increased risk
- Increasing size = high risk
- Pain level correlation
- Combined risk score (0-100)

### 3.3 Future Wound Simulation

Smart extrapolation based on:
- Current trend direction
- Rate of change
- Healing curve modeling
- Visual preview generation

---

## Phase 4: Frontend (React)

### 4.1 Setup React Project

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install shadcn/ui
npx shadcn-ui@latest init

# Install additional packages
npm install recharts plotly.js-dist-min @supabase/supabase-js axios react-router-dom date-fns framer-motion lucide-react
```

### 4.2 Frontend Structure

```
frontend/src/
├── components/
│   ├── ui/                  # shadcn components
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   └── Layout.tsx
│   ├── upload/
│   │   ├── ImageUpload.tsx
│   │   └── UploadProgress.tsx
│   ├── dashboard/
│   │   ├── HealingScore.tsx
│   │   ├── RiskIndicator.tsx
│   │   ├── Timeline.tsx
│   │   └── StatsCards.tsx
│   ├── analysis/
│   │   ├── WoundComparison.tsx
│   │   ├── FeatureAnalysis.tsx
│   │   └── TrendChart.tsx
│   ├── reports/
│   │   ├── DoctorReport.tsx
│   │   ├── CareSuggestions.tsx
│   │   └── ShareReport.tsx
│   └── simulation/
│       └── FutureSimulation.tsx
├── pages/
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── PatientProfile.tsx
│   ├── WoundDetail.tsx
│   ├── UploadScan.tsx
│   └── Reports.tsx
├── hooks/
│   ├── useAuth.ts
│   ├── useWounds.ts
│   ├── useAnalysis.ts
│   └── useReports.ts
├── services/
│   ├── api.ts
│   ├── supabase.ts
│   └── analysis.ts
├── types/
│   └── index.ts
├── lib/
│   └── utils.ts
├── App.tsx
└── main.tsx
```

### 4.3 Key UI Components

**Dashboard Layout:**
- Header with patient info
- Healing score card (large, prominent)
- Risk indicator (color-coded)
- Timeline view
- Recent scans gallery
- Quick actions

**Upload Flow:**
- Drag & drop image upload
- Pain level slider (0-10)
- Notes textarea
- Progress indicator
- Analysis results display

**Report View:**
- Professional report card
- Healing trend chart
- Care suggestions list
- Share/Export buttons

---

## Phase 5: Integration

### 5.1 API Endpoints

```
POST   /api/auth/login
POST   /api/auth/register
POST   /api/auth/refresh

GET    /api/patients
POST   /api/patients
GET    /api/patients/{id}
PUT    /api/patients/{id}

GET    /api/wounds
POST   /api/wounds
GET    /api/wounds/{id}
GET    /api/wounds/{id}/scans
POST   /api/wounds/{id}/scans

POST   /api/analysis/upload
GET    /api/analysis/{scan_id}/results
GET    /api/analysis/{case_id}/trends

POST   /api/reports/generate
GET    /api/reports/{report_id}
GET    /api/reports/{case_id}/history

POST   /api/predictions/risk
POST   /api/predictions/simulate
```

### 5.2 Data Flow

1. User uploads image → Frontend
2. Frontend sends to `/api/analysis/upload`
3. Backend stores image in Supabase Storage
4. Backend runs image processing (OpenCV)
5. Backend runs AI analysis (PyTorch)
6. Backend generates report (OpenAI)
7. Results stored in database
8. Response sent to frontend
9. Frontend updates dashboard

---

## Phase 6: Deployment

### 6.1 Supabase Setup

1. Create Supabase project
2. Run database migrations
3. Set up storage bucket for images
4. Configure authentication
5. Set up RLS policies

### 6.2 Backend Deployment (Render)

1. Push code to GitHub
2. Create Render Web Service
3. Connect GitHub repo
4. Set environment variables
5. Deploy

### 6.3 Frontend Deployment (Vercel)

1. Push frontend to GitHub
2. Import to Vercel
3. Set environment variables
4. Deploy

---

## Demo Script

### Opening (30 seconds)
"Every year, millions of patients struggle with post-surgery wound care at home. They can't tell if their wound is healing normally or if infection is setting in. Doctors only see snapshots, not the full healing journey."

### Problem (30 seconds)
- Show statistics on wound complications
- Demonstrate the confusion patients face
- Highlight the gap in remote monitoring

### Solution Demo (3 minutes)
1. **Upload Flow** (30s)
   - Upload a wound photo
   - Add pain level and notes
   - Show real-time analysis

2. **Dashboard** (1m)
   - Show healing score
   - Display trend chart
   - Highlight risk indicators
   - Show timeline comparison

3. **Report Generation** (30s)
   - Generate doctor report
   - Show care suggestions
   - Demonstrate sharing

4. **Future Simulation** (30s)
   - Show predicted next stage
   - Explain the wow factor

### Technical Highlights (1 minute)
- "We built a complete AI pipeline with OpenCV and PyTorch"
- "Our scoring algorithm combines multiple visual features"
- "We use OpenAI for professional report generation"
- "Everything is real-time and deployable"

### Closing (30 seconds)
"HealTrack AI transforms wound care from reactive to predictive. We're not just monitoring wounds - we're predicting recovery and preventing complications before they happen."

---

## Team Roles

| Role | Responsibilities |
|------|-----------------|
| Frontend Lead | React UI, Dashboard, Timeline, Upload flow |
| Backend Lead | FastAPI, Database, File handling, APIs |
| ML/CV Lead | OpenCV processing, Feature extraction, Scoring |
| LLM/Report Lead | OpenAI integration, Report generation |
| Integration Lead | End-to-end flow, Testing, Deployment |

---

## MVP Checklist

### Must Have (Core Demo)
- [ ] Image upload and storage
- [ ] Basic healing score (0-100)
- [ ] Trend visualization
- [ ] Risk flag (low/medium/high)
- [ ] Simple doctor report
- [ ] Timeline view

### Should Have (Polish)
- [ ] Care suggestions
- [ ] Patient notes
- [ ] Clean dashboard UI
- [ ] Shareable report
- [ ] Auth/login flow

### Stretch (Wow Factor)
- [ ] Future wound simulation
- [ ] Heatmap overlay
- [ ] Confidence scores
- [ ] Image enhancement

---

## Tips for Hackathon Success

1. **Start with the core flow** - Upload → Analyze → Display
2. **Use mock data** if ML takes too long
3. **Focus on the demo** - Make it visually impressive
4. **Have a backup plan** - Pre-computed results if live fails
5. **Practice the pitch** - Time it perfectly
6. **Show, don't tell** - Live demo beats slides

---

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Supabase Docs](https://supabase.com/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [OpenCV Python Docs](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [shadcn/ui Docs](https://ui.shadcn.com/docs)

---

Good luck with your hackathon! 🚀
