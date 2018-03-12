# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 23:11:09 2018

@author: Maksim
"""
import datetime
import os, errno
import pygame
import numpy as np
from scipy import ndimage
import colorsys
import random
from timeit import default_timer as timer


# -----input of necessary information


class ColorM():
    startRGB = (0,0,0)
    endRGB = (255,149,0)   
    hue = 0.5
    colorscale = 0
    counter = 0
    
    def lerp(x,y,t):
         return (1-t)*x+t*y

class interferention:
    window = pygame.display.get_surface()
    title = "untitled"
    rangexy = (200,200)    
    pos = [0,0]    
    method = 0
    date = 0
    counter = 0
    scale = 10
    directory = ""
 
  

#-----main render function------------------------------------------------------------------------

class wave:
    A = 3 #A/r amplitude
    w = 2 #krugovaya chastota
    k = 1 #wave number
    t = 0
    
def coloring2(z):
        if z.real<0:            
            ColorM.hue=0.2
        else:
            ColorM.hue=0.0        
        rgb_color = colorsys.hls_to_rgb(ColorM.hue, (abs(z.real/4))%1,1)                   
        try:
            
            w=(int(rgb_color[0]*255),int(rgb_color[1]*255),int(rgb_color[2]*255))
        except:
            w = (0,0,0)
        return w
        
    
def coloring(z):       
        try:
            w=(ColorM.lerp(0,255,(abs(z.real/4))%1),ColorM.lerp(0,149,(abs(z.real/4))%1),ColorM.lerp(0,0,(abs(z.real/4))%1))      
            #w =(ColorM.lerp(0,255,(abs(z/4))%1),ColorM.lerp(0,149,(abs(z/4))%1),ColorM.lerp(0,0,(abs(z/4))%1))  
        except:
            w = (0,0,0)
        return w
        
     
def spherical_wave(z):        
        #z = (wave.A * np.cos(wave.w*wave.t-wave.k*abs(z+1)))
        z1, z2 = wave.A/np.abs(z+5)*np.exp(1j*wave.w*wave.t-1j*wave.k*np.abs(z+5)), wave.A/np.abs(z-5)*np.exp(1j*wave.w*wave.t-1j*wave.k*abs(z-5))
        #z = np.exp(1j*wave.k*np.abs(z))*np.exp(-1j*2*np.pi*wave.t)/np.abs(z)       
        return  z1+z2
   
def start():
        start = timer()
        interferention.directory ="wave"+str(interferention.date)    
        try:
            os.makedirs(interferention.directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise    
        interferention.date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        pygame.init()  
        pygame.display.set_mode((interferention.rangexy[0],interferention.rangexy[1]))
        interferention.window = pygame.display.get_surface()
        x = np.arange(-(interferention.rangexy[0]/2),(interferention.rangexy[0]/2))
        y = np.arange(-(interferention.rangexy[1]/2),(interferention.rangexy[1]/2))
        xx, yy = np.meshgrid(x, y, sparse=True)
        z = (xx+1j*yy)/interferention.scale-(interferention.pos[0]/interferention.scale-1j*interferention.pos[1]/interferention.scale)
        
        npcolor = np.frompyfunc(coloring,1,1)
        end = timer()
        print("finished time:"+str(end - start))
        return z, npcolor
  
def render(z,counter,new,npwave):   
        
         
        z = npwave(spherical_wave(z))
        z = np.array([list(arr) for arr in z])
        z = np.flipud(np.fliplr(np.rot90(z))) 
        #w = ndimage.gaussian_filter(w, sigma=0.5)
            #pxarray = pygame.pixelarray
        pygame.surfarray.blit_array(interferention.window,z)
        pygame.display.flip()
        #showing final image          
        
        
        interferention.counter+=1
        pygame.image.save(interferention.window,interferention.directory+"/"+interferention.title+"_xy"+str(interferention.rangexy[0])+str(interferention.rangexy[1])+str(interferention.counter)+".png")
       
        
   
         




    
#------------------------------------------------------------------------------

    
   
    #initializing Pygame
    
#render(0,0,True)

z, npwave = start()    
while True:        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:      
            pygame.quit()
    start = timer()
    wave.t += 0.1
    render(z,0,True,npwave)
    end = timer()
    print("finished time:"+str(end - start))


 

          