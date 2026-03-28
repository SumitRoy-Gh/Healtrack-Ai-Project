# HealTrack AI - Predictive Wound Recovery Assistant

![HealTrack AI](https://img.shields.io/badge/HealTrack-AI-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai)

> 🏆 **Hackathon Project** - Transforming wound care from reactive to predictive

## Overview

**HealTrack AI** is a comprehensive wound monitoring and recovery prediction system that helps patients track healing progress, predicts infection risk, generates doctor-ready reports, and provides personalized care suggestions using AI-powered image analysis.

## Features

### Core Features
- **Image Upload & Analysis** - Upload wound photos for AI-powered analysis
- **Healing Score (0-100)** - Comprehensive healing progress metric
- **Infection Risk Prediction** - Early warning system for complications
- **Timeline Replay** - Day-by-day visual comparison of healing
- **Auto Doctor Reports** - Professional clinical summaries
- **Personal Care Suggestions** - Practical next steps for patients
- **Future Wound Simulation** - AI-powered healing trajectory preview

### Technical Highlights
- **OpenCV + PyTorch** - Computer vision for wound feature extraction
- **OpenAI Integration** - LLM-powered report generation
- **Trend Analysis** - Historical data tracking and prediction
- **Real-time Dashboard** - Interactive charts and visualizations

## Tech Stack

### Frontend
- **React 19** + **TypeScript**
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Recharts** - Data visualization
- **React Router** - Navigation

### Backend
- **FastAPI** - Python web framework
- **OpenCV** - Image processing
- **PyTorch** - Deep learning
- **OpenAI API** - Report generation
- **Supabase** - Database & storage

### Infrastructure
- **Supabase** - PostgreSQL + Auth + Storage
- **Vercel** - Frontend deployment
- **Render/Railway** - Backend deployment

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.10+
- Supabase account
- OpenAI API key

### 1. Clone & Setup

```bash
git clone <repository-url>
cd healtrack-ai
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials

# Run server
uvicorn app.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env with your API URL

# Run development server
npm run dev
```

### 4. Database Setup

1. Create a new Supabase project
2. Run the SQL schema from `docs/database_schema.sql`
3. Create a storage bucket named `wound-images`
4. Update environment variables with Supabase credentials

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Patients
- `GET /api/patients` - List patients
- `POST /api/patients` - Create patient
- `GET /api/patients/{id}` - Get patient details
- `PUT /api/patients/{id}` - Update patient

### Wound Cases
- `GET /api/patients/{id}/cases` - List cases
- `POST /api/patients/{id}/cases` - Create case

### Wound Scans
- `POST /api/wounds/upload` - Upload and analyze image
- `GET /api/wounds/cases/{id}/scans` - List scans
- `GET /api/wounds/cases/{id}/trends` - Get trends

### Reports
- `POST /api/reports/generate` - Generate report
- `GET /api/reports/case/{id}` - List case reports

### Predictions
- `POST /api/predictions/risk` - Predict infection risk
- `POST /api/predictions/simulate` - Simulate future wound
- `GET /api/predictions/case/{id}/forecast` - Get forecast

## Project Structure

```
healtrack-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry
│   │   ├── config.py            # Configuration
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── routers/
│   │   │   ├── auth.py          # Auth routes
│   │   │   ├── patients.py      # Patient routes
│   │   │   ├── wounds.py        # Wound routes
│   │   │   ├── reports.py       # Report routes
│   │   │   └── predictions.py   # Prediction routes
│   │   ├── services/
│   │   │   ├── image_processor.py   # OpenCV processing
│   │   │   ├── wound_analyzer.py    # Analysis logic
│   │   │   ├── report_generator.py  # OpenAI reports
│   │   │   └── prediction_engine.py # Predictions
│   │   └── utils/
│   │       └── supabase.py      # Supabase client
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── hooks/               # Custom hooks
│   │   ├── services/            # API service
│   │   ├── types/               # TypeScript types
│   │   └── contexts/            # React contexts
│   ├── package.json
│   └── .env.example
└── docs/
    ├── IMPLEMENTATION_GUIDE.md
    ├── database_schema.sql
    └── DEPLOYMENT.md
```

## Deployment

### Backend (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set environment variables
5. Deploy

### Frontend (Vercel)

1. Push code to GitHub
2. Import project on Vercel
3. Set environment variables
4. Deploy

### Supabase

1. Create project
2. Run database schema
3. Configure auth providers
4. Set up storage bucket

## Demo Script

### Opening (30s)
"Every year, millions of patients struggle with post-surgery wound care at home. They can't tell if their wound is healing normally or if infection is setting in."

### Problem (30s)
- Patients can't judge healing progress
- Doctors see only snapshots, not the journey
- Early warning signs are missed

### Solution Demo (3m)
1. **Upload** - Show image upload with pain/notes
2. **Dashboard** - Healing score, risk indicators, trends
3. **Report** - Auto-generated doctor report
4. **Simulation** - Future wound prediction

### Technical Highlights (1m)
- "Complete AI pipeline with OpenCV + PyTorch"
- "OpenAI-powered professional reports"
- "Real-time trend analysis and prediction"

### Closing (30s)
"HealTrack AI transforms wound care from reactive to predictive - preventing complications before they happen."

## Team Roles

| Role | Responsibilities |
|------|-----------------|
| Frontend Lead | React UI, Dashboard, Timeline |
| Backend Lead | FastAPI, Database, APIs |
| ML/CV Lead | OpenCV, Feature extraction |
| LLM/Report Lead | OpenAI integration |
| Integration Lead | End-to-end, Deployment |

## License

MIT License - Hackathon Project

## Acknowledgments

- Built for Hackathon 2024
- Powered by OpenAI, Supabase, and open-source tools

---

**Made with ❤️ for better healthcare**
