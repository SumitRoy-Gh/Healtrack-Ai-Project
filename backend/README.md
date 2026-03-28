# Backend README

## Setup

1. Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Start the backend server:

```bash
python app.py
```

The backend API will run on `http://localhost:5000`

## API Endpoints

### Health Check

- **GET** `/api/health` - Check if server is running

### Upload and Process

- **POST** `/api/upload` - Upload wound image and process through ML pipeline
  - Form data:
    - `image` (file): Wound image (jpg, jpeg, png)
    - `patient_id` (string): Patient identifier
    - `day` (integer): Monitoring day

Returns JSON with:

- Patient metrics (healing score, infection risk, etc.)
- Doctor summary and patient advice
- Predicted future wound image
- Generated charts

## Configuration

- **Max file size**: 10MB
- **Allowed formats**: JPG, JPEG, PNG
- **CORS**: Enabled for frontend integration
