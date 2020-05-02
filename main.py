#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from math import gcd
from theTrappedKnight import spiralBoard, knightPathFinder, pathAnimation


def main(xRange,yRange,outputType,pathType,color="white"):
    """[summary]

    Arguments:
        xRange {range} --  the first ccordinate of a general (x,y)-knight
        yRange {range} -- the second ccordinate of a general (x,y)-knight
        outputType {str} -- a selection of the output format: [screen|mp4|avi|animgif|gif|html|data]
        pathType {str} -- a selection of the path format: [line|scatter]

    Keyword Arguments:
        color {str} -- the color of the path (either dots or lines) (default: {"white"})
    """
    for x in xRange:
        for y in yRange:  
            if gcd(x,y)>1:continue  
            sb  = spiralBoard()
            kn  = knightPathFinder(sb.squares, [x,y])
            kn.genHistory()
            if outputType in ["screen","mp4","avi","animgif","gif","html"]:
                pa  = pathAnimation(kn)
                pa.animate(outputType=outputType, color=color, speed=len(kn.history)//100, outDir="out", type=pathType)


def help(): 
    """help string and exit with error"""
    
    sys.exit("Usage:\n\tPython "+__file__+" <num> <num>-... [screen|mp4|avi|animgif|gif|html|data] [line|scatter]\
    \n\tor\n\tPython "+__file__+" <num>-<num> <num>-<num> [screen|mp4|avi|animgif|gif|html|data] [line|scatter]")


if __name__=="__main__":
    if len(sys.argv)!=5: help()
    xRange      = range(int(sys.argv[1].split("-")[0]), int(sys.argv[1].split("-")[1])+1) if sys.argv[1].find("-")>0 else range(int(sys.argv[1]), int(sys.argv[1])+1)
    yRange      = range(int(sys.argv[2].split("-")[0]), int(sys.argv[2].split("-")[1])+1) if sys.argv[2].find("-")>0 else range(int(sys.argv[2]), int(sys.argv[2])+1)
    outputType  = sys.argv[3]
    pathType    = sys.argv[4]
    main(xRange,yRange,outputType,pathType)