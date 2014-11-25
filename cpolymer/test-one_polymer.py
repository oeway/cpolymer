# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 17:35:41 2014

@author: jarbona
"""

from one_polymer import generate
import numpy as np
from utils import norm
import unittest
from constrain import Box,Point
 
def test_create():
    
    coords,bonds,type_beads,ids = generate(N=2,type_bead=0,liaison_size={"0-0":1.0},ptolerance=0,type_polymer="linear",starting_id=0)
    assert (bonds == [[0,1]])
    assert (round(norm(coords[0]-coords[1]),3) == 1.00)
    assert(type_beads == [0,0])
    
    coords,bonds,type_beads,ids = generate(N=3,type_bead=[0,1,0],liaison_size={"0-0":1.0,"0-1":2},ptolerance=0,type_polymer="linear",starting_id=0)

    assert (bonds == [[0,1],[1,2]])
    assert (round(norm(coords[0]-coords[1]),3) == 2.00)
    assert (round(norm(coords[1]-coords[2]),3)== 2.00)
def test_startid():   
    coords,bonds,type_beads,ids = generate(N=2,type_bead=0,liaison_size={"0-0":1.0},ptolerance=0,type_polymer="linear",starting_id=1)
    assert (bonds == [[1,2]])
    #Test starting id
    
def test_constraint():
    
    box = Box()
    assert (box.is_inside([0.5,0.5,0.5]))
    assert ( not box.is_inside([0.5,0.5,1.5]))
    assert ( not box.is_inside([0.5,1.5,0.5]))
    assert ( not box.is_inside([1.5,0.5,0.5]))
    
def test_constrain_box_on_polymer():
    box = Box([0,0,0],[10,10,10])
    coords,bonds,type_beads,ids = generate(N=200,type_bead=0,liaison_size={"0-0":1.0},ptolerance=0,type_polymer="linear",starting_id=0,gconstrain=[box])
    for p in coords:
        assert(box.is_inside(p))
        
def test_constrain_on_polymer_start():    
    start = Point(index=0,position=[0.2,0.2,0.2])
    #end = Point(index=199,position=[0.2,0.2,0.2])
    box = Box([0,0,0],[10,10,10])
    coords,bonds,type_beads,ids = generate(N=20,type_bead=0,liaison_size={"0-0":1.0},ptolerance=0,type_polymer="linear",starting_id=0,lconstrain=[start],gconstrain=[box])   
    assert(norm(coords[0]-np.array([0.2,0.2,0.2])) < 0.01)
    
def test_constrain_on_polymer_quasi_start():    
    start = Point(index=1,position=[0.2,0.2,0.2])
    #end = Point(index=199,position=[0.2,0.2,0.2])
    box = Box([0,0,0],[20,20,20])
    coords,bonds,type_beads,ids = generate(N=20,type_bead=0,liaison_size={"0-0":1.0},ptolerance=0,type_polymer="linear",starting_id=0,lconstrain=[start],gconstrain=[box],max_trial=1000)   
    print norm(coords[0]-np.array([0.2,0.2,0.2]))
    assert(norm(coords[0]-np.array([0.2,0.2,0.2])) < 3)
    
def test_constrain_on_polymer_end():    
    end = Point(index=19,position=[0.2,0.2,0.2])
    #end = Point(index=199,position=[0.2,0.2,0.2])
    box = Box([0,0,0],[20,20,20])
    coords,bonds,type_beads,ids = generate(N=20,type_bead=0,liaison_size={"0-0":1.0},ptolerance=0,type_polymer="linear",starting_id=0,lconstrain=[end],gconstrain=[box],max_trial=1000)   
    print norm(coords[-2]-np.array([0.2,0.2,0.2]))
    assert(norm(coords[-2]-np.array([0.2,0.2,0.2])) < 3)
    
def test_constrain_on_polymer_start_end():
    start = Point(index=1,position=[0.2,0.2,0.2])    
    end = Point(index=199,position=[0.2,0.2,0.2])
    #end = Point(index=199,position=[0.2,0.2,0.2])
    box = Box([0,0,0],[20,20,20])
    coords,bonds,type_beads,ids = generate(N=200,type_bead=0,liaison_size={"0-0":1.0},ptolerance=0,type_polymer="linear",starting_id=0,lconstrain=[start,end],gconstrain=[box],max_trial=1000)   
    #print norm(coords[-1]-np.array([0.2,0.2,0.2]))
    print norm(coords[-2]-np.array([0.2,0.2,0.2]))
    print norm(coords[1]-np.array([0.2,0.2,0.2]))
    assert(norm(coords[-2]-np.array([0.2,0.2,0.2])) < 3)
    assert(norm(coords[1]-np.array([0.2,0.2,0.2])) < 3)

def test_constrain_on_polymer_start_middle_end():
    start = Point(index=1,position=[0.2,0.2,0.2])  
    middle = Point(index=100,position=[0.2,0.2,0.2])

    end = Point(index=199,position=[0.2,0.2,0.2])
    #end = Point(index=199,position=[0.2,0.2,0.2])
    box = Box([0,0,0],[20,20,20])
    coords,bonds,type_beads,ids = generate(N=200,type_bead=0,liaison_size={"0-0":1.0},ptolerance=0,type_polymer="linear",starting_id=0,lconstrain=[start,middle,end],gconstrain=[box],max_trial=1000)   
    #print norm(coords[-1]-np.array([0.2,0.2,0.2]))
    print norm(coords[-2]-np.array([0.2,0.2,0.2]))
    print norm(coords[1]-np.array([0.2,0.2,0.2]))
    assert(norm(coords[-2]-np.array([0.2,0.2,0.2])) < 3)
    assert(norm(coords[99]-np.array([0.2,0.2,0.2])) < 3)
    assert(norm(coords[101]-np.array([0.2,0.2,0.2])) < 3)
    assert(norm(coords[1]-np.array([0.2,0.2,0.2])) < 3)
    
class MyTestCase(unittest.TestCase):
    
    def testerror1(self):
        self.assertRaises(SomeCoolException, generate(N=3,type_bead=[0,1],liaison_size={"0-0":1.0,"0-1":2},ptolerance=0,type_polymer="linear",starting_id=0))