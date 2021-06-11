from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import Use,db,Note,Community
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import time
import smtplib
auth = Blueprint('auth',__name__)
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Use.query.filter_by(email=email).first()
        if user:
            print(user.password)
            if (user.password==password):
                flash('Logged in successfully!', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/com',methods=['GET','POST'])
@login_required
def com():
    s = Use.query.all()
    usr = Community.query.all()
    if request.method=='GET':
        return render_template('comm.html',user=current_user,usr=usr) 
    if request.method=='POST':
        usr = Community.query.all()
        cNote= request.form.get("Cnote")
        if len(cNote)<1:
            flash("Note is too short",category="error")
        else:
            new_note = Community(data=cNote,user_id= current_user.id)
            usr = Community.query.all()
            s = Use.query.all()
            pers = new_note.user_id
            db.session.add(new_note)
            db.session.commit()
            flash("Note added",category="success") 
            usr = Community.query.all()

            


    return render_template('comm.html',user=current_user,usr=usr,pers = pers,Use=s)      




@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    maybe = False
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(password1)
        user = Use.query.filter_by(email=email).first()
        if user:
            flash("Email already in use",category='error')
        elif len(email)<4:
            flash('Email must be greater than 4 characters',category='error')
        elif len(firstName)<2:
            flash('Name must be greater than 2 characters',category='error')
        elif password1!=password2:
            flash('Passwords do not match',category='error')
        else:
           
            new_user = Use(email=email,first_name =firstName, password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash("succes",category='success')
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))
    return render_template('sign_up.html',user=current_user)


@auth.route('/forgot_pass',methods=['GET','POST'])
def forgot_pass():
    if request.method =="POST":
        sender_email = "Sai.chimbili@gmail.com"
        recEM = request.form.get("emailF")
        password= "Sai123Rakshith"
        user = Use.query.filter_by(email=recEM).first()
        if user:
            message = user.password
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email,recEM,message)
        else:
            flash("user does not exist",category="error")

       

    return render_template('forgot_pass.html',user=current_user)