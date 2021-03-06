# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 23:11:09 2018

@author: Maksim
"""
import datetime
import os, errno
import pygame
import numpy as np
import colorsys
from timeit import default_timer as timer
from numba import jit
from scipy import ndimage

# -----input of necessary information


class ColorM():
    startRGB = (0, 0, 0)
    endRGB = (255, 149, 0)
    hue = 0.5
    colorscale = 1
   

    def lerp(x, y, t):
        return (1-t)*x+t*y

class wave:
    
    
    def __init__(self, A, w, k, t, pos):      
        self.A = A #A/r amplitude
        self.w = w #krugovaya chastota
        self.k = k #wave number
        self.t = t
        self.pos = pos
        self.phi = 1
        
    def plane_wave(self, z):
            z = self.A * np.exp(1j*(self.k*z-self.w*self.t+self.phi))          
            return z
       
    def spherical_wave(self, z):
            z = self.A/np.abs(z+self.pos[0]+self.pos[1]*1j)*np.exp(1j*self.w*self.t-1j*self.k*np.abs(z+self.pos[0]+self.pos[1]*1j))           
            return z


class simulation:
    
    window = pygame.display.get_surface()
    title = "untitled"
    rangexy = (289, 409)
    pos = [0, 0]
    method = 0
    date = 0
    counter = 0
    scale = 20
    directory = ""
    waves = []
    
    
    def coloring0(z):
            try:
                #w=(ColorM.lerp(0,255,(abs(z.real/ColorM.colorscale))%1), 
                  # ColorM.lerp(0,149,(abs(z.real/ColorM.colorscale))%1), 
                  # ColorM.lerp(0,0,(abs(z.real/ColorM.colorscale))%1))
                
                w=((int(abs(z.real/ColorM.colorscale)%1)*255), int((abs(z.real/ColorM.colorscale)%1)*255), int((abs(z.real/ColorM.colorscale)%1)*255))
            except:
                w = (0, 0, 0)
            return w
        
    def coloring3(z):
            try:
               if round(z.real,1) < 0:
                ColorM.hue = 0.5
               elif round(z.real,1)>0:
                    ColorM.hue = 0.0
               elif round(z.real,1)==0:
                    ColorM.hue = 0.2
               rgb_color = colorsys.hls_to_rgb(ColorM.hue, 0.5, 1)
               w=(int(rgb_color[0]*255), int(rgb_color[1]*255), int(rgb_color[2]*255))   
            except:
                w = (0, 0, 0)
            return w 
            
    
    def coloring1(z):
            if z.real < 0:
                ColorM.hue = 0.5
            else:
                ColorM.hue = 0.0
            rgb_color = colorsys.hls_to_rgb(ColorM.hue, (abs(z.real)/ColorM.colorscale), 1)
            try:

                w=(int(rgb_color[0]*255), int(rgb_color[1]*255), int(rgb_color[2]*255))
            except:
                w = (0, 0, 0)
            return w 
    
        
    def coloring2(z):
            try:
                phase = np.angle(z,deg=True)
                if phase<0:
                    phase+=360
                rgb_color = colorsys.hls_to_rgb((phase/360), abs(z.real/ColorM.colorscale)%1, abs(z.imag/ColorM.colorscale)%1)
                
                w=(int(rgb_color[0]*255), int(rgb_color[1]*255), int(rgb_color[2]*255))
                 
                
            except:
                w = (0, 0, 0)
            return w




    def start():
            start = timer()
            simulation.directory ="wave".join(str(simulation.date))
            try:
                os.makedirs(simulation.directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            simulation.date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
            pygame.init()
            pygame.display.set_mode((simulation.rangexy[0],simulation.rangexy[1]))
            simulation.window = pygame.display.get_surface()
            x = np.arange(-(simulation.rangexy[0]/2),(simulation.rangexy[0]/2))
            y = np.arange(-(simulation.rangexy[1]/2),(simulation.rangexy[1]/2))
            xx, yy = np.meshgrid(x, y, sparse=True)
            z = (xx+1j*yy)/simulation.scale-(simulation.pos[0]/simulation.scale-1j*simulation.pos[1]/simulation.scale)
            
            npcolor = np.frompyfunc(simulation.coloring3, 1, 1)
            end = timer()
            print(np.shape(z))
            print("finished time:"+str(end - start))
            return z, npcolor

    def render(z, npcolor, waves):
            zwave = np.zeros((simulation.rangexy[1],simulation.rangexy[0]), dtype=np.complex128)
            for wave in waves:
                zwave += wave.spherical_wave(z) 
            #print(zwave)
            w = npcolor(zwave)            
            w = np.array([list(arr) for arr in w])          
            w = np.flipud(np.fliplr(np.rot90(w)))
            w = ndimage.gaussian_filter(w, sigma=0.6)
            pygame.surfarray.blit_array(simulation.window, w)            
            pygame.display.update()
            

#------------------------------------------------------------------------------

z, npcolor = simulation.start()

waves = []
number = 10
#for x in range(number):
    
    #waves.append(wave(0.5,3,2,x/2,pos=[9*np.cos(np.pi/(number/2)*(x+1)), 9*np.sin(np.pi/(number/2)*(x+1))]))
for x in range(number):
    for y in range(number):
        waves.append(wave(0.5,3,1,x/3,pos=[x*8-5, y*8-5]))    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    start = timer()
    for x in range(len(waves)):
        waves[x].t += 0.05
    
    #w2.t += 0.05
    simulation.render(z, npcolor, waves)
    simulation.counter+=1
    pygame.image.save(simulation.window,simulation.directory+"/"+simulation.title+"_xy"+str(simulation.rangexy[0])+'_'+str(simulation.rangexy[1])+'_'+str(simulation.counter)+".png")

    end = timer()
    print("finished time:"+str(end - start))




