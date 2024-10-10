# Audio Transcription Web App

This is a web application built with Python and Flask that allows users to upload audio files and transcribe them using the Vosk speech recognition model. The app is designed to handle audio in multiple languages, with support for easy adaptation to different languages.

## Features

- **Web Interface**: Users can easily upload audio files through a user-friendly web interface.
- **File Support**: Supports .wav and .mp3 audio formats.
- **Speech Recognition**: Uses Vosk for accurate speech-to-text conversion.
- **Language Support**: Designed to be adaptable for various languages.
- **Easy Deployment**: Simple setup and deployment process.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/adibshirazi/VoiceToWords.git
    cd VoiceToWords
    ```

2. **Set up a virtual environment**:
    ```sh
    python -m venv .venv
    ```
    Activate the virtual environment:
    - On Windows:
      ```sh
      .venv\Scripts\activate
      ```
    - On macOS and Linux:
      ```sh
      source .venv/bin/activate
      ```

3. **Install the required libraries**:
    ```sh
    pip install -r requirements.txt
    ```


    To use a different language model:
    - Download the desired model from [Vosk Models](https://alphacephei.com/vosk/models)
    - Extract the model to the `kaldi/` directory
    - Rename the extracted folder to your preferred name, e.g., `your_language_model_folder`
    - Update the `transcribe_file()` function in `app.py` to point to the new model directory. Replace `your_language_model_folder` with the name of the new model folder.

    Example update for `transcribe_file()` function:
    ```python
    
    def transcribe_file(filepath):
        # Specify the name of the folder containing your language model
        model_folder = "your_language_model_folder"
        model_path = os.path.abspath(f'kaldi/{model_folder}')
        
        # Path to the Python executable in the virtual environment
        venv_python = os.path.abspath('.venv/Scripts/python.exe')
        
        # Path to the transcription script
        script_path = os.path.abspath('kaldi/transcribe.py')
    ```

## Usage

1. **Run the application**:
    ```sh
    python app.py
    ```

2. **Using the Application**:
    - Open a web browser and navigate to `http://localhost:5000`
    - Upload an audio file (.wav or .mp3) using the web interface
    - View the transcription result on the page

## Project Structure

- `app.py`: Main Flask application
- `transcribe.py`: Script for audio transcription using Vosk
- `templates/index.html`: HTML template for the web interface
- `uploads/`: Directory for storing uploaded audio files
- `requirements.txt`: List of Python package dependencies

## How It Works

### Vosk Speech Recognition

Vosk is an offline speech recognition toolkit that uses neural network models for accurate speech-to-text conversion. It supports multiple languages and can work on various platforms, including mobile devices and embedded systems.

Key features of Vosk:
- Offline functionality (no internet required)
- Small model size (50-100 Mb)
- Fast recognition speed
- Support for speaker identification

### Project Workflow

1. **File Upload**: 
   - User uploads an audio file through the web interface.
   - The file is temporarily saved in the `uploads/` directory.

2. **Transcription Process**:
   - The Flask application (`app.py`) calls the `transcribe_file()` function.
   - This function executes the `transcribe.py` script using subprocess.

3. **Audio Processing**:
   - `transcribe.py` uses librosa to load and process the audio file.
   - The audio is converted to the required format for Vosk (16-bit PCM).

4. **Speech Recognition**:
   - The Vosk model is loaded.
   - The audio data is passed through the Vosk recognizer.
   - The recognizer converts speech to text.

5. **Result Handling**:
   - The transcription result is returned as JSON.
   - The text is extracted and sent back to the Flask application.

6. **Display**:
   - The Flask app renders the result on the web page for the user to view.

This process allows for efficient, offline transcription of audio files, with the potential to expand to other languages by changing the Vosk model.

## License

This project is open-source and available under the [AGPL-3.0 License](LICENSE)
