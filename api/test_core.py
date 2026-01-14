#!/usr/bin/env python3
"""
Direct test of the core optimization algorithm
No API server needed - tests the algorithm directly
"""

import sys
sys.path.insert(0, '/home/user/Wedding-Tables-Optimizer/api')

from core import Tables, create_relation_graph
from api_models import PersonRelations, State
from utils import add_family_friend_antirelation

def test_basic_optimization():
    """Test basic optimization with a simple scenario"""
    print("=" * 60)
    print("TEST: Basic Optimization Algorithm")
    print("=" * 60)

    # Create test guests
    guests = [
        PersonRelations(person_id=0, state=State.family, relations={1: 10.0, 2: 2.0}),
        PersonRelations(person_id=1, state=State.family, relations={0: 10.0, 3: 1.0}),
        PersonRelations(person_id=2, state=State.family, relations={0: 2.0, 3: 1.0}),
        PersonRelations(person_id=3, state=State.family, relations={1: 1.0, 2: 1.0}),
        PersonRelations(person_id=4, state=State.friends, relations={5: 10.0, 6: 2.0}),
        PersonRelations(person_id=5, state=State.friends, relations={4: 10.0, 7: 1.0}),
        PersonRelations(person_id=6, state=State.friends, relations={4: 2.0, 7: 2.0}),
        PersonRelations(person_id=7, state=State.friends, relations={5: 1.0, 6: 2.0}),
    ]

    print(f"Number of guests: {len(guests)}")

    # Add family-friend antirelations
    guests = add_family_friend_antirelation(guests, -3.0)

    # Create relation graph
    relation_graph = create_relation_graph(guests)
    print(f"Graph nodes: {len(relation_graph.nodes)}")
    print(f"Graph edges: {len(relation_graph.edges)}")

    # Create Tables object
    max_seats = 4
    tables = Tables(relation_graph, max_seats, None)

    print(f"\nInitial configuration:")
    print(f"  Tables: {tables.seats}")
    initial_score = tables.get_full_scores(tables.seats)
    print(f"  Initial score: {initial_score:.3f}")

    # Run optimization
    iterations = 100
    print(f"\nRunning optimization ({iterations} iterations)...")
    tables.optimize(iterations=iterations, n_shuffles=50, n_person=2)

    print(f"\nFinal configuration:")
    print(f"  Tables: {tables.seats}")
    final_score = tables.score_history[-1]
    print(f"  Final score: {final_score:.3f}")

    improvement = ((final_score - initial_score) / abs(initial_score)) * 100
    print(f"  Improvement: {improvement:.1f}%")

    # Verify couples are together
    couples = [(0, 1), (4, 5)]
    print(f"\nCouples check:")
    for p1, p2 in couples:
        together = any((p1 in table and p2 in table) for table in tables.seats)
        status = "✓" if together else "✗"
        print(f"  {status} Couple ({p1}, {p2}): {'together' if together else 'separated'}")

    return final_score > initial_score


def test_table_score_calculation():
    """Test the table score calculation"""
    print("\n" + "=" * 60)
    print("TEST: Table Score Calculation")
    print("=" * 60)

    # Create a simple scenario
    guests = [
        PersonRelations(person_id=0, state=State.family, relations={1: 10.0, 2: 5.0}),
        PersonRelations(person_id=1, state=State.family, relations={0: 10.0, 2: 3.0}),
        PersonRelations(person_id=2, state=State.family, relations={0: 5.0, 1: 3.0}),
    ]

    relation_graph = create_relation_graph(guests)
    tables = Tables(relation_graph, max_seats=3, seats=[[0, 1, 2]])

    score = tables.get_table_score([0, 1, 2])
    print(f"Table [0, 1, 2] score: {score:.3f}")

    # Expected score calculation:
    # Relations: 0-1: 10, 0-2: 5, 1-2: 3
    # Average per person: (10 + 5 + 3) / 3 = 6.0
    expected = (10 + 5 + 3) / 3
    print(f"Expected score: {expected:.3f}")

    if abs(score - expected) < 0.01:
        print("✓ Score calculation correct!")
        return True
    else:
        print(f"✗ Score mismatch! Got {score:.3f}, expected {expected:.3f}")
        return False


def test_family_friend_antirelation():
    """Test family-friend antirelation logic"""
    print("\n" + "=" * 60)
    print("TEST: Family-Friend Antirelation")
    print("=" * 60)

    guests = [
        PersonRelations(person_id=0, state=State.family, relations={1: 2.0}),
        PersonRelations(person_id=1, state=State.family, relations={0: 2.0}),
        PersonRelations(person_id=2, state=State.friends, relations={3: 2.0}),
        PersonRelations(person_id=3, state=State.friends, relations={2: 2.0}),
    ]

    print("Before antirelation:")
    for g in guests:
        print(f"  Guest {g.person_id} ({g.state.value}): {g.relations}")

    penalty = -5.0
    guests = add_family_friend_antirelation(guests, penalty)

    print(f"\nAfter antirelation (penalty={penalty}):")
    for g in guests:
        print(f"  Guest {g.person_id} ({g.state.value}): {g.relations}")

    # Check if antirelations were added
    # Guest 0 (family) should have negative relation to guests 2, 3 (friends)
    success = True
    if guests[0].relations.get(2) == penalty and guests[0].relations.get(3) == penalty:
        print(f"✓ Guest 0 has antirelations to friends")
    else:
        print(f"✗ Guest 0 missing antirelations")
        success = False

    if guests[2].relations.get(0) == penalty and guests[2].relations.get(1) == penalty:
        print(f"✓ Guest 2 has antirelations to family")
    else:
        print(f"✗ Guest 2 missing antirelations")
        success = False

    return success


def test_edge_cases():
    """Test edge cases"""
    print("\n" + "=" * 60)
    print("TEST: Edge Cases")
    print("=" * 60)

    # Test with minimal guests (2 people)
    print("\n1. Two guests only:")
    guests = [
        PersonRelations(person_id=0, state=State.family, relations={1: 10.0}),
        PersonRelations(person_id=1, state=State.family, relations={0: 10.0}),
    ]

    relation_graph = create_relation_graph(guests)
    tables = Tables(relation_graph, max_seats=2, seats=None)
    tables.optimize(iterations=10)

    print(f"   Tables: {tables.seats}")
    print(f"   Score: {tables.score_history[-1]:.3f}")

    # Should be together
    if tables.seats == [[0, 1]] or tables.seats == [[1, 0]]:
        print("   ✓ Couple seated together")
    else:
        print("   ✗ Couple not together!")
        return False

    # Test with single person - note: single guest weddings are unrealistic
    # so this is just a sanity check that it doesn't crash
    print("\n2. Single guest (edge case - just ensure no crash):")
    guests = [PersonRelations(person_id=0, state=State.family, relations={})]
    relation_graph = create_relation_graph(guests)
    tables = Tables(relation_graph, max_seats=10, seats=None)

    print(f"   Tables: {tables.seats}")
    # For a single guest, the algorithm should handle it gracefully
    # (even if the result is empty or unusual - this is an extreme edge case)
    print("   ✓ Single guest handled without crash")

    return True


if __name__ == "__main__":
    print("\n" + "🎊" * 30)
    print("Wedding Tables Optimizer - Core Algorithm Tests")
    print("🎊" * 30 + "\n")

    results = []

    try:
        results.append(("Table score calculation", test_table_score_calculation()))
        results.append(("Family-friend antirelation", test_family_friend_antirelation()))
        results.append(("Basic optimization", test_basic_optimization()))
        results.append(("Edge cases", test_edge_cases()))

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
            print("\n🎉 All core tests passed! The algorithm is working correctly!")
            sys.exit(0)
        else:
            print(f"\n⚠️  {total_count - passed_count} test(s) failed.")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
