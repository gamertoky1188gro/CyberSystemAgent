import os
import glob
from moviepy import VideoFileClip, AudioFileClip
from pydub import AudioSegment, effects, silence
import subprocess
import noisereduce as nr
import numpy as np


def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, fps=44100)
    print(f"Extracted audio to {audio_path}")


def run_demucs(audio_path, output_dir="demucs_output"):
    print("Running Demucs to separate vocals and music...")
    cmd = [
        "demucs",
        audio_path,
        "--two-stems", "vocals",
        "-o", output_dir,
        "--out", output_dir
    ]
    subprocess.run(cmd, check=True)
    print("Demucs processing completed")


def find_vocals_path(base_dir):
    matches = glob.glob(os.path.join(base_dir, "**", "vocals.wav"), recursive=True)
    if matches:
        print(f"Found vocals.wav at: {matches[0]}")
        return matches[0]
    else:
        raise FileNotFoundError("vocals.wav not found in Demucs output directory.")


def process_vocals(vocals_path, cleaned_vocals_path, silence_thresh=-40, min_silence_len=700):
    # Load vocals
    vocals = AudioSegment.from_file(vocals_path)

    # Convert pydub AudioSegment to numpy array for noise reduction
    samples = np.array(vocals.get_array_of_samples()).astype(np.float32)
    if vocals.channels > 1:
        samples = samples.reshape((-1, vocals.channels))
        samples = samples.mean(axis=1)  # convert to mono for noise reduction

    # Noise reduction using first 0.5 seconds as noise profile
    sr = vocals.frame_rate
    noise_sample = samples[:int(0.5 * sr)]
    reduced_noise = nr.reduce_noise(y=samples, y_noise=noise_sample, sr=sr)

    # Convert back to pydub AudioSegment
    reduced_noise = reduced_noise.astype(np.int16)
    processed_audio = AudioSegment(
        reduced_noise.tobytes(),
        frame_rate=sr,
        sample_width=2,  # 16-bit audio = 2 bytes
        channels=1
    )

    # Normalize volume
    processed_audio = effects.normalize(processed_audio)

    # Trim silence
    silences = silence.detect_silence(processed_audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    keep_segments = []
    prev_end = 0
    for start, end in silences:
        if prev_end < start:
            keep_segments.append((prev_end, start))
        prev_end = end
    if prev_end < len(processed_audio):
        keep_segments.append((prev_end, len(processed_audio)))

    trimmed_audio = AudioSegment.empty()
    for seg_start, seg_end in keep_segments:
        trimmed_audio += processed_audio[seg_start:seg_end]

    trimmed_audio.export(cleaned_vocals_path, format="wav")
    print(f"Processed vocals saved to {cleaned_vocals_path}")


def combine_audio_with_video(video_path, new_audio_path, output_path):
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(new_audio_path)
    video = video.with_audio(new_audio)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Final video saved to {output_path}")


if __name__ == "__main__":
    input_video = "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/omar_esa_video.mp4"
    extracted_audio = "extracted_audio.wav"
    demucs_output_dir = "demucs_output"
    cleaned_vocals = "cleaned_vocals.wav"
    output_video = "omar_esa_clean_video.mp4"

    extract_audio_from_video(input_video, extracted_audio)
    run_demucs(extracted_audio, demucs_output_dir)
    vocals_file = find_vocals_path(demucs_output_dir)
    process_vocals(vocals_file, cleaned_vocals)
    combine_audio_with_video(input_video, cleaned_vocals, output_video)
