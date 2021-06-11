from flask import Blueprint
from flask import render_template,flash,request
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note,db
views = Blueprint('views',__name__)

@views.route('/',methods=['POST','GET'])
@login_required
def home():
    if request.method =='POST':
        note = request.form.get('note')
        if len(note)<1:
            flash("Note is too short",category="error")
        else:
            new_note = Note(data=note, user_id= current_user.id)
       
            db.session.add(new_note)
            db.session.commit()
            
            flash("Note added",category="success")
    return render_template('home.html',user=current_user)