from flask import Flask ,render_template , url_for , session , request , redirect
from flask_wtf import FlaskForm
from wtforms import StringField , EmailField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired ,InputRequired , Email 


app = Flask(__name__)
app.secret_key = 'hello'


class SigninForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email() , DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    terms = BooleanField('Accept Terms', validators=[InputRequired()])
    login = SubmitField('Login')



@app.route('/')
def WelcomePage():
    return render_template("WelcomePage.html")



@app.route('/login' , methods = ['GET' , 'POST'])
def login():
    if request.method == 'POST' :
        user = request.form['user']
        session['user'] = user
        return redirect(url_for( 'userpage',user= user))
    return render_template('login.html')



@app.route('/signup' , methods = ['GET' , 'POST'])
def signup():
    name = None
    email= None
    password = None
    terms = None
    form = SigninForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        terms = form.terms.data
        form.name.data = ''
        form.email.data = ''
        form.password.data = ''
        form.terms.data = ''
        return redirect(url_for('userpage'))
    else:
        print(form.errors)
    return render_template('signup.html', form = form , email = email, name = name , password = password )



@app.route('/home')
def userpage():
    return render_template('home.html')

@app.route('/terms')
def terms_of_service():
    return 'just accept it you have nothing to lose !'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

app.run(debug=True)