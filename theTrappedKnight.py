#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import os

from matplotlib.animation import FuncAnimation, ImageMagickFileWriter, FFMpegFileWriter, writers
Xs      = []
Ys      = []

class board:
    directions={"e":[0,-1,"n",1,0],"n":[-1,0,"w",0,-1],"w":[0,1,"s",-1,0],"s":[1,0,"e",0,1]}

    def __init__(self, direction, size=[50,50]):        
        self.squares = np.zeros((2*size[0]+1, 2*size[1]+1))
        self.direction = direction
        self.x = size[0]
        self.y = size[1]
        self.count = 1
        self.squares[self.x][self.y] = 1 
        self.count += 1 
        self.x += 1
        self._initSq(4*size[0]*size[1])

    def _initSq(self, loops):       
        for _ in range(loops):
            self.squares[self.x][self.y] = self.count
            self.count += 1 
            if self.squares[self.x + board.directions[self.direction][0]][self.y+board.directions[self.direction][1]]==0:
                self.x += board.directions[self.direction][0]
                self.y += board.directions[self.direction][1]
                self.direction = board.directions[self.direction][2]
            else:
                self.x += board.directions[self.direction][3]
                self.y += board.directions[self.direction][4]

class knight:
        
    def __init__(self, squares, steps=[1,2], size=[50,50]):        
        self.squares = squares
        self.shape=steps
        self.movetypes=[[steps[0],-steps[1]],[steps[1],-steps[0]],[steps[1], steps[0]],[steps[0],steps[1]],[-steps[0],steps[1]],[-steps[1],steps[0]],[-steps[1],-steps[0]],[-steps[0],-steps[1]]]
        self.x = size[0]
        self.y = size[1]
        self.maxsize=4*size[0]*size[1]

    def nextMove(self):
        allMoves = [self.squares[self.x + mt[0]][self.y + mt[1]] for mt in self.movetypes]
        self.squares[self.x][self.y] += self.maxsize
        self.x+=self.movetypes[allMoves.index(min(allMoves))][0]
        self.y+=self.movetypes[allMoves.index(min(allMoves))][1]
        return [self.x,self.y, (min(allMoves) <= self.maxsize)]


    def genHistory(self):
        global Xs, Ys
        self.history=[]
        self.history.append(self.nextMove())
        while self.history[-1][2] and len(self.history)<self.maxsize: 
            self.history.append(self.nextMove())
        for step in self.history:
            Xs.append(step[0])
            Ys.append(step[1])
        self.xMin=min(Xs)
        self.xMax=max(Xs)
        self.yMin=min(Ys)
        self.yMax=max(Ys)
        self.dimMax=max(self.xMax,self.yMax)
        self.dimMin=max(self.xMin,self.yMin)

def genLine(i,speed, color="random"):
    global Xs, Ys
    if color=="random": c=np.random.rand(3,)
    else: c=color
    for j in range(speed):
        if i+j<=len(Xs): 
            ax.plot(Xs[i-2+j:i+j], Ys[i-2+j:i+j], color=c, lw=1)
            ax.set_title('({},{})-Knight\n(Generation {} of {})\n'.format(knightGeom[0],knightGeom[1],min(len(kn.history),i+speed),len(kn.history)))
            

def anim(kn, speed, type="show", color="random"):
    directory="out"
    if not os.path.exists(directory): os.mkdir(directory) 
    fname=os.path.join(directory,"knight-{}-{}".format(kn.shape[0],kn.shape[1]))
    
    knightAnimation=FuncAnimation(fig,genLine, fargs=(speed, color), repeat=False, frames=range(2,len(kn.history),speed,),blit=False, interval=10, cache_frame_data=False)
    if   type=="show":  plt.show()
    elif type=="video": knightAnimation.save(fname+".avi", writer=FFMpegFileWriter(fps=speed, bitrate=100000, extra_args=['-vcodec', 'libx264']),)
    elif type=="gif":   knightAnimation.save(fname+'.gif', writer=ImageMagickFileWriter(fps=5))
    elif type=="html":  open(fname+".html", "w").write(knightAnimation.to_html5_video())

def initPlot(kn):
    fig,ax=plt.subplots(figsize=(8,8))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.set_xlim( kn.dimMin-10, kn.dimMax+10)
    ax.set_ylim( kn.dimMin-10 ,kn.dimMax+10)
    ax.xaxis.label.set_color('white')
    ax.set_xlabel('step 0',)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    ax.set_title('({},{})-Knight\nGeneration {} of {})\n'.format(knightGeom[0],knightGeom[1],0,len(kn.history)), fontsize=14, color="white", fontweight='bold')
    return fig, ax

if __name__=="__main__":

    if len(sys.argv)!=4: 
        sys.exit("Usage:\nPython "+__file__+" <number> <number> [show|video|gif|html]")
    knightGeom=[int(sys.argv[1]),int(sys.argv[2])]
    type=sys.argv[3]

    dim=400
    speed=200
    boardGeom=[dim,dim]

    sp  = board(direction='e',  size=[dim,dim])
    kn  = knight(sp.squares, knightGeom, size=boardGeom)
    kn.genHistory()
    print("knight of shape ("+str(knightGeom[0])+","+str(knightGeom[1])+"): length =", len(kn.history))
    fig, ax = initPlot(kn)
    anim(kn, 10, type, "white")
