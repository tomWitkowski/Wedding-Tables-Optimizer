import itertools
from math import ceil
from typing import List
from copy import deepcopy

import networkx as nx
import numpy as np


class Tables:
    """
    A class describing a set of tables with guests
    Tables' goal is to optimize average relation between guests in all tables
    
    Assumptions:
        - relations between guests are defined properly
        - distance between guest in one table is neglected
    """
    @staticmethod
    def get_init_seats(guests: list, max_seats: int, I: int = 0):
        """
        Sets initial random tables
        """
        hall = [[] for _ in range(ceil(len(guests) / max_seats))]
        guests = list(guests)
        np.random.shuffle(guests)
            
        for guest in guests:
            hall[I].append(guest)
            if len(hall[I]) == max_seats:
                I += 1
                
        return hall
    
    
    def __init__(self, relation_graph: nx.Graph, max_seats: int = 10, seats: List[List[int]] = None):
        self.relation_graph = relation_graph
        self.guests = relation_graph.nodes
        self.max_seats = max_seats
        if seats in [None, [None], [[None]]]:
            self.seats = self.get_init_seats(self.guests, max_seats)
        else:
            self.seats = seats
            
        self.score_history = []
        
    
    def get_table_score(self, table: list) -> int:
        raw_scores = [self.relation_graph.get_edge_data(*x) for x in itertools.combinations(table, 2)]
        return sum([float(x['score']) for x in raw_scores if x!=None])/len(table)
    
    
    def get_full_scores(self, seats: list):
        return sum([self.get_table_score(table) for table in seats])/len(seats)
        
        
    def get_random_tables(self):
        return np.random.choice(range(len(self.seats)), 2, False)        
        
        
    def get_tables_scores(self):
        return [round(self.get_table_score(table), 3) for table in self.seats]
        
        
    def cross_random_seats(self, persons: int = 4):
        """
        Exchange {persons} guests between random tables
        """
        if persons >= len(self.seats[0]):
            raise ValueError('number of switched peaple should be lower than number of seats')
        
        seats = deepcopy(self.seats)
        
        i1, i2 = self.get_random_tables()
        
        seats1 = seats[i1]
        seats2 = seats[i2]

        persons1 = np.random.choice(seats1, persons, False).tolist()
        persons2 = np.random.choice(seats2, persons, False).tolist()

        [seats1.remove(person) for person in persons1]
        [seats2.remove(person) for person in persons2]
        
        seats1 += persons2
        seats2 += persons1
        
        return seats
    
    
    def move_random_person(self):
        """
        Moves one or two persons to the table with a minimal number of persons
        """
        seats = deepcopy(self.seats)
        
        # shorter table
        i2 = np.argmin([len(x) for x in self.seats])
        
        # random table
        i1 = np.random.choice([x for x in range(len(self.seats)) if x != i2], 1)[0]
        
        seats1 = seats[i1]
        seats2 = seats[i2]

        persons1 = np.random.choice(seats1, 
                                    np.random.randint(
                                        1,
                                        min((self.max_seats-len(self.seats[i2]))+1,3)),
                                    False).tolist()

        [seats1.remove(person) for person in persons1]
        
        seats2 += persons1
        
        return seats
    
    
    def iteration(self, n_shuffles: int = 100, n_person: int = 2):
        """
        It basically makes guests running and switching tables randomly
        to check if these operations increase overall relations in tables
        """
        hall_set = [self.seats]
        hall_set += [self.cross_random_seats(n_person) for _ in range(n_shuffles)]
        hall_set += [self.move_random_person() for _ in range(n_shuffles)]
        scores = [self.get_full_scores(table) for table in hall_set]
        best_score = max(scores)
        self.seats = hall_set[np.argmax(scores)]
        self.score_history.append(best_score)
        
        
    def optimize(self, iterations: int = 200, n_shuffles: int = 50, n_person: int = 2):
        """
        Run iterations repeatedly
        """
        for _ in range(iterations):
            self.iteration(n_shuffles, n_person)
            
            
def create_relation_graph(persons_request: list) -> nx.Graph:
    """
    Creates a Graph from a List of PersonRelations
    """
    g = nx.Graph()
    for person in persons_request:
        for other_person_id, score in person.relations.items():
            g.add_edge(person.person_id, other_person_id, **{'score':score})
            
    return g