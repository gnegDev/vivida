#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API Service for Glioblastoma Treatment Optimization v3.0
Full Feature Set: Neurological, Genetic, Clinical features

Version: 3.0 (Production)
Model: 115 features, R² > 99.4% for all parameters
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import traceback
from typing import Dict, Any

# Import v3.0 optimization
from gbm_optimize_treatment_extended_dosage_v3 import optimize_treatment_with_dosage_grid

app = Flask(__name__)
CORS(app)  # Enable CORS

MODEL_VERSION = "3.0"
MODEL_FEATURES = 115

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'GBM Treatment Optimization API v3.0',
        'version': MODEL_VERSION,
        'features': MODEL_FEATURES,
        'model_type': 'full_features'
    }), 200

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        'version': MODEL_VERSION,
        'features': MODEL_FEATURES,
        'accuracy': {
            'r_target': '99.98%',
            'K_target': '99.99%',
            'alpha_target': '99.93%',
            'beta_target': '99.48%'
        },
        'supported_features': {
            'required': ['id', 'age', 'tumor_size_before', 'kps', 'treatment'],
            'basic': ['gender', 'resection_extent', 'molecular_subtype', 'tumor_location', 'contrast_enhancement'],
            'genetic': ['mgmt_methylation', 'idh_mutation', 'egfr_amplification', 'tert_mutation', 'atrx_mutation'],
            'clinical': ['edema_volume', 'steroid_dose', 'antiseizure_meds'],
            'neurological': ['neurological_symptoms', 'has_headache', 'has_seizures', 'symptom_count'],
            'other': ['lateralization', 'rano_response', 'family_history', 'previous_radiation']
        }
    }), 200

@app.route('/optimize', methods=['POST'])
def optimize_treatment():
    """
    Main optimization endpoint

    Request Body:
    {
        "id": "PATIENT_001",
        "age": 58,
        "tumor_size_before": 3.5,
        "kps": 80,
        "treatment": "chemoradiotherapy",

        // Optional v3.0 features:
        "mgmt_methylation": true,
        "idh_mutation": false,
        "edema_volume": 6.5,
        "neurological_symptoms": "headache, seizures",
        ...
    }

    Response: Full optimization results
    """
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON',
                'message': 'Content-Type must be application/json'
            }), 400

        patient_data = request.get_json()

        # Validate required fields
        required_fields = ['id', 'age', 'tumor_size_before', 'kps', 'treatment']
        missing_fields = [field for field in required_fields if field not in patient_data]

        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'required_fields': required_fields
            }), 400

        # Optional parameters
        test_all_modalities = request.args.get('test_all_modalities', 'true').lower() == 'true'

        # Run optimization (suppress console output)
        import sys
        from io import StringIO

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = optimize_treatment_with_dosage_grid(
                patient=patient_data,
                doctor_plan=patient_data,
                test_all_modalities=test_all_modalities
            )
        finally:
            console_output = sys.stdout.getvalue()
            sys.stdout = old_stdout

        # Add debug output if requested
        if request.args.get('debug', 'false').lower() == 'true':
            result['console_output'] = console_output

        result['model_version'] = MODEL_VERSION
        result['model_features'] = MODEL_FEATURES

        return jsonify(result), 200

    except Exception as e:
        error_trace = traceback.format_exc()
        return jsonify({
            'error': 'Optimization failed',
            'message': str(e),
            'traceback': error_trace,
            'model_version': MODEL_VERSION
        }), 500

@app.route('/optimize/summary', methods=['POST'])
def optimize_summary():
    """
    Simplified summary for UI

    Returns concise results with key information
    """
    try:
        patient_data = request.get_json()

        print(patient_data)

        # Run optimization
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = optimize_treatment_with_dosage_grid(
                patient=patient_data,
                doctor_plan=patient_data,
                test_all_modalities=True
            )
        finally:
            sys.stdout = old_stdout

        # Build simplified summary
        summary = {
            'model_version': MODEL_VERSION,
            'patient_id': result.get('patient_id'),
            'doctor_plan': {
                'prediction': result.get('doctor_plan_prediction'),
                'treatment_type': result.get('doctor_treatment_type')
            },
            'global_optimal': {
                'treatment_type': result['best_dosage_global']['treatment_type'],
                'prediction': result['best_dosage_global']['pred_12m'],
                'improvement_percent': result.get('global_improvement', 0),
                'chemotherapy': {
                    'dose_mg_per_m2': result['best_dosage_global'].get('chemo_dose_mg_per_m2', 0)
                } if result['best_dosage_global'].get('chemo_dose_mg_per_m2', 0) > 0 else None,
                'radiotherapy': {
                    'total_dose_Gy': result['best_dosage_global'].get('radio_total_Gy', 0),
                    'fractions': result['best_dosage_global'].get('radio_fractions', 0),
                    'BED': result['best_dosage_global'].get('BED', 0)
                } if result['best_dosage_global'].get('radio_total_Gy', 0) > 0 else None
            },
            'local_optimal': None,
            'recommendation': 'optimal'
        }

        # Add local optimal
        if 'best_dosage_local' in result:
            summary['local_optimal'] = {
                'treatment_type': result['best_dosage_local']['treatment_type'],
                'prediction': result['best_dosage_local']['pred_12m'],
                'improvement_percent': result.get('local_improvement', 0)
            }

        # Determine recommendation
        global_improvement = result.get('global_improvement', 0)
        if global_improvement >= 10:
            summary['recommendation'] = 'major_change'
        elif global_improvement >= 3:
            summary['recommendation'] = 'minor_change'
        else:
            summary['recommendation'] = 'optimal'

        # Add patient characteristics (v3.0 specific)
        characteristics = {}
        if patient_data.get('mgmt_methylation'):
            characteristics['mgmt_status'] = 'methylated'
        if patient_data.get('idh_mutation'):
            characteristics['idh_status'] = 'mutant'
        if patient_data.get('edema_volume', 0) > 0:
            characteristics['edema_volume'] = patient_data['edema_volume']
        if patient_data.get('symptom_count', 0) > 0:
            characteristics['symptom_count'] = patient_data['symptom_count']

        if characteristics:
            summary['patient_characteristics'] = characteristics

        return jsonify(summary), 200

    except Exception as e:
        error_trace = traceback.format_exc()
        return jsonify({
            'error': 'Optimization failed',
            'message': str(e),
            'traceback': error_trace
        }), 500

@app.route('/validate', methods=['POST'])
def validate_patient():
    """Validate patient data without running optimization"""
    try:
        patient_data = request.get_json()

        required_fields = ['id', 'age', 'tumor_size_before', 'kps', 'treatment']
        missing_fields = [field for field in required_fields if field not in patient_data]

        validation_errors = []

        # Validate basic fields
        if 'age' in patient_data:
            if not isinstance(patient_data['age'], (int, float)) or patient_data['age'] < 0 or patient_data['age'] > 120:
                validation_errors.append('age must be between 0 and 120')

        if 'tumor_size_before' in patient_data:
            if not isinstance(patient_data['tumor_size_before'], (int, float)) or patient_data['tumor_size_before'] <= 0:
                validation_errors.append('tumor_size_before must be positive')

        if 'kps' in patient_data:
            if not isinstance(patient_data['kps'], (int, float)) or patient_data['kps'] < 0 or patient_data['kps'] > 100:
                validation_errors.append('kps must be between 0 and 100')

        # Validate v3.0 fields
        if 'edema_volume' in patient_data:
            if not isinstance(patient_data['edema_volume'], (int, float)) or patient_data['edema_volume'] < 0:
                validation_errors.append('edema_volume must be non-negative')

        if 'steroid_dose' in patient_data:
            if not isinstance(patient_data['steroid_dose'], (int, float)) or patient_data['steroid_dose'] < 0:
                validation_errors.append('steroid_dose must be non-negative')

        if missing_fields or validation_errors:
            return jsonify({
                'valid': False,
                'missing_fields': missing_fields,
                'validation_errors': validation_errors
            }), 400

        return jsonify({
            'valid': True,
            'message': 'Patient data is valid',
            'model_version': MODEL_VERSION
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Validation failed',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /health',
            'GET /model/info',
            'POST /optimize',
            'POST /optimize/summary',
            'POST /validate'
        ]
    }), 404

if __name__ == '__main__':
    print("="*80)
    print("GBM TREATMENT OPTIMIZATION API v3.0")
    print("="*80)
    print(f"Model Version: {MODEL_VERSION}")
    print(f"Features: {MODEL_FEATURES}")
    print(f"Accuracy: R² > 99.4% for all parameters")
    print()
    print("NEW in v3.0:")
    print("  - Genetic markers (MGMT, IDH, EGFR, TERT, ATRX)")
    print("  - Neurological symptoms (7 types + count)")
    print("  - Clinical features (edema, steroids, antiseizure)")
    print("  - Enhanced personalization")
    print()
    print("Endpoints:")
    print("  GET  /health              - Health check")
    print("  GET  /model/info          - Model information")
    print("  POST /optimize            - Full optimization")
    print("  POST /optimize/summary    - Simplified summary")
    print("  POST /validate            - Validate patient data")
    print()
    print("Starting server on http://localhost:5000")
    print("="*80)

    app.run(host='0.0.0.0', port=5050, debug=True)
