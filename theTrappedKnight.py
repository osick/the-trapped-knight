#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
plt.rcParams['animation.convert_path'] = r'magick'
import random
import sys
import os
from matplotlib.animation import FuncAnimation, ImageMagickFileWriter, FFMpegFileWriter

class spiralBoard:
    directions={"e":[0,-1,"n",1,0],"n":[-1,0,"w",0,-1],"w":[0,1,"s",-1,0],"s":[1,0,"e",0,1]}

    def __init__(self, size=[400,400]):     
        self.squares = np.zeros((2*size[0]+1, 2*size[1]+1))
        self.direction = "e"
        self.x = size[0] 
        self.y = size[1]
        self.count = 1
        self.squares[self.x][self.y] = 1 
        self.count += 1 
        self.x += 1
        self._initSq(4*size[0]*size[1])
    
    # PRIVATE METHODS
    def _initSq(self, loops):       
        for _ in range(loops):
            self.squares[self.x][self.y] = self.count
            self.count += 1 
            if self.squares[self.x + spiralBoard.directions[self.direction][0]][self.y+spiralBoard.directions[self.direction][1]]==0:
                self.x += spiralBoard.directions[self.direction][0]
                self.y += spiralBoard.directions[self.direction][1]
                self.direction = spiralBoard.directions[self.direction][2]
            else:
                self.x += spiralBoard.directions[self.direction][3]
                self.y += spiralBoard.directions[self.direction][4]

class knightPathFinder:
        
    def __init__(self, squares, steps=[1,2]):        
        self.squares = squares
        self.shape=steps
        self.movetypes=[[steps[0],-steps[1]],[steps[1],-steps[0]],[steps[1], steps[0]],[steps[0],steps[1]],[-steps[0],steps[1]],[-steps[1],steps[0]],[-steps[1],-steps[0]],[-steps[0],-steps[1]]]
        self.x = (self.squares.shape[0]-1)//2
        self.y = (self.squares.shape[1]-1)//2
        self.maxsize=self.squares.shape[0]*self.squares.shape[1]

    # PUBLIC METHODS
    def genHistory(self):
        self.history=[]
        self.history.append(self._nextMove())
        while self.history[-1][2] and len(self.history)<self.maxsize: 
            self.history.append(self._nextMove())
        self.xMin=min([s[0]  for s in self.history])
        self.yMin=min([s[1]  for s in self.history])
        self.xMax=max([s[0]  for s in self.history])
        self.yMax=max([s[1]  for s in self.history])
        self.dimMax=max(self.xMax,self.yMax)
        self.dimMin=max(self.xMin,self.yMin)
        print("Knight path of shape ("+str(self.shape[0])+","+str(self.shape[1])+"): length =", len(kn.history))

    # PRIVATE METHODS
    def _nextMove(self):
        allMoves = [self.squares[self.x + mt[0]][self.y + mt[1]] for mt in self.movetypes]
        self.squares[self.x][self.y] += self.maxsize
        self.x+=self.movetypes[allMoves.index(min(allMoves))][0]
        self.y+=self.movetypes[allMoves.index(min(allMoves))][1]
        return [self.x,self.y, (min(allMoves) <= self.maxsize)]

class pathAnimation:

    def __init__(self, kn):
        self.Xs=[]
        self.Ys=[]
        self.kn=kn
        for step in kn.history:
            self.Xs.append(step[0])
            self.Ys.append(step[1])    
        self.fig, self.ax = self._initPlot()

    # PUBLIC METHODS
    def animate(self, outputType="show", color="random", speed=10, outDir="out"): 
        if not os.path.exists(outDir): os.mkdir(outDir) 
        fname=os.path.join(outDir,"knightPath-{}-{}".format(self.kn.shape[0],self.kn.shape[1]))
        knightAnimation=FuncAnimation(self.fig,self._genLine, fargs=(speed, color), repeat=False ,frames=range(-speed,len(self.kn.history),speed,) ,blit=False ,interval=10, cache_frame_data=False)
        if   outputType == "screen":  plt.show()
        elif outputType == "avi":     knightAnimation.save(fname+".avi", writer=FFMpegFileWriter(fps=1, bitrate=100000, extra_args=['-vcodec', 'libx264']),)
        elif outputType == "mp4":     knightAnimation.save(fname+".mp4", writer=FFMpegFileWriter(fps=1, bitrate=100000, extra_args=['-vcodec', 'libx264']),)
        elif outputType == "gif":     knightAnimation.save(fname+'.gif', writer=ImageMagickFileWriter(fps=1))
        elif outputType == "html":    open(fname+".html", "w").write(self._genHtmlFrame(knightAnimation.to_html5_video(50.0))) 
        else: sys.exit("Unknown outputType '"+outputType+"': sys.exit()")

    # PRIVATE METHODS
    def _initPlot(self):
        fig,ax=plt.subplots(figsize=(8,8))
        #fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.set_xlim(self.kn.dimMin - 5 , self.kn.dimMax + 5)
        ax.set_ylim(self.kn.dimMin - 5 , self.kn.dimMax + 5)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(self._update_xticks))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(self._update_yticks))
        ax.set_title('(Generation {} of {})\n'.format(0,len(self.kn.history)), fontsize=14, color="black")
        return fig, ax

    def _update_xticks(self,x, pos): 
        return str(int(x-self.Xs[0]))
    
    def _update_yticks(self,x, pos): 
        return str(int(x-self.Ys[0]))

    def _genLine(self,i,speed,color):
        if i<0:return
        c=np.random.rand(3,) if color=="random" else color
        self.ax.set_title('(Generation {} of {})\n'.format(min(len(kn.history),i+speed),len(kn.history)))
        for j in range(speed):
            if i+j<=len(self.Xs) and i-2+j>=0: 
                self.ax.plot(self.Xs[i-2+j:i+j], self.Ys[i-2+j:i+j], color=c, lw=1, alpha=0.5)
        
    def _genHtmlFrame(self,mainBody):
        header='<html><body style="background-color:black;color:white;text-align:center;margin:0;padding:0;border:0">'
        header+='<h1> <br/>THE TRAPPED ({}-{})-KNIGHT</h1>'.format(self.kn.shape[0],self.kn.shape[1])
        header+='<div style="border-top: 4px solid red;width:100%">'
        header+='<div style="display: table;margin: 0 auto;border:3px solid white;">'
        footer='</div></div><p>Page generated by <a href="https://github.com/osick/the-trapped-knight">theTrappedKnight.py</a></p></body></html>'
        return header+mainBody+footer

if __name__=="__main__":

    if len(sys.argv)!=4: sys.exit("Usage:\nPython "+__file__+" <number> <number> [screen|mp4|avi|gif|html]")
    
    sb  = spiralBoard()
    kn  = knightPathFinder(sb.squares, [int(sys.argv[1]),int(sys.argv[2])])
    kn.genHistory()
    
    pa  = pathAnimation(kn)
    pa.animate(outputType=sys.argv[3], color="random", speed=50, outDir="out")
