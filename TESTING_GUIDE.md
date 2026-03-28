# HealTrack AI - Testing & Verification Guide

## Pre-Flight Checklist

Before starting, verify:

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Git installed (for version control)
- [ ] Have a wound image to upload (JPG or PNG)

Check versions:

```bash
python --version
node --version
npm --version
```

## Step 1: Install All Dependencies

### Install ML Dependencies

```bash
cd ml
pip install -r requirements.txt
```

Expected: All packages installed without errors

### Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

Expected: Dependencies cached or installed, no errors

### Install Backend Dependencies

```bash
cd ../backend
pip install -r requirements.txt
```

Expected: Flask, Flask-CORS, Werkzeug installed

## Step 2: Start Services

### Option A: Automated (Windows)

```bash
cd ..
start.bat
```

### Option B: Automated (macOS/Linux)

```bash
cd ..
chmod +x start.sh
./start.sh
```

### Option C: Manual (All Platforms)

**In Terminal 1:**

```bash
cd backend
python app.py
```

Expected:

```
============================================================
  HealTrack AI Backend API
============================================================
  Server: http://localhost:5000
  Upload endpoint: POST http://localhost:5000/api/upload
============================================================
```

**In Terminal 2:**

```bash
cd frontend
npm run dev
```

Expected:

```
  VITE v8.0.3  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

## Step 3: Verify Services

### Check Backend Health

```bash
curl http://localhost:5000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2024-03-28T12:00:00.000000"
}
```

### Check Frontend

Open browser: http://localhost:5173

Expected: See HealTrack AI dashboard

## Step 4: Test Upload Flow

### Using Web Interface

1. Open http://localhost:5173
2. Click "Upload Scan" button
3. Drag and drop or click to select image
4. Enter:
   - Patient ID: `patient_001`
   - Monitoring Day: `3`
5. Click "Analyze Scan"
6. Wait for processing (5-20 seconds)
7. View results!

### Using cURL (Command Line)

```bash
# Replace "path/to/image.jpg" with actual image path
curl -X POST \
  -F "image=@C:/path/to/image.jpg" \
  -F "patient_id=patient_001" \
  -F "day=3" \
  http://localhost:5000/api/upload
```

Windows PowerShell:

```powershell
$form = @{
    image = Get-Item -Path "C:\path\to\image.jpg"
    patient_id = "patient_001"
    day = "3"
}
Invoke-WebRequest -Uri "http://localhost:5000/api/upload" -Method Post -Form $form
```

### Expected Response

The API should return JSON with:

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
  "report": {...},
  "uploaded_at": "2024-03-28T12:00:00.000000"
}
```

## Step 5: Verify Frontend Display

After successful upload, check:

- [ ] Page displays patient metrics banner
- [ ] Cards show: Healing Score, Status, Infection Risk, Flags
- [ ] Charts display healing trends
- [ ] Doctor summary tab shows clinical notes
- [ ] Patient advice tab shows care recommendations

## Common Test Scenarios

### Scenario 1: Quick Success Test

```bash
# Assuming you have a test image
curl -X POST \
  -F "image=@test.jpg" \
  -F "patient_id=test_patient" \
  -F "day=1" \
  http://localhost:5000/api/upload | python -m json.tool
```

### Scenario 2: Multiple Patients

```bash
# Day 1
curl -X POST -F "image=@wound_day1.jpg" -F "patient_id=patient_001" -F "day=1" http://localhost:5000/api/upload

# Day 2
curl -X POST -F "image=@wound_day2.jpg" -F "patient_id=patient_001" -F "day=2" http://localhost:5000/api/upload

# Day 3
curl -X POST -F "image=@wound_day3.jpg" -F "patient_id=patient_001" -F "day=3" http://localhost:5000/api/upload
```

### Scenario 3: Edge Cases

**Test missing patient_id:**

```bash
curl -X POST \
  -F "image=@test.jpg" \
  -F "day=1" \
  http://localhost:5000/api/upload
```

Expected: 200 OK (defaults to "unknown_patient")

**Test file too large:**

```bash
# Create 11MB file and try to upload
curl -X POST \
  -F "image=@large_file.jpg" \
  -F "patient_id=test" \
  -F "day=1" \
  http://localhost:5000/api/upload
```

Expected: 413 error (File too large)

**Test invalid format:**

```bash
curl -X POST \
  -F "image=@document.pdf" \
  -F "patient_id=test" \
  -F "day=1" \
  http://localhost:5000/api/upload
```

Expected: 400 error (Invalid file type)

## Monitoring & Logs

### Backend Logs

Look at the terminal running `python app.py`:

- Request logs
- Processing status
- Errors/warnings

### Frontend Logs

Open browser console (F12):

- Upload progress
- API responses
- React component logs

### ML Pipeline Logs

Terminal running the pipeline shows:

- Preprocessing steps
- ML calculations
- Report generation progress

## Performance Testing

### Measure Upload Time

```bash
# Record start time
$start = Get-Date

# Upload
curl -X POST \
  -F "image=@test.jpg" \
  -F "patient_id=test" \
  -F "day=1" \
  http://localhost:5000/api/upload -o response.json

# Calculate duration
$end = Get-Date
$duration = ($end - $start).TotalSeconds
Write-Host "Processing time: $duration seconds"
```

Expected: 5-20 seconds depending on image size

## Troubleshooting Tests

### Backend won't start

```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Try different port
# Edit backend/app.py and change port from 5000 to 5001
```

### Frontend can't reach backend

```bash
# Make sure backend is running
curl http://localhost:5000/api/health

# Check CORS headers
curl -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  http://localhost:5000/api/upload -v
```

### Image not processing

```bash
# Check image exists and is readable
file C:\path\to\image.jpg

# Try smaller image
```

## Success Criteria

✅ All services start without errors
✅ Backend responds to health check
✅ Frontend loads at localhost:5173
✅ Image upload succeeds
✅ Results display in UI
✅ All metrics are populated
✅ Charts render correctly
✅ Doctor report shows
✅ Patient advice displays

## Next: Production Testing

After basic tests pass:

1. Test with real wound images
2. Test multiple patients
3. Test stress (many uploads)
4. Test error recovery
5. Test with different image sizes
6. Monitor performance metrics

## Debug Mode

To enable debug logging:

**Backend:**

```python
# Add to backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**

```javascript
// Add to frontend/src/App.jsx
const DEBUG = true;
if (DEBUG) console.log("Request:", { file, patientId, day });
```

---

You're all set! Follow these steps to verify and test your HealTrack AI system.

For issues, check:

1. Service terminal logs
2. Browser console (F12)
3. SETUP_GUIDE.md troubleshooting
