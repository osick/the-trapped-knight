

## The "trapped knight" Problem

The trapped knight problem is the following:
  Think of an infinite chess board where the squares are labeled according to the following pattern:
  <table>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
    <tr><td>...</td><td>20</td><td>21</td><td>22</td><td>23</td><td>24</td><td>25</td><td>...</td></tr>
    <tr><td>...</td><td>19</td><td>6</td><td>7</td><td>8</td><td>9</td><td>26</td><td>...</td></tr>
    <tr><td>...</td><td>18</td><td>5</td><td>0</td><td style="color:green">1</td><td>10</td><td>27</td><td>...</td></tr>
    <tr><td>...</td><td>17</td><td>4</td><td>3</td><td>2</td><td>11</td><td>28</td><td>...</td></tr>
    <tr><td>...</td><td>16</td><td>15</td><td style="color:blue">14</td><td>13</td><td>12</td><td>29</td><td>...</td></tr>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
  </table>
  the squares are numbered along a spiral staruing at one and circling around it until infnity

  Next put a knight on the **1** square of this spiral chess board and ask for the path of the knight according to the following two rules
  1. never go to a square were the knight has been before
  2. Go to the square with minimum weight. 

  In the situation above starting at the **1** the next square i **14**. 

  The questions are now? 
  * How long is ths path? 
  * Can it be infinite? 

This problem can be generalized to generylized knight, not only hopping in (1,2) steps on the board, but with arbitrary step patterns (x,y) with x>0 and y>0. The problem can be simplified to the situtation where `gcd(x,y)==1`.

# Example 

## theTrappedKnight library

# Requirements
  The source is a Python 3 library using 
  * Numpy
  * Matplotlib
  * Ffmpeg
  * imagemagick 
# Installation

1. Download the the file [theTrappedKnight.py](./theTrappedKnight.py) from this repository
2. Copy it into your working directory. 
3. Done

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
  # -> "Knight path of shape (1,2) , Length = 2016 , xDiam = 55 , yDiam = 56 , Density = 0.65455"
   
  # Define a new pathAnimation Class passing a knightPathFinder instance to it
  myPathAnimation=pathAnimation(myKnightPathFinder)
  
  # Animate the Path
  myPathAnimation.animate(outputType="animgif", color="white", speed=100, outDir="out", type="scatter")
  ```
* We are done! 
* The result is <img src="./samples/knightPath-1-2.anim.gif" alt="Animated Gif for 1-2 Knight" width="400" height="400">

## References
  * The problem will be explaiend in detail at [Numberphile](https://www.youtube.com/watch?v=RGQe8waGJ4w)
  * On [OEIS](https://oeis.org/A323472) the length is computed for a large quantity of x,y-knights (aka x,y-leapers) 

