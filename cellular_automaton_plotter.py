# Custom module
import cellular_automaton_runner as car
#For plotting
import pylab 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import figure 
import matplotlib.colors


class Cellular_automaton_plotter(car.Cellular_automaton_runner):

    #### Real_time plotting
    
    def get_dynamic_plots(self, add = False):
        
        ### To animate
        
        def animate(i): 
            
            
            plt.cla() 
            self.current_state = self.next_step()
            
            if(add) : 
            
                all_states.append(self.current_state)
                if len(colors) > 0 : pylab.imshow(current_state, cmap = cmap)
                else : pylab.imshow(current_state)
                
            else : 
                
                if len(colors) > 0 : pylab.imshow(self.current_state, cmap = cmap)
                else : pylab.imshow(self.next_step())
                
                
        #### Animation
        
        all_states = self.all_states; colors = self.cols; current_state = self.current_state
        
        
        if len(colors) > 0 : cmap = matplotlib.colors.ListedColormap(colors, name = 'colors', N = None) 
        
        plt.style.use('fivethirtyeight')
        ani = animation.FuncAnimation(plt.gcf(), animate, 10)
        plt.show()
        return 0
        
        
        
     #### Video of recorded states   
        
    def get_video(self, name = 'last_video'):
        
        colors = self.cols
        
        if len(colors) > 0 : cmap = matplotlib.colors.ListedColormap(colors, name='colors', N=None)
        
        frames = [] 
        fig = pylab.figure()
        
        for i in range(len(self.all_states)):
            
            
            if len(colors) > 0 : next_frame = [ pylab.imshow(self.all_states[i], animated = True, cmap=cmap) ] 
            
            else : next_frame = [ pylab.imshow(self.all_states[i], animated = True) ] 
            
            frames.append(next_frame)
        
        ani = animation.ArtistAnimation(fig, frames, interval = 100, blit = True)
        
        ani.save(name+'.htm')
        return 0
        
        
    #### plot last state
    # plot current_state the last validated state
    
    def get_last_plot(self) :
        
        colors = self.cols
        fig = pylab.figure()
        
        if len(colors) > 0 : 
            
            cmap = matplotlib.colors.ListedColormap(colors, name = 'colors', N = None)
            pylab.imshow(self.current_state, cmap = cmap)
            
        else :   pylab.imshow(self.current_state)  
        
        plt.show()
        return 0