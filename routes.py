from app import app
from flask import request,render_template, redirect
from user import user_service
from messages import message_service


@app.route('/', methods=["GET", "POST"])
def main():
    messages = message_service.get_all_messages()
    if request.method == "POST":
        return redirect("/result")
    if request.method == "GET":
        return render_template("index.html", messages=messages)

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user_service.login(username, password):
            return redirect("/")
        return render_template("login.html")

#A2:2017-Broken Authentication
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if not user_service.register_user(username, password, email):
            return render_template("register.html")
        user_service.register_user(username, password, email)
        return redirect("/")

@app.route("/result", methods=["POST"])
def result():
    message = request.form["text"]
    message_service.create_message(message)
    return redirect("/")

# A7:2017-Cross-Site Scripting (XSS)
# A3:2017-Sensitive Data Exposure
@app.route("/logout/<int:user_id>", methods=["GET", "POST"])
def logout_page(user_id):
    username = user_service.get_current_username(user_id)
    email = user_service.get_current_email(user_id)
    template = f'''<!DOCTYPE html>
                    <head>
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
                    <title>Website</title>
                    <a href="/"></a>
                    <a href="/login"></a>
                    <a href="/profile"></a>
                    <a href="/result"></a>
                    <link href="../static/index.css" rel="stylesheet">
                    </head>
                    <body>
                        <nav class="navbar navbar-dark bg-dark">
                            <div class="navbar-content" align="left">
                                <a class="navbar-brand" href="/">Homepage</a>
                                <a class="navbar-brand" href="/profile">Profile</a>
                                </div>
                            </nav>
                        <p></p>
                        <h3>Hi <b>{username} with email {email}</b>!</h3>

                        It is sad to see you leaving...
                        log out by clicking <a href="/logout">this!</a>
                    </body>
                    '''
    return template

@app.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = user_service.get_user_id()
    email = user_service.get_current_email(user_id)
    return render_template("profile.html", user_id=user_id, email=email)

# A1:2017-Injection
# A5:2017-Broken Access Control
@app.route("/profile/modify-email", methods=["GET", "POST"])
def modify_email():
    user_id = user_service.get_user_id()
    new_email = request.form["new_email"]
    sql = "UPDATE Users SET email='" + new_email + "' WHERE id=" + str(user_id)
    user_service.modify_user_email(sql)
    return redirect('/profile')

@app.route("/logout", methods=["GET","POST"])
def logout():
    user_service.logout()
    return redirect("/")
