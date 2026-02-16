from flask import Flask, render_template, request,redirect,session
# NEW!!!!!!!
from flask_session import Session 
# END OF NEW!!!!!!!
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
# NEW!!!!!!!
web_site = Flask(__name__)
# Session Configuration 
web_site.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
web_site.config["SESSION_TYPE"] = "filesystem"     # Store session data in files
web_site.secret_key = "Super secret key"
# END OF NEW!!!!!!!
@web_site.route('/', methods=['GET','POST'])
def home():
    msg = ""
    if request.args.get('msg') == "not_logged_in": #this is set when user has tried to open a page when not logged in
        msg = "You must be logged in"
    if request.method == "POST":
        # user has attempted to login
        name = request.form["name"];
        password = request.form["password"];
        # get user record from db
        con = sqlite3.connect('sudoku.db')
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        sql = 'SELECT * FROM users WHERE username = ? and password = ?'
        cursor.execute(sql, (name, password)) 
        con.commit()        
        rows = cursor.fetchall() 
        if len(rows)==1:
        # if name == "laura" and password == "cake": #TODO look these up from the db
            session["name"] = name #set users name in the session
            session["user_id"] = rows[0]["user_id"] #set user_id in the session
            return redirect('mypuzzles')
        elif name == "" or password == "":
            msg = "Please fill in both fields to login"
        else:
            msg = "Could not login"
    return render_template("home.html", msg = msg, session = session)


#add puzzle
#@web_site.route('/puzzleadd',methods = ['GET', 'POST'])
@web_site.route('/startpuzzle/<difficulty>') 
def puzzleadd(difficulty):
    api_url = 'https://api.api-ninjas.com/v1/sudokugenerate?difficulty=' + difficulty
    response = requests.get(api_url, headers={'X-Api-Key':my_secret }, verify=False)
    if response.status_code == requests.codes.ok:
        data = response.json()         # Parse JSON
        puzzle = data['puzzle']        # Get the "puzzle" 
        solution = data['solution']    # Get the solution      
    else:
        print("Error:", response.status_code, response.text)
    
    # attempt to connect to the db
    con = sqlite3.connect('sudoku.db')
    # NEW added attempt_json
    sql = "INSERT INTO puzzles(puzzle_json, solution_json, difficulty, isFinished, user_id,attempt_json) VALUES(?,?,?,?,?,?)"
    cursor = con.cursor()
    # Convert to JSON strings
    puzzle_json_string = json.dumps(puzzle)
    solution_json_string = json.dumps(solution)
   
    #user_id = 1 #CHANGE THIS!!
    user_id = session["user_id"]
    cursor.execute(sql,(puzzle_json_string, solution_json_string, difficulty, 0,user_id, puzzle_json_string))
    con.commit()
    # Get the ID of the last inserted record
    last_id = cursor.lastrowid
    print(f"Inserted puzzle with ID: {last_id}")
    con.close()   # Close the connection
    # redirect to web page /do_puzzle/puzzle_id
    return redirect(f'/do_puzzle/{last_id}')

@web_site.route('/do_puzzle/<puzzle_id>')
def get_puzzle(puzzle_id):
   # user_id = 1 # change this when users can login!
    user_id = session["user_id"]
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
        attempt = json.loads(row["attempt_json"])
    con.close()   # Close the connection
    num_hints = get_num_hints(puzzle_id, user_id) # gets number of hints used for this puzzle
    return render_template("suduko.html",puzzle_id = puzzle_id, puzzle = puzzle, solution = solution, num_hints = num_hints, attempt = attempt , session = session) 


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
    # Takes the puzzle data submitted from the browser in the POST
    # from the javascript function save_puzzle(puzzle_id)
    data = request.get_json();
    puzzle_list = data['puzzle'] # Access the puzzle data directly

    # Convert the puzzle data to a string for the database
    json_string = json.dumps(puzzle_list)

    # Update the attempt_json in the puzzle record
    con = sqlite3.connect('sudoku.db')
    cursor = con.cursor()
    sql = "UPDATE puzzles SET attempt_json = ? WHERE puzzle_id = ?"
    cursor.execute(sql, (json_string, puzzle_id))
    con.commit()
    con.close()

    return "OK" # just return a simple string

@web_site.route('/puzzle_finished/<int:puzzle_id>/<int:user_id>')
def puzzle_finished(puzzle_id, user_id):
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
        if row["difficulty"]=="easy":
            score = 10
        if row["difficulty"]=="medium":
            score = 20
        if row["difficulty"]=="hard":
            score = 30
    num_hints = get_num_hints(puzzle_id, user_id)
    score = score - num_hints # subtract the number of hints used from the difficulty score to get the final score for the puzzle
    con.close()
    # update the puzzles table to store the score

    con = sqlite3.connect('sudoku.db')
    cursor = con.cursor()
    sql = "UPDATE puzzles SET isFinished = 1, score = ? WHERE puzzle_id = ?"
    cursor.execute(sql, (score, puzzle_id,))
    con.commit()
    con.close()
    ## TODO SHOULD ALSO SAVE THE USERS GO AS WELL AS SET IS FINISHED!
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

#======= MY PUZZLES ===========

@web_site.route('/mypuzzles')
def my_puzzles():
    print(session["name"]) #NEW print session name
    print(session) #NEW print session array
    if session["name"]==None:
        #not logged in so redirect
        return redirect('/?msg=not_logged_in')

    #user_id = 1 # remember to change this!
    user_id = session["user_id"]
    con = sqlite3.connect('sudoku.db')
    con.row_factory = sqlite3.Row #should get row as an associative array - so you can use table field names rather than array indexes
    cursor = con.cursor()
    sql = '''
            SELECT (SELECT COUNT(hint_id) FROM hints WHERE hints.puzzle_id = puzzles.puzzle_id and user_id = ?) AS num_hints,* FROM puzzles WHERE user_id = ?
            '''
    cursor.execute(sql, (user_id,user_id)) 
    con.commit()
    
    puzzles = cursor.fetchall()
    # attempt at doing scores....?
    scores = []
    for puzz in puzzles:
        if puzz["difficulty"]=="easy":
            score = 10
        if puzz["difficulty"]=="medium":
            score = 15
        if puzz["difficulty"]=="hard":
            score = 20
        if puzz["isFinished"] == 0:
            score = 0
        # then think about how to take off number of hints
        scores.append(score)
    con.close()   # Close the connection
    return render_template("my_puzzles.html", puzzles = puzzles, scores = scores, session = session)

#NEW!!!!!!
@web_site.route("/logout")
def logout():
    # Clear the username from session
    session["name"] = None
    session["user_id"] = None
    return redirect("/")

#NEW!!!!!!!!!!!!!!
@web_site.route("/register",methods=['GET','POST'])
def register():
    msg = ""
    if request.method == "POST":
        # user has attempted to register
        name = request.form["name"];
        password = request.form["password"];
        password2 = request.form["password2"];
        ###### validation to go here!
        if password != password2:
            msg = "The passwords don't match"
        # ADD OTHER VALIDATION HERE
        else: 
            # all validation is good so save user record in db
            con = sqlite3.connect('sudoku.db')
            cursor = con.cursor()
            sql = 'INSERT INTO users (username,password) VALUES (?,?)'
            cursor.execute(sql, (name, password)) 
            con.commit()
            print("user ",name," added to db")        
            session["name"] = name #set users name in the session
            # Get the ID of the last inserted record
            session["user_id"]  = cursor.lastrowid
            return redirect('mypuzzles')

    return render_template("register.html",msg=msg)

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