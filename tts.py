import torch
import flask
import sounddevice as sd
import numpy as np
import tiktoken
from flask import request, jsonify

from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig, XttsArgs
from TTS.tts.models.xtts import Xtts
from TTS.tts.models.base_tts import BaseTTS
from TTS.utils.audio import AudioProcessor
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.utils.helpers import sequence_mask

# Safe classes for PyTorch deserialization
torch.serialization.add_safe_globals([
    BaseDatasetConfig,
    XttsConfig,
    Xtts,
    XttsAudioConfig,
    XttsArgs,
    BaseTTS,
    sequence_mask,
    AudioProcessor
])

app = flask.Flask(__name__)
MAX_TOKENS = 300  # Safe under XTTS 400-token limit
MAX_CHARS = 250   # XTTS also has char limit per chunk

def count_tokens(text: str, encoding_name="cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def split_text_to_chunks(text: str, max_tokens=400, max_chars=250, encoding_name="cl100k_base"):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)

    chunks = []
    i = 0
    while i < len(tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = encoding.decode(chunk_tokens)

        while len(chunk_text) > max_chars or len(encoding.encode(chunk_text)) > max_tokens:
            chunk_tokens = chunk_tokens[:-1]
            chunk_text = encoding.decode(chunk_tokens)

        chunks.append(chunk_text)
        i += len(chunk_tokens)
    return chunks

def synthesize_chunk(model, config, content, sw, gcl, lang):
    outputs = model.synthesize(
        content,
        config,
        speaker_wav=sw,
        gpt_cond_len=gcl,
        language=lang,
    )
    audio = np.array(outputs["wav"], dtype=np.float32)
    audio /= np.max(np.abs(audio))  # Normalize audio
    return audio

def main(lj="XTTS-v2/config.json",
         cd="XTTS-v2",
         content="Hello from XTTS!",
         sw="downloads/example.wav",
         gcl=3,
         lang="en"):

    # Load model
    config = XttsConfig()
    config.load_json(lj)
    model = Xtts.init_from_config(config)
    model.load_checkpoint(config, checkpoint_dir=cd, eval=True)
    model.to(torch.device("cpu"))  # CPU mode to avoid CUDA error

    # Split input
    chunks = split_text_to_chunks(content, max_tokens=MAX_TOKENS, max_chars=MAX_CHARS)
    print(f"[+] Total chunks: {len(chunks)}")

    all_audio = []

    for idx, chunk in enumerate(chunks, 1):
        token_count = count_tokens(chunk)
        char_count = len(chunk)
        print(f"[Chunk {idx}/{len(chunks)}] Tokens: {token_count}, Characters: {char_count} ... synthesizing")
        audio = synthesize_chunk(model, config, chunk, sw, gcl, lang)
        all_audio.append(audio)
        print(f"[Chunk {idx}/{len(chunks)}] ✔ Synthesized")

    # Concatenate and play all audio
    final_audio = np.concatenate(all_audio)
    print("[✔] All chunks synthesized. Playing final audio...")
    sd.play(final_audio, samplerate=config.audio.sample_rate)
    sd.wait()
    print("[✔] Playback complete.")

    return all_audio

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    lj = data.get('lj', "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/XTTS-v2/config.json")
    cd = data.get('cd', "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/XTTS-v2")
    content = data.get('content', "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.")
    sw = data.get('sw', "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/downloads/Adele - Hello (Muslim Version by Omar Esa) ｜ Vocals Only_processed.wav")
    gcl = data.get('gcl', 3)
    lang = data.get('lang', 'en')

    try:
        outputs = main(lj, cd, content, sw, gcl, lang)
        return jsonify({
            'status': 'success',
            'chunks': len(outputs),
            'message': f'Successfully synthesized and played {len(outputs)} chunks.'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=9900)
