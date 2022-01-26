from flask import Flask, g, render_template, request
app = Flask(__name__)

import sqlite3

def get_message_db():
    g.message_db = sqlite3.connect("messages_db.sqlite")
    cursor = g.message_db.cursor()
    
    # create messages table
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER, handle TEXT, message TEXT)")

    return g.message_db


def insert_message(request):
    message = request.form["message"]
    handle = request.form["handle"]

    g.message_db = sqlite3.connect("messages_db.sqlite")
    cursor = g.message_db.cursor()

    # count number of rows in table
    cursor.execute("SELECT COUNT(*) FROM messages")
    rows = cursor.fetchall()

    # insert message into table 
    cursor.execute("INSERT INTO messages(id, handle, message) VALUES (1 + rows, message, handle)")
    
    g.message_db.commit()
    g.message_db.close()

    return message, handle

@app.route('/', methods = ['POST', 'GET'])
def submit():
    if request.method == "GET":
        return render_template('submit.html')

    else:
        insert_message(request)
        return render_template('submit-basic.html', thanks = True)