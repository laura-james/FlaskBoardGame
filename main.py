from flask import Flask, render_template, request,redirect
import sqlite3 # to connect to the database
# you shouldn't store api keys in plain site so I have created a secret key in replit and called it here
import os
my_secret = os.environ['APININJA']


import requests #used to get the suduko puzzle from the api
import certifi
import os
import urllib3
# Disable the SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

web_site = Flask(__name__)


@web_site.route('/')
def get_suduko():
    api_url = 'https://api.api-ninjas.com/v1/sudokugenerate?difficulty=medium'
    response = requests.get(api_url, headers={'X-Api-Key':my_secret }, verify=False)
    if response.status_code == requests.codes.ok:
        data = response.json()         # Parse JSON
        puzzle = data['puzzle']        # Get just the "puzzle" key
        solution = data['solution']        # Get the solution not using yet
                
    else:
        print("Error:", response.status_code, response.text)
    
    # attempt to get something from the db

    con = sqlite3.connect('sudoku.db')
    cursor = con.cursor()
    sql = '''
            SELECT * FROM users 
            '''
    cursor.execute(sql)
    con.commit()
    
    rows = cursor.fetchall() 
    for row in rows:
        print(row)
    con.close()   # Close the connection
    return render_template("suduko.html",puzzle = puzzle, users = rows, solution=solution) #added users = rows to end to pass in the rows from users table

#@web_site.route('/hint')

#add puzzle
@web_site.route('/puzzleadd',methods = ['GET', 'POST'])
def puzzleadd():
  #  api_url = 'https://api.api-ninjas.com/v1/sudokugenerate?difficulty=medium'
  # response = requests.get(api_url, headers={'X-Api-Key':my_secret })
  #  if response.status_code == requests.codes.ok:
  #      data = response.json()         # Parse JSON
   #     puzzle = data['puzzle']        # Get just the "puzzle" key
  #      solution = data['solution']        # Get the solution not using yet      
   # else:
  #      print("Error:", response.status_code, response.text)
    
    # attempt to connect to the db
    con = sqlite3.connect('sudoku.db')
    sql = "INSERT INTO puzzles(puzzle_json,solution_json,difficulty, isFinished) VALUES(?,?,?,?)"
    cursor = con.cursor()
    puzzle_json = "test puzzle json"
    solution_json = "test solution json"
    difficulty = "easy"
    cursor.execute(sql,(puzzle_json, solution_json, difficulty, 0))
    con.commit()
    con.close()   # Close the connection
    print(" added to the puzzle table")
    return "puzzle added"

@web_site.route('/tictactoe')
def tictactoe():
  return render_template("tictactoe.html")






web_site.run(host='0.0.0.0', port=8080)