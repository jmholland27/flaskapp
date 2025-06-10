from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from createfile.create import createfile

app = Flask(__name__)
app.register_blueprint(createfile, url_prefix='/createfile')
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class User(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def home():
    return render_template('index.html', names=['jake', 'caleb', 'ben'])

@app.route('/view')
def view():
    return render_template('view.html', values=User.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        session['user'] = user

        found_user = User.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = User(user, '')
            db.session.add(usr)
            db.session.commit()

        flash(f'Successful login', 'info')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash(f'Already logged in', 'info')
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None
    if 'user' in session:
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            found_user = User.query.filter_by(name=session['user']).first()
            found_user.email = email
            db.session.commit()
            flash(f'Email updated successfully', 'info')
        else:
            if 'email' in session:
                email = session['email']
        return render_template('user.html', email=email)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        session.pop('user', None)
        session.pop('email', None)
        flash(f'You have been logged out {user}', 'info')
    return redirect(url_for('login'))

@app.route('/styles')
def styles():
    return render_template('styles.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)