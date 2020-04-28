#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""[summary]
see

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import sys

plt.rcParams['animation.convert_path'] = r'd:\bin\imagemagick\magick.exe'
plt.rcParams['animation.ffmpeg_path']  = r'd:\bin\ffmpeg-20200426-1128aa8-win64-static\bin\ffmpeg.exe'

from matplotlib.animation import FuncAnimation, ImageMagickFileWriter, FFMpegFileWriter

history = []
Xs      = []
Ys      = []

# initialize variables and create empty dataframe

class spiral:
    """
    Spiral class.
    
    Creates dataframe incrementing in a spiral.
    """
    directions={"e":[0,-1,"n",1,0],"n":[-1,0,"w",0,-1],"w":[0,1,"s",-1,0],"s":[1,0,"e",0,1]}

    def __init__(self, environment, direction, size=[50,50]):        
        self.environment = environment
        self.direction = direction
        self.x = size[0]
        self.y = size[1]
        self.count = 1
        self.environment[self.x][self.y] = 1
        self.count += 1 
        self.x += 1
        self._initEnv(size[0]*size[1])

    def _initEnv(self, loops):       
        for _ in range(loops):
            self.environment[self.x][self.y] = self.count
            self.count += 1 
            if self.environment[self.x + spiral.directions[self.direction][0]][self.y+spiral.directions[self.direction][1]]==0:
                self.x += spiral.directions[self.direction][0]
                self.y += spiral.directions[self.direction][1]
                self.direction = spiral.directions[self.direction][2]
            else:
                self.x += spiral.directions[self.direction][3]
                self.y += spiral.directions[self.direction][4]

class knight:
    
    """
    Knight class.
    
    Starts at the centre of the spiral. Moves according to it's rules in chess, selecting the lowest tile that has not been previously visited. 
    """
    
    def __init__(self, environment, steps=[1,2], size=[50,50]):        
        self.environment = environment
        self.movetypes=[[steps[0],-steps[1]],[steps[1],-steps[0]],[steps[1], steps[0]],[steps[0],steps[1]],[-steps[0],steps[1]],[-steps[1],steps[0]],[-steps[1],-steps[0]],[-steps[0],-steps[1]]]
        self.x = size[0]
        self.y = size[1]
        self.maxsize=size[0]*size[0]*4

    def moves(self):
        allMoves = [self.environment[self.x + mt[0]][self.y + mt[1]] for mt in self.movetypes]
        self.environment[self.x][self.y] = self.environment[self.x][self.y] + 10000
        self.x+=self.movetypes[allMoves.index(min(allMoves))][0]
        self.y+=self.movetypes[allMoves.index(min(allMoves))][1]
        return [self.x,self.y, (min(allMoves) <= self.maxsize)]


def genLine(i):
    global history, Xs,Ys, ron
    for _ in range(30):
        if history[-1][2] and len(history)<ron.maxsize:
            history.append(ron.moves())
            Xs.append(history[-1][0])
            Ys.append(history[-1][1])
            ax.plot(Xs[-3:-1], Ys[-3:-1], color="silver", lw=1)

if __name__=="__main__":
    

    size=[300,300]
    shape=[1,2]
    df = pd.DataFrame(np.zeros((2*size[0], 2*size[1])))
    
    test    = spiral(df, direction = 'e', size=size)
    ron     = knight(test.environment,shape,size=size)
    history = [[size[0],size[1],True]]
    
    fig,ax=plt.subplots()
    ax.set_xlim(0,2*size[0])
    ax.set_ylim(0,2*size[1])

    knightAnimation=FuncAnimation(fig,genLine)
    if len(sys.argv)>1: 
        if sys.argv[1]=="show":
            plt.show()
        elif sys.argv[1]=="video": 
            writer=FFMpegFileWriter()
            knightAnimation.save('knight.mp4', writer=writer, fps=60)            
        elif sys.argv[1]=="gif": 
            writer=ImageMagickFileWriter()
            knightAnimation.save('knight.gif', writer=writer, fps=60)
    