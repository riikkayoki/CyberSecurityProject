# CyberSecurityProject

This is a repository for MOOC's [Cyber Security Base Project 1](https://cybersecuritybase.mooc.fi/module-3.1)


##### Disclaimer:
This application is vulnerable and should not be reused.

## Installation
### Requirements
* python3
* pip3
* Postgresql (Instructions: https://github.com/hy-tsoha/local-pg & https://www.postgresql.org/download/)

### Install
* pip install -r requirements.txt
* create .env file:
    DATABASE_URL=postgresql:///[your username]
    SECRET_KEY=[your secret key]
### Usage
* To start the program enter flask run on terminal in the project file.

## Vulnerabilities in the application

This web application contains five different [OWASP Top Ten 2017](https://owasp.org/www-project-top-ten/) vulnerabilities.

### 1. A1:2017-Injection

Here is the source for the flaw: https://github.com/riikkayoki/CyberSecurityProject/blob/d5915bd02fb48babbca7d2060a12450179c91b1c/routes.py#L82

SQL injection is a data security problem that arises from inserting user input into an SQL command by concatenating strings.

The code in my project allows SQL injection because the input given by the user is directly inserted into the SQL command and the user can use this to change the structure of the SQL command.

#### How to fix the bug

To prevent SQL injection is to combine inputs with SQL commands using parameters. We can remove the SQL injection from the code above by changing the code like this:

user_id = session["user_id"]
email = request.form["email"]
sql = "UPDATE Users SET email=:email WHERE id=:user_id"
db.session.execute(sql, {"email":email, "user_id":user_id})

Ideally this could would also be moved to its own function in user.py file. 

### 2. A2:2017-Broken Authentication

Here is the source for the flaw: https://github.com/riikkayoki/CyberSecurityProject/blob/d5915bd02fb48babbca7d2060a12450179c91b1c/routes.py#L27


When an application has broken authentication, attackers can exploit authentication details by using automated tools with password lists and dictionary attacks. So in other words, this flaw allows attackers to hack user's profile a lot easier. This

At the moment, this web application does not require users for strong passwords or repeat the password again while registering.

#### How to fix the bug:

The issue can be implemented by implementing weak-password checks and requiring users to enter a secure password while registering. Also, user could be required to have passwords with certain lengths and characters, with big and low cases. There could also be implemented a list that has top 1000 easiest passwords, for example password1 which would be prohibited for users.

So for example we could add something like this to the code:

if len(password1) < 8:
    print("Password is too short. Try again!")
    return render_template("register.html")
if password1 != password2:
    print("Passwords do not match. Try again!")
    return render_template("register.html")

### 3. A3:2017-Sensitive Data Exposure

Here is the source for the flaw: https://github.com/riikkayoki/CyberSecurityProject/blob/d5915bd02fb48babbca7d2060a12450179c91b1c/routes.py#L48

Sensitive data exposure means that there is some sensitive data accessible for an attacker. Sensitive data is any information that is meant to be protected from unauthorized access so for example anything from emails to banking information.

In my project, an attacker can access to user's logout page when entering for example http://127.0.0.1:5000/logout/1
By doing this, an attacker can see user's username and link it to the user id which makes it easier for them to hack the profiles. Also, at the moment the attacker may see user's email address, which is quite a sensitive information. 

#### How to fix the bug:

1. Change the lines 49-51 to this:
@app.route("/logout", methods=["GET", "POST"])
def logout_page():
    user_id = user_service.get_user_id()
    username = user_service.get_current_username(user_id)

2. Remove {{session.user_id}} from layout.html in the logout links

### 4. A5:2017-Broken Access Control (CSRF)

Here is the source for the flaw: https://github.com/riikkayoki/CyberSecurityProject/blob/d5915bd02fb48babbca7d2060a12450179c91b1c/routes.py#L83 & https://github.com/riikkayoki/CyberSecurityProject/blob/d5915bd02fb48babbca7d2060a12450179c91b1c/templates/profile.html#L12

A CSRF vulnerability occurs when a web application does not verify that a page request made by a logged-in user actually comes from the user.

[This](https://github.com/riikkayoki/CyberSecurityProject/blob/d5915bd02fb48babbca7d2060a12450179c91b1c/templates/profile.html#L12) form has a CSRF vulnerability because an attacker could lure a logged-in user to an external page that calls the page send in the background without the user's knowledge. Since the user is logged in in the browser, the message is sent through. Thus, the attacker can change email.

#### How to fix the bug:

1. Add < input type="hidden" name="csrf_token" value="{{ session.csrf_token }}" > to the form.

2. Remove hashtag from file users.py from lines 21 and 76-78.

Overall, check that csrf is checked everything a form is posted in the application.

### 5. A7:2017-Cross-Site Scripting (XSS)

Here is the source for the flaw: https://github.com/riikkayoki/CyberSecurityProject/blob/d5915bd02fb48babbca7d2060a12450179c91b1c/routes.py#L47

The XSS vulnerability is based on the fact that the input provided by the user is combined as such with the HTML code of the page, in which case the user is able to influence the operation of the page in the browser by providing input with HTML code.

For example, user may give username "< h3>LOL< h3/>" in which case the username will be shown in bigger font than originally.

#### How to fix it

XSS vulnerability can be prevented by making sure that user input is never displayed on the page as it is. When we use page templates in Flask, this happens automatically.

To do this in my app, you should do the following steps:

1. Create file /templates/logout.html
2. Move the HTML code to the file
3. Replace return line with return render_template("logout.html", username=username)

