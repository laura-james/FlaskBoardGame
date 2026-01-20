from flask import Flask, render_template, request,redirect
import sqlite3 # to connect to the database
# you shouldn't store api keys in plain site so I have created a secret key and called it here
import os
my_secret = os.environ['APININJA']


import requests # used to get the sudoku puzzle from the api
import os # used to store the api key in the operating system and not in plain site on github!
import urllib3 # used to disable pesky ssl warnings
# Disable the SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json 

web_site = Flask(__name__)

@web_site.route('/')
def home():
    return render_template("home.html")


#add puzzle
#@web_site.route('/puzzleadd',methods = ['GET', 'POST'])
@web_site.route('/startpuzzle/<difficulty>') 
def puzzleadd(difficulty):
    api_url = 'https://api.api-ninjas.com/v1/sudokugenerate?difficulty=' + difficulty
    response = requests.get(api_url, headers={'X-Api-Key':my_secret }, verify=False)
    if response.status_code == requests.codes.ok:
        data = response.json()         # Parse JSON
        puzzle = data['puzzle']        # Get just the "puzzle" key
        solution = data['solution']        # Get the solution not using yet      
    else:
        print("Error:", response.status_code, response.text)
    
    # attempt to connect to the db
    con = sqlite3.connect('sudoku.db')
    sql = "INSERT INTO puzzles(puzzle_json,solution_json,difficulty, isFinished,user_id) VALUES(?,?,?,?,?)"
    cursor = con.cursor()
    # Convert to JSON strings
    puzzle_json_string = json.dumps(puzzle)
    solution_json_string = json.dumps(solution)
   
    user_id = 1
    cursor.execute(sql,(puzzle_json_string, solution_json_string, difficulty, 0,user_id))
    con.commit()
    # Get the ID of the last inserted record
    last_id = cursor.lastrowid
    print(f"Inserted puzzle with ID: {last_id}")
    con.close()   # Close the connection
    # redirect to web page /do_puzzle/puzzle_id
    return redirect(f'/do_puzzle/{last_id}')

@web_site.route('/do_puzzle/<puzzle_id>')
def get_puzzle(puzzle_id):
    user_id = 1 # chnage this when users can login!
    # Get the puzzle stored in the db using its puzzle id
    con = sqlite3.connect('sudoku.db')
    con.row_factory = sqlite3.Row #should get row as an associative array - so you can use table field names rather than array indexes
    cursor = con.cursor()
    sql = '''
            SELECT * FROM puzzles WHERE puzzle_id = ?
            '''
    cursor.execute(sql, (puzzle_id,)) #the trailing comma IS important! It tells  Python  that the brackets are defining a tuple even though its only one item
    con.commit()
    
    rows = cursor.fetchall() 
    for row in rows:
         # FYI Reading JSON back from the database: Use json.loads() to convert the string back to a Python list/dict:
        puzzle = json.loads(row["puzzle_json"])
        solution = json.loads(row["solution_json"])
    con.close()   # Close the connection
    num_hints = get_num_hints(puzzle_id, user_id) # gets number of hints used for this puzzle
    return render_template("suduko.html",puzzle_id = puzzle_id, puzzle = puzzle, solution = solution, num_hints = num_hints) 


#====================== GET HINT ==============================
@web_site.route('/get_hint/<user_id>/<puzzle_id>') #NEW!! swapped the parameters around!
def get_hint(puzzle_id, user_id): # notice how this is taking in two parameters
    # TODO how do we stop them adding multiple hints for the same cell???
    # attempt to connect to the db
    con = sqlite3.connect('sudoku.db')
    sql = "INSERT INTO hints(puzzle_id,user_id) VALUES(?,?)"
    cursor = con.cursor()
    cursor.execute(sql,(puzzle_id,user_id))
    con.commit()
    con.close()   # Close the connection
    # NEW - go and get how many hints there are now and return THAT at the end of this function instead of 'hint gotten'!
    num_hints = get_num_hints(puzzle_id, user_id) # gets number of hints used for this puzzle
    print(f"hint added to the hints table {puzzle_id} {user_id}")
    # return "hint gotten"
    return str(num_hints)

#======= SAVE PUZZLE ==========
@web_site.route('/save_puzzle/<int:puzzle_id>', methods=['POST'])
def save_puzzle(puzzle_id):
# Get the data sent from the browser
    data = request.get_json()
    puzzle_list = data['puzzle'] # Access the list directly

    # Convert the list to a string for the database
    json_string = json.dumps(puzzle_list)

    # Save to database
    con = sqlite3.connect('sudoku.db')
    cursor = con.cursor()
    sql = "UPDATE puzzles SET puzzle_json = ? WHERE puzzle_id = ?"
    cursor.execute(sql, (json_string, puzzle_id))
    con.commit()
    con.close()

    return "OK" # just return a simple string

#======== GET NUM HINTS ========
def get_num_hints(puzzle_id, user_id):
    # Get the number of hints stored in the db using its puzzle id & user id
    con = sqlite3.connect('sudoku.db')
    cursor = con.cursor()
    sql = '''
            SELECT COUNT(hint_id) FROM hints WHERE puzzle_id = ? and user_id = ?
            '''
    cursor.execute(sql, (puzzle_id, user_id)) 
    con.commit()
    
    rows = cursor.fetchall() 
    for row in rows:
        print("Number of hints used for this puzzle:", row[0])
        return row[0]

# Could probably delete this now...

@web_site.route('/tictactoe')
def tictactoe():
  return render_template("tictactoe.html")



#OLD STUFF

# def get_suduko(difficulty):
#     api_url = 'https://api.api-ninjas.com/v1/sudokugenerate?difficulty='+difficulty
#     response = requests.get(api_url, headers={'X-Api-Key':my_secret }, verify=False)
#     if response.status_code == requests.codes.ok:
#         data = response.json()         # Parse JSON
#         puzzle = data['puzzle']        # Get just the "puzzle" key
#         solution = data['solution']    # Get the solution not using yet
#     else:
#         print("Error:", response.status_code, response.text)
    
    # attempt to get something from the db

    # con = sqlite3.connect('sudoku.db')
    # cursor = con.cursor()
    # sql = '''
    #         SELECT * FROM users 
    #         '''
    # cursor.execute(sql)
    # con.commit()
    
    # rows = cursor.fetchall() 
    # for row in rows:
    #     print(row)
    # con.close()   # Close the connection
  #  return render_template("suduko.html",puzzle = puzzle, solution = solution) 




web_site.run(host='0.0.0.0', port=8080, debug=True) #added debug=True - much more helpful error messages!!!