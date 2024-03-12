from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from forms import RegistrationForm, LoginForm, ConfirmationForm
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField ,SubmitField 
from wtforms.validators import InputRequired, Length 
from email_validator import validate_email, EmailNotValidError
#from controller.payment import generate_card_token, create_payment_charge
from stripegw.stripepay import add_card_details
import os, sys
from pathlib import Path
import configparser
import eagle

 
config = configparser.ConfigParser()

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

global o,p,a,pw

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
 savfil = os.path.join(os.path.dirname(__file__)+"/","dsgfile.txt")

 p = request.form.get('options')
 e = request.form.get('email')
 pw = request.form.get('password')
 o = request.form.get('orgname')
 a = request.form.get('acronym')
 w = request.form.get('website')
 pu = "1111111" #request.form.get('puv_monthly')
 wp = "/"

 #### write to tmp ini file
 tfnam = os.path.join(os.path.dirname(__file__)+"/","dsgtmp.ini")
 #config.set("~/."+filnam)
 config.remove_section('install')
 config.add_section('install')
 config.set('install', 'CLI_NME',o)
 config.set('install', 'wurl',w)
 config.set('install', 'acronym',a)
 config.set('install', 'work_path',wp)
 config.set('install','puv_month',pu)

 # save to a file
 with open(tfnam, 'w+') as configfile:
  config.write(configfile)
 with open(savfil, 'w') as gfile:
  gfile.write(tfnam)


 if p == 'SMB':
  return redirect("https://buy.stripe.com/test_eVadRod6egFSg0w144")
 else:
  if p == 'GRW':
   return redirect("https://buy.stripe.com/00g3cf9YvczpeascMO")
  else:
   if p == 'COR':
    return redirect("https://buy.stripe.com/test_4gw14C7LUgFScOk4gh")
   else:
    if p == 'ENT':
     flash('Please contact us for a discussion to setup your trial. Thanks')
     return redirect(url_for('home'))
    else:
     if p =="GLO":
       flash('Please contact us for a discussion to setup your trial. Thanks')
       return redirect(url_for('home'))
     else:
      return redirect(url_for('pay'))
 x = eagle.main()
 if x == 1:
   import dsgix1
   dsgix1.main()
 #confirm()
 return render_template("confirmation.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Trial', form=form)

@app.route("/confirmation", methods=['GET', 'POST'])
def confirm():
 form = ConfirmationForm()
 x = eagle.main()
 if x == 1:
   import dsgix1
   dsgix1.main()
 return render_template('confirmation.html')



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
