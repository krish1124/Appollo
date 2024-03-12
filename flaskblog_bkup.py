from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from forms import RegistrationForm, LoginForm, ConfirmationForm
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField ,SubmitField 
from wtforms.validators import InputRequired, Length 
from email_validator import validate_email, EmailNotValidError
#from controller.payment import generate_card_token, create_payment_charge
from stripegw.stripepay import add_card_details

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

global o,p,a, pw

posts =[]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/payment", methods=['GET', 'POST'])
def pay():
 p = request.form.get('options')
 e = request.form.get('email')
 pw = request.form.get('password')
 o = request.form.get('orgname')
 a = request.form.get('acronym')
 w = request.form.get('website')
 #result = request.form
 #from werkzeug.datastructures import ImmutableMultiDict
 #data = dict(request.form)
 #flash(data) 
 file1 = open('dsgconfig_tmp.ini', 'a')
 #Write the content of the variables to the text.txt file
 file1.write(request.form.get('options'))
 file1.write("\n")
 file1.write(o)
 file1.write("\n")
 file1.write(a)
 file1.write("\n")
 file1.write(w)
 file1.write("\n")
 #Close the text.txt file
 file1.close()
#print(p + '  ' + w)
 '''
 if p == 'option1':
  return redirect("https://buy.stripe.com/test_eVadRod6egFSg0w144")
 else:
  if p == 'option2':
   return redirect("https://buy.stripe.com/00g3cf9YvczpeascMO")
  else:
   if p == 'option3':
    return redirect("https://buy.stripe.com/test_4gw14C7LUgFScOk4gh")
   else:
    if p == 'option4':
     flash('Please contact us for a discussion to setup your trial. Thanks')
     return redirect(url_for('home'))
    else:
     if p =="option5":
       flash('Please contact us for a discussion to setup your trial. Thanks')
       return redirect(url_for('home'))
     else:
      return redirect(url_for('payment'))
'''
 return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Trial', form=form)

@app.route("/confirmation", methods=['GET', 'POST'])
def confirm():

    with open("dsgconfig_tmp.ini", "r+") as file1:
    # Reading from a file
     f= file1.read()
    file1.close()
    form = ConfirmationForm()
    return render_template('confirmation.html', form=form, result=f)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
