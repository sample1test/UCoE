import pyrebase
import json
from flask import *
from flask_mail import Mail, Message


############# UTSAV ACCOUNT ################
# config = {
#     "apiKey": "AIzaSyB2R0KsX4nv0R-22hEy-Nwrs6FjL0BNnzw",
#     "authDomain": "test-iaswum.firebaseapp.com",
#     "databaseURL": "https://test-iaswum.firebaseio.com",
#     "projectId": "test-iaswum",
#     "storageBucket": "test-iaswum.appspot.com",
#     "messagingSenderId": "1069995406208",
#     "appId": "1:1069995406208:web:a8ea3bcd31ab9a13874765",
# }

#############   TEST EMAIL ID   ###############
config = {
    "apiKey": "AIzaSyDKM5jToFhKzJOiEyI13T-7uTZhut-fzVk",
    "authDomain": "test-db319.firebaseapp.com",
    "databaseURL": "https://test-db319.firebaseio.com",
    "projectId": "test-db319",
    "storageBucket": "test-db319.appspot.com",
    "messagingSenderId": "878248691705",
    "appId": "1:878248691705:web:feb670fc0bc47710421f28",
    "measurementId": "G-F07GBFWC5S",
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()

admin_email = {"admin1@gmail.com": "password", "admin2@gmail.com": "password"}


# db.child("Names").push({"Name": "Utsav", "Email" : "utsav@gmail.com"})
# db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").update({"Name": "Utsav", "Email" : "maan@gmail.com"})
# users = db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").get()
# print(users.val())
# db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").remove()


app = Flask(__name__)


#####FOR MAIL#####
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "sample1test.it2@gmail.com"
app.config["MAIL_PASSWORD"] = "youknowhowto"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
#####FOR MAIL#####


@app.route("/", methods=["GET", "POST"])
def index():
    allposts = db.child("Posts").get()
    if request.method == "POST":
        if request.form["submit"] == "Send Message":
            try:
                name = request.form["name"]
                email = request.form["email"]
                message = request.form["message"]
                msg = Message(
                    "Hello {}".format(name.capitalize()),
                    sender="sample1test.it2@gmail.com",
                    recipients=[email],
                )
                msg.body = "Hello {}, \n We received your mail regarding a query \n This is your Query :- {} \n \n We hope to resolve your Query as soon as possible".format(
                    name.capitalize(), message
                )
                mail.send(msg)
                query = {"email": email, "message": message, "name": name}
                db.child("Queries").push(query)
                return render_template("thankyou.htm")
            except:
                return render_template("failed.htm")
    if allposts.val() == None:
        return render_template("index.html")
    else:
        return render_template("index.html", posts=allposts)


@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if request.form["submit"] == "signup":
            try:
                name = request.form["name"]
                lastname = request.form["lastname"]
                email = request.form["email"]
                password = request.form["password"]
                db.child("Student Name").push(
                    {
                        "Name": name,
                        "Lastname": lastname,
                        "Email ID": email,
                        "Password": password,
                    }
                )
                signup = auth.create_user_with_email_and_password(email, password)
            except:
                return "Error Loading page please try again Later......"
            # sname = db.child("Student Name").get()
            # to = sname.val()
            # return render_template("login.html", t=to.values())
    return render_template("signup.html")


@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["submit"] == "login":
            email = request.form["email"]
            password = request.form["password"]
            try:
                login = auth.sign_in_with_email_and_password(email, password)
                users = db.child("Student Name").get()
                user = users.val()
                for key, values in user.items():
                    # return values
                    for inkey, invalues in values.items():
                        # return inkey
                        if email in invalues:
                            user_name = values["Name"].upper()
                            try:
                                news_get = db.child("News Updates").get()
                                return render_template(
                                    "student.html",
                                    news=news_get.val(),
                                    user_detail=user_name,
                                )
                            except:
                                return "No NEWS FOUND."
                            #     return "NO NEWS FOUND"
                            # return render_template("index.html", user_detail=user_name)
                # return render_template("index.html", t=user)
            except:
                # print("Wrong Pass")
                return "Wrong Email or Password"
            # print(login)

        elif request.form["submit"] == "pass":
            return redirect(url_for("forgotpass"))
            # return render_template("forgotpass.html")
    return render_template("login.html")


@app.route("/forgotpass.html", methods=["GET", "POST"])
def forgotpass():
    if request.method == "POST":
        if request.form["submit"] == "pass":
            email = request.form["email"]
            auth.send_password_reset_email(email)

            # elif request.form["submit"] == "get":
            #     users = db.child("Student Name").get()
            #     a = users.val()
            #     # sub = json.loads(users.val())
            #     print(type(users.val()))
            #     return a
    return render_template("forgotpass.html")


@app.route("/admin.html", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["submit"] == "add":
            headline = request.form["headline"]
            story = request.form["story"]
            db.child("News Updates").push(
                # {"Headline": headline, "Story": story,}
                {headline: story}
            )
            # return render_template("admin.html")
            return redirect(url_for("admin.html"))
    return 'render_template("admin.html")'


@app.route("/adminlogin.html", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        if request.form["submit"] == "adminlogin":
            email = request.form["email"]
            password = request.form["password"]
            try:
                admin_email[email] == password
                try:
                    login = auth.sign_in_with_email_and_password(email, password)
                    queries_get = db.child("Queries").get()
                    return render_template("admin.html", query=queries_get.val())
                except:
                    return " Loading page please try again Later......"
            except:
                return "Wrong Email or Password"

            # print(login)

        elif request.form["submit"] == "home":
            return render_template("index.html")
    return render_template("adminlogin.html")


if __name__ == "__main__":
    app.run(debug=True)
