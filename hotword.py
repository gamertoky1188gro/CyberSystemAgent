import os
import queue
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from colorama import Fore
import main

def always_listen_for_hotword(callback_func, hotword="ok windows"):
    print(Fore.CYAN + f"[*] Listening for hotword: '{hotword}' (via main.transcribe_file)...")

    sample_rate = 16000
    block_duration = 1  # seconds
    q = queue.Queue()

    def callback(indata, frames, time_, status):
        q.put(indata.copy())

    with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, dtype='int16',
                        blocksize=512, device=main.select_microphone()):
        while True:
            try:
                # Collect 1s of audio
                audio_blocks = [q.get() for _ in range(int(sample_rate / 512 * block_duration))]
                audio = np.concatenate(audio_blocks, axis=0)

                # Save to temporary .wav in current working directory
                temp_filename = "temp_hotword.wav"
                write(temp_filename, sample_rate, audio)

                # Use your own transcriber from main
                result = main.transcribe_file(temp_filename)
                detected_text = result['text'].lower().strip()
                print(Fore.LIGHTYELLOW_EX + f"[~] Heard: {detected_text}")

                # Delete file after processing
                os.remove(temp_filename)

                if hotword in detected_text:
                    print(Fore.GREEN + "[✔] Hotword detected! Running callback function...")
                    callback_func()
                    print(Fore.YELLOW + "[*] Callback done. Listening again...")

            except Exception as e:
                print(Fore.RED + f"[!] Listening error: {e}")

# Example callback function
def hd():
    print("Hi")

# Run listener
always_listen_for_hotword(hd, hotword="ok windows")
