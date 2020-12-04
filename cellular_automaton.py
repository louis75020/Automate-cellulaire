# For computations
import numpy as np
import random   
#Custom package
import cellular_automaton_plotter as cap
#Logging
import logging
from logging.handlers import RotatingFileHandler


class Cellular_automaton(cap.Cellular_automaton_plotter):
    

    #### Builder
    
    
    def __init__(self, initial_state, transition_matrix, cols = [], direction = np.array(['random']), max_range = None, step_by_step = True, log_level = 2, log_file_name = 'activity.log' ):
  
        
        
        ####1. Logging initializer
        
        def logger_initialization (real_log_level, log_file_name) :
            
            logger = logging.getLogger()
            logger.setLevel(real_log_level)
            
            formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
            
            file_handler = RotatingFileHandler(log_file_name, 'w', 1000000, 1)
            file_handler.setLevel(real_log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.WARNING)
            logger.addHandler(stream_handler)
            
            return logger
        
        try:
            
            if( log_level < 1 ): logger = logger_initialization(logging.DEBUG, log_file_name)
            elif ( log_level < 2): logger = logger_initialization(logging.INFO, log_file_name)
            elif ( log_level < 3): logger = logger_initialization(logging.WARNING, log_file_name)
            else: logger = logger_initialization(logging.ERROR, log_file_name)
            
        except:
            
            print("Logger has not been initialized. The builder failed")
            return 
        
        
        
            
        #### 2. Input errors manager
        
        #### initial_state
        # Catch if there is no initial_state
        
        def check_initial_state (n_spieces, initial_state = initial_state):
            
            logger.debug(">>>>>check_initial_state>>>>>>>>")
            
            assert len(initial_state) != 0, "ERROR : No initial state"
            tmp_initial_state=initial_state
    
            if np.shape(initial_state)[0] != np.shape(initial_state)[1] : logger.info("The initial state is not a square")
            if len(np.unique(initial_state)) < n_spieces : logger.infor("All spieces are not represented in the initial state")
                
            logger.debug("<<<<<check_initial_state<<<<<<<")
            return tmp_initial_state
            
            
        #### max_range    
        # Catch: negative value of max_range, float value of max_range, zero value of max_range, max_range  <shape(initial_state)
        
        def check_max_range (initial_state = initial_state , max_range = max_range):
            
            logger.debug(">>>>>check_max_range>>>>>>>>")
            tmp_max_range = max_range
            
            if max_range != None :
                
                logger.debug( "The space is finite" )
                if max_range > 0: tmp_max_range = int(max_range)
                    
                else:
                    
                    logger.warning( "The max range is negative or 0: it will be set to its absolute value" )
                    tmp_max_range = int(abs(max_range))
                    
                if tmp_max_range == 0:
                    
                    logger.warning( "The max range is 0: it will be set to None" )
                    tmp_max_range=None 
                
                if (np.shape(initial_state)[0] != np.shape(initial_state)[1]): 
                    
                    logger.warning("The initial state is not a square, and max_range has a value; it is meaningless. max_range will be set to infinite")
                    tmp_max_range=None
                    
                else:
                    
                    if tmp_max_range < np.shape(initial_state)[0]:
                        
                        logger.warning("The initial state is a square, and max_range has a value lower than the dimension of the initial state; it is meaningless. max_range will be set to the dimension of the initial state")
                        tmp_max_range = np.shape(initial_state)[0]
                
            else:
                
                logger.debug("The space is infinite")
                    
            logger.debug("<<<<<check_max_range<<<<<<<")
            return tmp_max_range
            
            
        #### transition_matrix
        #Catch negative values, non-proba values, wrong dimensions    
        
        def check_transition_matrix (transition_matrix = transition_matrix):
            
            logger.debug('>>>>>>>>check_transition_matrix>>>>>>>>>>')
            tmp_transition_matrix = transition_matrix
            negative_values = False
            non_proba_laws = False
            
            assert len(transition_matrix) != 0, "ERROR : No transition matrix"
            assert np.shape(transition_matrix)[0] == np.shape(transition_matrix)[1],"Wrong dimensions for the transition matrix (it should be a square)"
            
            for i in range(len(transition_matrix)) :
                
                for j in range(len(transition_matrix)) :
                    
                    if transition_matrix[i,j] < 0 :
                        
                        negative_values = True
                        tmp_transition_matrix[i,j] = np.abs(transition_matrix[i,j])
                
                if np.sum(transition_matrix)!=1. :
                
                    non_proba_laws = True
                    tmp_transition_matrix[i,:] *= 1/np.sum(tmp_transition_matrix[i,:])
                    
            if negative_values : logger.warning("The program found negative values, it has taken theirs absolute values")
                
            if non_proba_laws : logger.warning("Some of the transition laws in the transition matrix were not proba laws. The program has renormalized the laws")
                        
            logger.debug('<<<<<<check_transition_matrix<<<<<<<<<')
            return tmp_transition_matrix  
            
              
        #### cols 
        # Catch wrong number of colors    
        def check_cols(cols = cols, transition_matrix = transition_matrix) :
            
            logger.debug('>>>>>>>check cols>>>>>>>')
            tmp_cols = cols
            
            if len(cols) == 0 : logger.info( "No colors passed, the colors of cells on plots will be arbitrary" )
            else :
                
                if len(cols) != np.round(np.sqrt(len(transition_matrix))) : 
                    logger.warning( "Wrong dimensions for the color vector, the colors will be arbitrary" )
                    tmp_cols = []
            
            logger.debug('<<<<<<check_cols<<<<<<')
            return tmp_cols
            
        
        ### direction
        
        def check_direction():
            
            logger.debug('>>>>>check_direction>>>>>>>')
            
            tmp_direction = direction
            
            if ('random' in direction or 'right' in direction or 'left' in direction or 'up' in direction or 'down' in direction or 'gravity' in direction or 'wind:left' in direction or 'wind:right' in direction or 'fly' in direction) : return tmp_direction
            
            else:
                self.logger.warning('BEWARE, no allowed directions passed as arguments, the parameter will be set to random')
                
                logger.debug('<<<<<<check_direction<<<<<<<<<')
                return ['random']
            
            
            
        #### 3. Attribute values
        
        self.logger = logger
        self.n_spieces = int(np.round(np.sqrt(len(transition_matrix))))
        self.cols = check_cols()
        self.current_state = check_initial_state(self.n_spieces)
        self.max_range = check_max_range()
        self.transition_matrix = check_transition_matrix()
        self.all_states = [] 
        self.all_states.append(self.current_state)
        self.step_by_step = step_by_step
        self.direction = check_direction()
        
        
        
    
    #### To_string() 
    
    def __str__(self):

        #print("n_transitions: ", self.n_transitions)
        print("n_spieces: ", self.n_spieces)
        print("max-range: ", self.max_range)
        print("colors", self.cols)
        print("transition_matrix: ")
        print(self.transition_matrix)
        print("current_state:")
        print(self.current_state)
        print('direction:')
        print(self.direction)
        
        return('')
   
        
    ##### Destructor
    
    def __del__(self) :
        
        x = logging._handlers.copy()
        for i in x:
            log.removeHandler(i)
            i.flush()
            i.close()
        del self
 
 
    
#### Main for fast test
    
def main() :
    
    # max_range3 = 10
    # n_spieces3 = 3
    # initial_state3 = np.asarray([[1,1,0,2,1,2,1,2,0,0], [1,1,0,2,1,2,1,2,0,0], [1,2,1,2,2,0,0,1,0,1], [2,2,0,2,1,1,2,0,0,1], [1,2,1,2,2,0,0,1,0,1], [2,2,0,2,1,1,2,0,0,1], [2,2,0,2,1,1,2,0,0,1], [1,1,0,2,1,2,1,2,0,0], [1,1,0,2,1,2,1,2,0,0], [1,2,1,2,2,0,0,1,0,1]]) 
    # transition_matrix3 = np.random.rand(n_spieces3**2,n_spieces3**2)
    # transition_matrix3 = np.array([e/sum(e) for e in transition_matrix3])
    # cols3 = np.array(['white', 'yellow', 'black'])
    # direction3 = ['random']
    # step_by_step3 = True
    
    max_range3 = 10
    #initial_state3 = np.zeros((100,100))
    #initial_state3 [0,:] = np.ones((1,15))
    initial_state3 = np.random.randint(2, size=(30, 30))
    initial_state3 [ 20, 17:22 ] = 2 *np.ones((1,5))
    initial_state3 [ 29,:] = 2*np.ones((1,30))
    transition_matrix3 = np.eye(9)
    transition_matrix3[3,1] =1
    transition_matrix3[3,3] = 0
    cols3 = np.array(['white', 'yellow', 'black'])
    step_by_step3 = False
    direction3 = np.array(['gravity'])
    
    # initial_state3 = np.zeros((31,31))
    # initial_state3[14:16,14:16] = np.ones((2,2))
    # transition_matrix3 = np.asarray([[1,0,0,0],[0,0,0,1],[0,0,0,1],[1,0,0,0]], dtype = 'f')
    # max_range3 = 31
    # step_by_step3 = False
    # cols3 = np.array(['white','black'])
    # direction3 = ['random']
    
    cg3 = Cellular_automaton (initial_state3, transition_matrix3, cols3, direction3, max_range3, step_by_step3, log_level=1, log_file_name = 'activity_logger3')
    cg3.get_dynamic_plots(add = False)
    
    
#### Script
    
if __name__ == "__main__":

    main()
