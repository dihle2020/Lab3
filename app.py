from flask import Flask, render_template, request, redirect, url_for
from models.user import Db, User
from modules.userform import UserForm
from modules.updateuserform import UpdateUserForm
import os
import random
import string

app = Flask(__name__)

DB_PASS = os.getenv("DB_PASS")
DB_USER = os.getenv("DB_USER")
#connecting database to app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+DB_USER+':'+DB_PASS+'@localhost/usersdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
Db.init_app(app)


@app.route('/')
def index():
    # Query all
    users = User.query.all()

    # Iterate and print
    for user in users:
        User.toString(user)

    return render_template("index.html", users=users)


# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            Db.session.add(new_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)

# @route /adduser/<first_name>/<age>
@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    Db.session.add(User(first_name=first_name, age=age))
    Db.session.commit()
    return redirect(url_for('index'))

@app.route('/lookupID/<user_id>')
def lookupUserByID(user_id):
    user = User.query.filter_by(user_id=user_id).first()  # could also use User.query.get(1) to filter by PK
    #  user = User.toString(user)
    return render_template('lookupID.html', first_name=user.first_name, id=user.user_id, age=user.age)

@app.route('/deleteID/<user_id>')
def deleteByID(user_id):
    User.query.filter_by(user_id=user_id).delete()
    Db.session.commit()

    users = User.query.all()

    # Iterate and print
    for user in users:
        User.toString(user)

    return render_template("index.html", users=users)

@app.route('/editUser', methods=['GET', 'POST'])
def editUser():
    form = UpdateUserForm()

    # If GET
    if request.method == 'GET':
        return render_template('edituser.html', form=form)

    # If POST
    else:
        if form.validate_on_submit():
            user_id = request.form['id']
            new_name = request.form['first_name']
            new_age = request.form['age']
            user = User.query.get(user_id)
            user.first_name = new_name
            user.age = new_age
            Db.session.commit()

            return redirect(url_for('index'))
        else:
            return render_template('edituser.html', form=form)



@app.route('/generateusers/<num_users>')
def generateUsers(num_users):
    for i in range(int(num_users)):
        letters = string.ascii_lowercase
        first_name = ''.join(random.choice(letters) for j in range(15))
        age = random.SystemRandom().randint(1, 100)
        print(first_name)

        Db.session.add(User(first_name=first_name, age=age))
        Db.session.commit()
    return redirect(url_for('index'))