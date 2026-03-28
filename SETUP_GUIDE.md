# HealTrack AI - Complete Setup Guide

## Project Structure

```
Healtrack-Ai-Project/
├── frontend/              # React Vite app
│   ├── src/
│   │   ├── App.jsx       # Main app (backend-integrated)
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
├── backend/              # Flask API server
│   ├── app.py           # Backend API
│   ├── requirements.txt
│   └── README.md
└── ml/                  # Python ML pipeline
    ├── pipeline.py
    ├── preprocessing.py
    ├── healing_score.py
    ├── risk_predictor.py
    ├── report_generator.py
    ├── simulation.py
    ├── visualisation.py
    └── requirements.txt
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Installation & Setup

### Step 1: Install ML Dependencies

```bash
cd ml
pip install -r requirements.txt
```

This installs:

- OpenCV (cv2) - Image processing
- Torch/TorchVision - Deep learning models
- Scikit-learn - ML algorithms
- Requests - HTTP requests
- Python-dotenv - Environment variables
- Plotly & Kaleido - Charting
- OpenAI - AI/LLM support (optional)

### Step 2: Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

This installs React, Tailwind CSS, Framer Motion, Recharts, and Lucide React icons.

### Step 3: Install Backend Dependencies

```bash
cd ../backend
pip install -r requirements.txt
```

This installs:

- Flask - Web framework
- Flask-CORS - Cross-origin requests
- Werkzeug - WSGI utilities

## Running the Application

You need to run **3 terminal windows** (one for each service):

### Terminal 1: Backend API Server

```bash
cd backend
python app.py
```

Expected output:

```
============================================================
  HealTrack AI Backend API
============================================================
  Server: http://localhost:5000
  Upload endpoint: POST http://localhost:5000/api/upload
============================================================
```

✅ The backend will be running on **http://localhost:5000**

### Terminal 2: ML Pipeline (Optional - for testing)

```bash
cd ml
python pipeline.py
```

This runs a test of the full ML pipeline with sample data.

### Terminal 3: Frontend Dev Server

```bash
cd frontend
npm run dev
```

Expected output:

```
  VITE v8.0.3  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network:   use --host to expose
```

✅ Open your browser to **http://localhost:5173**

## How It Works

### User Flow:

1. **User opens the app** → Browser loads React app on `localhost:5173`
2. **User clicks "Upload Scan"** → Opens file upload modal
3. **User selects an image** → Fills in Patient ID and Monitoring Day
4. **User clicks "Analyze Scan"** → Frontend sends POST request to backend
5. **Backend receives image** →
   - Saves the image temporarily
   - Runs ML pipeline (preprocessing, scoring, risk prediction)
   - Generates doctor report (via Ollama Mistral)
   - Simulates future wound state
   - Generates charts
6. **Backend returns JSON** with all results
7. **Frontend displays results** with metrics, charts, and AI-generated reports

### API Endpoint

**POST** `/api/upload`

**Request (Form Data):**

```
image: (binary file)
patient_id: "patient_001"
day: "3"
```

**Response (JSON):**

```json
{
  "success": true,
  "patient_id": "patient_001",
  "day": 3,
  "metrics": {
    "healing_score": 72.5,
    "status": "Improving ↑",
    "redness": 0.45,
    "wound_area": 1200,
    "infection_risk_pct": 35,
    "risk_level": "Medium",
    "contributing_factors": ["Wound area growing"]
  },
  "report": {
    "doctor_summary": "Clinical assessment...",
    "patient_advice": ["Advice 1", "Advice 2", "Advice 3"]
  },
  "predicted_image": "outputs/predicted/patient_001_day3_predicted.jpg",
  "charts": {...},
  "uploaded_at": "2024-01-01T12:00:00"
}
```

## Testing the System

### Option 1: Using the Web Interface

1. Make sure all 3 services are running
2. Open http://localhost:5173
3. Click "Upload Scan"
4. Select a wound image (JPG or PNG)
5. Enter patient ID and monitoring day
6. Click "Analyze Scan"
7. View results instantly!

### Option 2: Testing via cURL

```bash
curl -X POST \
  -F "image=@path/to/wound.jpg" \
  -F "patient_id=patient_001" \
  -F "day=3" \
  http://localhost:5000/api/upload
```

### Option 3: Health Check

```bash
curl http://localhost:5000/api/health
```

## Troubleshooting

### Backend won't start

**Error: "Port 5000 already in use"**

```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (Windows PowerShell)
Stop-Process -Id <PID> -Force
```

### Frontend can't reach backend

**Error: "Failed to process image. Make sure backend is running..."**

Check that:

1. Backend is running on `http://localhost:5000`
2. CORS is enabled (it is in app.py)
3. Firewall allows localhost:5000

### Image upload fails

**Common issues:**

- File format: Only JPG/PNG supported
- File size: Max 10MB
- Image path: Make sure file exists

### ML modules import errors

```bash
# Reinstall ML dependencies
cd ml
pip install --upgrade -r requirements.txt
```

## Advanced Configuration

### Change Backend Port

Edit `backend/app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000
```

Then update Frontend API URL in `frontend/src/App.jsx`:

```javascript
const API_BASE_URL = "http://localhost:5000"; // Change port here
```

### Enable Production Mode

Frontend:

```bash
cd frontend
npm run build
npm run preview
```

Backend:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Configure Ollama for Reports

The backend uses Ollama's Mistral model for generating doctor reports. Make sure Ollama is running:

```bash
ollama pull mistral
ollama serve
```

If Ollama isn't available, the system falls back to default templates.

## Next Steps

1. ✅ Setup complete!
2. 📊 Start uploading wound images
3. 🔍 Monitor healing progress over days
4. 📈 Track metrics and infection risk
5. 🚀 Integrate with hospital systems

## Support

- Backend logs → Check terminal running `python app.py`
- Frontend logs → Check browser console (F12)
- ML pipeline logs → Check terminal running the pipeline

## Project Files Modified

- `frontend/src/App.jsx` - Updated with backend integration
- `frontend/src/index.css` - Tailwind CSS
- `backend/app.py` - New Flask API server
- `backend/requirements.txt` - Backend dependencies
