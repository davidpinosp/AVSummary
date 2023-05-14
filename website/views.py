import json
from flask import Flask, render_template, request, redirect, url_for, Blueprint, jsonify, flash
from .utils.audio_processing import get_transcription_and_summary
import tempfile
import os
from .models import Note
from . import db
from flask_login import login_user, login_required, logout_user, current_user


views = Blueprint('views', __name__)


@views.route('/')
def index():
    print(current_user.is_authenticated)
    return render_template('index.html', user=current_user)


@views.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    return render_template('main.html', user=current_user)


@views.route('/save-input', methods=['POST'])
@login_required
def save_input():
    note = request.form.get('resultText')
    # Perform the desired action with the input value
    print("Input value:", note)
    # You can store the value in a database, send it to another route, or perform any other operation here
    if len(note) < 1:
        flash('ID is too short!', category='error')
    else:
        # providing the schema for the note
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)  # adding the note to the database
        db.session.commit()

        # insert logic here navigate to next page that pulls image into the html
        flash('Your summary has been saved!', category='success')
        # render another thing

    return redirect(url_for('views.main'))


@views.route('notes')
@login_required
def notes():
    return render_template('notes.html', user=current_user)


@views.route('/process-audio', methods=['POST'])
def process_audio():
    # Get the uploaded file
    audio_file = request.files['audioFile']

    # Save the file to a temporary location
    temp_audio_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio_file.save(temp_audio_file.name)

    # Perform speech-to-text conversion
    transcript = get_transcription_and_summary(temp_audio_file.name)

    # Remove the temporary file
    os.remove(temp_audio_file.name)

    # Return the result
    return {'transcript': transcript}


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # get_points(1718560715)
    # this function expects a JSON from the INDEX.js file
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
