from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, List, Union


class State(Enum):
    """
    Class containing information about the state of the person
    
    f - person belongs to the family
    z - person is not from family
    """
    family: str = 'f'
    friends: str = 'z' # z from polish 'znajomi'

    
class PersonRelations(BaseModel):
    """
    Class containing information about a guest
    
    It's best when:
    - == 1 - relation between acquiantances
    - == 2 - relation between good friends
    - <= -1 - relation between foes
    - == 10 - relation between accompanying pair
    """
    person_id: int = Field(default=..., 
                           ge=0,
                           description='identifier of the guest'
                          )
    state: State = Field(default=..., 
                         description='whether the person belongs to the family or friends'
                        )
    relations: Dict[int, float] = Field(default={},
                                        description='relations with other guests'
                                       )
    
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
    seats: List[List[Union[int, None]]] = Field(default=[[None]], 
                                                description='optional list of seats (e.g. from previous optimization)'
                                               )
    family_friends_not_score: float = Field(default=-3., 
                                            lt=0,
                                            description='value indicating how much family and friends shouldnt sit together'
                                           )
    max_seats: int = Field(default=10, 
                           gt=1,
                           description='maximal number of seats'
                          )
    iterations: int = Field(default=200, 
                            ge=1,
                            description='maximal number of seats'
                           )
    
    
class TablesResponse(BaseModel):
    """
    Contains information about guests and tables
    """
    tables: List[List[int]] = Field(description='tables containing guests ids')
    tables_scores: List[float] = Field(description='scores how good is particular table relation')
    score_history: List[float] = Field(description='history of average relations score')
    
