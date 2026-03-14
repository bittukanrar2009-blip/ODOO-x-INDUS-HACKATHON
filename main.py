import os
from pprint import pprint
from datetime import datetime
from flask import Flask, render_template, session, request, url_for, redirect
from sqlalchemy import func
from sqlmodel import select

from models.db import create_db, Users, Stock, Transaction, TransactionType

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
db = create_db()

@app.route("/")
def home():

    #check login status
    if "logged_in" not in session:
        return redirect("login")

    # getting transaction data
    transaction = db.exec(select(Transaction)).all()
    transaction_list_of_dicts = [t.model_dump() for t in transaction]
    receipts = []
    deliveries = []
    for item in transaction_list_of_dicts:
        if item['type'] == TransactionType.Receipt and item['status'] != "Completed":
            if item['schedule_date'] > datetime.now():
                item['schedule'] = "Operation"
            elif item['schedule_date'] < datetime.now():
                item['schedule'] = "Late"
            else:
                item['schedule'] = "Waiting"
            receipts.append(item)
        elif item['type'] == TransactionType.Delivery and item['status'] != "Completed":
            deliveries.append(item)
    pprint(deliveries)
    return render_template("index.html", recieve = len(receipts), deliver=len(deliveries),
                           receipts=receipts, deliveries=deliveries)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # print(request.form.to_dict())
        lid = request.form.get("loginId")
        password = request.form.get("password")

        statement = select(Users).where((Users.LoginId == lid) & (Users.password_hash == password))
        results = db.exec(statement).all()
        print(results)

        if len(results) != 0:
            session['logged_in'] = True
            return redirect(url_for("home"))
        else:
            print("login failed")
            session['logged_in'] = False
            return render_template("login.html", login_failed = True, error="")
    return render_template("login.html", login_failed= False, error="")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # validation logic in frontend ;-;
    # TODO: compare loginId and email with database, if similar found, redirect user to login.
    # TODO: if new user, store credentials to database.
    if request.method == "POST":
        email = request.form.get("email")
        loginid = request.form.get("loginId")
        password = request.form.get("password")

        statement = select(Users).where((Users.email == email) | (Users.LoginId == loginid))
        results = db.exec(statement).all()
        print(results)
        if len(results) != 0:
            error = "User already exists! Please log-in instead"
            return render_template("login.html", error=error)
        else:
            new_user = Users(email=email, LoginId=loginid, password_hash=password)
            db.add(new_user)
            db.commit()


    return render_template("signup.html")

@app.route("/stock")
def stock():
    if "logged_in" not in session:
        return redirect("login")

    return render_template("stock.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8888)