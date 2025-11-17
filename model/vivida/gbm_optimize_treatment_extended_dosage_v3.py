#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gbm_optimize_treatment_extended_dosage_v3.py

ENHANCED VERSION v3.0 - Extended optimization with ALL features
Compatible with models trained with gbm_train_models_enhanced_full_features.py

NEW in v3.0:
- Support for neurological symptoms
- Support for genetic markers (MGMT, IDH, EGFR, TERT, ATRX)
- Support for clinical features (edema, steroids, antiseizure)
- Support for tumor characteristics (lateralization, RANO response)

Usage:
    python gbm_optimize_treatment_extended_dosage_v3.py patient.json
"""

import os
import json
import argparse
import sys
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import warnings

# Suppress sklearn warnings about feature names
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# Import from v3.0 base module
from gbm_optimize_treatment_dosage_v3 import (
    stacked_models, BASELINE_R, R_UNTREATED, SIM_MONTHS,
    parse_treatment_flags, extract_dosages_from_patient,
    build_feature_vector, predict_params_from_features_row,
    simulate_gompertz_with_treatment
)

# ============================================================================
# OPTIMIZATION WITH DOSAGE GRID SEARCH
# ============================================================================

def optimize_treatment_with_dosage_grid(
    patient: Dict[str, Any],
    doctor_plan: Dict[str, Any] = None,
    chemo_dose_range: List[float] = [50, 75, 100, 125, 150],
    radio_dose_configs: List[Tuple[float, int]] = [(40, 15), (50, 25), (60, 30), (66, 33)],
    test_all_modalities: bool = True
) -> Dict[str, Any]:
    """
    Extended optimization with v3.0 full feature support

    Args:
        patient: Patient data (can include new features: mgmt_methylation,
                 neurological_symptoms, edema_volume, etc.)
        doctor_plan: Current treatment plan (for comparison)
        chemo_dose_range: Chemotherapy doses to test (mg/m²)
        radio_dose_configs: Radiotherapy configs [(total_Gy, fractions), ...]
        test_all_modalities: Test all treatment types or only current

    Returns:
        dict with optimization results
    """
    current_treatment = patient.get('treatment', '')
    flags = parse_treatment_flags(current_treatment)

    all_results = []
    T0 = float(patient.get('tumor_size_before', 3.0))

    # Determine which modalities to test
    if test_all_modalities:
        test_chemo_only = True
        test_radio_only = True
        test_combination = True
        print("\n[i] Mode: testing ALL treatment types")
    else:
        test_chemo_only = flags['chemo'] and not flags['radio']
        test_radio_only = flags['radio'] and not flags['chemo']
        test_combination = flags['chemo'] and flags['radio']
        print(f"\n[i] Mode: optimizing current type ({current_treatment})")

    # 1. RADIATION ONLY
    if test_radio_only:
        print("\n=== RADIATION ONLY ===")
        for total_Gy, fractions in radio_dose_configs:
            dosages = {
                'chemo_dose_mg_per_m2': 0.0,
                'radio_total_Gy': total_Gy,
                'radio_BED': fractions * (total_Gy/fractions) * (1 + (total_Gy/fractions) / 10.0)
            }

            feat = build_feature_vector(patient, "radiation", dosages=dosages)
            params = predict_params_from_features_row(feat)

            pred_12m, curve = simulate_gompertz_with_treatment(
                T0, params, chemo=0, radio=1, months=SIM_MONTHS
            )

            result = {
                'treatment_type': 'radiation',
                'chemo_dose_mg_per_m2': 0.0,
                'radio_total_Gy': total_Gy,
                'radio_fractions': fractions,
                'radio_fraction_dose_Gy': total_Gy / fractions,
                'BED': dosages['radio_BED'],
                'pred_12m': pred_12m,
                'alpha_calculated': params['alpha'],
                'beta_calculated': params['beta'],
                'params': params
            }
            all_results.append(result)

            print(f"  {total_Gy} Gy / {fractions} fr (BED={dosages['radio_BED']:.1f}) -> "
                  f"beta={params['beta']:.4f}, prediction: {pred_12m:.2f} cm3")

    # 2. CHEMOTHERAPY ONLY
    if test_chemo_only:
        print("\n=== CHEMOTHERAPY ONLY ===")
        for dose in chemo_dose_range:
            dosages = {
                'chemo_dose_mg_per_m2': dose,
                'radio_total_Gy': 0.0,
                'radio_BED': 0.0
            }

            feat = build_feature_vector(patient, "chemotherapy", dosages=dosages)
            params = predict_params_from_features_row(feat)

            pred_12m, curve = simulate_gompertz_with_treatment(
                T0, params, chemo=1, radio=0, months=SIM_MONTHS
            )

            result = {
                'treatment_type': 'chemotherapy',
                'chemo_dose_mg_per_m2': dose,
                'radio_total_Gy': 0.0,
                'radio_fractions': 0,
                'radio_fraction_dose_Gy': 0.0,
                'BED': 0.0,
                'pred_12m': pred_12m,
                'alpha_calculated': params['alpha'],
                'beta_calculated': params['beta'],
                'params': params
            }
            all_results.append(result)

            print(f"  TMZ {dose} mg/m2 -> alpha={params['alpha']:.4f}, prediction: {pred_12m:.2f} cm3")

    # 3. COMBINATION THERAPY
    if test_combination:
        print("\n=== COMBINATION THERAPY ===")
        for c_dose in chemo_dose_range:
            for r_total, r_frac in radio_dose_configs:
                dosages = {
                    'chemo_dose_mg_per_m2': c_dose,
                    'radio_total_Gy': r_total,
                    'radio_BED': r_frac * (r_total/r_frac) * (1 + (r_total/r_frac) / 10.0)
                }

                feat = build_feature_vector(patient, "chemoradiotherapy", dosages=dosages)
                params = predict_params_from_features_row(feat)

                pred_12m, curve = simulate_gompertz_with_treatment(
                    T0, params, chemo=1, radio=1, months=SIM_MONTHS
                )

                result = {
                    'treatment_type': 'chemoradiotherapy',
                    'chemo_dose_mg_per_m2': c_dose,
                    'radio_total_Gy': r_total,
                    'radio_fractions': r_frac,
                    'radio_fraction_dose_Gy': r_total / r_frac,
                    'BED': dosages['radio_BED'],
                    'pred_12m': pred_12m,
                    'alpha_calculated': params['alpha'],
                    'beta_calculated': params['beta'],
                    'params': params
                }
                all_results.append(result)

        # Show best 3 combinations
        combo_sorted = sorted([r for r in all_results if r['treatment_type'] == 'chemoradiotherapy'],
                             key=lambda x: x['pred_12m'])[:3]
        for r in combo_sorted:
            print(f"  TMZ {r['chemo_dose_mg_per_m2']:.0f} mg/m2 + RT {r['radio_total_Gy']:.0f} Gy/{r['radio_fractions']} fr -> "
                  f"prediction: {r['pred_12m']:.2f} cm3")

    # Find global best
    best = min(all_results, key=lambda x: x['pred_12m'])

    # ========================================================================
    # DOCTOR'S PLAN ANALYSIS
    # ========================================================================
    doctor_pred = None
    doctor_dosages = None
    doctor_treatment_type = None
    local_best = None
    improvement = 0.0

    if doctor_plan:
        print("\n" + "="*80)
        print("DOCTOR'S PLAN ANALYSIS")
        print("="*80)

        doctor_dosages = extract_dosages_from_patient(doctor_plan, doctor_plan.get('treatment', ''))

        print(f"\nCurrent treatment: {doctor_plan.get('treatment', 'N/A')}")
        if doctor_dosages.get('chemo_dose_mg_per_m2', 0) > 0:
            print(f"  Chemotherapy: Temozolomide {doctor_dosages['chemo_dose_mg_per_m2']:.0f} mg/m2")
        if doctor_dosages.get('radio_total_Gy', 0) > 0:
            fractions = doctor_plan.get('radiotherapy', {}).get('fractions', 30)
            print(f"  Radiotherapy: {doctor_dosages['radio_total_Gy']:.0f} Gy / {fractions} fractions")

        # NEW v3.0: Show genetic and clinical features
        print("\nPatient characteristics:")
        if patient.get('mgmt_methylation'):
            print(f"  MGMT methylated: YES (better chemo response expected)")
        if patient.get('idh_mutation'):
            print(f"  IDH mutant: YES (better prognosis)")
        if patient.get('edema_volume', 0) > 0:
            print(f"  Edema volume: {patient['edema_volume']:.1f} cm3")
        if patient.get('symptom_count', 0) > 0:
            print(f"  Neurological symptoms: {patient['symptom_count']} symptoms")

        # Predict with doctor's dosages
        doctor_feat = build_feature_vector(doctor_plan, doctor_plan.get('treatment', ''), dosages=doctor_dosages)
        doctor_params = predict_params_from_features_row(doctor_feat)

        doctor_flags = parse_treatment_flags(doctor_plan.get('treatment', ''))
        doctor_pred, _ = simulate_gompertz_with_treatment(
            T0, doctor_params, doctor_flags['chemo'], doctor_flags['radio'], months=SIM_MONTHS
        )

        print(f"\nPredicted tumor size (12 months): {doctor_pred:.2f} cm3")

    # ========================================================================
    # RECOMMENDATIONS
    # ========================================================================

    print("\n" + "="*80)
    print("OPTIMIZATION RESULTS")
    print("="*80)

    if doctor_pred is not None:
        print(f"\nCURRENT PLAN:")
        if doctor_dosages.get('chemo_dose_mg_per_m2', 0) > 0:
            print(f"  Chemotherapy: Temozolomide {doctor_dosages['chemo_dose_mg_per_m2']:.0f} mg/m2")
        if doctor_dosages.get('radio_total_Gy', 0) > 0:
            fractions = doctor_plan.get('radiotherapy', {}).get('fractions', 30)
            print(f"  Radiotherapy: {doctor_dosages['radio_total_Gy']:.0f} Gy / {fractions} fractions")
        print(f"  Predicted tumor size (12 months): {doctor_pred:.2f} cm3")

    print("\n" + "="*80)
    print("OPTIMAL DOSAGE (from analysis):")
    print("="*80)

    print(f"  Treatment type: {best['treatment_type']}")

    if best.get('chemo_dose_mg_per_m2', 0) > 0:
        print(f"\n  CHEMOTHERAPY:")
        print(f"    Drug: Temozolomide")
        print(f"    Dose: {best['chemo_dose_mg_per_m2']:.0f} mg/m2")
        print(f"    Calculated alpha: {best.get('alpha_calculated', 0):.4f}")

    if best.get('radio_total_Gy', 0) > 0:
        print(f"\n  RADIOTHERAPY:")
        print(f"    Total dose: {best['radio_total_Gy']:.0f} Gy")
        print(f"    Fractions: {best['radio_fractions']}")
        print(f"    Dose per fraction: {best['radio_fraction_dose_Gy']:.2f} Gy")
        print(f"    BED: {best['BED']:.1f} Gy")
        print(f"    Calculated beta: {best.get('beta_calculated', 0):.4f}")

    print(f"\n  PREDICTION:")
    print(f"    Tumor size (12 months): {best['pred_12m']:.2f} cm3")

    # ========================================================================
    # DUAL RECOMMENDATIONS (GLOBAL + LOCAL)
    # ========================================================================

    print("\n" + "="*80)
    print("SYSTEM RECOMMENDATIONS:")
    print("="*80)

    if doctor_pred is not None:
        # Determine doctor's treatment type
        doctor_flags = parse_treatment_flags(doctor_plan.get('treatment', ''))

        if doctor_flags['chemo'] and doctor_flags['radio']:
            doctor_treatment_type = 'chemoradiotherapy'
        elif doctor_flags['chemo']:
            doctor_treatment_type = 'chemotherapy'
        elif doctor_flags['radio']:
            doctor_treatment_type = 'radiation'

        # Find local best (within same treatment type)
        if doctor_treatment_type:
            same_type_results = [r for r in all_results if r['treatment_type'] == doctor_treatment_type]
            if same_type_results:
                local_best = min(same_type_results, key=lambda x: x['pred_12m'])

        # Global improvement
        improvement = (doctor_pred - best['pred_12m']) / doctor_pred * 100

        print(f"\n1. GLOBAL OPTIMIZATION (best among all treatment types):")
        print(f"   Current plan prediction: {doctor_pred:.2f} cm3")
        print(f"   Global optimal prediction: {best['pred_12m']:.2f} cm3")
        print(f"   Difference: {improvement:.1f}%")

        # Local optimization
        if local_best and local_best['pred_12m'] != doctor_pred:
            local_improvement = (doctor_pred - local_best['pred_12m']) / doctor_pred * 100
            print(f"\n2. LOCAL OPTIMIZATION (best within '{doctor_treatment_type}'):")
            print(f"   Current plan prediction: {doctor_pred:.2f} cm3")
            print(f"   Optimized plan prediction: {local_best['pred_12m']:.2f} cm3")
            print(f"   Difference: {local_improvement:.1f}%")

        # ====================================================================
        # OPTION A: GLOBAL (may change treatment type)
        # ====================================================================

        print(f"\n" + "-"*80)
        print("OPTION A: GLOBAL RECOMMENDATION (may change treatment type)")
        print("-"*80)

        if improvement >= 10:
            print(f"\n[!] Recommend changing treatment plan")
            print(f"    Improvement: {improvement:.1f}%")
            print(f"\n    Changes to global optimal ({best['treatment_type']}):")

            # Chemotherapy changes
            if doctor_dosages.get('chemo_dose_mg_per_m2', 0) != best.get('chemo_dose_mg_per_m2', 0):
                old_dose = doctor_dosages.get('chemo_dose_mg_per_m2', 0)
                new_dose = best.get('chemo_dose_mg_per_m2', 0)
                if old_dose > 0 and new_dose > 0:
                    print(f"      - Change Temozolomide dose: {old_dose:.0f} -> {new_dose:.0f} mg/m2")
                elif old_dose == 0 and new_dose > 0:
                    print(f"      - Add chemotherapy: Temozolomide {new_dose:.0f} mg/m2")
                elif old_dose > 0 and new_dose == 0:
                    print(f"      - Remove chemotherapy")

            # Radiotherapy changes
            if doctor_dosages.get('radio_total_Gy', 0) != best.get('radio_total_Gy', 0):
                old_dose = doctor_dosages.get('radio_total_Gy', 0)
                new_dose = best.get('radio_total_Gy', 0)
                old_fr = doctor_plan.get('radiotherapy', {}).get('fractions', 30)
                new_fr = best.get('radio_fractions', 30)
                if old_dose > 0 and new_dose > 0:
                    print(f"      - Change radiotherapy: {old_dose:.0f} Gy / {old_fr} fr -> {new_dose:.0f} Gy / {new_fr} fr")
                elif old_dose == 0 and new_dose > 0:
                    print(f"      - Add radiotherapy: {new_dose:.0f} Gy / {new_fr} fr")
                elif old_dose > 0 and new_dose == 0:
                    print(f"      - Remove radiotherapy")

        elif improvement >= 3:
            print(f"\n[~] Minor adjustment possible")
            print(f"    Improvement: {improvement:.1f}%")
            print(f"    Consider changing to: {best['treatment_type']}")

        else:
            print(f"\n[OK] Current plan is globally optimal")
            print(f"    Improvement would be: {improvement:.1f}% (insignificant)")

        # ====================================================================
        # OPTION B: LOCAL (optimize current type only)
        # ====================================================================

        print(f"\n" + "-"*80)
        print("OPTION B: LOCAL RECOMMENDATION (optimize current type)")
        print("-"*80)

        if local_best:
            local_improvement = (doctor_pred - local_best['pred_12m']) / doctor_pred * 100

            if local_improvement < 0.5:
                print(f"\n[OK] Current dosages are optimal for '{doctor_treatment_type}'")
                print(f"    No dosage adjustments needed")

            elif local_improvement >= 3:
                print(f"\n[~] Dosage optimization recommended")
                print(f"    Improvement: {local_improvement:.1f}%")
                print(f"\n    Suggested dosage changes:")

                if local_best.get('chemo_dose_mg_per_m2', 0) != doctor_dosages.get('chemo_dose_mg_per_m2', 0):
                    old = doctor_dosages.get('chemo_dose_mg_per_m2', 0)
                    new = local_best.get('chemo_dose_mg_per_m2', 0)
                    if old > 0 and new > 0:
                        print(f"      - TMZ: {old:.0f} -> {new:.0f} mg/m2")

                if local_best.get('radio_total_Gy', 0) != doctor_dosages.get('radio_total_Gy', 0):
                    old = doctor_dosages.get('radio_total_Gy', 0)
                    new = local_best.get('radio_total_Gy', 0)
                    old_fr = doctor_plan.get('radiotherapy', {}).get('fractions', 30)
                    new_fr = local_best.get('radio_fractions', 30)
                    if old > 0 and new > 0:
                        print(f"      - RT: {old:.0f} Gy/{old_fr} fr -> {new:.0f} Gy/{new_fr} fr")

            else:
                print(f"\n[~] Minor dosage optimization possible")
                print(f"    Improvement: {local_improvement:.1f}%")

        # ====================================================================
        # FINAL RECOMMENDATION
        # ====================================================================

        print(f"\n" + "="*80)
        print("FINAL RECOMMENDATION:")
        print("="*80)

        if improvement >= 10 and local_improvement >= 3:
            print(f"\nDoctor has TWO options:")
            print(f"  1. GLOBAL: Change to {best['treatment_type']} -> {improvement:.1f}% improvement")
            print(f"  2. LOCAL: Keep {doctor_treatment_type}, adjust dosages -> {local_improvement:.1f}% improvement")
            print(f"\nRecommendation: Consider GLOBAL option for better outcome")

        elif improvement >= 10:
            print(f"\nRECOMMENDATION: Change treatment type")
            print(f"  - Current: {doctor_treatment_type}")
            print(f"  - Optimal: {best['treatment_type']}")
            print(f"  - Improvement: {improvement:.1f}%")

        elif local_improvement >= 3:
            print(f"\nRECOMMENDATION: Adjust dosages")
            print(f"  - Keep treatment type: {doctor_treatment_type}")
            print(f"  - Optimize doses")
            print(f"  - Improvement: {local_improvement:.1f}%")

        else:
            print(f"\nRECOMMENDATION: Current plan is optimal")
            print(f"  - Treatment type: correct")
            print(f"  - Dosages: optimal")
            print(f"  - No changes needed")

    else:
        print(f"\n[i] RECOMMENDED DOSAGE:")
        print(f"    Optimal plan gives prediction {best['pred_12m']:.2f} cm3 at 12 months")

    print("="*80)

    # Prepare result dictionary
    result = {
        'patient_id': patient.get('id', patient.get('patient_id', 'UNKNOWN')),
        'all_results': all_results,
        'best_dosage_global': best,
        'doctor_plan_prediction': doctor_pred,
        'optimization_summary': {
            'tested_regimens': len(all_results),
            'best_pred_12m': best['pred_12m'],
            'treatment_type': best['treatment_type']
        }
    }

    # Add local optimization info
    if doctor_pred is not None and local_best:
        result['best_dosage_local'] = local_best
        result['local_improvement'] = (doctor_pred - local_best['pred_12m']) / doctor_pred * 100
        result['global_improvement'] = improvement
        result['doctor_treatment_type'] = doctor_treatment_type

    return result

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='GBM Treatment Optimization v3.0 (Full Features)')
    parser.add_argument('patient_json', help='Path to patient JSON file')
    parser.add_argument('--output', '-o', help='Output JSON file (optional)')
    parser.add_argument('--all-modalities', action='store_true',
                       help='Test all treatment modalities (not just current plan)')
    parser.add_argument('--current-only', action='store_true',
                       help='Only optimize current treatment type (default: test all)')
    args = parser.parse_args()

    # Load patient
    with open(args.patient_json, 'r', encoding='utf-8') as f:
        patient = json.load(f)

    # Check if doctor plan is specified
    test_all = not args.current_only if not args.all_modalities else True

    # Run optimization
    result = optimize_treatment_with_dosage_grid(
        patient=patient,
        doctor_plan=patient,
        test_all_modalities=test_all
    )

    # Save output if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n[i] Results saved to: {args.output}")

if __name__ == '__main__':
    main()
