import pandas as pd
import cellular_automaton as ca
import sys

class Ca_manager(): 
    
    def __init__(self, initial_state_path, transition_matrix_path, other_params_path = None) :
        
        ##### wo other_params
        
        with open(transition_matrix_path,'r') as file : transition_matrix = pd.read_table(file, header = None, sep = ';')
        #print(transition_matrix.values)
        
        with open(initial_state_path,'r') as file : initial_state = pd.read_table(file, header = None, sep = ';', dtype='i')
        #print(initial_state.values)
        
        ##### other params
            
        if other_params_path != None :
        
            with open(other_params_path,'r') as file :
        
                other_params = pd.read_table(file, sep= ';', header = 0, index_col = False)
                
            #print(other_params) 
            
            try :   
                
                cols = str( other_params['cols'][0] )
                cols = cols.split(',')
                #print(cols, type(cols))
                
                max_range = str(other_params['max_range'] [0])
                if max_range == 'None' :
                    max_range = -1
                else : 
                    max_range = int(max_range)
                #print(max_range)
                
                step_by_step = other_params['step_by_step'][0]
                #print(step_by_step)
                
                log_level = int( other_params['log_level'] )
                #print(log_level)
                 
                log_file_name = other_params['log_file_name'][0]
                #print(log_file_name)
                
            except :
                
                print('Issue while type casting in other params')
                max_range = 10
                step_by_step = True
                log_level = 2
                log_file_name = 'activity.log'
                
            finally :
              
                if max_range <0 :
                    
                    self.c_a = ca.Cellular_automaton ( initial_state.values, transition_matrix.values, cols, None, step_by_step, log_level, log_file_name )
                    
                else :
                    
                    self.c_a = ca.Cellular_automaton ( initial_state.values, transition_matrix.values, cols, max_range, step_by_step, log_level, log_file_name )
                
        #### Back wo other params
                
        else :
            
            try :
                    
                self.c_a = ca.Cellular_automaton ( initial_state.values, transition_matrix.values )
            
            except :
                
                print ('ERROR : builder of Cellular_automaton() failed')
                return
        
        
    ####### to string for tests            
    def __str__(self) :
        
        print( self.c_a )
        return ''
        
        
        
####### main
def main() :
    
    #print(sys.argv)
    
    assert len(sys.argv) > 2, "Not enough args, the program will stop runing"
    assert len(sys.argv) < 5, "Too many args, the program will stop running"
    
    if len(sys.argv) == 3 :
        
        ca_manager = Ca_manager ( sys.argv[1], sys.argv[2] )
        
    else :
        
        ca_manager = Ca_manager ( sys.argv[1], sys.argv[2], sys.argv[3] )
        
        #print(ca_manager)
        #print(ca_manager.c_a.next_step())
    
    if ca_manager.c_a.max_range != None :
        ca_manager.c_a.get_dynamic_plots()
        
    else : 
        n = int(input('Input an integer not too large <15'))
        ca_manager.c_a.n_steps(n, add = True)
        ca_manager.c_a.get_video()
        
    
    del ca_manager
    
    
###### script    
if __name__ == "__main__":

    main()