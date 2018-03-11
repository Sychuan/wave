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
    startR = 0
    startG = 0    
    startB = 0
    endR = 255
    endG = 149
    endB = 0
    colorscale = 0
    counter = 0
    
    def lerp(x,y,t):
         return (1-t)*x+t*y

class interferention:
    title = "untitled"
    rangexy = 100
    typeM = True
    expR = 0
    count = 10
    pos = [0,0]
    C = 0#-0.621#-1+0.1j
    z0 = 0
    Cm = 1.3+2j
    trap = 1
    fracnum = 1
    method = 0
    date = 0
    
    scale = 5
 
  

#-----main render function------------------------------------------------------------------------
class wave:
    A = 1 #A/r amplitude
    w = 0.5 #krugovaya chastota
    k = 12 #wave number
    t = 0
    
  
def spherical_wave(z):
    
    #z = (wave.A * np.cos(wave.w*wave.t-wave.k*abs(z+1)))
    z = wave.A/np.abs(z)*np.exp(1j*wave.w*wave.t-1j*wave.k*abs(z))
    #z = np.exp(1j*wave.k*np.abs(z))*np.exp(-1j*2*np.pi*wave.t)/np.abs(z)
    
    modul = abs(z)
    phase = np.angle(z, deg=True)
    if phase<0:
        phase+=360
    
    rgb_color = colorsys.hls_to_rgb(1,phase/360,1) 
    try:
        w=(int(rgb_color[0]*255),int(rgb_color[1]*255),int(rgb_color[2]*255))
    except:
        w = (0,0,0)
    return w

def render(dz,counter,new):   
    start = timer()
    pygame.init()
    pygame.display.set_mode((interferention.rangexy,interferention.rangexy))
    window = pygame.display.get_surface()
    
    directory ="wave"+str(interferention.date)
    
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    x = np.arange(-(interferention.rangexy/2),(interferention.rangexy/2))
    y = np.arange(-(interferention.rangexy/2),(interferention.rangexy/2))
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = (xx+1j*yy)/interferention.scale-(interferention.pos[0]/interferention.scale-1j*interferention.pos[1]/interferention.scale)+dz
    npwave = np.frompyfunc(spherical_wave,1,1)
    z = npwave(z)
    w = np.array([list(arr) for arr in z])
    w = np.flipud(np.fliplr(np.rot90(w))) 
    w = ndimage.gaussian_filter(w, sigma=0.5)
        #pxarray = pygame.pixelarray
    pygame.surfarray.blit_array(window,w)
    pygame.display.flip()
    #showing final image          
    pxarray = None       
    #saving image
    pygame.image.save(window,interferention.title+"_xy"+str(interferention.rangexy)+".png")
    end = timer()
    print("finished time:"+str(end - start))
    
    print('-'*15+'end'+'-'*15)    
         




    
#------------------------------------------------------------------------------

    print('-'*15+'start'+'-'*15)
    interferention.date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    #initializing Pygame
    
#render(0,0,True)
    
while True:
    wave.t += 0.1
    render(0,0,True)    
    for event in pygame.event.get():
     if event.type == pygame.QUIT:            
            
            pygame.quit()
    
    


 

          