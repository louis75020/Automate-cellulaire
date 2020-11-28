import random
import numpy as np

class Tinder_manager():
    
    def __init__(self, next_state):
        
        tinder_matrix = 4 * np.ones( np.shape(next_state), dtype='f' )
        tinder_matrix[0,:] = 3 ; tinder_matrix[:, np.shape(tinder_matrix)[1] - 1] = 3 ; tinder_matrix[ np.shape(tinder_matrix)[0] - 1, :] = 3 ; tinder_matrix[:, 0 ] = 3
        tinder_matrix[0,0] = 2 ; tinder_matrix[0, np.shape(tinder_matrix)[1] - 1] = 2 ; tinder_matrix[ np.shape(tinder_matrix)[0] - 1, 0] = 2 ; tinder_matrix[ np.shape(tinder_matrix)[0] - 1, np.shape(tinder_matrix)[1] - 1 ]=2
        self.tinder_matrix = tinder_matrix
        
        
        
    #Find the lonely cells
    def check_tinder_alert(self):
        
        tinder_matrix = self.tinder_matrix
        lonely_cells = []
        
        for i in range(np.shape(tinder_matrix)[0]):
            
            for j in range(np.shape(tinder_matrix)[1]):
                
                if tinder_matrix [i,j] == 1 : lonely_cells.append((i,j))
                    
        return lonely_cells
        
        
        
    #Find randomly a couple among the neighbors
    def regular_mariage (self, tuples, tmp_coord):
        
        potential_husbands = []
        if (tmp_coord[0] - 1, tmp_coord[1]) in tuples : potential_husbands.append( (tmp_coord[0] - 1, tmp_coord[1]) )
        if (tmp_coord[0] + 1, tmp_coord[1]) in tuples : potential_husbands.append( (tmp_coord[0] + 1, tmp_coord[1]) )
        if (tmp_coord[0], tmp_coord[1] - 1) in tuples : potential_husbands.append( (tmp_coord[0], tmp_coord[1] - 1) )
        if (tmp_coord[0], tmp_coord[1] + 1) in tuples : potential_husbands.append( (tmp_coord[0],tmp_coord[1] + 1) )
        return potential_husbands
        
        
    #Update the single cells
    def update_tinder (self,  tmp_coord,  husband, tuples):
        
        tinder_matrix = self.tinder_matrix 
        
        tinder_matrix[ tmp_coord ] = np.inf
        tinder_matrix[ husband ] = np.inf
        
        if tmp_coord[0] > 0 :
            tinder_matrix[ tmp_coord[0] - 1, tmp_coord[1] ] -= 1
            if tinder_matrix[ tmp_coord[0] - 1, tmp_coord[1] ] == 0 :
                tuples.remove( (tmp_coord[0] - 1, tmp_coord[1]) )
                
        if tmp_coord[0] +1 < np.shape(tinder_matrix)[0] :
            tinder_matrix[ tmp_coord[0] + 1, tmp_coord[1] ] -= 1
            if tinder_matrix[ tmp_coord[0] + 1, tmp_coord[1] ] == 0 :
                tuples.remove( (tmp_coord[0] + 1, tmp_coord[1]) )
                
        if tmp_coord[1] > 0 :
            tinder_matrix[ tmp_coord[0], tmp_coord[1] - 1 ] -= 1
            if tinder_matrix[ tmp_coord[0], tmp_coord[1] - 1] == 0 :
                tuples.remove( (tmp_coord[0], tmp_coord[1] - 1) )
                
        if tmp_coord[1] + 1 < np.shape(tinder_matrix)[1] :
            tinder_matrix[ tmp_coord[0], tmp_coord[1] + 1 ] -= 1
            if tinder_matrix[ tmp_coord[0], tmp_coord[1] + 1] == 0 :
                tuples.remove( (tmp_coord[0], tmp_coord[1] + 1) )
                
        if husband[0] > 0 :
            tinder_matrix[ husband[0] - 1, husband[1] ] -= 1
            if tinder_matrix[ husband[0] - 1, husband[1] ] == 0 :
                tuples.remove( (husband[0] - 1, husband[1]) )
                
        if husband[0] +1 < np.shape(tinder_matrix)[0] :
            tinder_matrix[ husband[0] + 1, husband[1] ] -= 1
            if tinder_matrix[  husband[0] + 1, husband[1] ] == 0 :
                tuples.remove( ( husband[0] + 1, husband[1]) )
                
        if husband[1] > 0 :
            tinder_matrix[ husband[0], husband[1] -1 ] -= 1
            if tinder_matrix[  husband[0], husband[1] -1 ] == 0 :
                tuples.remove( ( husband[0], husband[1] -1) )
                
        if husband[1] + 1 < np.shape(tinder_matrix)[1] :
            tinder_matrix[ husband[0], husband[1] +1 ] -=1
            if tinder_matrix[  husband[0], husband[1] +1 ] == 0 :
                tuples.remove( (husband[0], husband[1] +1) )
                
        return tinder_matrix
        
            
    
    def get_next_tuples(self, next_state, logger):
        
        logger.debug('>>>>>>>>>get_next_tupes>>>>>>>>')
        tinder_matrix = self.tinder_matrix
        
        #list of coordinates
        
        tuples = [ (i,j) for i in range(np.shape(next_state)[0]) for j in range(np.shape(next_state)[1]) ]
        output = [] 
        
        while len(tuples) > len(tuples) % 2 : #if the number of cells is odd at least 1 cell will stay alone     
            lonely_cells = self.check_tinder_alert()
            
            if lonely_cells != [] : tmp_coord = lonely_cells[0]
            else: tmp_coord = tuples[ random.randint(0, len(tuples) -1 ) ] #Choose any left coordinate
            
            #Find its possible husband
            if  self.regular_mariage(lonely_cells, tmp_coord) != [] : 
                potential_husbands =  self.regular_mariage(lonely_cells, tmp_coord) 
                
            else : potential_husbands = self.regular_mariage(tuples, tmp_coord)
            
            assert len(potential_husbands) > 0, "No possible couples found! The method does not work"

            #Choose randomly the husband and add it to output
            husband = potential_husbands[ random.randint(0, len(potential_husbands) -1 ) ]
            output.append( ( tmp_coord,  husband ) )
            #Tinder update
            self.update_tinder( tmp_coord, husband, tuples)
            #Next step
            try:
                tuples.remove( tmp_coord )
                tuples.remove( husband )
            except:
                self.logger.error("Issue with get_next_tuples while removing tuples")
                return []
                
        logger.debug('<<<<<<<<<<<get_next_tuples<<<<<<<<<<')
            
        return output