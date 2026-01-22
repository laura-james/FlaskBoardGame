## Suduko Puzzles

A database driven Sudoku platform using Python (Flask) and Javascript.

Can be found online here on render.com [https://flaskboardgame.onrender.com/]

21/1/2026
* BIG CHANGE - Add a new field into the db for each puzzle (called `attempt_json`) That should be the field that gets updated when the user saves. When the puzzle is loaded it should use puzzle_json as normal to decide if the boxes are editable not editable but use the `attempt_json` to read in the values. This will allow users to change what they have added. DONE
* Update hint number using jscript when you accept a hint? (Low priority as the page works when refreshed) DONE
* Check if the puzzle has been completed - and set isFinished to True (or 1) I guess after each character entered it should run a program to check if the game array is the same as the solution array. If it is it should set setFinished to True and show a message to the user DONE
* Create a scoreboard or scoring system for The user based on completed puzzles and number of hints 
* Cant remember what your algorithm was but something like
    * Easy puzzle = 10 point minus hints
    * Med puzzle = 20 point minus hints etc etc
    * write the SQL select statement to get that out of the db tables
* Create a login form and a register form 
* Look into sessions in order to remember the user ID between different pages (slide 27-31 here)

