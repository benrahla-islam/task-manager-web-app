from flask import Flask ,render_template , url_for , session , request , redirect , flash 
from flask_wtf import FlaskForm
from wtforms import StringField , EmailField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired ,InputRequired , Email 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import validates
from sqlalchemy import ForeignKey
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column("id",db.Integer , primary_key = True , autoincrement = True)
    email = db.Column("email", db.String(100), unique = True , nullable = False)
    username = db.Column("username", db.String(100), nullable = False)
    password = db.Column("password", db.String(100) , nullable = False)
    subscription_type = db.Column("subscription_type", db.Enum('basic','premium','admin') , default = 'basic')

    def __init__(self , username , email , password ):
        self.username = username
        self.email = email
        self.password = password

    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email address.")
        return email

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username cannot be empty.")
        return username

    @validates('password')
    def validate_password(self, key, password):
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return password



class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column("id",db.Integer , primary_key = True , autoincrement = True)
    title = db.Column("title", db.String(200) , nullable = False)
    description = db.Column("description", db.String(500), nullable = True)
    status = db.Column("status", db.Enum('active','inactive') , default = 'active')
    group_id = db.Column(db.Integer, ForeignKey('group.id'), nullable=True)
    user_id = db.Column(db.Integer , ForeignKey('user.id') , nullable = False)


    group = db.relationship('Group', backref='tasks')
    user = db.relationship('User', backref='tasks')

    def __init__(self,title, description = None , group_id = None):
        self.title = title
        self.description = description
        self.group_id = group_id

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title cannot be empty.")
        return title


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column("id",db.Integer, primary_key = True , autoincrement = True)
    name = db.Column("name", db.String(50) , nullable = False)
    color = db.Column("color", db.String(10) , default = 'blue')
    user_id = db.Column(db.Integer , ForeignKey('user.id') , nullable = False)

    user = db.relationship('User', backref='groups')

    def __init__(self,name,color = 'blue'):
        self.name = name 
        self.color = color



class SigninForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email() , DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    terms = BooleanField('Accept Terms', validators=[InputRequired()])
    signup = SubmitField('signup')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email() , DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('login')


@app.route('/')
def WelcomePage():
    return render_template("WelcomePage.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    Email = None
    Password = None
    form = LoginForm()
    if request.method == 'POST':
        Email = form.email.data
        Password = form.password.data
        user = User.query.filter_by(email=Email).first()
        if user is None:
            flash(
                'No account registered with this email, do you want to signup?' , 
                'error'
            )
        elif not sha256_crypt.verify(Password, user.password):
            flash('Incorrect password. Please try again.', 'error')
        else:
            session['user'] = user.username
            return redirect(url_for('userpage', user=user))
    return render_template('login.html', form=form)


@app.route('/signup' , methods = ['GET' , 'POST'])
def signup():
    email = None
    password = None
    name = None
    form = SigninForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        if User.query.filter_by(username=name).first():
            flash('Username already exist','error')
            # return render_template('signup.html', form = form)
        elif  User.query.filter_by(email= email).first():
            flash('Email already exist','error')
        else:
            hashed_password = sha256_crypt.hash(password)
            new_user = User(username=name , email= email , password= hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session['user']=name
            return redirect(url_for('userpage'))
    else:
        flash('Please correct the errors in the form.', 'error')
    return render_template('signup.html', form = form , email = email, name = name , password = password )



@app.route('/home')
def userpage():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('welcome_page'))

@app.route('/terms')
def terms_of_service():
    return 'just accept it you have nothing to lose !'


@app.route('/create_task' , methods = ['POST'])
def create_task():
    pass


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)