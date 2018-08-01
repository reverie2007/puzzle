# puzzle game
python3 practice using pygame.

<br>
1. How to create new puzzle?
    First fill grid using random number, then check if the grid is solvable.<br>
    Formula to check solvable:<br>
    a. if the grid width is odd, the number of inversions must be even.
    b. if the grid width is even, the blank row from bottom is odd, the number of inversions must be even.
                                  the blank row from bottom is even,the number of inversions must be odd.
    if the grid is insolvable, just swap two tile to get a solvable grid.

