from flask import Flask, render_template, session, redirect, url_for,request
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
undo_row=0
undo_col=0
@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["move"]=1
        session["row"]=None
        session["col"]=None

    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    for i in range(3):
        if session["board"] and session["move"]>4:

            if session["board"][i][0]  and session["board"][i][0]==session["board"][i][1] and session["board"][i][1]==session["board"][i][2]:
               return render_template("game.html", game=session["board"],move=session["move"],winner=session["board"][i][0],won="won")
            if session["board"][0][i] and  session["board"][0][i]==session["board"][1][i] and session["board"][1][i]==session["board"][2][i]:
               return render_template("game.html", game=session["board"],move=session["move"],winner=session["board"][0][i],won="won")
            if (session["board"][0][0] ) and session["board"][0][0]==session["board"][1][1] and session["board"][1][1]==session["board"][2][2]:
                return render_template("game.html", game=session["board"],move=session["move"],winner=session["board"][0][0],won="won")
        if session["board"][2][0] and (session["board"][2][0]==session["board"][1][1]) and (session["board"][1][1]==session["board"][0][2]):
            return render_template("game.html", game=session["board"],move=session["move"],winner=session["board"][2][0],won="won")
    if session["turn"]=="X":
        session["board"][row][col]=session["turn"]
        session["turn"]="0"
        session["move"]=session["move"]+1
    else:
        session["board"][row][col]=session["turn"]
        session["turn"]="X"
        session["move"]=session["move"]+1
    session["row"]=row
    session["col"]=col
    return render_template("game.html", game=session["board"], turn=session["turn"],move=session["move"])
@app.route("/undo")
def undo():
    if session["move"]==1:
        return render_template("game.html", game=session["board"], turn=session["turn"],move=session["move"],display="Nothing to UNDO !")

    undo_row=session["row"]
    undo_col=session["col"]
    if session["turn"]=="X":
        session["board"][undo_row][undo_col]=None
        session["turn"]="X"
        session["move"]=session["move"]-1
        return render_template("game.html", game=session["board"], turn=session["turn"],move=session["move"],undo_row=undo_row,undo_col=undo_col)

    else:
        session["board"][undo_row][undo_col]=None
        session["turn"]="0"
        session["move"]=session["move"]-1
        return render_template("game.html", game=session["board"], turn=session["turn"],move=session["move"],undo_row=undo_row,undo_col=undo_col)
@app.route('/reset')
def reset():
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    return render_template("game.html", game=session["board"], turn=session["turn"],move=session["move"],undo_row=undo_row,undo_col=undo_col)
