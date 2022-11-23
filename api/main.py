from fastapi import FastAPI, Body
from api_models import PersonRelations, TablesResponse, OptimizationData
from utils import add_family_friend_antirelation
from core import Tables, create_relation_graph
from typing import List

app = FastAPI()


@app.get('/')
async def route():
    return({'message':'Smacznej kawusi życzę!'})


@app.post('/api/', response_model = TablesResponse)
async def optimize_tables(
    relations: List[PersonRelations] = ...,
    opt: OptimizationData = ...
):
    """
    to be deifned:
    
    family_friends_not_score
    table init - max_seats
    table init - seats - initial set of seats
    optimize - iterations
    """
    # adds antirelations between family and friends
    relations = add_family_friend_antirelation(relations,
                                               opt.family_friends_not_score)
    
    # creates networkx Graph about all guest
    relation_graph = create_relation_graph(relations)
    
    # create Tables Optimization object
    tables = Tables(relation_graph, opt.max_seats, opt.seats)
    
    # optimize
    tables.optimize(opt.iterations)
    
    return TablesResponse(tables=tables.seats, 
                          tables_scores=tables.get_tables_scores(),
                          score_history=tables.score_history
                         )