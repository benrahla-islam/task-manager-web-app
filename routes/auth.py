from flask import render_template , url_for , session , request , redirect , flash , Blueprint
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user , logout_user , current_user , LoginManager

from auths.forms import LoginForm , SigninForm
from models.models import User, db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
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
        elif not check_password_hash(user.password , password= Password):
            flash('Incorrect password. Please try again.', 'error')
        else:
            login_user(user=user , remember= True)
            return redirect(url_for('other.userpage', user=user))
    return render_template('login.html', form=form)


@auth_bp.route('/signup' , methods = ['GET' , 'POST'])
def signup():
    email = None
    password = None
    name = None
    form = SigninForm()
    try:
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
                hashed_password = generate_password_hash(password)
                new_user = User(username=name , email= email , password= hashed_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('other.userpage'))
    except Exception as e:
        print(e)
    else:
        flash('Please correct the errors in the form.', 'error')
    return render_template('signup.html', form = form , email = email, name = name , password = password )


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('other.WelcomePage'))