from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
Bootstrap(app)

@app.route('/')
def home():
    return render_template('home.html')

# Define the 'help' route
@app.route("/help")
def help():
    return render_template("help.html")

@app.route('/audio_text', methods=['GET', 'POST'])
def audio_text():
    if request.method == 'POST':
        r = sr.Recognizer()

        if 'audio_file' not in request.files:
            return "No file part"

        file = request.files['audio_file']
        if file.filename == '':
            return "No selected file"

        # Save the uploaded file temporarily
        temp_file_path = "temp_audio_file"  # You can use a specific extension like ".wav" if needed
        file.save(temp_file_path)

        try:
            with sr.AudioFile(temp_file_path) as source:
                audio_data = r.record(source)  # Use r.record() to read the entire audio file
                text = r.recognize_google(audio_data)
                return render_template("audio_text.html", text=text)
        except sr.UnknownValueError:
            return "Error: Unable to recognize audio"
        except sr.RequestError:
            return "Error: Could not request results; check your internet connection"
        except Exception as e:
            return f"Error: {e}"
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    return render_template("audio_text.html")

@app.route('/text_audio', methods=['GET', 'POST'])
def text_audio():
    if request.method == 'POST':
        input_text = request.form['input_text']
        output_filename = "static/output.mp3"
        text_to_audio(input_text, output_filename)
        audio_file = url_for('static', filename='output.mp3')
        return render_template('text_audio.html', audio_file=audio_file)
    return render_template('text_audio.html')

def text_to_audio(text, output_file):
    tts = gTTS(text)
    tts.save(output_file)

@app.route('/real_time')
def real_time():
    return render_template('real_time.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Give Command, Sir..!!")
        audio_text = r.listen(source)  # listening the speech and store in audio_text variable
        print("Analyzing Speech, thanks")
        try:
            recognized_text = r.recognize_google(audio_text)
            return recognized_text
        except sr.UnknownValueError:
            return "Sorry, I did not get that, Please repeat"
        except sr.RequestError:
            return "Could not request results; check your internet connection"

# if __name__ == "__main__":
#     app.run(debug=True)
