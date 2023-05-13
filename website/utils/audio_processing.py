import os
from google.cloud import speech_v1p1beta1 as speech

# Set up Google Cloud credentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv(
    'GOOGLE_APPLICATION_CREDENTIALS')


def transcribe_audio(audio_file):
    client = speech.SpeechClient()

    # Read the audio file
    with open(audio_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code='en-US',
        audio_channel_count=2
    )

    # Perform the speech-to-text transcription
    response = client.recognize(config=config, audio=audio)

    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript


def summarize_text(text):
    # You can use your preferred text summarization algorithm here
    # This is a simple example that extracts the first few sentences as a summary
    sentences = text.split('. ')
    # Adjust the number of sentences for your desired summary length
    summary = '. '.join(sentences[:3])
    return summary


# Provide a list of audio files you want to summarize
def get_transcription_and_summary(filepath):
    audio_file = filepath
    print(f"Processing audio file: {audio_file}")
    transcript = transcribe_audio(audio_file)
    # summary = summarize_text(transcript)

    # print("Transcript:")
    # print(transcript)
    # print("Summary:")
    # print(summary)
    # print('\n')
    return transcript
