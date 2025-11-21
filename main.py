from flask import Flask, render_template, request,redirect
import sqlite3 # to connect to the database
# you shouldn't store api keys in plain site so I have created a secret key in replit and called it here
import os
my_secret = os.environ['APININJA']


import requests #used to get the suduko puzzle from the api


web_site = Flask(__name__)


@web_site.route('/')
def get_suduko():
    api_url = 'https://api.api-ninjas.com/v1/sudokugenerate?difficulty=medium'
    response = requests.get(api_url, headers={'X-Api-Key':my_secret })
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

    return render_template("suduko.html",puzzle = puzzle, users = rows) #added users = rows to end to pass in the rows from users table



@web_site.route('/tictactoe')
def tictactoe():
  return render_template("tictactoe.html")






web_site.run(host='0.0.0.0', port=8080)