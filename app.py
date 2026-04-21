from flask import Flask, request, redirect, url_for, render_template, session
import database 

app = Flask(__name__)
app.secret_key = "oidjwoiqj./uqj0q9/871d23hqd45f6"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=["POST", "GET"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    else:
        login = request.form["login"]
        pass1 = request.form["pass1"]
        pass2 = request.form["pass2"]
        errors = []


        if database.check_user_exists(login):
            errors.append("Такой пользователь уже существует")

        if pass1 != pass2:
            errors.append("Пароли не совпадают")
        

        if len(pass1) < 8:
            errors.append("Длина пароля должна быть больше 8 символов")
        

        if len(errors) == 0:
            database.add_user(login, pass1)
            return render_template("success_register.html")
        else:
            return render_template("register.html", errors=errors)
        
@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    else:
        login = request.form["login"]
        password = request.form["password"]
        user_id = database.auth_user(login, password)

        if user_id >= 0:
            print("Успешный вход")
            session["user_id"] = user_id
            session["login"] = login
            return redirect(url_for("main_page"))
        else:
            print("Что-то не так")
            return render_template("login.html", errors=["Неверный логин или пароль"])

@app.route("/admin")
def admin_page():
    users = database.get_users()

    return render_template("admin.html", users=users)

@app.route('/main_page')
def main_page():
    return render_template('main_page.html')
        
if __name__ == '__main__':
    app.run(debug=True)