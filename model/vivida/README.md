# GBM Treatment Optimization API v3.0

**Full Feature Set - Production Ready**

This is the dedicated API service for the v3.0 model with all 115 features including genetic markers, neurological symptoms, and clinical features.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Train the Model

The folder already includes pre-trained models, but if you want to retrain:

```bash
python gbm_train_models_enhanced_full_features.py
```

This will:
- Read data from `glioblastoma_data.xlsx`
- Train models with 115 features
- Save to `gbm_models_output_all90_dosage_full_features/`
- Take ~7 minutes

### 3. Start the Server

**Windows:**
```bash
start_server.bat
```

**Linux/Mac:**
```bash
./start_server.sh
```

Or manually:
```bash
python app.py
```

Server will start on `http://localhost:5000`

## API Endpoints

### GET /health
Health check and version info

**Response:**
```json
{
  "status": "ok",
  "service": "GBM Treatment Optimization API v3.0",
  "version": "3.0",
  "features": 115,
  "model_type": "full_features"
}
```

### GET /model/info
Detailed model information and supported features

**Response:**
```json
{
  "version": "3.0",
  "features": 115,
  "accuracy": {
    "r_target": "99.98%",
    "K_target": "99.99%",
    "alpha_target": "99.93%",
    "beta_target": "99.48%"
  },
  "supported_features": {
    "required": ["id", "age", "tumor_size_before", "kps", "treatment"],
    "genetic": ["mgmt_methylation", "idh_mutation", "egfr_amplification", "tert_mutation", "atrx_mutation"],
    "clinical": ["edema_volume", "steroid_dose", "antiseizure_meds"],
    "neurological": ["neurological_symptoms", "has_headache", "has_seizures", "symptom_count"]
  }
}
```

### POST /optimize
Full optimization with all results

**Request:**
```json
{
  "id": "PATIENT_001",
  "age": 58,
  "tumor_size_before": 3.5,
  "kps": 80,
  "treatment": "chemoradiotherapy",

  "mgmt_methylation": true,
  "idh_mutation": false,
  "edema_volume": 6.5,
  "neurological_symptoms": "headache, seizures"
}
```

**Response:** Complete optimization results with all tested dosages

### POST /optimize/summary
Simplified summary for UI

**Request:** Same as /optimize

**Response:**
```json
{
  "model_version": "3.0",
  "patient_id": "PATIENT_001",
  "doctor_plan": {
    "prediction": 1.36,
    "treatment_type": "chemoradiotherapy"
  },
  "global_optimal": {
    "treatment_type": "chemoradiotherapy",
    "prediction": 1.35,
    "improvement_percent": 0.9,
    "chemotherapy": {
      "dose_mg_per_m2": 150
    },
    "radiotherapy": {
      "total_dose_Gy": 60,
      "fractions": 30,
      "BED": 72.0
    }
  },
  "recommendation": "optimal",
  "patient_characteristics": {
    "mgmt_status": "methylated",
    "edema_volume": 6.5,
    "symptom_count": 2
  }
}
```

### POST /validate
Validate patient data without running optimization

**Request:** Patient data JSON

**Response:**
```json
{
  "valid": true,
  "message": "Patient data is valid",
  "model_version": "3.0"
}
```

## Testing

Run the test script:
```bash
python test_api.py
```

Or use cURL:
```bash
curl http://localhost:5000/health

curl -X POST http://localhost:5000/optimize/summary \
  -H "Content-Type: application/json" \
  -d @example_patient.json
```

## Features v3.0

### NEW: Genetic Markers
- `mgmt_methylation` - MGMT methylation status (better chemo response)
- `idh_mutation` - IDH mutation status (better prognosis)
- `egfr_amplification` - EGFR amplification
- `tert_mutation` - TERT promoter mutation
- `atrx_mutation` - ATRX mutation

### NEW: Clinical Features
- `edema_volume` - Peritumoral edema volume (cm³)
- `steroid_dose` - Steroid dosage (mg)
- `antiseizure_meds` - Antiseizure medication (boolean)

### NEW: Neurological Symptoms
- `neurological_symptoms` - String: "headache, seizures, motor_deficit"
- Or individual flags: `has_headache`, `has_seizures`, etc.
- `symptom_count` - Total symptom count

### Tumor Characteristics
- `lateralization` - "left" / "right" / "bilateral"
- `rano_response` - RANO response category

### History
- `family_history` - Family history of cancer
- `previous_radiation` - Previous radiation therapy

## Model Performance

- **r_target:** R² = 99.98% (tumor growth rate)
- **K_target:** R² = 99.99% (carrying capacity)
- **alpha_target:** R² = 99.93% (chemotherapy sensitivity)
- **beta_target:** R² = 99.48% (radiotherapy sensitivity)

## Clinical Significance

### MGMT Methylation
- **MGMT+** patients → +30% chemotherapy effectiveness
- Model automatically increases expected alpha parameter

### IDH Mutation
- **IDH+** patients → +20% overall response
- Better prognosis, can tolerate more aggressive treatment

### Neurological Symptoms
- More symptoms → reduced treatment tolerance
- Model reduces alpha/beta by ~3% per symptom

### Edema Volume
- **Edema > 5 cm³** → reduced tolerance
- Model reduces alpha/beta by ~5% per cm³ above 5

## Files in This Directory

```
api_service_v3/
├── app.py                                          # API server (Flask)
├── requirements.txt                                # Python dependencies
├── README.md                                       # This file
├── example_patient.json                           # Example patient data
├── test_api.py                                    # Test script
├── start_server.bat                               # Windows startup
├── start_server.sh                                # Linux/Mac startup
├── gbm_optimize_treatment_dosage_v3.py           # Optimization module
├── gbm_optimize_treatment_extended_dosage_v3.py  # Extended optimizer
└── gbm_models_output_all90_dosage_full_features/ # Trained models
    ├── model_r_target.pkl
    ├── model_K_target.pkl
    ├── model_alpha_target.pkl
    ├── model_beta_target.pkl
    ├── scaler.pkl
    ├── label_encoders.pkl
    └── metadata.json
```

## Port Configuration

Default port: 5000

To change port, edit `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## Production Deployment

For production use:
1. Set `debug=False` in app.py
2. Use production WSGI server (gunicorn, waitress)
3. Add authentication/authorization
4. Enable HTTPS
5. Add rate limiting
6. Add logging and monitoring

## Support

For issues or questions, refer to the main project documentation:
- `../README_V3.md` - v3.0 documentation
- `../ENHANCED_FEATURES_INFO.md` - Feature details

## Version

**API Version:** 3.0
**Model Version:** 3.0 (Full Features)
**Features:** 115
**Status:** Production Ready
