from flask import Flask, render_template, request,redirect




web_site = Flask(__name__)


@web_site.route('/')

def tictactoe():

  return render_template("tictactoe.html")






web_site.run(host='0.0.0.0', port=8080)