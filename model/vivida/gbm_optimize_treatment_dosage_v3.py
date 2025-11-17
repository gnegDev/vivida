#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gbm_optimize_treatment_dosage_v3.py

ENHANCED VERSION v3.0 - Support for ALL features
- Neurological symptoms
- Genetic markers (MGMT, IDH, EGFR, TERT, ATRX)
- Clinical features (edema, steroids, antiseizure)
- Tumor characteristics (lateralization, family_history, previous_radiation)
- Treatment response (RANO)

Compatible with models trained with gbm_train_models_enhanced_full_features.py
"""

import os
import re
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from joblib import load
import json
import warnings

# Suppress sklearn warnings about feature names
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# ============================================================================
# CONFIG
# ============================================================================
MODEL_DIR = "gbm_models_output_all90_dosage_full_features"
BASELINE_R = 0.12
R_UNTREATED = 0.12
SIM_MONTHS = 12

# ============================================================================
# LOAD MODELS
# ============================================================================
print(f"Loading models from {MODEL_DIR}...")
stacked_models = load(os.path.join(MODEL_DIR, "stacked_models.joblib"))
enc = load(os.path.join(MODEL_DIR, "onehot_encoder.joblib"))
scaler = load(os.path.join(MODEL_DIR, "scaler.joblib"))

with open(os.path.join(MODEL_DIR, "feature_columns.json"), "r") as f:
    feature_columns = json.load(f)

with open(os.path.join(MODEL_DIR, "metadata.json"), "r") as f:
    metadata = json.load(f)
    BASELINE_R = metadata.get('baseline_r', BASELINE_R)
    R_UNTREATED = metadata.get('r_untreated', R_UNTREATED)

print(f"Loaded {len(feature_columns)} features")
print(f"Model version: {metadata.get('version', '2.3')}")
print(f"Full features: {metadata.get('full_features', False)}")

# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_treatment_flags(tstr: str) -> Dict[str, int]:
    """Extract binary treatment flags"""
    t = str(tstr).lower() if tstr else ""

    flags = {
        'chemo': int('temozolomide' in t or 'tmz' in t or 'chem' in t),
        'radio': int('radiation' in t or 'radiotherapy' in t or 'rt' in t or 'radiother' in t),
        'beva': int('bevacizumab' in t or 'beva' in t),
        'other_drug': int(('lomustine' in t or 'ccnu' in t or 'carboplatin' in t or 'etoposide' in t or 'irinotecan' in t))
    }

    # Specific drugs
    flags['drug_temozolomide'] = int('temozolomide' in t or 'tmz' in t)
    flags['drug_lomustine'] = int('lomustine' in t or 'ccnu' in t)
    flags['drug_carboplatin'] = int('carboplatin' in t)
    flags['drug_etoposide'] = int('etoposide' in t)
    flags['drug_irinotecan'] = int('irinotecan' in t)
    flags['drug_bevacizumab'] = int('bevacizumab' in t or 'beva' in t)

    return flags

def parse_dosage_from_treatment(tstr: str) -> Dict[str, float]:
    """Extract dosages from treatment string"""
    t = str(tstr).lower() if tstr else ""

    result = {
        'chemo_dose_mg_per_m2': 0.0,
        'radio_total_Gy': 0.0,
        'radio_fractions': 0.0,
        'radio_BED': 0.0
    }

    # Chemo dose
    chemo_patterns = [r'(\d+)\s*mg\s*/\s*m2', r'(\d+)\s*mg/m²', r'temozolomide\s+(\d+)', r'tmz\s+(\d+)']
    for pattern in chemo_patterns:
        match = re.search(pattern, t)
        if match:
            result['chemo_dose_mg_per_m2'] = float(match.group(1))
            break

    # Radio dose
    radio_patterns = [r'(\d+)\s*gy\s*/\s*(\d+)\s*fr', r'(\d+)\s*gy\s*\/\s*(\d+)', r'radiation\s+(\d+)\s*gy.*?(\d+)\s*fr']
    for pattern in radio_patterns:
        match = re.search(pattern, t)
        if match:
            result['radio_total_Gy'] = float(match.group(1))
            result['radio_fractions'] = float(match.group(2))
            break

    # Calculate BED
    if result['radio_total_Gy'] > 0 and result['radio_fractions'] > 0:
        n = result['radio_fractions']
        d = result['radio_total_Gy'] / n
        result['radio_BED'] = n * d * (1 + d / 10.0)

    return result

def parse_neurological_symptoms(patient: Dict[str, Any]) -> Dict[str, int]:
    """NEW: Parse neurological symptoms from patient data"""
    # Check if explicit neurological symptoms field exists
    if 'neurological_symptoms' in patient:
        s = str(patient['neurological_symptoms']).lower()
    else:
        # Try to infer from individual symptom flags
        s = ""

    symptoms = {
        'has_headache': int(patient.get('has_headache', 0)) if 'has_headache' in patient else int('headache' in s),
        'has_motor_deficit': int(patient.get('has_motor_deficit', 0)) if 'has_motor_deficit' in patient else int('motor_deficit' in s or 'motor deficit' in s),
        'has_seizures': int(patient.get('has_seizures', 0)) if 'has_seizures' in patient else int('seizure' in s),
        'has_sensory_deficit': int(patient.get('has_sensory_deficit', 0)) if 'has_sensory_deficit' in patient else int('sensory_deficit' in s or 'sensory deficit' in s),
        'has_cognitive_decline': int(patient.get('has_cognitive_decline', 0)) if 'has_cognitive_decline' in patient else int('cognitive' in s),
        'has_speech_disturbance': int(patient.get('has_speech_disturbance', 0)) if 'has_speech_disturbance' in patient else int('speech' in s),
        'has_visual_disturbance': int(patient.get('has_visual_disturbance', 0)) if 'has_visual_disturbance' in patient else int('visual' in s)
    }

    # Count symptoms
    if 'symptom_count' in patient:
        symptoms['symptom_count'] = patient['symptom_count']
    elif 'asymptomatic' in s:
        symptoms['symptom_count'] = 0
    else:
        symptoms['symptom_count'] = sum(symptoms.values())

    return symptoms

def extract_dosages_from_patient(patient: Dict[str, Any], treatment_string: str) -> Dict[str, float]:
    """Extract dosages from patient dict or treatment string"""
    dosages = {
        'chemo_dose_mg_per_m2': 0.0,
        'radio_total_Gy': 0.0,
        'radio_BED': 0.0
    }

    # Try explicit chemotherapy field
    if 'chemotherapy' in patient and isinstance(patient['chemotherapy'], dict):
        dosages['chemo_dose_mg_per_m2'] = float(patient['chemotherapy'].get('dose_mg_per_m2', 0))

    # Try explicit radiotherapy field
    if 'radiotherapy' in patient and isinstance(patient['radiotherapy'], dict):
        rt = patient['radiotherapy']
        total_Gy = float(rt.get('total_dose_Gy', 0))
        fractions = int(rt.get('fractions', 0))

        if total_Gy > 0:
            dosages['radio_total_Gy'] = total_Gy
            if fractions > 0:
                d = total_Gy / fractions
                dosages['radio_BED'] = fractions * d * (1 + d / 10.0)

    # If not found, try parsing treatment string
    if dosages['chemo_dose_mg_per_m2'] == 0 or dosages['radio_total_Gy'] == 0:
        parsed = parse_dosage_from_treatment(treatment_string)
        if dosages['chemo_dose_mg_per_m2'] == 0:
            dosages['chemo_dose_mg_per_m2'] = parsed['chemo_dose_mg_per_m2']
        if dosages['radio_total_Gy'] == 0:
            dosages['radio_total_Gy'] = parsed['radio_total_Gy']
            dosages['radio_BED'] = parsed['radio_BED']

    # Apply defaults based on treatment flags
    flags = parse_treatment_flags(treatment_string)
    if flags['chemo'] and dosages['chemo_dose_mg_per_m2'] == 0:
        dosages['chemo_dose_mg_per_m2'] = 75.0

    if flags['radio'] and dosages['radio_total_Gy'] == 0:
        dosages['radio_total_Gy'] = 60.0
        dosages['radio_BED'] = 30 * 2.0 * (1 + 2.0 / 10.0)

    return dosages

# ============================================================================
# FEATURE BUILDING
# ============================================================================

def build_feature_vector(
    patient: Dict[str, Any],
    treatment_string: str,
    dosages: Dict[str, float]
) -> pd.Series:
    """Build feature vector for ML model with ALL features"""

    # Parse treatment flags
    flags = parse_treatment_flags(treatment_string)

    # Parse neurological symptoms
    neuro = parse_neurological_symptoms(patient)

    # Build numeric features
    numeric = {
        # Original features
        'age': float(patient.get('age', 50)),
        'tumor_size_before': float(patient.get('tumor_size_before', 3.0)),
        'kps': float(patient.get('kps', 70)),

        # Treatment flags
        'chemo': flags['chemo'],
        'radio': flags['radio'],
        'beva': flags['beva'],
        'other_drug': flags['other_drug'],

        # Dosages
        'chemo_dose_mg_per_m2': dosages['chemo_dose_mg_per_m2'],
        'radio_total_Gy': dosages['radio_total_Gy'],
        'radio_BED': dosages['radio_BED'],

        # Specific drugs
        'drug_temozolomide': flags['drug_temozolomide'],
        'drug_lomustine': flags['drug_lomustine'],
        'drug_carboplatin': flags['drug_carboplatin'],
        'drug_etoposide': flags['drug_etoposide'],
        'drug_irinotecan': flags['drug_irinotecan'],
        'drug_bevacizumab': flags['drug_bevacizumab'],

        # NEW: Genetic markers
        'mgmt_methylation': int(patient.get('mgmt_methylation', 0)),
        'idh_mutation': int(patient.get('idh_mutation', 0)),
        'egfr_amplification': int(patient.get('egfr_amplification', 0)),
        'tert_mutation': int(patient.get('tert_mutation', 0)),
        'atrx_mutation': int(patient.get('atrx_mutation', 0)),

        # NEW: Clinical features
        'edema_volume': float(patient.get('edema_volume', 0)),
        'steroid_dose': float(patient.get('steroid_dose', 0)),
        'antiseizure_meds': int(patient.get('antiseizure_meds', 0)),

        # NEW: Neurological symptoms
        'has_headache': neuro['has_headache'],
        'has_motor_deficit': neuro['has_motor_deficit'],
        'has_seizures': neuro['has_seizures'],
        'has_sensory_deficit': neuro['has_sensory_deficit'],
        'has_cognitive_decline': neuro['has_cognitive_decline'],
        'has_speech_disturbance': neuro['has_speech_disturbance'],
        'has_visual_disturbance': neuro['has_visual_disturbance'],
        'symptom_count': neuro['symptom_count'],

        # NEW: Other features
        'family_history': int(patient.get('family_history', 0)),
        'previous_radiation': int(patient.get('previous_radiation', 0))
    }

    # Categorical features
    categorical = {
        'gender': str(patient.get('gender', 'M')),
        'resection_extent': str(patient.get('resection_extent', 'subtotal')),
        'molecular_subtype': str(patient.get('molecular_subtype', 'classical')),
        'tumor_location': str(patient.get('tumor_location', 'frontal_lobe')),
        'contrast_enhancement': str(patient.get('contrast_enhancement', 'ring')),
        'stage': str(patient.get('stage', 'Stage 1')),

        # NEW
        'lateralization': str(patient.get('lateralization', 'left')),
        'rano_response': str(patient.get('rano_response', 'stable_disease'))
    }

    # OneHot encode categoricals
    cat_df = pd.DataFrame([categorical])
    enc_arr = enc.transform(cat_df)
    enc_cols = [f"{cat}_{v}" for i, cat in enumerate(['gender', 'resection_extent', 'molecular_subtype',
                                                        'tumor_location', 'contrast_enhancement', 'stage',
                                                        'lateralization', 'rano_response'])
                for v in enc.categories_[i]]
    encoded = dict(zip(enc_cols, enc_arr[0]))

    # Combine
    combined = {**numeric, **encoded}

    # Add fitted params placeholders
    combined['r_fit'] = 0.0
    combined['K_fit'] = numeric['tumor_size_before'] * 2.0
    combined['n_obs'] = 5

    # Add alpha/beta computed (will be predicted)
    combined['alpha_computed'] = 0.05
    combined['beta_computed'] = 0.03

    # Add interactions (same as in training)
    T0 = numeric['tumor_size_before']
    K = combined['K_fit']

    combined['r_fit_x_chemo'] = combined['r_fit'] * numeric['chemo']
    combined['r_fit_x_radio'] = combined['r_fit'] * numeric['radio']
    combined['K_fit_x_chemo'] = K * numeric['chemo']
    combined['K_fit_x_radio'] = K * numeric['radio']
    combined['alpha_computed_x_chemo'] = combined['alpha_computed'] * numeric['chemo']
    combined['beta_computed_x_radio'] = combined['beta_computed'] * numeric['radio']

    combined['chemo_x_radio'] = numeric['chemo'] * numeric['radio']
    combined['chemo_x_tumor_size'] = numeric['chemo'] * T0
    combined['radio_x_tumor_size'] = numeric['radio'] * T0
    combined['beva_x_chemo'] = numeric['beva'] * numeric['chemo']
    combined['kps_x_chemo'] = numeric['kps'] * numeric['chemo']
    combined['treatment_count'] = numeric['chemo'] + numeric['radio'] + numeric['beva']

    combined['chemo_dose_x_tumor_size'] = numeric['chemo_dose_mg_per_m2'] * T0
    combined['chemo_dose_x_kps'] = numeric['chemo_dose_mg_per_m2'] * numeric['kps']
    combined['chemo_dose_x_age'] = numeric['chemo_dose_mg_per_m2'] * numeric['age']
    combined['radio_BED_x_tumor_size'] = numeric['radio_BED'] * T0
    combined['radio_BED_x_kps'] = numeric['radio_BED'] * numeric['kps']
    combined['radio_BED_x_age'] = numeric['radio_BED'] * numeric['age']
    combined['chemo_dose_x_radio_BED'] = numeric['chemo_dose_mg_per_m2'] * numeric['radio_BED']

    # NEW: Genetic × treatment interactions
    combined['mgmt_x_chemo'] = numeric['mgmt_methylation'] * numeric['chemo']
    combined['mgmt_x_chemo_dose'] = numeric['mgmt_methylation'] * numeric['chemo_dose_mg_per_m2']
    combined['idh_x_chemo'] = numeric['idh_mutation'] * numeric['chemo']
    combined['idh_x_radio'] = numeric['idh_mutation'] * numeric['radio']
    combined['egfr_x_chemo'] = numeric['egfr_amplification'] * numeric['chemo']

    # NEW: Clinical × treatment interactions
    combined['edema_x_chemo'] = numeric['edema_volume'] * numeric['chemo']
    combined['edema_x_radio'] = numeric['edema_volume'] * numeric['radio']
    combined['steroid_x_chemo'] = numeric['steroid_dose'] * numeric['chemo']
    combined['symptom_count_x_chemo'] = numeric['symptom_count'] * numeric['chemo']
    combined['symptom_count_x_radio'] = numeric['symptom_count'] * numeric['radio']

    # Non-linear terms
    combined['age_squared'] = numeric['age'] ** 2
    combined['tumor_size_squared'] = T0 ** 2
    combined['tumor_size_log'] = np.log1p(T0)
    combined['r_fit_squared'] = combined['r_fit'] ** 2
    combined['K_fit_log'] = np.log1p(K)
    combined['chemo_dose_squared'] = numeric['chemo_dose_mg_per_m2'] ** 2
    combined['radio_BED_squared'] = numeric['radio_BED'] ** 2
    combined['chemo_dose_log'] = np.log1p(numeric['chemo_dose_mg_per_m2'])
    combined['radio_BED_log'] = np.log1p(numeric['radio_BED'])

    # NEW: Non-linear for new features
    combined['edema_squared'] = numeric['edema_volume'] ** 2
    combined['steroid_squared'] = numeric['steroid_dose'] ** 2
    combined['symptom_count_squared'] = numeric['symptom_count'] ** 2

    # Ensure all features exist
    for feat in feature_columns:
        if feat not in combined:
            combined[feat] = 0.0

    # Create series in correct order
    feat_series = pd.Series([combined.get(f, 0.0) for f in feature_columns], index=feature_columns)

    # Scale
    scaled = scaler.transform(feat_series.values.reshape(1, -1))
    return pd.Series(scaled[0], index=feature_columns)

# ============================================================================
# PREDICTION
# ============================================================================

def predict_params_from_features_row(feat_row: pd.Series) -> Dict[str, float]:
    """Predict Gompertz parameters from feature vector"""
    X_input = feat_row.values.reshape(1, -1)

    r_pred = _predict_single_target(X_input, 'r_target')
    K_pred = _predict_single_target(X_input, 'K_target')
    alpha_pred = _predict_single_target(X_input, 'alpha_target')
    beta_pred = _predict_single_target(X_input, 'beta_target')

    return {
        'r': float(r_pred),
        'K': float(K_pred),
        'alpha': float(alpha_pred),
        'beta': float(beta_pred)
    }

def _predict_single_target(X_input, target):
    """Predict single target using stacking"""
    model = stacked_models[target]
    bases = model['bases']
    meta = model['meta']

    base_preds = np.array([m.predict(X_input)[0] for name, m in bases]).reshape(1, -1)
    return meta.predict(base_preds)[0]

# ============================================================================
# SIMULATION
# ============================================================================

def simulate_gompertz_with_treatment(
    T0: float,
    params: Dict[str, float],
    chemo: int,
    radio: int,
    months: int = 12,
    dt: float = 0.01
) -> Tuple[float, np.ndarray]:
    """Simulate Gompertz growth with treatment"""
    r, K, alpha, beta = params['r'], params['K'], params['alpha'], params['beta']

    T0 = max(T0, 0.1)
    K = max(K, T0 * 1.1)

    t_steps = int(months / dt)
    V = np.zeros(t_steps)
    V[0] = T0

    for i in range(1, t_steps):
        V_curr = max(V[i-1], 0.01)
        dV = r * V_curr * np.log(K / V_curr) - alpha * chemo * V_curr - beta * radio * V_curr
        V[i] = max(V_curr + dV * dt, 0.01)

    return float(V[-1]), V

print("="*80)
print("ENHANCED OPTIMIZATION MODULE v3.0 LOADED")
print("="*80)
print(f"Features: {len(feature_columns)}")
print(f"NEW: Neurological symptoms, genetic markers, clinical features")
print("="*80)
