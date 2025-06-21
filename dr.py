import os
import csv
import torch
import whisper
import yt_dlp
from pydub import AudioSegment

# Function to download audio from YouTube
def download_youtube_audio(urls, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                ydl.download([url.strip()])
            except Exception as e:
                print(f"Failed to download {url}: {e}")

# Function to preprocess audio to mono, 16kHz, 16-bit WAV
def preprocess_audio(input_path):
    audio = AudioSegment.from_file(input_path)
    processed = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    processed_path = input_path.replace(".wav", "_processed.wav")
    processed.export(processed_path, format="wav")
    return processed_path

# Function to split audio into timestamp-named chunks
def split_audio(audio_path, chunk_length_ms=3000, output_folder="chunks"):
    audio = AudioSegment.from_wav(audio_path)
    os.makedirs(output_folder, exist_ok=True)

    chunk_files = []
    for i, start_ms in enumerate(range(0, len(audio), chunk_length_ms)):
        end_ms = min(start_ms + chunk_length_ms, len(audio))
        chunk = audio[start_ms:end_ms]

        start_sec = start_ms // 1000
        end_sec = end_ms // 1000
        chunk_filename = os.path.join(output_folder, f"chunk_{start_sec:04d}-{end_sec:04d}.wav")
        chunk.export(chunk_filename, format="wav")
        chunk_files.append(chunk_filename)

    return chunk_files

# Main process
def process_all_links(video_links):
    print("[*] Checking for CUDA availability...")
    if not torch.cuda.is_available():
        raise SystemExit("❌ CUDA is not available. Aborting.")

    print("[*] Loading Whisper model on GPU...")
    model = whisper.load_model("small", device="cuda")

    # Confirm the model is on CUDA
    device_used = next(model.parameters()).device
    print(f"[✔] Whisper model loaded on device: {device_used}")
    if not str(device_used).startswith("cuda"):
        raise RuntimeError("❌ Whisper model is not on CUDA. Exiting.")

    # Step 1: Download audio
    print("[*] Downloading audio from YouTube...")
    download_youtube_audio(video_links)

    # Step 2: Process each downloaded file
    with open("temp/speaker1/metadata.csv", "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')

        for file in os.listdir("downloads"):
            if not file.endswith(".wav"):
                continue

            full_path = os.path.join("downloads", file)
            print(f"\n[*] Preprocessing: {file}")
            processed_path = preprocess_audio(full_path)

            # Step 3: Split into chunks
            base_name = os.path.splitext(os.path.basename(file))[0]
            chunk_dir = os.path.join("temp/speaker1/chunks", base_name)
            print(f"[*] Splitting {file} into chunks...")
            chunk_files = split_audio(processed_path, output_folder=chunk_dir)
            print(f"[*] Total chunks: {len(chunk_files)}")

            # Step 4: Transcribe each chunk
            for chunk_file in chunk_files:
                print(f"[+] Transcribing {chunk_file}...")
                result = model.transcribe(chunk_file, fp16=True)
                transcript = result["text"].strip()
                writer.writerow([chunk_file, transcript])

    print("\n✅ All done. Transcriptions saved to metadata.csv.")

# Entry point
if __name__ == "__main__":
    links_input = input("Enter YouTube links (comma separated):\n> ")
    video_links = links_input.split(",")
    process_all_links(video_links)
