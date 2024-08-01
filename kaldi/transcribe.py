"""Transcribes audio files with Vosk (https://alphacephei.com/vosk)"""
import argparse
import json
import sys
import numpy as np
import librosa
from vosk import Model, KaldiRecognizer

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser("vosk_example")
    parser.add_argument("model", help="Directory with speech to text model")
    parser.add_argument("audio", nargs="+", help="Audio file(s) to transcribe")
    parser.add_argument(
        "--sample-rate", default=16000, help="Sample rate of model in Hertz"
    )
    args = parser.parse_args()

    model = Model(args.model)

    for audio_path in args.audio:
        # Load and re-sample audio if necessary
        audio, _sample_rate = librosa.load(audio_path, sr=args.sample_rate, mono=True)
        audio = audio_float_to_int16(audio).tobytes()

        rec = KaldiRecognizer(model, args.sample_rate)
        rec.SetWords(True)
        rec.AcceptWaveform(audio)

        # Parse JSON result
        result = rec.FinalResult()
        try:
            # Load JSON and get the 'text' field
            json_result = json.loads(result)
            text = json_result.get('text', '')
            # Output result with utf-8 encoding
            sys.stdout.buffer.write(text.encode('utf-8'))
            sys.stdout.buffer.write(b"\n")
        except (UnicodeEncodeError, json.JSONDecodeError) as e:
            sys.stderr.write(f"Error processing result: {e}\n")
            sys.exit(1)

def audio_float_to_int16(
    audio: np.ndarray, max_wav_value: float = 32767.0
) -> np.ndarray:
    """Normalize audio and convert to int16 range"""
    audio_norm = audio * (max_wav_value / max(0.01, np.max(np.abs(audio))))
    audio_norm = np.clip(audio_norm, -max_wav_value, max_wav_value)
    audio_norm = audio_norm.astype("int16")
    return audio_norm

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
