import random
import numpy as np

class Tinder_manager():
    
    def __init__(self, next_state, direction):
        
        self.direction = direction 
        self.next_state = next_state
        self.up = (('random' in direction) or ('fly' in direction) or ('up' in direction))
        self.down = (('random' in direction) or ('down' in direction) or ('gravity' in direction) )
        self.right = (('random' in direction) or ('wind:right'in direction) or ('right' in direction))
        self.left = (('random' in direction) or ('wind:left'in direction) or ('left' in direction))
        
    
    def get_potential_husbands(self, wife):
        
        left = self.left; right =self.right; up = self.up; down = self.down; next_state = self.next_state
        coord0 = wife[0]
        coord1 = wife[1]
        potential_husbands = [] 
        dim0, dim1 = np.shape(next_state)
        
        if coord0 == 0 : up = False
        if coord0 ==  dim0 -1 : down = False
        if coord1 == 0 : left = False
        if coord1 == dim1 - 1 : right = False
        
        #left
        if left :  
            potential_husbands.append( (coord0, coord1 - 1))
            
        #right
        if  right : 
            potential_husbands.append( (coord0, coord1 + 1) )
            
        #up
        if  down :
            potential_husbands.append( (coord0 + 1, coord1) )
                    
        #down
        if up :
            potential_husbands.append( (coord0 - 1, coord1) )
        
        return potential_husbands
    
    
    
    def get_next_tuple(self) :
        
        
        next_state = self.next_state
        dim0, dim1 = np.shape(next_state)
            
        while(True) :
            
            wife_x = random.randint(0, dim0 -1 )
            wife_y = random.randint(0, dim1 -1 )
            wife = (wife_x, wife_y)
        
            potential_husbands = self.get_potential_husbands(wife)
            if potential_husbands != [] : break
            
        husband_coordinate = random.randint(0, len(potential_husbands) -1 )
        husband = potential_husbands[ husband_coordinate ]
        
        output = []
        output.append( (wife, husband) )
        
        return output
       

    
    def get_next_tuples(self) :
        
        next_state = self.next_state
        dim0, dim1 = np.shape(next_state)
        n = int( np.min([ dim0, dim1])/2 )
        
        output = []
        
        for k in range(n):
            
            new_couple = self.get_next_tuple()
            output.append( new_couple[0] )
            
        return output
           
       
       
        
    
