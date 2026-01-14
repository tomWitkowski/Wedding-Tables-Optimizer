from api_models import PersonRelations
from typing import List
import itertools
        
def add_family_friend_antirelation(request: List[PersonRelations],
                                   family_friends_not_score: float = -3):
    """
    Adds antirelations between friends and family (bidirectional)
    """
    antirelations = [[person1.person_id, person2.person_id, family_friends_not_score]
                     for (person1, person2) in itertools.combinations(request, 2)
                     if person1.state != person2.state]

    # Create a set of all person IDs that need antirelations
    antirelation_ids = set()
    for id1, id2, _ in antirelations:
        antirelation_ids.add(id1)
        antirelation_ids.add(id2)

    # Add antirelations bidirectionally
    for person in request:
        if person.person_id in antirelation_ids:
            # Add relations where this person is the first in the pair
            for id1, id2, score in antirelations:
                if id1 == person.person_id:
                    person.relations = {**person.relations, **{id2: score}}
                # Also add relations where this person is the second in the pair
                elif id2 == person.person_id:
                    person.relations = {**person.relations, **{id1: score}}

    return request