import whisper
import torch
import os
import sys as s
import time
import msvcrt
import argparse
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from tkinter import filedialog, Tk
from colorama import init, Fore, Style

sys = s

# Init colorama
init(autoreset=True)

# CLI Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("--file", default="true", help="Set to false to use mic")
parser.add_argument("--rs", default="false", help="Use RAM storage (true/false)")
parser.add_argument("--keep", action="store_true", help="Keep audio file if not in RAM")
args = parser.parse_args()

# Model choices
models = ["tiny", "base", "small", "medium", "large", "turbo"]
model_index = 1  # default to base

# Detect device
device = "cuda" if torch.cuda.is_available() else "cpu"

def print_models():
    print(Fore.YELLOW + "\nSelect a model with ↑ / ↓ arrow keys. Press Enter to confirm.\n")
    for i, model in enumerate(models):
        if i == model_index:
            print(Fore.GREEN + f"> {model}")
        else:
            print(f"  {model}")

def select_model(modelindex=None):
        global model_index
        if modelindex is None:
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print_models()
                key = msvcrt.getch()
                if key == b'\xe0':
                    key = msvcrt.getch()
                    if key == b'H':
                        model_index = (model_index - 1) % len(models)
                    elif key == b'P':
                        model_index = (model_index + 1) % len(models)
                elif key == b'\r':
                    break
        else:
            model_index = modelindex

        return models[model_index]

def select_audio_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.webm *.mp4")])
    return file_path

def get_input_devices():
    devices = sd.query_devices()
    return [(i, d['name']) for i, d in enumerate(devices) if d['max_input_channels'] > 0]

def print_microphones(mics, selected_index):
    print(Fore.YELLOW + "\nSelect a microphone with ↑ / ↓ arrow keys. Press Enter to confirm.\n")
    for i, (idx, name) in enumerate(mics):
        if i == selected_index:
            print(Fore.GREEN + f"> [{idx}] {name}")
        else:
            print(f"  [{idx}] {name}")

def select_microphone():
    mics = get_input_devices()
    selected = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print_microphones(mics, selected)
        key = msvcrt.getch()
        if key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                selected = (selected - 1) % len(mics)
            elif key == b'P':
                selected = (selected + 1) % len(mics)
        elif key == b'\r':
            return mics[selected][0]

def record_from_mic(silence_timeout=2, sample_rate=16000, max_duration=30, micindex=None):
    import numpy as np
    import queue

    if micindex is None:
        mic_index = select_microphone()
    else:
        mic_index = micindex
    print(Fore.YELLOW + "\n[*] Recording... Stop speaking to end recording.")

    q = queue.Queue()
    recording = []
    silent_frames = 0
    silence_threshold = 500
    silence_limit_frames = silence_timeout * sample_rate // 512
    max_frames = max_duration * sample_rate // 512

    def callback(indata, frames, time_, status):
        q.put(indata.copy())

    try:
        with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate,
                            blocksize=512, dtype='int16', device=mic_index):
            for _ in range(max_frames):
                block = q.get()
                recording.append(block)
                if np.abs(block).mean() < silence_threshold:
                    silent_frames += 1
                    if silent_frames > silence_limit_frames:
                        print(Fore.YELLOW + "[*] Detected silence. Stopping recording.")
                        break
                else:
                    silent_frames = 0
    except Exception as e:
        print(Fore.RED + f"[!] Failed to record audio: {e}")
        sys.exit(1)

    audio = np.concatenate(recording, axis=0)

    if args.rs.lower() == "true":
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    else:
        temp_file = open("mic_input.wav", "wb")

    write(temp_file.name, sample_rate, audio)
    return temp_file.name

def transcribe_file(file_path):
    model_name = models[model_index]
    print(Fore.CYAN + f"\n[+] Using model: {model_name} ({device.upper()})")
    print(Fore.YELLOW + "[*] Loading model...")

    try:
        global result
        model = whisper.load_model(model_name, device=device)
        print(Fore.YELLOW + "[*] Transcribing...")
        result = model.transcribe(file_path, fp16=False)
        print(Fore.GREEN + f"\n[✔] Detected Language: {result['language']}")
        print(Fore.WHITE + Style.BRIGHT + "\n--- Transcription Output ---\n")
        print(result['text'])
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

    if file_path.startswith(tempfile.gettempdir()) or file_path == "mic_input.wav":
        if not args.keep:
            os.remove(file_path)
            print(Fore.YELLOW + f"\n[*] Deleted temporary audio file: {file_path}")

    return result['text']

if __name__ == "__main__":
    print(Fore.CYAN + "[Whisper STT CLI App]")
    print(Fore.MAGENTA + f"Detected device: {device.upper()}")

    select_model()
    print(Fore.GREEN + f"✔ Model selected: {models[model_index]}")

    if args.file.lower() == "true":
        print(Fore.YELLOW + "\n[*] Choose audio file from file picker...")
        file_path = select_audio_file()
        if not file_path:
            print(Fore.RED + "[!] No file selected. Exiting.")
            sys.exit()
    else:
        file_path = record_from_mic()

    transcribe_file(file_path)
    print(Fore.CYAN + "\n[✔] Transcription completed. Exiting.")

