#!/usr/bin/env python3
"""
Test script for Wedding Tables Optimizer API
Tests various scenarios to ensure the algorithm works correctly
"""

import requests
import json
from typing import List, Dict

API_URL = "http://localhost:8000/api/"

def test_simple_scenario():
    """Test with a simple 8-person scenario"""
    print("=" * 60)
    print("TEST 1: Simple scenario (8 guests, 2 tables)")
    print("=" * 60)

    guests = [
        {"person_id": 0, "state": "f", "relations": {"1": 10, "2": 2}},
        {"person_id": 1, "state": "f", "relations": {"0": 10, "3": 1}},
        {"person_id": 2, "state": "f", "relations": {"0": 2, "3": 1}},
        {"person_id": 3, "state": "f", "relations": {"1": 1, "2": 1}},
        {"person_id": 4, "state": "z", "relations": {"5": 10, "6": 2}},
        {"person_id": 5, "state": "z", "relations": {"4": 10, "7": 1}},
        {"person_id": 6, "state": "z", "relations": {"4": 2, "7": 2}},
        {"person_id": 7, "state": "z", "relations": {"5": 1, "6": 2}},
    ]

    params = {
        "max_seats": 4,
        "family_friends_not_score": -3,
        "iterations": 50
    }

    try:
        response = requests.post(API_URL, json=guests, params=params)
        response.raise_for_status()
        result = response.json()

        print(f"✓ Optimization successful!")
        print(f"  Tables: {result['tables']}")
        print(f"  Table scores: {result['tables_scores']}")
        print(f"  Initial score: {result['score_history'][0]:.3f}")
        print(f"  Final score: {result['score_history'][-1]:.3f}")
        print(f"  Improvement: {((result['score_history'][-1] - result['score_history'][0]) / abs(result['score_history'][0]) * 100):.1f}%")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_couples_together():
    """Test that couples (score 10) are seated together"""
    print("\n" + "=" * 60)
    print("TEST 2: Couples should sit together (score 10 relationships)")
    print("=" * 60)

    guests = [
        {"person_id": 0, "state": "f", "relations": {"1": 10}},  # Couple 1
        {"person_id": 1, "state": "f", "relations": {"0": 10}},
        {"person_id": 2, "state": "f", "relations": {"3": 10}},  # Couple 2
        {"person_id": 3, "state": "f", "relations": {"2": 10}},
        {"person_id": 4, "state": "z", "relations": {"5": 10}},  # Couple 3
        {"person_id": 5, "state": "z", "relations": {"4": 10}},
    ]

    params = {
        "max_seats": 3,
        "family_friends_not_score": -3,
        "iterations": 100
    }

    try:
        response = requests.post(API_URL, json=guests, params=params)
        response.raise_for_status()
        result = response.json()

        # Check if couples are together
        tables = result['tables']
        couples = [(0, 1), (2, 3), (4, 5)]

        all_together = True
        for p1, p2 in couples:
            together = any((p1 in table and p2 in table) for table in tables)
            if together:
                print(f"✓ Couple ({p1}, {p2}) seated together")
            else:
                print(f"✗ Couple ({p1}, {p2}) NOT seated together!")
                all_together = False

        if all_together:
            print(f"✓ All couples seated together!")
            print(f"  Tables: {result['tables']}")
            print(f"  Final score: {result['score_history'][-1]:.3f}")

        return all_together
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_family_friends_separation():
    """Test that family and friends are preferably separated"""
    print("\n" + "=" * 60)
    print("TEST 3: Family-friends separation penalty")
    print("=" * 60)

    guests = [
        {"person_id": 0, "state": "f", "relations": {"1": 2, "2": 2}},
        {"person_id": 1, "state": "f", "relations": {"0": 2, "2": 2}},
        {"person_id": 2, "state": "f", "relations": {"0": 2, "1": 2}},
        {"person_id": 3, "state": "z", "relations": {"4": 2, "5": 2}},
        {"person_id": 4, "state": "z", "relations": {"3": 2, "5": 2}},
        {"person_id": 5, "state": "z", "relations": {"3": 2, "4": 2}},
    ]

    params = {
        "max_seats": 3,
        "family_friends_not_score": -5,
        "iterations": 100
    }

    try:
        response = requests.post(API_URL, json=guests, params=params)
        response.raise_for_status()
        result = response.json()

        tables = result['tables']

        # Check if tables are homogeneous
        family_ids = {0, 1, 2}
        friends_ids = {3, 4, 5}

        separated = True
        for i, table in enumerate(tables):
            family_count = sum(1 for guest_id in table if guest_id in family_ids)
            friends_count = sum(1 for guest_id in table if guest_id in friends_ids)

            if family_count > 0 and friends_count > 0:
                print(f"✗ Table {i+1}: Mixed ({family_count} family, {friends_count} friends)")
                separated = False
            else:
                print(f"✓ Table {i+1}: Homogeneous ({family_count} family, {friends_count} friends)")

        if separated:
            print(f"✓ Family and friends properly separated!")

        print(f"  Final score: {result['score_history'][-1]:.3f}")
        return separated
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_conflict_avoidance():
    """Test that conflicts (negative scores) are avoided"""
    print("\n" + "=" * 60)
    print("TEST 4: Conflict avoidance (negative relationship scores)")
    print("=" * 60)

    guests = [
        {"person_id": 0, "state": "f", "relations": {"1": 2, "2": -5}},  # 0 and 2 are enemies
        {"person_id": 1, "state": "f", "relations": {"0": 2}},
        {"person_id": 2, "state": "f", "relations": {"0": -5, "3": 2}},
        {"person_id": 3, "state": "f", "relations": {"2": 2}},
    ]

    params = {
        "max_seats": 2,
        "family_friends_not_score": -3,
        "iterations": 100
    }

    try:
        response = requests.post(API_URL, json=guests, params=params)
        response.raise_for_status()
        result = response.json()

        tables = result['tables']

        # Check if person 0 and 2 are separated
        separated = not any((0 in table and 2 in table) for table in tables)

        if separated:
            print(f"✓ Conflicting guests (0 and 2) seated separately!")
        else:
            print(f"✗ Conflicting guests (0 and 2) seated together!")

        print(f"  Tables: {result['tables']}")
        print(f"  Final score: {result['score_history'][-1]:.3f}")
        return separated
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_large_scenario():
    """Test with a larger scenario"""
    print("\n" + "=" * 60)
    print("TEST 5: Large scenario (20 guests)")
    print("=" * 60)

    # Generate 20 guests with random-ish relationships
    guests = []
    for i in range(20):
        relations = {}
        # Create some connections
        if i > 0:
            relations[i - 1] = 1.5
        if i < 19:
            relations[i + 1] = 1.5
        if i % 2 == 0 and i < 19:
            relations[i + 1] = 10  # Couples

        guests.append({
            "person_id": i,
            "state": "f" if i < 10 else "z",
            "relations": relations
        })

    params = {
        "max_seats": 8,
        "family_friends_not_score": -3,
        "iterations": 200
    }

    try:
        response = requests.post(API_URL, json=guests, params=params)
        response.raise_for_status()
        result = response.json()

        print(f"✓ Optimization successful for large scenario!")
        print(f"  Number of tables: {len(result['tables'])}")
        print(f"  Table sizes: {[len(t) for t in result['tables']]}")
        print(f"  Table scores: {[round(s, 2) for s in result['tables_scores']]}")
        print(f"  Final score: {result['score_history'][-1]:.3f}")
        print(f"  Iterations: {len(result['score_history'])}")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "🎊" * 30)
    print("Wedding Tables Optimizer - Test Suite")
    print("🎊" * 30 + "\n")

    # Note: These tests require the API to be running
    # Start the API with: uvicorn main:app --reload

    print("Note: Make sure the API is running on http://localhost:8000")
    print("Start it with: cd api && uvicorn main:app --reload\n")

    input("Press Enter to start tests...")

    results = []
    results.append(("Simple scenario", test_simple_scenario()))
    results.append(("Couples together", test_couples_together()))
    results.append(("Family-friends separation", test_family_friends_separation()))
    results.append(("Conflict avoidance", test_conflict_avoidance()))
    results.append(("Large scenario", test_large_scenario()))

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)

    print(f"\nTotal: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 All tests passed! The application is working correctly!")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Please review the output above.")
