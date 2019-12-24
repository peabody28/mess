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
    password = request.form.get('password')

    connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (id, name, email, passwd) VALUES (NULL, %s, %s, %s)"
            cursor.execute(sql, (username, email, password))
            connection.commit()
    finally:
        connection.close()

    session["username"] = username.lower()
    session["email"] = email
    session["password"] = password

    f = open("logs.txt", "a")
    text = "NEW_USER: " + session['username'] + "   "
    f.write(text + (50 - len(text)) * " " + time.ctime()[4:] + "\n")
    f.close()
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
        session["email"] = email[0]
        session.modified = True

        f = open("logs.txt", "a")
        text = username + " LOGIN "
        f.write(text + (50 - len(text)) * " " + time.ctime()[4:] + "\n")
        f.close()
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
                sql = "SELECT * FROM message WHERE id=%s"
                cursor.execute(sql, i + 1)
                answer = cursor.fetchall()[0]

                mes.append({"name": answer[2],
                            "mes":  answer[1],
                            "time": answer[3]})
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
        return render_template("user_page.html", session=session)
    return redirect(url_for('login'))


@app.route("/change_name", methods=['GET'])
def change_name():
    return render_template("change_name.html")


@app.route("/cn", methods=['POST'])
def cn():
    new_name = request.form.get("username")
    if new_name:
        connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
        try:
            with connection.cursor() as cursor:
                sql = "SELECT email FROM users WHERE name=%s"
                answer = cursor.execute(sql, new_name)

                if answer:
                    return json.dumps({"status": "error", "message": "Имя занято"})
                else:
                    sql = "UPDATE users SET name=%s WHERE email=%s"
                    cursor.execute(sql, (new_name, session['email']))
                    connection.commit()

                    session["username"] = new_name
                    session.modified = True
                    return json.dumps({"status": "OK"})
        finally:
            connection.close()
    else:
        return json.dumps({"status": "error", "message": "Заполните поле"})


@app.route("/change_email")
def change_email():
    return render_template("change_email.html")


@app.route("/ce", methods=['POST'])
def ce():
    new_email = request.form.get("email")
    if new_email:
        connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
        try:
            with connection.cursor() as cursor:
                sql = "SELECT name FROM users WHERE email=%s"
                answer = cursor.execute(sql, new_email)

                if answer:
                    return json.dumps({"status": "error", "message": "E-mail занят"})
                else:
                    sql = "UPDATE users SET email=%s WHERE name=%s"
                    cursor.execute(sql, (new_email, session['username']))
                    connection.commit()

                    session["email"] = new_email
                    session.modified = True
                    return json.dumps({"status": "OK"})
        finally:
            connection.close()
    else:
        return json.dumps({"status": "error", "message": "Заполните поле"})


@app.route("/change_pass")
def change_pass():
    return render_template("change_pass.html")


@app.route("/cp", methods=['POST'])
def cp():
    new_pass = request.form.get("password")
    if new_pass and new_pass != session['password']:
        connection = pymysql.connect("127.0.0.1", "root", "1234", "users_list")
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET passwd=%s WHERE name=%s"
                cursor.execute(sql, (new_pass, session['username']))
                connection.commit()

                session["password"] = new_pass
                session.modified = True
                return json.dumps({"status": "OK"})
        finally:
            connection.close()
    elif new_pass == session['password']:
        return json.dumps({"status": "error", "message": "Вы ввели старый пароль"})
    else:
        return json.dumps({"status": "error", "message": "Заполните поле"})


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
