from flask import Flask, render_template, request,redirect
import os
my_secret = os.environ['APININJA']
import requests

web_site = Flask(__name__)


@web_site.route('/')
def get_suduko():
    api_url = 'https://api.api-ninjas.com/v1/sudokugenerate?difficulty=easy'
    response = requests.get(api_url, headers={'X-Api-Key':my_secret })
    if response.status_code == requests.codes.ok:
        data = response.json()         # Parse JSON
        puzzle = data['puzzle']        # Get just the "puzzle" key
                
    else:
        print("Error:", response.status_code, response.text)
    #return puzzle
    return render_template("suduko.html",puzzle=puzzle)

@web_site.route('/tictactoe')
def tictactoe():
  return render_template("tictactoe.html")






web_site.run(host='0.0.0.0', port=8080)