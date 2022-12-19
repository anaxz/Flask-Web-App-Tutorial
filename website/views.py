from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# blueprint -> allows you sperate app out and can have the views/routes separated to multiple files
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    #user=current_user -> ref user and check if authenticated
    #this is used to display logout btn or not etc
    return render_template("home.html", user=current_user)

# cuz its in form, need to use json
@views.route('/delete-note', methods=['POST'])
def delete_note():
    #load it as json object/python dictionary
    note = json.loads(request.data)
    #access note id attribute
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    # return empty response object
    return jsonify({}) 
