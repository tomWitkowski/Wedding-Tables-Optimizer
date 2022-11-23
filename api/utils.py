from api_models import PersonRelations
from typing import List
import itertools
        
def add_family_friend_antirelation(request: List[PersonRelations], 
                                   family_friends_not_score: float = -3):
    """
    Adds antirelations between friends and family
    """
    antirelations = [[person1.person_id, person2.person_id]+[family_friends_not_score] 
                     for (person1, person2) in itertools.combinations(request, 2)
                     if person1.state != person2.state]
    
    antirelation_ids = set([x[0] for x in antirelations])

    for person in request:
        if person.person_id in antirelation_ids:
            for _, id2, score in [x for x in antirelations if x[0] == person.person_id]:
                person.relations = {**person.relations, **{id2:score}}
    
    return request