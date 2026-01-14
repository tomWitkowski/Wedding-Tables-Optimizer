from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api_models import PersonRelations, TablesResponse, OptimizationData
from utils import add_family_friend_antirelation
from core import Tables, create_relation_graph
from typing import List
import os

app = FastAPI(
    title="Wedding Tables Optimizer",
    description="Optimize wedding table seating based on guest relationships",
    version="2.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files if frontend build exists
if os.path.exists("../frontend/build"):
    app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")


@app.get('/')
async def route():
    return({'message':'Smacznej kawusi życzę!'})


@app.post('/api/', response_model = TablesResponse)
async def optimize_tables(
    relations: List[PersonRelations] = ...,
    opt: OptimizationData = ...
):
    """
    Function maximizing average relations between guests inside tables
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
                          score_history=tables.score_history )