# Gemini Voice Assistant

A modular, extensible voice assistant for Windows, featuring speech-to-text (STT), text-to-speech (TTS), AI-powered content generation, and advanced automation capabilities.

## Features

- **Speech-to-Text (STT):** Uses OpenAI Whisper for accurate audio transcription from file or microphone.
- **Text-to-Speech (TTS):** High-quality voice synthesis using XTTS-v2, with support for long texts and multiple languages.
- **AI Content Generation:** Integrates with Google Gemini for advanced text and file-based AI responses.
- **Automation:** Control mouse, keyboard, and system actions programmatically.
- **Custom GUI:** Frameless, rounded-corner PyQt5 window for notifications or assistant UI.
- **Extensible:** Modular codebase for easy addition of new features and integrations.

## Requirements

- Windows OS
- [PyTorch](https://pytorch.org/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [TTS (Coqui XTTS)](https://github.com/coqui-ai/TTS)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [sounddevice](https://pypi.org/project/sounddevice/)
- [colorama](https://pypi.org/project/colorama/)
- [keyboard](https://pypi.org/project/keyboard/)
- [pyautogui](https://pypi.org/project/pyautogui/)
- [tiktoken](https://pypi.org/project/tiktoken/)
- [Flask](https://pypi.org/project/Flask/)
- [scipy](https://pypi.org/project/scipy/)
- [requests](https://pypi.org/project/requests/)

## Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/gamertoky1188gro/CyberSystemAgent.git
   cd <folder>
   ```

2. **Create two virtual environments:**
   - For Python 3.12:
     ```
     python -m venv .venv
     .venv\Scripts\activate
     pip install -r .\venv.txt
     ```
   - For Python 3.10:
     ```
     python3.10 -m venv .venv310
     .venv310\Scripts\activate
     pip install -r .\venv310.txt
     ```

   **Note:** Sometimes package version or torch errors may occur. If you get a torch error, remove torch from the txt files and manually install a compatible version. If you have issues with all package versions, try to fix them; if you can't, remove `==<ver>` from every package name in the requirements files.

3. **Configure API keys:**
   - For Gemini integration, set your Google API key in `gemini.py` at line 43, inside the string for the `api_key` section.

## How to Run

After setting up your virtual environments and installing dependencies, activate the appropriate environment for your task:

- For running all files except TTS files (like `tts.py`), use Python 3.12:
  ```
  .venv\Scripts\activate
  ```
- For running TTS files (like `tts.py`), use Python 3.10:
  ```
  .venv310\Scripts\activate
  ```

Then run the desired module:

- **Main Gemini Agent App:**
  ```
  python "really main.py"
  ```
  This is the main orchestrator for the Gemini Voice Assistant. After running, it acts as the core agent, handling:
  - Voice command listening and processing
  - Speech-to-text (STT) and text-to-speech (TTS) integration
  - AI-powered content generation using Gemini
  - Automation tasks (mouse, keyboard, system actions)
  - GUI notifications (if enabled)
  - Task parsing and coordination between modules

  **Configuration options:**
  - To use Whisper, set `var2 = True` at line 175 in `really main.py`.
  - To use input, set `var2 = False` at line 175 in `really main.py`.
  - To use TTS for AI reply, set `var = True` at line 484 in `really main.py`.
  - To use the GUI to print messages, set `var = False` at line 484 in `really main.py`.

- **Speech-to-Text (STT) CLI:**
  ```
  python main.py --file true
  ```
- **Text-to-Speech (TTS) Server:**
  ```
  python tts.py
  ```
- **AI Content Generation (as module):**
  ```python
  from gemini import send
  response = send(content="Your prompt here")
  ```
- **Automation (as module):**
  ```python
  from curtp import Mouse, Keyboard
  mouse = Mouse()
  keyboard = Keyboard()
  mouse.move(100, 100)
  keyboard.s("Hello!")
  ```
- **Custom GUI Window:**
  ```
  python wellwhatnameicansetuhmmidontknowwellthennonthing.py
  ```

## Usage

### Speech-to-Text (STT)

Run the CLI app to transcribe audio:

```
python main.py --file true
```
- Use `--file false` to record from the microphone.

**CLI Options:**
- `--file` (default: true): Set to false to use mic
- `--rs` (default: false): Use RAM storage (true/false)
- `--keep`: Keep audio file if not in RAM

### Text-to-Speech (TTS)

Start the TTS server:
```
python tts.py
```
Send a POST request to `http://localhost:9900/synthesize` with your text and config.

**Request Example:**
```json
POST /synthesize
Content-Type: application/json
{
  "lj": "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/XTTS-v2/config.json",
  "cd": "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/XTTS-v2",
  "content": "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
  "sw": "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/downloads/Adele - Hello (Muslim Version by Omar Esa) ｜ Vocals Only_processed.wav",
  "gcl": 3,
  "lang": "en"
}
```
**Response Example:**
```json
{
  "status": "success",
  "chunks": 1,
  "message": "Successfully synthesized and played 1 chunks."
}
```

### AI Content Generation

Use `gemini.py` as a module to send text or files to Gemini and receive responses. Example:
```python
from gemini import send
response = send(content="Your prompt here")
```

### Automation

Use `curtp.py` as a module for mouse and keyboard automation. Example:
```python
from curtp import Mouse, Keyboard
mouse = Mouse()
keyboard = Keyboard()
mouse.move(100, 100)
keyboard.s("Hello!")
```

## File Structure

- `main.py` - Whisper STT CLI
- `tts.py` - XTTS TTS server and synthesis
- `gemini.py` - Gemini AI integration
- `curtp.py` - Mouse/keyboard automation
- `wellwhatnameicansetuhmmidontknowwellthennonthing.py` - PyQt5 frameless window
- `really main.py` - Main orchestrator (task parsing, integration)
- `XTTS-v2/` - XTTS model files

## Configuration Tips

- To use Whisper, set `var2 = True` at line 175 in `really main.py`.
- To use input, set `var2 = False` at line 175 in `really main.py`.
- To use TTS for AI reply, set `var = True` at line 484 in `really main.py`.
- If you want to use the GUI to print messages, set `var = False` at line 484 in `really main.py`.

## License

This project is for educational and personal use. See individual model licenses for details.
