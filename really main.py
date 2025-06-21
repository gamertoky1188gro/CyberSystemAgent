import json
import os
import re
import sys
import time

import pyautogui
import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

import curtp
import main
import wellwhatnameicansetuhmmidontknowwellthennonthing
from gemini import send, Fore

queued_tasks = []
filefile = False

def parse_all_ai_responses(response_text: str):
    """
    Extracts all 'task' and 'arg' blocks from AI-generated text wrapped in ```json ... ``` sections.
    Returns: list of (task: str, arg: dict)
    """
    results = []
    json_blocks = re.findall(r'```json\s*({[\s\S]*?})\s*```', response_text)

    for json_str in json_blocks:
        try:
            data = json.loads(json_str)
            task = data.get("task")
            arg = data.get("arg", {})
            if task:
                results.append((task, arg))
        except json.JSONDecodeError as e:
            print("[!] JSON decode error:", e)
            continue

    return results


def handle_task(task, arg):
    global queued_tasks, history, filefile

    mouse = curtp.Mouse()
    keyboard = curtp.Keyboard()

    if task == "cursor_move":
        x = arg.get("x")
        y = arg.get("y")
        if x is not None and y is not None:
            print(f"Moving cursor to ({x}, {y})")
            mouse.smooth_move(x=x, y=y)
        else:
            print("[!] Invalid cursor_move arguments")
    elif task == "click":
        button = arg.get("button")
        print(f"Clicking {button} button")
        mouse.click(button=button)
    elif task == "drag_and_drop":
        to_x = arg.get("to_x")
        to_y = arg.get("to_y")
        if to_x is not None and to_y is not None:
            print(f"Dragging to ({to_x}, {to_y})")
            mouse.drag_and_drop(to_x=to_x, to_y=to_y)
        else:
            print("[!] Invalid drag_and_drop arguments")
    elif task == "scroll":
        steps = arg.get("steps", 1)
        upordown = arg.get("upordown", "down")
        print(f"Scrolling {upordown} by {steps} steps")
        mouse.smooth_scroll(amount=steps, upordown=upordown)
    elif task == "scroll_horizontal":
        steps = arg.get("steps", 1)
        direction = arg.get("direction", "right")
        print(f"Scrolling horizontally {direction} by {steps} steps")
        mouse.smooth_scroll_horizontal(amount=steps, direction=direction)
    elif task == "press_key":
        key = arg.get("key")
        if key:
            print(f"Pressing key: {key}")
            mouse.press_key(vk_code=key)
        else:
            print("[!] Invalid press_key arguments")
    elif task == "page_up":
        steps = arg.get("steps", 1)
        print(f"Page up by {steps} steps")
        mouse.smooth_page_up(steps=steps)
    elif task == "page_down":
        steps = arg.get("steps", 1)
        print(f"Page down by {steps} steps")
        mouse.smooth_page_down(steps=steps)
    elif task == "skc":
        key_combo = arg.get("key")
        if key_combo:
            print(f"Pressing key combination: {key_combo}")
            keyboard.skc(key=key_combo)
        else:
            print("[!] Invalid skc arguments")
    elif task == "s":
        sentence = arg.get("sen")
        if sentence:
            print(f"Typing sentence: {sentence}")
            keyboard.s(sen=sentence)
        else:
            print("[!] Invalid s arguments")
    elif task == "ps":
        command = arg.get("command")
        admin = arg.get("admin", False)
        if not command:
            print("[!] Invalid PowerShell command")
            return

        print(f"Running PowerShell command: {command} with admin={admin}")

        if admin:
            # Run with admin rights by launching powershell with RunAs verb
            os.system(
                f'powershell Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command \\"{command}\\"" -Verb RunAs')
        else:
            # Run normally
            os.system(f'powershell -NoProfile -ExecutionPolicy Bypass -Command "{command}"')
    elif task == "screenshot":
        filefile = True  # Set flag to indicate screenshot task
        print("Taking screenshot...")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        print("Screenshot saved as screenshot.png")
    elif task == "New Chat":
        print(Fore.CYAN + "Starting a new chat session...")

        # Validate task list structure
        if isinstance(arg, dict) and "task" in arg and isinstance(arg["task"], list):
            # Add New Chat initiation to history
            history.append({
                "role": "system",
                "input": f"New Chat (code: {arg.get('code')}) with tasks: {arg.get('task', [])}",
                "output": json.dumps({
                    "task": "New Chat",
                    "arg": arg
                }, indent=2)
            })

            # Queue the tasks
            queued_tasks = arg["task"]
            print(Fore.YELLOW + f"Queued tasks: {queued_tasks}")
        else:
            print(Fore.RED + "Invalid New Chat task structure.")


def show_window_with_parts(text):
    app = QApplication(sys.argv)
    window = wellwhatnameicansetuhmmidontknowwellthennonthing.FramelessWindow()
    window.show()

    parts = [p.strip() for p in re.split(r'[,.!?;:\n]', text) if p.strip()]
    interval_ms = 1050  # delay between messages in ms

    for i, part in enumerate(parts):
        QTimer.singleShot(i * interval_ms, lambda p=part: window.setContent(p))

    # Close window after last message + 1 second buffer
    total_duration = len(parts) * interval_ms + 1000
    QTimer.singleShot(total_duration, window.close)

    app.exec_()


def Main(historya=[], forced_input=None):
    global filefile

    print(Fore.CYAN + "[WIN Voice CLI App]")
    history = historya
    transcript = ""
    var2 = False

    if var2:
        print(Fore.MAGENTA + f"Detected device: {main.device.upper()}")

        time.sleep(1)

        main.select_model(3)
        print(Fore.GREEN + f"✔ Model selected: {main.models[main.model_index]}")

        time.sleep(1)

        file_path = main.record_from_mic(micindex=5)
        transcript = main.transcribe_file(file_path)
    else:
        if forced_input:
            var3 = forced_input
        else:
            var3 = input(Fore.YELLOW + "Enter transcript text: ")

        transcript = var3.strip()

    user_name = "ccm"
    user_role = "moderator"
    user_expertise = "none"
    language = "Detect language from user_input and reply in that language."
    current_task = "extract current task from: " + transcript
    user_input = transcript

    contentl = f"""
You are an advanced AI assistant named CyberSystemAgent, designed to help users with tasks such as coding, system control, answering questions, and solving problems intelligently.

Your output should always follow these strict formatting and behavior rules:

After each GUI task, you must verify success by taking a screenshot and if failure is detected (e.g., wrong page opened), retry the previous step or adjust.

Examples:

If a website fails to open, simulate pressing Enter after URL.

If Chrome doesn't open, re-run the PowerShell command.

For each task in the task list, provide a complete JSON block with "task" and "arg" fields filled properly.

Example:
{{
  "task": "skc",
  "arg": {{"key": "win+d" }}
}}

If you cannot provide full details for any task, respond with "I don't know".

- After completing each task, take a screenshot to verify the task's success.
- If verification shows the task was not successful (e.g., the expected UI change is not visible), retry the task until it completes correctly.
- Only proceed to the next task once the current task is successfully verified by the screenshot.
- Always include the screenshot task as the final step in each task sequence for verification purposes.

### 🔧 Output Formatting Guidelines:

- **Always** wrap each JSON request inside triple backticks with a `json` label, like:
  ```json
  {{
    "task": "cursor_move",
    "arg": {{"x": 300, "y": 500}}
  }}
````

* **Only use `task: "New Chat"`** if the instruction involves:

  * **Multiple separate steps**, or
  * **A mix of different task types** (e.g., GUI + command line), or
  * **Code 2** (advanced/multi-action task group).
    In this case, start with:

  ```json
  {{
    "task": "New Chat",
    "arg": {{
      "code": "2",
      "task": ["task1", "task2", "task3"]
    }}
  }}
  ```

* **Never use `New Chat`** for simple one-step tasks (code 1 or single instruction).

* **Only include a screenshot task (`task: "screenshot"`)** if the user’s command clearly involves a **GUI-based** interaction (e.g., clicking, dragging, cursor movement).

* For answering questions, **use natural language directly** unless the user explicitly asks you to type it in a text field — in that case, use:

  ```json
  {{
    "task": "s",
    "arg": {{
      "sen": "Your sentence here."
    }}
  }}
  ```

* Always **end** with a final summary like:

  ```json
  {{
    "task": "done",
    "arg": {{
      "summary": "Brief description of what was accomplished."
    }}
  }}
  ```

---

### 🧠 Context:

User Info:

* Name: {user_name}
* Role: {user_role}
* Expertise Level: {user_expertise}

Session Info:

* Current Task: {current_task}
* Previous Tasks / Sessions / History:
  {json.dumps(history, indent=2)}

---

### 🔌 Task Format Reference:

* PowerShell command:

  ```json
  {{
    "task": "ps",
    "arg": {{
      "command": "<powershell_command>",
      "admin": true or false
    }}
  }}
  ```

* Cursor movement:

  ```json
  {{
    "task": "cursor_move",
    "arg": {{
      "x": <x>,
      "y": <y>
    }}
  }}
  ```

* Mouse click:

  ```json
  {{
    "task": "click",
    "arg": {{
      "button": "left" or "right" or "middle"
    }}
  }}
  ```

* Drag and drop:

  ```json
  {{
    "task": "drag_and_drop",
    "arg": {{
      "to_x": <x>,
      "to_y": <y>
    }}
  }}
  ```

* Scroll vertically:

  ```json
  {{
    "task": "scroll",
    "arg": {{
      "steps": <int>,
      "upordown": "up" or "down"
    }}
  }}
  ```

* Scroll horizontally:

  ```json
  {{
    "task": "scroll_horizontal",
    "arg": {{
      "steps": <int>,
      "direction": "left" or "right"
    }}
  }}
  ```

* Key press:

  ```json
  {{
    "task": "press_key",
    "arg": {{
      "key": "<key_name>"
    }}
  }}
  ```

* Page up/down:

  ```json
  {{
    "task": "page_up",
    "arg": {{
      "steps": <int>
    }}
  }}
  ```

  or

  ```json
  {{
    "task": "page_down",
    "arg": {{
      "steps": <int>
    }}
  }}
  ```

* Shortcut keys:

  ```json
  {{
    "task": "skc",
    "arg": {{
      "key": "ctrl+c"  // Use + to join key combo
    }}
  }}
  ```

* Type a sentence:

  ```json
  {{
    "task": "s",
    "arg": {{
      "sen": "Your message here."
    }}
  }}
  ```

---

### 🧾 Rules:

* Respond in {language}.
* Never guess — if unsure, say: `"I don't know"`.
* Use natural language for answering general questions unless typing is explicitly needed.
* Always give a proper summary at the end describing what you did or accomplished.
* If code is requested or needed, always wrap in triple backticks (` ``` `) with a language label (e.g., `python`, `bash`).
- DO NOT use "task": "s" (typing a sentence) to answer regular questions. Only use it if:
  - The user clearly says: "type", "write", or "input" something.
  - The context implies you're interacting with a GUI element or form.

- For general responses to voice/text questions, respond normally using natural language, and summarize with a "task": "done" only.


---

### 🎤 Input:

{user_input}
"""

    def send_ai_request(attach_file: bool = False, file_path: str = None):
        kwargs = {
            "fileUpload": attach_file,
            "content": contentl,
            "modelindex": 23
        }

        if attach_file and file_path:
            kwargs["file"] = file_path

        return send(**kwargs)

    response = send_ai_request(attach_file=filefile, file_path="screenshot.png" if filefile else None)

    if filefile:
        filefile = False  # Reset file flag after sending
        os.remove("screenshot.png")  # Clean up screenshot file

    history.append({
        "role": "user",
        "input": user_input,
        "output": response.text
    })

    print("tasks:")
    tasks = parse_all_ai_responses(response.text)
    for task, arg in tasks:
        print(f"Task: {task}, Arg: {arg}")
        handle_task(task, arg)

    var = False  # Set to False to test the GUI text update logic

    if var:
        url = 'http://127.0.0.1:9900/synthesize'

        payload = {
            "lj": "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/XTTS-v2/config.json",
            "cd": "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/XTTS-v2",
            "content": response.text,
            "sw": "C:/Users/tokyi/PycharmProjects/Gemini voice assistant/downloads/Adele - Hello (Muslim Version by Omar Esa) ｜ Vocals Only_processed.wav",
            "gcl": 3,
            "lang": "en"
        }

        res = requests.post(url, json=payload)

        print("Status:", res.status_code)
        try:
            print("Response:", res.json())
        except Exception:
            print("Raw response:", res.text)
    else:
        show_window_with_parts(response.text)


if __name__ == "__main__":
    history = []
    my = True
    queued_tasks = []

    while my:
        try:
            if queued_tasks:
                next_task_input = queued_tasks.pop(0)
                print(Fore.MAGENTA + f"Executing queued task: {next_task_input}")
                Main(history, forced_input=next_task_input)
            else:
                Main(history)
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            time.sleep(2)
            print(Fore.YELLOW + "Restarting...")
            continue

        if not queued_tasks:
            cont = input(Fore.GREEN + "Do you want to continue? (yes/no): ").strip().lower()
            if cont != 'yes':
                my = False
                print(Fore.CYAN + "Exiting...")
                print(history)

