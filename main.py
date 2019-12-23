from flask import Flask, render_template, url_for, request, redirect, json, session, escape
from flask_socketio import SocketIO, emit
import pymysql
import time
import cryptography


app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/signup", methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route("/search_pair",  methods=['POST'])
def search_pair(username=None, email=None):
    if not username:
        username = request.form.get('username')
        email = request.form.get('email')
    answer = []

    connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
    try:
        with connection.cursor() as cursor:

            sql = "SELECT name FROM users WHERE name=%s"
            pair_name = cursor.execute(sql, username)
            answer.append(pair_name)

            if not email:
                answer.append(0)
            else:
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
    f = open("logs.txt", "a")
    text = "NEW_USER: " + username.lower() + "   "
    f.write(text + (50 - len(text)) * " " + time.ctime()[4:] + "\n")
    f.close()
    return json.dumps({"status": "OK"})


@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')


@app.route("/exit", methods=['GET'])
def exit():
    session.pop("username", None)
    return redirect(url_for('login'))


@app.route("/check", methods=['POST'])
def check():

    username = request.form.get('username')
    password = request.form.get('password')

    connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE name=%s AND passwd=%s"
            answer = cursor.execute(sql, (username, password))
    finally:
        connection.close()

    if answer:
        session["username"] = username.lower()
        f = open("logs.txt", "a")
        text = username + " LOGIN "
        f.write(text + (50 - len(text)) * " " + time.ctime()[4:] + "\n")
        f.close()
        return json.dumps({"status": "OK"})
    else:
        return json.dumps({"status": "error", "message": "Неверный логин или пороль"})


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


@app.route("/change_name")
def change_name():

    if "username" in session:
        return render_template('change_name.html')
    return redirect(url_for('login'))


@app.route("/cn", methods=['POST', 'GET'])
def cn():
    new_name = request.form.get("username")
    past_name = session["username"]

    if new_name:
        spa = search_pair(new_name)
        print(spa)
        if spa['status'] == "OK":
            connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
            try:
                with connection.cursor() as cursor:

                    sql = "SELECT email FROM users WHERE name=%s"
                    cursor.execute(sql, past_name)
                    email = cursor.fetchone()

                    sql = "SELECT passwd FROM users WHERE name=%s"
                    cursor.execute(sql, past_name)
                    passwd = cursor.fetchall()

                    sql = "DELETE FROM users WHERE name=%s"
                    cursor.execute(sql, past_name)
                    connection.commit()

                    sql = "INSERT INTO users (id, name, email, passwd) VALUES (NULL, %s, %s, %s)"
                    cursor.execute(sql, (new_name, email[0], passwd[0]))
                    connection.commit()
                    session.pop("username", None)
                    session["username"] = new_name.lower()

            finally:
                connection.close()
            f = open("logs.txt", "a")
            text = past_name + " CHANGED THE NAME TO " + new_name
            f.write(text + (50 - len(text)) * " " + time.ctime()[4:] + "\n")
            f.close()

            mes = {"mes": text, "name": "system", "time": time.ctime()[10:16]}
            connection = pymysql.connect("127.0.0.1", "root", "1234", "messages")
            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO message (id, tag, message, time) VALUES (NULL, %s, %s, %s)"
                    cursor.execute(sql, (mes['name'], mes['mes'], mes['time']))
                    connection.commit()

            finally:
                connection.close()
            
            return json.dumps({"status": "OK", "name": new_name})
        else:
            return json.dumps({"status": "error", "message": "Имя занято"})
    else:
        return json.dumps({"status": "error", "message": "Введи новое имя"})


@app.route("/change_email")
def change_email():

    if "username" in session:
        return render_template('change_email.html')
    return redirect(url_for('login'))


@app.route("/ce", methods=['POST', 'GET'])
def ce():

    new_email = request.form.get('email')
    if new_email:
        spa = search_pair(None, new_email)
        if not (spa[0]):

            connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
            try:
                with connection.cursor() as cursor:

                    sql = "SELECT passwd FROM users WHERE name=%s"
                    cursor.execute(sql, session["username"])
                    passwd = cursor.fetchone()

                    sql = "DELETE FROM users WHERE name=%s"
                    cursor.execute(sql, session["username"])
                    connection.commit()

                    sql = "INSERT INTO users (id, name, email, passwd) VALUES (NULL, %s, %s, %s)"
                    cursor.execute(sql, (session["username"], new_email, passwd[0]))
                    connection.commit()

            finally:
                connection.close()
            return json.dumps({"status": "OK", "eml": new_email})
        else:
            return json.dumps({"status": "error", "message": "E-mail занят"})
    else:
        return json.dumps({"status": "error", "message": "E-mail не введен"})


@app.route("/change_pass")
def change_pass():

    if "username" in session:
        return render_template('change_pass.html')
    return redirect(url_for('login'))


@app.route("/cp", methods=['POST', 'GET'])
def cp():

    new_passwd = request.form['password']
    if new_passwd:
        connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
        try:
            with connection.cursor() as cursor:

                sql = "SELECT email FROM users WHERE name=%s"
                cursor.execute(sql, session["username"])
                email = cursor.fetchone()

                sql = "DELETE FROM users WHERE name=%s"
                cursor.execute(sql, session["username"])
                connection.commit()

                sql = "INSERT INTO users (id, name, email, passwd) VALUES (NULL, %s, %s, %s)"
                cursor.execute(sql, (session["username"], email[0], new_passwd))
                connection.commit()

        finally:
            connection.close()
        return json.dumps({"status": "OK", 'pass': new_passwd})
    else:
        return json.dumps({"status": "error", 'message': "Введи пароль"})


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
