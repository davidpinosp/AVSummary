import json
from flask import Flask, render_template, request, redirect, url_for, Blueprint, jsonify, flash
from .utils.audio_processing import get_transcription_and_summary
import tempfile
import os
from flask_login import login_user, login_required, logout_user, current_user
# //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


# ToDO : finish front end (loading and formatting), hide keys , launch , add ads.


# input a video and get it to translate the text then summarize the text


views = Blueprint('views', __name__)


@views.route('/')
def index():
    print(current_user.is_authenticated)
    return render_template('index.html', user=current_user)


@views.route('main')
@login_required
def main():
    return render_template('main.html', user=current_user)


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
