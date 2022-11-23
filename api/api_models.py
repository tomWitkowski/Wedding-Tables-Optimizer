from pydantic import BaseModel
from enum import Enum
from typing import Dict, List, Union


class State(Enum):
    """
    Class containing information about the state of the person
    
    family - person belongs to the family
    friends - person is not from family
    """
    family: str = 'f'
    friends: str = 'z' # z from polish 'znajomi'

    
class PersonRelations(BaseModel):
    """
    It's best when:
    - == 1 - relation between acquiantances
    - == 2 - relation between good friends
    - <= -1 - relation between foes
    - == 10 - relation between accompanying pair
    """
    person_id: int = ...
    state: State = ...
    relations: Dict[int, float] = {}
    
    class Config:
        schema_extra = {
            'example':{
                'person_id':3, 
                'state':'f', 
                'relations':{1:1.5, 4:-3, 2:10}
            }
        }
     
    
class OptimizationData(BaseModel):
    """
    Request with metadata needed for tables optimization
    
    If seats are set, they will be treated as initial ones
    """
    seats: List[List[Union[int, None]]] = [[None]]
    family_friends_not_score: float = -3.
    max_seats: int = 10
    iterations: int = 200
    
    
class TablesResponse(BaseModel):
    """
    Contains information about guests and tables
    """
    tables: List[List[int]] = ...
    tables_scores: List[float] = ...
    score_history: List[float] = ...
    
