import torch
import soundfile as sf

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts, XttsAudioConfig, XttsArgs  # ✅ Required for PyTorch deserialization
from TTS.config.shared_configs import BaseDatasetConfig  # ✅ Add this line

def main(cp="C:/Users/tokyi/PycharmProjects/Gemini voice assistant/XTTS-v2/config.json", cd="C:/Users/tokyi/PycharmProjects/Gemini voice assistant/XTTS-v2", txt="It took me quite a long time to develop a voice and now that I have it I am not going to be silent.", swp="C:/Users/tokyi/PycharmProjects/Gemini voice assistant/downloads/Adele - Hello (Muslim Version by Omar Esa) ｜ Vocals Only_processed.wav", lang="en", gcl="3", op="output.wav"):
    # ✅ Tell PyTorch that we trust these custom classes in the checkpoint
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, Xtts, XttsArgs])

    # ✅ Load model configuration
    config_path = cp
    config = XttsConfig()
    config.load_json(config_path)

    # ✅ Initialize model using the config
    model = Xtts.init_from_config(config)

    # ✅ Load the model checkpoint
    checkpoint_dir = cd
    model.load_checkpoint(config, checkpoint_dir=checkpoint_dir, eval=True)

    # ✅ Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"Using device: {device}")

    # ✅ Input text to synthesize
    text = txt

    # ✅ Speaker reference WAV (optional, for voice cloning)
    speaker_wav_path = swp

    # ✅ Run synthesis
    outputs = model.synthesize(
        text,
        config,
        speaker_wav=speaker_wav_path,
        gpt_cond_len=gcl,
        language=lang,
    )

    # ✅ Get audio and convert to NumPy
    wav = outputs["wav"]
    wav_numpy = wav.squeeze()

    # ✅ Save the generated audio
    output_path = op
    sf.write(output_path, wav_numpy, samplerate=config.audio.sample_rate)
    print(f"Saved synthesized audio to: {output_path}")

if __name__ == "__main__":
    main()