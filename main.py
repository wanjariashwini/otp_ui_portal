from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import requests
import json

app = Flask(__name__)
'''
SQLLight Studio https://sqlitestudio.pl/
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
'''
app.config['SECRET_KEY'] = 'ravi'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)


# Database ORMs
class User(db.Model):
    __tablename__ = "user_details"
    # id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    # public_id = db.Column(db.String(50), unique = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    mobile_no = db.Column(db.String(50), unique=True)
    dob = db.Column(db.Date)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    is_active = db.Column(db.Integer, default=1)  ## 1- means active and 0 means deactivate
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_modified_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # default=datetime.strftime(datetime.now(), "%b %d %Y"))

    def __init__(self, first_name, last_name, email, password, mobile_no, dob,
                 city, country):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mobile_no = mobile_no
        self.dob = dob
        self.city = city
        self.country = country

    def __repr__(self):
        print(self.first_name, self.last_name)
        return 1


@app.route("/")
def index():
    if session:
        if session.get('email-id'):  # session['email-id']
            return render_template("home.html")
    return render_template("index.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/home")
def home():
    if session:
        if session.get('email-id'):  # session['email-id']
            return render_template("home.html")
    return render_template("login.html")


@app.route("/otp_free_service")
def otp_free_service():
    return render_template("otp_free_service.html")


@app.route("/demo")
def demo():
    if session:
        if session.get('email-id'):  # session['email-id']
            return render_template("demo.html")
    return render_template("login1.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    if session:
        try:
            if session.get('email-id'):  # session['email-id']
                session.pop('email-id')
                # session.pop('user')
        except:
            session['email-id'] = None
            # session['user'] = None
    return render_template("login.html")


@app.route("/slogin", methods=["POST"])
def submit_login():
    if request.method == "POST":
        if request.form["username"] and request.form["password"]:
            user_username = request.form["username"]
            user_password = request.form["password"]
            # status = validate_user(username, password)
            user = User.query.filter_by(email=user_username, password=user_password).first()
            if user:
                # session['user'] = user;
                session['email-id'] = user.email
                # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
                return redirect(url_for("home"))
            else:
                message = "Plz check username and password"
                return render_template("login.html", error=message)
        else:
            message = "Plz check username and password"
            return render_template("login.html", error=message)
    return render_template("login.html")


@app.route("/slogin1", methods=["POST"])
def submit_login1():
    if request.method == "POST":
        if request.form["username"] and request.form["password"]:
            user_username = request.form["username"]
            user_password = request.form["password"]
            # status = validate_user(username, password)
            user = User.query.filter_by(email=user_username, password=user_password).first()
            if user:
                # session['user'] = user;
                session['email-id'] = user.email
                # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
                return redirect(url_for("demo"))
            else:
                message = "Plz check username and password"
                return render_template("login.html", error=message)
        else:
            message = "Plz check username and password"
            return render_template("login.html", error=message)
    return render_template("login.html")


@app.route("/signup_submit", methods=["POST"])
def signup_submit():
    status = "FAILED"
    message = ""
    if request.method == "POST":
        if request.form:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]
            mobile_no = request.form["mobile_no"]
            dob = request.form["dob"]
            y, m, d = dob.split('-')
            d_o_b = datetime(int(y), int(m), int(d))
            city = request.form["city"]
            country = request.form["country"]
            if password == confirm_password:
                user = User(first_name, last_name, email, password, mobile_no, d_o_b, city, country)
                db.session.add(user)
                db.session.commit()
                status = "SUCCESS"
                message = "You have registered successfully"
                return render_template("msg.html", status=status, msg=message)
            else:
                message = "Check the password, its not matching"
                return render_template("signup.html", status=status, msg=message)
        else:
            message = "Plz enter correct details"
            return render_template("signup.html", status=status, msg=message)
    return render_template("signup.html")


@app.route("/aboutOTP")
def aboutOTP():
    return render_template("aboutOTP.html")


@app.route("/aboutAPI")
def aboutAPI():
    return render_template("aboutAPI.html")


@app.route("/listOfAPI")
def listOfAPI():
    return render_template("listOfAPI.html")


@app.route('/sendOTP', methods=["POST"])
def send_OTP():
    if request.form:
        mob_no = request.form['mobile_no']
        url = "http://localhost:5000/sendOTP"

        payload = json.dumps({
            "mdn": mob_no,
            "otp_method": "sms"
        })
        headers = {
            'Authorization': 'Basic cGFua2FqOnBhbmthakAxMjM=',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        result = json.loads(response.text)
        print(result)
        return render_template("validate_otp.html", session_key=result["session_key"], mobile_no=mob_no,
                               response=response.json())
    else:
        response = {
            "messages": "Fail to send OTP",
            "status": "FAILED"
        }
        return render_template("demo.html", response=response)


@app.route('/validateOTP', methods=['POST'])
def validate_OTP():
    if request.form:
        otp = request.form['otp']
        session_key = request.form['session_key']
        url = "http://localhost:5000/validateOTP"

        payload = json.dumps({
            "otp": otp,
            "session_key": session_key
        })
        headers = {
            'Authorization': 'Basic cGFua2FqOnBhbmthakAxMjM=',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        return render_template("msg.html", response=response.json(), status="SUCCESS", msg="OTP verified successfully")
    else:
        response = {
            "messages": "Fail to validate OTP",
            "status": "FAILED"
        }
    return render_template("validate_otp.html", response=response)


if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port="5002", debug=True)

"""
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: user_details.mobile_no
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: user_details.email
https://stackoverflow.com/questions/22024661/jinja2-template-not-rendering-if-elif-else-statement-properly
https://stackoverflow.com/questions/42013067/how-to-access-session-variables-in-jinja-2-flask
https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_quick_guide.htm
"""

"""
https://exotel.com/otp-service-provider/
"""
