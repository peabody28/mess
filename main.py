from flask import Flask, render_template, url_for, request, redirect, json, session, escape
from flask_socketio import SocketIO, emit
import pymysql
import time
import cryptography
import json


app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/signup", methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route("/search_pair",  methods=['POST'])
def search_pair():
    username = request.form.get('username')
    email = request.form.get('email')
    answer = []

    connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM users WHERE name=%s"
            pair_name = cursor.execute(sql, username)
            answer.append(pair_name)

            sql = "SELECT email FROM users WHERE email=%s"
            pair_email = cursor.execute(sql, email)
            answer.append(pair_email)

    finally:
        connection.close()

    if (not answer[0]) and (not answer[1]):
        return json.dumps({"status": "OK"})
    elif answer[0]:
        return json.dumps({"status": "error", "message": "Имя занято"})
    else:
        return json.dumps({"status": "error", "message": "E-mail занят"})


@app.route("/add_user", methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    passwd = request.form.get('password')

    connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (id, name, email, passwd) VALUES (NULL, %s, %s, %s)"
            cursor.execute(sql, (username, email, passwd))
            connection.commit()
    finally:
        connection.close()

    session["username"] = username.lower()
    session["email"] = email
    session["password"] = passwd

    f = open("logs.txt", "a")
    text = "NEW_USER: " + session['username'] + "   "
    f.write(text + (50 - len(text)) * " " + time.ctime()[4:] + "\n")
    f.close()
    print(session)
    return json.dumps({"status": "OK"})


@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')


@app.route("/check", methods=['POST'])
def check():

    username = request.form.get('username')
    password = request.form.get('password')

    connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT email FROM users WHERE name=%s AND passwd=%s"
            answer = cursor.execute(sql, (username, password))
            email = cursor.fetchone()
    finally:
        connection.close()
    if answer:
        session["username"] = username.lower()
        session["password"] = password
        session["email"] = email
        session.modified = True

        f = open("logs.txt", "a")
        text = username + " LOGIN "
        f.write(text + (50 - len(text)) * " " + time.ctime()[4:] + "\n")
        f.close()
        print(session)
        return json.dumps({"status": "OK"})
    else:
        return json.dumps({"status": "error", "message": "Неверный логин или пороль"})


@app.route("/exit", methods=['GET'])
def exit():
    session.pop("username", None)
    return redirect(url_for('login'))


def get_mes():
    mes = []
    connection = pymysql.connect("127.0.0.1", "root", "1234", "messages")
    try:
        with connection:
            cursor = connection.cursor()
            sql = "SELECT id FROM message"
            id = cursor.execute(sql)

            for i in range(id):
                sql = "SELECT message FROM message WHERE id=%s"
                cursor.execute(sql, i + 1)
                message = cursor.fetchone()

                sql = "SELECT tag FROM message WHERE id=%s"
                cursor.execute(sql, i + 1)
                tag = cursor.fetchone()

                sql = "SELECT time FROM message WHERE id=%s"
                cursor.execute(sql, i + 1)
                time = cursor.fetchone()

                mes.append({"name": tag[0],
                            "mes": message[0],
                            "time": time[0]})
    finally:
        connection.close()

    return mes


@app.route("/")
def main():

    if "username" in session:
        return render_template("messenger.html", messages=get_mes())
    return redirect(url_for('login'))


@app.route("/messenger")
def messenger():

    if "username" in session:
        return render_template('messenger.html', messages=get_mes())
    return redirect(url_for('login'))


@app.route("/userpage")
def user_page():

    if "username" in session:
        connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
        try:
            with connection.cursor() as cursor:

                sql = "SELECT email FROM users WHERE name=%s"
                cursor.execute(sql, session["username"])
                email = cursor.fetchone()

                sql = "SELECT passwd FROM users WHERE name=%s"
                cursor.execute(sql, session["username"])
                passwd = cursor.fetchone()

        finally:
            connection.close()

        return render_template("user_page.html", password=passwd[0], email=email[0], username=session["username"])
    return redirect(url_for('login'))


@app.route("/change_name")
def change_name():
    print(session)
    return render_template("change_name.html")


@app.route("/change_email")
def change_email():
    print(session)
    return render_template("change_email.html")


@app.route("/change_pass")
def change_pass():
    print(session)
    return render_template("change_pass.html")


@app.route("/dlt")
def dlt_user():

    if "username" in session:
        connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM users WHERE name=%s"
                cursor.execute(sql, session["username"])
                connection.commit()
        finally:
            connection.close()
        f = open("logs.txt", "a")
        text = session["username"] + " DELETED "
        f.write(text + (50 - len(text)) * " " + time.ctime()[4:] + "\n")
        f.close()
        session.pop("username", None)
    return redirect(url_for('login'))


@socketio.on('add_mess')
def value_changed(m):
    mes = {"mes": m['data'][5:], "name": session['username'], "time": time.ctime()[10:16]}
    connection = pymysql.connect("127.0.0.1", "root", "1234", "messages")
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO message (id, tag, message, time) VALUES (NULL, %s, %s, %s)"
            cursor.execute(sql, (mes['name'], mes['mes'], mes['time']))
            connection.commit()

    finally:
        connection.close()
    emit('update', mes, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
# IT'S NOT A BUG IT'S A FEATURE
