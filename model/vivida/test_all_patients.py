#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test optimizer with multiple patient profiles
"""

import json
import os
import sys
from pathlib import Path

# Import optimizer
from gbm_optimize_treatment_extended_dosage_v3 import optimize_treatment_with_dosage_grid

def test_patient(patient_file: str):
    """Test optimization for a single patient"""
    print("\n" + "="*80)
    print(f"TESTING: {patient_file}")
    print("="*80)

    # Load patient
    with open(patient_file, 'r') as f:
        patient = json.load(f)

    print(f"\nPatient ID: {patient['id']}")
    print(f"Age: {patient['age']}, KPS: {patient['kps']}, Tumor: {patient['tumor_size_before']} cm3")

    if patient.get('mgmt_methylation'):
        print("MGMT: Methylated (good prognosis)")
    if patient.get('idh_mutation'):
        print("IDH: Mutant (better prognosis)")
    if patient.get('symptom_count', 0) > 0:
        print(f"Symptoms: {patient['symptom_count']}")

    # Run optimization
    try:
        result = optimize_treatment_with_dosage_grid(
            patient=patient,
            doctor_plan=patient,
            test_all_modalities=True
        )

        print("\n" + "-"*80)
        print("RESULT SUMMARY:")
        print("-"*80)
        print(f"Current plan prediction: {result['doctor_plan_prediction']:.2f} cm3")
        print(f"Global optimal prediction: {result['best_dosage_global']['pred_12m']:.2f} cm3")
        print(f"Improvement: {result['global_improvement']:.1f}%")
        print(f"Optimal treatment: {result['best_dosage_global']['treatment_type']}")

        if result['best_dosage_global'].get('chemo_dose_mg_per_m2', 0) > 0:
            print(f"  Chemo: {result['best_dosage_global']['chemo_dose_mg_per_m2']:.0f} mg/m2")
        if result['best_dosage_global'].get('radio_total_Gy', 0) > 0:
            print(f"  Radio: {result['best_dosage_global']['radio_total_Gy']:.0f} Gy / {result['best_dosage_global']['radio_fractions']} fr")

        return True

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Test all patients in test_patients folder"""
    test_dir = Path("test_patients")

    if not test_dir.exists():
        print(f"Error: {test_dir} not found")
        return

    # Find all patient JSON files
    patient_files = sorted(test_dir.glob("patient_*.json"))

    if not patient_files:
        print(f"No patient files found in {test_dir}")
        return

    print("="*80)
    print("GBM OPTIMIZER - MULTI-PATIENT TEST")
    print("="*80)
    print(f"\nFound {len(patient_files)} patient(s)")

    results = []
    for pf in patient_files:
        success = test_patient(str(pf))
        results.append((pf.name, success))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    for name, success in results:
        status = "[OK] PASSED" if success else "[FAIL] FAILED"
        print(f"{status}: {name}")

    passed = sum(1 for _, s in results if s)
    total = len(results)
    print(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        print("\n[OK] ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"\n[FAIL] {total - passed} TEST(S) FAILED")
        sys.exit(1)

if __name__ == '__main__':
    main()
