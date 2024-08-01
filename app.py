import os
import subprocess
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.lower().endswith(('.wav', '.mp3')):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Process the file and get the result
        result = transcribe_file(filepath)
        return render_template('index.html', result=result)
    
    return redirect(request.url)

def transcribe_file(filepath):
    model_path = os.path.abspath('kaldi/vosk-model-fa-0.5')
    venv_python = os.path.abspath('.venv/Scripts/python.exe')
    script_path = os.path.abspath('kaldi/transcribe.py')

    command = [venv_python, script_path, model_path, filepath]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        print(f"Transcription result: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_message = f"Error during transcription:\n{e.stdout}\n{e.stderr}"
        print(f"Subprocess error: {error_message}")
        return error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        return error_message



def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith(('.wav', '.mp3')):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        print(f"Saved file path: {filepath}")  # Debugging line
        print(f"File exists: {os.path.isfile(filepath)}")  # Debugging line
        print(f"File size: {os.path.getsize(filepath)} bytes")  # Debugging line
        result = transcribe_file(filepath)
        return render_template('index.html', result=result)
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
