import os
import colorama
import keyboard
from google import genai
from colorama import Fore, Style

colorama.init(autoreset=True)

def selector(options=None):
    if options is None:
        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    selected = 0

    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def show_menu():
        clear()
        print("Use ↑ ↓ to move and Enter to select:\n")
        for i, option in enumerate(options):
            if i == selected:
                print(Fore.GREEN + f"> {option} <" + Style.RESET_ALL)
            else:
                print(f"  {option}")

    show_menu()

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "up":
                selected = (selected - 1) % len(options)
                show_menu()
            elif event.name == "down":
                selected = (selected + 1) % len(options)
                show_menu()
            elif event.name == "enter":
                clear()
                print(Fore.CYAN + f"You selected: {options[selected]}" + Style.RESET_ALL)
                return selected

# Initialize Gemini client
client = genai.Client(api_key="API")

def send(fileUpload=False, file="gemini.py", content="Can you tell me about the instruments in this photo?", modelindex=None):
    # Get model names
    models = client.models.list()
    model_names = [model.name.replace("models/", "") for model in models]  # Use .name to get string

    if modelindex is not None:
        selected_index = modelindex
    else:
        # Use selector to choose a model
        selected_index = selector(model_names)

    selected_model = model_names[selected_index]

    # Final output
    print("Final selected model:", selected_model)

    if fileUpload is not False:
        myfile = client.files.upload(file=file)
        print(f"{myfile=}")
        result = client.models.generate_content(
            model=selected_model,
            contents=[
                myfile,
                "\n\n",
                content,
            ],
        )

        print("response:")
        print(f"{result.text=}")
        return result
    else:
        response = client.models.generate_content(
            model=selected_model, contents=content
        )

        print("response:")
        print(response.text)
        return response


if __name__ == "__main__":
    print(send(fileUpload=True, file="gemini.py", content="explain it"))