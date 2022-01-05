#!/usr/bin/env python3
# -*- coding: utf-8 -
__author__  = "Oliver Sick"
__version__= "0.1.0"
__date__= "03.06.2020"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from math import gcd
plt.rcParams['animation.convert_path'] = r'magick'
import random
import sys
import os
from matplotlib.animation import FuncAnimation, ImageMagickFileWriter, FFMpegFileWriter

class spiralBoard:
    """static class generating a A x B board with a spiral enumeration of the squares"""

    directions={"e":[0,-1,"n",1,0],"n":[-1,0,"w",0,-1],"w":[0,1,"s",-1,0],"s":[1,0,"e",0,1]}

    def __init__(self, size=[1000,1000]):     
        """init method

        Keyword Arguments:
            size {list} -- the size of the board (default: {[1000,1000]})
        """
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
        """private method to generate the spiral enumerations 

        Arguments:
            loops {int} -- the number of squares enumerated as a spiral (starting from the middle of the board)
        """
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
        print("Knight path of shape ("+str(self.shape[0])+","+str(self.shape[1])+")",
            ", Length =",     len(self.history), 
            ", xDiam =",    self.xMax-self.xMin,
            ", yDiam =",    self.yMax-self.yMin,
            ", Density =",  "{:.5f}".format(len(self.history)/(self.yMax-self.yMin)/(self.xMax-self.xMin)))

    # PRIVATE METHODS
    def _nextMove(self):
        allMoves = [self.squares[self.x + mt[0]][self.y + mt[1]] for mt in self.movetypes]
        self.squares[self.x][self.y] += self.maxsize
        self.x+=self.movetypes[allMoves.index(min(allMoves))][0]
        self.y+=self.movetypes[allMoves.index(min(allMoves))][1]
        return [self.x,self.y, (min(allMoves) <= self.maxsize)]

class pathAnimation:

    def __init__(self, kn):
        self.kn=kn
        arr2d = list(zip(*self.kn.history))   
        self.Xs=arr2d[0]
        self.Ys=arr2d[1] 
        self.fig, self.ax = self._initPlot() 

    # PUBLIC METHODS
    def animate(self, outputType="screen", color="random", speed=10, outDir="out",type="line"): 
        if not os.path.exists(outDir): os.mkdir(outDir) 
        fname=os.path.join(outDir,"knightPath-{}-{}".format(self.kn.shape[0],self.kn.shape[1]))
        knightAnimation=FuncAnimation(self.fig,self._genLine, fargs=(speed, color, type), repeat=False ,frames=range(-speed,len(self.kn.history),speed,) ,blit=False ,interval=10, cache_frame_data=False)
        if   outputType == "screen":  
            plt.show()
        elif outputType == "avi":     
            knightAnimation.save(fname+".avi", writer=FFMpegFileWriter(fps=1, bitrate=100000, extra_args=['-vcodec', 'libx264']),)
            print("video file written to",fname+".avi")
        elif outputType == "mp4":     
            knightAnimation.save(fname+".mp4", writer=FFMpegFileWriter(fps=1, bitrate=100000, extra_args=['-vcodec', 'libx264']),)
            print("MP4 video file written to",fname+".mp4")
        elif outputType == "gif":     
            knightPathAnim=FuncAnimation(self.fig,self._genAllLines, repeat=False ,frames=range(1) ,blit=False ,interval=10, cache_frame_data=False)
            knightPathAnim.save(fname+'.gif', writer=ImageMagickFileWriter(fps=1))
            print("Image written to",fname+".gif")
        elif outputType == "animgif": 
            knightAnimation.save(fname+'.anim.gif', writer=ImageMagickFileWriter(fps=1))
            print("Animated gif written to",fname+".anim.gif")
        elif outputType == "html":    
            open(fname+".html", "w").write(self._genHtmlFrame(knightAnimation.to_html5_video(50.0))) 
            print("HTML file written to",fname+".html")
        else: 
            print("Unknown outputType '"+outputType+"'")
            return

    # PRIVATE METHODS
    def _initPlot(self):
        fig,ax=plt.subplots(figsize=(10,10))
        ax.set_aspect('equal', 'box')
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

    def _genLine(self, i, speed, color, type): 
        c=np.random.rand(3,) if color=="random" else color
        self.ax.set_title('(Generation {} of {})\n'.format(min(len(self.kn.history), i+speed), len(self.kn.history)))
        for j in range(speed):
            if i+j==0: 
                self.ax.scatter(self.Xs[i+j], self.Ys[i+j], color="green", alpha=1)
            if i+j==1: 
                self.ax.scatter(self.Xs[i+j], self.Ys[i+j], color="blue", alpha=1)
            if type=="line" and i+j<=len(self.Xs) and i-2+j>=0: 
                self.ax.plot(self.Xs[i-2+j:i+j], self.Ys[i-2+j:i+j], color=c, lw=1, alpha=0.5)
            elif type=="scatter" and i+j<len(self.Xs) and i+j>0: 
                self.ax.scatter(self.Xs[i+j], self.Ys[i+j], color=c, alpha=0.7, s=2)
            if i+j==len(self.Xs)-1: 
                self.ax.scatter(self.Xs[i+j], self.Ys[i+j], color="red", alpha=1)

    def _genAllLines(self,i,color="white"):
        self.ax.set_title('(Generations {})\n'.format(len(self.kn.history)))
        for j in range(0,len(self.kn.history)-2): self.ax.plot(self.Xs[j:j+2], self.Ys[j:j+2], color=color, lw=1, alpha=0.5)
        
    def _genHtmlFrame(self,mainBody):
        header=r'<html><body style="background-color:white;color:black;text-align:center;margin:0;padding:0;border:0;font-weight:bold">'
        header+=r'<h1><br/>THE TRAPPED ({}-{})-KNIGHT</h1>'.format(self.kn.shape[0],self.kn.shape[1])
        header+=r'<div style="border-top: 4px solid red;width:100%">'
        header+=r'<div style="display: table;margin: 0 auto;border:3px solid white;">'
        footer=r'</div></div><p>Page generated by <a href="https://github.com/osick/the-trapped-knight">theTrappedKnight.py</a></p></body></html>'
        return header+mainBody+footer
