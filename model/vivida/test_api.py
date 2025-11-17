#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for GBM Treatment Optimization API v3.0
"""

import requests
import json
import sys

API_BASE = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*80)
    print("TEST 1: Health Check")
    print("="*80)

    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            data = response.json()
            if data['version'] == '3.0' and data['features'] == 115:
                print("✓ PASSED: v3.0 API is running with 115 features")
                return True
            else:
                print("✗ FAILED: Unexpected version or feature count")
                return False
        else:
            print("✗ FAILED: Health check returned non-200 status")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n" + "="*80)
    print("TEST 2: Model Info")
    print("="*80)

    try:
        response = requests.get(f"{API_BASE}/model/info")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Version: {data['version']}")
            print(f"Features: {data['features']}")
            print(f"Accuracy:")
            for param, acc in data['accuracy'].items():
                print(f"  {param}: {acc}")

            print("✓ PASSED: Model info retrieved")
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_validate():
    """Test validation endpoint"""
    print("\n" + "="*80)
    print("TEST 3: Validate Patient Data")
    print("="*80)

    # Valid patient
    valid_patient = {
        "id": "TEST_001",
        "age": 58,
        "tumor_size_before": 3.5,
        "kps": 80,
        "treatment": "chemoradiotherapy"
    }

    try:
        response = requests.post(
            f"{API_BASE}/validate",
            json=valid_patient,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200 and response.json()['valid']:
            print("✓ PASSED: Valid patient accepted")
            return True
        else:
            print("✗ FAILED: Valid patient rejected")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_optimize_minimal():
    """Test optimization with minimal patient data"""
    print("\n" + "="*80)
    print("TEST 4: Optimize (Minimal Data)")
    print("="*80)

    minimal_patient = {
        "id": "TEST_MINIMAL",
        "age": 58,
        "tumor_size_before": 3.5,
        "kps": 80,
        "treatment": "chemoradiotherapy"
    }

    try:
        response = requests.post(
            f"{API_BASE}/optimize/summary",
            json=minimal_patient,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Patient ID: {data['patient_id']}")
            print(f"Model Version: {data['model_version']}")
            print(f"\nDoctor Plan:")
            print(f"  Treatment: {data['doctor_plan']['treatment_type']}")
            print(f"  Prediction: {data['doctor_plan']['prediction']:.2f} cm")
            print(f"\nGlobal Optimal:")
            print(f"  Treatment: {data['global_optimal']['treatment_type']}")
            print(f"  Prediction: {data['global_optimal']['prediction']:.2f} cm")
            print(f"  Improvement: {data['global_optimal']['improvement_percent']:.1f}%")
            print(f"\nRecommendation: {data['recommendation']}")

            print("✓ PASSED: Optimization successful (minimal data)")
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_optimize_full_features():
    """Test optimization with full v3.0 features"""
    print("\n" + "="*80)
    print("TEST 5: Optimize (Full v3.0 Features)")
    print("="*80)

    # Load example patient
    try:
        with open('example_patient.json', 'r') as f:
            full_patient = json.load(f)
    except:
        print("Warning: example_patient.json not found, using inline data")
        full_patient = {
            "id": "TEST_FULL_V3",
            "age": 58,
            "gender": "M",
            "tumor_size_before": 3.5,
            "kps": 80,
            "resection_extent": "gross_total",
            "molecular_subtype": "classical",
            "tumor_location": "temporal_lobe",
            "contrast_enhancement": "ring",
            "treatment": "chemoradiotherapy",

            "mgmt_methylation": True,
            "idh_mutation": False,
            "egfr_amplification": True,
            "tert_mutation": True,
            "atrx_mutation": False,

            "edema_volume": 6.5,
            "steroid_dose": 12.0,
            "antiseizure_meds": True,

            "neurological_symptoms": "headache, seizures",

            "lateralization": "left",
            "rano_response": "stable_disease",
            "family_history": False,
            "previous_radiation": False
        }

    try:
        response = requests.post(
            f"{API_BASE}/optimize/summary",
            json=full_patient,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Patient ID: {data['patient_id']}")
            print(f"Model Version: {data['model_version']}")

            if 'patient_characteristics' in data:
                print(f"\nPatient Characteristics (v3.0):")
                for key, value in data['patient_characteristics'].items():
                    print(f"  {key}: {value}")

            print(f"\nDoctor Plan:")
            print(f"  Treatment: {data['doctor_plan']['treatment_type']}")
            print(f"  Prediction: {data['doctor_plan']['prediction']:.2f} cm")

            print(f"\nGlobal Optimal:")
            print(f"  Treatment: {data['global_optimal']['treatment_type']}")
            print(f"  Prediction: {data['global_optimal']['prediction']:.2f} cm")
            print(f"  Improvement: {data['global_optimal']['improvement_percent']:.1f}%")

            if data['global_optimal'].get('chemotherapy'):
                print(f"  Chemo: {data['global_optimal']['chemotherapy']['dose_mg_per_m2']} mg/m²")

            if data['global_optimal'].get('radiotherapy'):
                radio = data['global_optimal']['radiotherapy']
                print(f"  Radio: {radio['total_dose_Gy']} Gy in {radio['fractions']} fractions (BED: {radio.get('BED', 0):.1f})")

            print(f"\nRecommendation: {data['recommendation']}")

            print("✓ PASSED: Optimization successful (full v3.0 features)")
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_invalid_data():
    """Test API with invalid data"""
    print("\n" + "="*80)
    print("TEST 6: Invalid Data Handling")
    print("="*80)

    # Missing required field
    invalid_patient = {
        "id": "TEST_INVALID",
        "age": 58,
        "tumor_size_before": 3.5
        # Missing 'kps' and 'treatment'
    }

    try:
        response = requests.post(
            f"{API_BASE}/optimize",
            json=invalid_patient,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 400:
            data = response.json()
            print(f"Error: {data.get('error')}")
            print(f"Missing fields: {data.get('missing_fields')}")
            print("✓ PASSED: Invalid data properly rejected")
            return True
        else:
            print("✗ FAILED: Invalid data should return 400")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("GBM TREATMENT OPTIMIZATION API v3.0 - TEST SUITE")
    print("="*80)
    print(f"Testing API at: {API_BASE}")

    # Check if server is running
    try:
        requests.get(f"{API_BASE}/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: API server is not running!")
        print("Please start the server first:")
        print("  python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)

    # Run tests
    tests = [
        test_health,
        test_model_info,
        test_validate,
        test_optimize_minimal,
        test_optimize_full_features,
        test_invalid_data
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
        sys.exit(1)

if __name__ == '__main__':
    main()
