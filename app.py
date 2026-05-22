from flask import Flask, request, redirect, url_for, render_template, session
import database 
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "oidjwoiqj./uqj0q9/871d23hqd45f6"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/admin")
def admin_page():
    users = database.get_users()

    return render_template("admin.html", users=users)

@app.route('/main_page')
def main_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    books_db = database.get_books(session["user_id"])
    login = session["login"]
    return render_template("main_page.html", username=login, books=books_db)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    if request.method == "GET":
        return render_template("add_book.html")

    title = request.form['book-title']
    author = request.form['book-author']
    image = request.files.get('image')

    image_path = "nobook.png"
    
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = filename
        
    database.add_book(title, author, session["user_id"], image_path)
    return redirect(url_for("main_page"))

@app.route("/delete_book", methods=["POST"])
def delete_book():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    book_id = int(request.form["book-id"])
    database.delete_book(book_id, session["user_id"])
    return redirect(url_for("main_page"))

@app.route("/change_book_status", methods=["POST"])
def change_book_status():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    book_id = int(request.form["book-id"])
    new_status = int(request.form["book-status"]) 
    
    database.change_book_status(book_id, session["user_id"], new_status)
    return redirect(url_for("main_page"))

@app.route("/update_book_mark", methods=["POST"])
def change_book_mark():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    book_id = int(request.form["book-id"])
    new_mark = int(request.form["book-mark"])
    
    if 1 <= new_mark <= 10:
        database.change_book_mark(book_id, session["user_id"], new_mark)
    
    return redirect(url_for("main_page"))
        
if __name__ == '__main__':
    app.run(debug=True)