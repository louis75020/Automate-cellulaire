# For computations
import numpy as np
import random
#Logging
import logging
from logging.handlers import RotatingFileHandler
#For plotting
import pylab 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import figure 
import matplotlib.colors
#Utilitary
#from itertools import count
#Custom package
import tinder_manager as tm



class Cellular_automaton():
    
    all_states = []

    
    
    #### 1. Builder
    
    
    def __init__(self, initial_state, transition_matrix, cols = [], max_range = None, step_by_step = True, log_level = 2, log_file_name = 'activity.log' ):
        
        #### Logger
        
        #### Logging initializer
        
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
        
        # Catch if there is no initial_state
        def check_initial_state (n_spieces, initial_state = initial_state):
            
            logger.debug(">>>>>check_initial_state>>>>>>>>")
            assert len(initial_state) != 0, "ERROR : No initial state"
            tmp_initial_state=initial_state
    
            if np.shape(initial_state)[0] != np.shape(initial_state)[1] : logger.info("The initial state is not a square")
            if len(np.unique(initial_state)) < n_spieces : logger.infor("All spieces are not represented in the initial state")
                
            logger.debug("<<<<<check_initial_state<<<<<<<")
            return tmp_initial_state
            
            
            
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
            
              
         
        # Catch wrong number of colors    
        def check_cols(cols = cols, transition_matrix = transition_matrix) :
            
            tmp_cols = cols
            
            if len(cols) == 0 : logger.info( "No colors passed, the colors of cells on plots will be arbitrary" )
            else :
                
                if len(cols) != np.round(np.sqrt(len(transition_matrix))) : 
                    logger.warning( "Wrong dimensions for the color vector, the colors will be arbitrary" )
                    tmp_cols = []
        
            return tmp_cols
            
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
        
        return('')
        
    ####### Automaton running
    
    #### 1. Get randomly couples of cells
        
    def get_next_tuple (self, next_step) : 
        
        self.logger.debug('>>>>>>get_next_tuple>>>>>>>>')
        tuples = [ (i,j) for i in range(np.shape(next_step)[0]) for j in range(np.shape(next_step)[1]) ]
        output = []
        tmp_coord = tuples[ random.randint(0, len(tuples) -1 ) ]
        tinder = tm.Tinder_manager(next_step)
        potential_husbands = tinder.regular_mariage(tuples, tmp_coord)
        husband = potential_husbands[ random.randint(0, len(potential_husbands) -1 ) ]
        output = list()
        output.append( (tmp_coord, husband) )
        self.logger.debug('<<<<<<<get_next_tuple<<<<<<')
        return output
       
    #### 2. Get the next current state   
       
    def next_step(self):
        
        self.logger.debug('>>>>>>>>>>>>next_step>>>>>>>>>>>>')
        
        max_range = self.max_range ; current_state = self.current_state ; n_spieces = self.n_spieces ;  step_by_step = self.step_by_step ; transition_matrix = self.transition_matrix
        dim0 = np.shape(current_state)[0] ; dim1 = np.shape(current_state)[1]
        
        if max_range == None :
            
            next_state = np.zeros ( (dim0 + 2, dim1 +2) , dtype='i' ) #space expansion
            next_state [1 : dim0 + 1, 1 : dim1 +1 ] = current_state
            
        else :
            
            next_state = np.zeros( (dim0, dim1 ), dtype = 'i' )
            next_state[:,:] = current_state
            
        if step_by_step : transition_couples = self.get_next_tuple( next_state )
        else : transition_couples = tm.Tinder_manager( next_state ).get_next_tuples( next_state, self.logger )
        
        for couple in transition_couples :
            
            cell_type_husband = next_state [ couple[0] ]
            cell_type_wife = next_state [ couple[1] ]
            transition_law_index = cell_type_husband * n_spieces + cell_type_wife
            tmp_transition_law = transition_matrix [transition_law_index ,:]
            new_couple_index = random.choices( population = range(len(tmp_transition_law)), weights = tmp_transition_law, k=1)[0]
            new_couple = ( new_couple_index // n_spieces, new_couple_index % n_spieces )
            next_state[ couple[0] ] = new_couple[0]
            next_state[ couple[1] ] = new_couple[1]
        
        self.logger.debug('<<<<<<next_step<<<<<<<<<')
        return next_state
        
    #### Run n_steps
        
    def n_steps(self, n = 1, add = False):
        
        self.logger.debug('>>>>>>n_steps>>>>>')
        
        if n > 0 :
        
            for t in range(n):
                
                self.current_state = self.next_step()
                if(add) : self.all_states.append(self.current_state)
        
        self.logger.debug('<<<<<<n_steps<<<<')
        
    #### Plot methods
    
    def get_dynamic_plots(self, add = False):
        
        self.logger.debug('>>>>>>>video>>>>>>>>')
        
        all_states = self.all_states; colors=self.cols
        
        
        if len(colors) > 0 : 
            cmap = matplotlib.colors.ListedColormap(colors, name='colors', N=None) #fixing colors
        plt.style.use('fivethirtyeight')
        
        def animate(i): #almost a lambda function
            
            
            plt.cla() #remove axes
            
            if(add) : 
            
                self.current_state = self.next_step()
                all_states.append(self.current_state)
                if len(colors)>0 : pylab.imshow(self.current_state, cmap=cmap)
                else : pylab.imshow(self.current_state)
                
            else : 
                
                if len(colors)>0 : pylab.imshow(self.next_step(), cmap=cmap)
                else : pylab.imshow(self.next_step())
        

        ani = animation.FuncAnimation(plt.gcf(), animate, 1000) #plot until interruption
        #plt.tight_layout()
        plt.show()
        
        self.logger.debug('>>>>>>>>>video>>>>>>>>')
        
    def get_video(self, name = 'last_video'):
        
        self.logger.debug('>>>>>>>>>get video>>>>>>>')
        colors=self.cols
        if len(colors)>0 : cmap = matplotlib.colors.ListedColormap(colors, name='colors', N=None)
        frames = [] # for storing the generated images
        fig = pylab.figure()
        
        for i in range(len(self.all_states)):
            
            if len(colors) > 0 : frames.append( [ pylab.imshow(self.all_states[i], animated = True, cmap=cmap) ] )
            else : frames.append( [ pylab.imshow(self.all_states[i], animated = True) ] )
        
        ani = animation.ArtistAnimation(fig, frames, interval = 100, blit = True)
        ani.save(name+'.htm')
        self.logger.debug('<<<<<get video<<<<<<<')
        
    def get_last_plot(self) :
         
        self.logger.debug('>>>>>>>get last plot>>>>>>')
        colors=self.cols
        fig = pylab.figure()
        
        if len(colors) > 0 : 
            
            cmap = matplotlib.colors.ListedColormap(colors, name='colors', N=None)
            pylab.imshow(self.current_state, cmap=cmap)
            
        else :   pylab.imshow(self.current_state)  
        plt.show()
        self.logger.debug('<<<<<<get_last_plot<<<<<')
        
    ##### Destructor
    
    def __del__(self) :
        
        x = logging._handlers.copy()
        for i in x:
            print('here')
            log.removeHandler(i)
            i.flush()
            i.close()
        del self
    
    #### Main for fast test
    
def main() :
    
    max_range3 = 10
    n_spieces3 = 3
    initial_state3 = np.asarray([[1,1,0,2,1,2,1,2,0,0], [1,1,0,2,1,2,1,2,0,0], [1,2,1,2,2,0,0,1,0,1], [2,2,0,2,1,1,2,0,0,1], [1,2,1,2,2,0,0,1,0,1], [2,2,0,2,1,1,2,0,0,1], [2,2,0,2,1,1,2,0,0,1], [1,1,0,2,1,2,1,2,0,0], [1,1,0,2,1,2,1,2,0,0], [1,2,1,2,2,0,0,1,0,1]]) 
    transition_matrix3 = np.random.rand(n_spieces3**2,n_spieces3**2)
    transition_matrix3 = np.array([e/sum(e) for e in transition_matrix3])
    #cols3 = np.array(['white', 'blue', 'red'])
    cols3 = []
    step_by_step3 = True
    cg3 = Cellular_automaton (initial_state3, transition_matrix3, cols3, max_range3, step_by_step3, log_level=1, log_file_name = 'activity_logger3')
    print(cg3)
    cg3.get_dynamic_plots(add = True)
    cg3.get_video("test")
    del cg3
    
if __name__ == "__main__":

    main()
