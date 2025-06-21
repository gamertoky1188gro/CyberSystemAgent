import keyboard


class HotkeyListener:
    current_word = ""

    @staticmethod
    def keyc(Hotkeys=None):
        if Hotkeys is None:
            Hotkeys = [
                "ctrl+c",
                "ctrl+v",
                "alt+f4",
                "ctrl+alt+del",
                "win+d",
                "ctrl+shift+esc"
            ]

        def handle_shortcut(hotkey):
            print(f"[+] Detected hotkey: {hotkey}")

        # Register each hotkey
        for hotkey in Hotkeys:
            keyboard.add_hotkey(hotkey, handle_shortcut, args=(hotkey,))

        # Word typing tracker
        def on_key_press(e):
            if len(e.name) == 1:
                HotkeyListener.current_word += e.name
            elif e.name == 'backspace':
                HotkeyListener.current_word = HotkeyListener.current_word[:-1]

            clear = False

            while clear is True:
                HotkeyListener.current_word = ""
                clear = False

            while e.name:
                if HotkeyListener.current_word:
                    print(f"[+] Current word: {HotkeyListener.current_word}")
                    return HotkeyListener.current_word
                break

        keyboard.on_press(on_key_press)


# Start the listener
HotkeyListener.keyc()

print("Tracking hotkeys and words... Press ESC to stop.")
while True:
    if keyboard.is_pressed("esc") or keyboard.is_pressed("ctrl+c"):
        break
