# puzzle game
python3 practice using pygame.
<hr>
1. How to create new puzzle?<br>
    First fill grid using random number, then check if the grid is solvable.<br><br>
    Formula to check solvable:<br>
    a. if the grid width is odd, the number of inversions must be even.<br>
    b. if the grid width is even, the blank row from bottom is odd, the number of inversions must be even,
                                  the blank row from bottom is even,the number of inversions must be odd.<br><br>
    if the grid is insolvable, just swap two tile to get a solvable grid.
<hr>
