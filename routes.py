from app import app
from flask import Flask, request,render_template, redirect, session
from user import User


@app.route('/', methods=['GET', "POST"])
def main():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    return redirect("/")

#A2:2017-Broken Authentication
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if not User.register_user(username, password, email):
            return render_template("register.html")
        User.register_user(username, password, email)
        return redirect("/")
    return render_template("register.html")

# A7:2017-Cross-Site Scripting (XSS)
@app.route("/result", methods=["POST"])
def result():
    text=request.form["text"]

    template = f'''<!DOCTYPE html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
        <title>Website</title>
        <a href="/"></a>
        <a href="/result"></a>
        </head>

        <body>
        <nav class="navbar navbar-dark bg-dark">
            <a class="navbar-brand" href="/">Homepage</a>
        </nav>
            <form action="/result" method="POST">
                Post your message to the world:
                <textarea class="form-control form-group input-sm" style="width: 40%" type="text" name="text"></textarea>
                <input class="btn btn-secondary" type="submit" value="Send">
        </form>
        {text}
        </body>'''
    return template

# A3:2017-Sensitive Data Exposure
@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id):
    user_id = session["user_id"]
    return render_template("profile.html", user_id=user_id)

# A1:2017-Injection
# A5:2017-Broken Access Control
@app.route("/profile/<int:user_id>/modify-email", methods=["GET", "POST"])
def modify_email(user_id):
    new_email = request.form["new_email"]
    sql = "UPDATE Users SET email='" + new_email + "' WHERE id=" + str(user_id)
    User.modify_user_email(sql)
    return redirect('/profile' + str(user_id))

