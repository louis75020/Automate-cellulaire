# For computations
import numpy as np
import random   
#Custom package
import tinder_manager as tm  

   
    ####### Automaton running

class Cellular_automaton_runner() :
    
        #### 1. Abstract attributes
            
    max_range = None
    current_state = None
    n_spieces = None
    step_by_step = None
    transition_matrix = None
    logger = None
    cols = None 
    all_states = []
    direction = []
        
 
       
    #### 2. Get the next current state   
       
    def next_step(self):
        
        ### Methods
        
        def next_state_initialization(current_state, max_range):
            
            dim0 = np.shape(current_state)[0] 
            dim1 = np.shape(current_state)[1]
            
            if max_range == None :
                
                next_state = np.zeros ( (dim0 + 2, dim1 +2) , dtype='i' ) 
                next_state [1 : dim0 + 1, 1 : dim1 +1 ] = current_state
                
            else :
                
                next_state = np.zeros( (dim0, dim1 ), dtype = 'i' )
                next_state[:,:] = current_state
                
            return next_state
            
            
        def get_transition_couples(next_state, step_by_step, direction):
            
            tmp_direction = direction[:]
            tinder = tm.Tinder_manager(next_state, tmp_direction)
            
            if step_by_step : 
                transition_couples = tinder.get_next_tuple()
                
            else : 
                transition_couples = tinder.get_next_tuples()
                
            return transition_couples
            
            
        
        #self.logger.debug('>>>>>>>>>>>>next_step>>>>>>>>>>>>')
        
        ### Values
        
        
        max_range = self.max_range ; current_state = self.current_state ; n_spieces = self.n_spieces ;  step_by_step = self.step_by_step ; transition_matrix = self.transition_matrix; direction = self.direction
        
        next_state = next_state_initialization(current_state, max_range)
        
        transition_couples = get_transition_couples(next_state, step_by_step, direction)
        
        
        #### for
        
        for couple in transition_couples :
            
            coord_husband = couple[0]
            coord_wife = couple[1]
            
            cell_type_husband = next_state [ coord_husband ]
            cell_type_wife = next_state [ coord_wife ]
            
            transition_law_index = cell_type_husband * n_spieces + cell_type_wife
            tmp_transition_law = transition_matrix [transition_law_index ,:]
            
            population = range(len(tmp_transition_law))
            new_couple_index = random.choices( population = population , weights = tmp_transition_law, k=1)[0]
            
            new_couple = ( new_couple_index // n_spieces, new_couple_index % n_spieces )
            
            next_state[ coord_husband ] = new_couple[0]
            next_state[ coord_wife ] = new_couple[1]
        
        
        return next_state
   
   
   
        
    ####3. Run n_steps
        
    def n_steps(self, n = 1, add = False):
        
        
        for t in range(n):
                
            self.current_state = self.next_step()
            if(add) : self.all_states.append(self.current_state)
        
        
        