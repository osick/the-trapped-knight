# The Trapped Knight Problem Solver

## Table of Contents
=================
* [The Problem](#the-problem)
  * [Examples](#examples)
* [The Python Libary](#the-python-library)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [The Classes](#the-classes)
    * [Class spiralBoard](#class-spiralboard)
    * [Class knightPathFinder](#class-knightpathfinder)
    * [Class pathAnimation](#class-pathanimation)
  * [Sample Usage](#sample-usage)
  * [The main file](#the-main-file)
* [References](#references)

## The Problem

The trapped knight problem is the following:
  Think of an infinite chess board where the squares are labeled according to the following pattern:
  <table>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
    <tr><td>...</td><td>20</td><td>21</td><td>22</td><td>23</td><td>24</td><td>25</td><td>...</td></tr>
    <tr><td>...</td><td>19</td><td>6</td><td>7</td><td>8</td><td>9</td><td>26</td><td>...</td></tr>
    <tr><td>...</td><td>18</td><td>5</td><td>0</td><td>`1`</td><td>10</td><td>27</td><td>...</td></tr>
    <tr><td>...</td><td>17</td><td>4</td><td>3</td><td>2</td><td>11</td><td>28</td><td>...</td></tr>
    <tr><td>...</td><td>16</td><td>15</td><td>`14`</td><td>13</td><td>12</td><td>29</td><td>...</td></tr>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
  </table>
  the squares are numbered along a spiral starting at one and circling around it until infnity.

  Next put a knight on the **1** square of this spiral chess board and ask for the path of the knight according to the following two rules
  1. never go to a square were the knight has been before
  2. Go to the square with minimum weight. 

  In the situation above starting at the **1** the next square is **14**. 

This problem can be generalized to other types of knights, not only hopping in (1,2) steps on the board, but with arbitrary step patterns (x,y) (with x>0 and y>0). It is importantt to notice the problem can be simplified to the situtation where `gcd(x,y)==1`. In the case `gcd(x,y)==c>1` this can be simplified to the case `(x/c,y/c)` withput loss of  generality. 

Questions are now? 
  1. How long is ths path? 
  2. Can it be infinite? 

For a (1,2)-knight the path has length 2016, for other types of knight we have the following data

Type of knight | Length | xDiam | yDiam | Density
-------------- | ------ | ----- | ----- | -------
(1,2)-knight   | 2016   | 55    |  56   | 0.65455
(1,3)-knight   | 3723   | 92    |  91   | 0.44470
(1,4)-knight   | 13103  | 125   |  125  | 0.83859
(2,1)-knight   | 2016   | 55    |  56   | 0.65455
(2,3)-knight   | 4634   | 81    |  81   | 0.70629
(3,1)-knight   | 3723   | 92    |  91   | 0.44470
(3,2)-knight   | 4634   | 81    |  81   | 0.70629

The meaning of the values is

* `Length` is path length
* `xDiam` is the maximum diameter of the path in x-direction
* `yDiam` is the maximum diameter of the path in y-direction
* `Density` is the ratio `Length/(xDiam*yDiam)` which is always `<=1`. The density expresses the degreaa of foldedness of the path.

Up to now no (x,y) knight is known with infinite path length

## Examples 

All the examples are generated using this lib.

* An [MP4](./samples/knightPath-1-22.mp4) for the (1,22)-knight
* A gif for the (1,2)-knight\
  ![knightPath-1-2.gif](./samples/knightPath-1-2.gif)
* A HTML file for the [(2,5)-knight](./samples/knightPath-2-5.html)


# The Python Library

## Requirements
  The source is a Python 3 library using 
  * Numpy
  * Matplotlib
  * Ffmpeg
  * imagemagick 

## Installation

1. Download the the file [theTrappedKnight.py](./theTrappedKnight.py) from this repository
2. Copy it into your working directory. 
3. Done

## The Classes

### Class spiralBoard
  tbd

### Class knightPathFinder  
  tbd

### Class pathAnimation
  tbd

## Sample Usage 

* A basic example may look like this:

  ```Python
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-

  # Import the three classes
  from theTrappedKnight import spiralBoard, knightPathFinder, pathAnimation 
  
  # Generate a spiral board
  mySpiralBoard  = spiralBoard()
  
  # Together with x,y geometry pass the board to the 
  # knightPathFinder class (here for the (1,2)-knight)
  myKnightPathFinder  = knightPathFinder(sb.squares, [1,4])
  
  # Generate the spiral path of the Knight
  myKnightPathFinder.genHistory()
  # The genHitory() method has a rudimentary output of some data of the path.
  # In this we have
  # -> "Knight path of shape (1,2) , 2016 | 55  |  56  |   0.65455"
   
  # Define a new pathAnimation Class passing a knightPathFinder instance to it
  myPathAnimation=pathAnimation(myKnightPathFinder)
  
  # Animate the Path
  myPathAnimation.animate(outputType="animgif", color="white", speed=100, outDir="out", type="scatter")
  ```
* We are done! 
* The result is\ 
<img src="./samples/knightPath-1-2.anim_02.gif" alt="Animated Gif for 1-2 Knight" width="500" height="500">


## The main file
  
  main.py is a reference implementation of the library and can be used to generate data and graphical representantions of the problem. We have
  ```
  Usage:
        Python main.py <num> <num>-... [screen|mp4|avi|animgif|gif|html|data] [line|scatter]
        or
        Python main.py <num>-<num> <num>-<num> [screen|mp4|avi|animgif|gif|html|data] [line|scatter]
  ```

# References
  * The problem will be explaiend in detail at [Numberphile](https://www.youtube.com/watch?v=RGQe8waGJ4w)
  * On [OEIS](https://oeis.org/A323472) the length is computed for a large quantity of x,y-knights (aka x,y-leapers) 

