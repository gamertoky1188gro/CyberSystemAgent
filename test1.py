import main

def t():
    print(main.Fore.CYAN + "[Whisper STT CLI App]")
    print(main.Fore.MAGENTA + f"Detected device: {main.device.upper()}")

    main.select_model()
    print(main.Fore.GREEN + f"✔ Model selected: {main.models[main.model_index]}")

    if main.args.file.lower() == "true":
        print(main.Fore.YELLOW + "\n[*] Choose audio file from file picker...")
        file_path = main.select_audio_file()
        if not file_path:
            print(main.Fore.RED + "[!] No file selected. Exiting.")
            main.sys.exit()
    else:
        file_path = main.record_from_mic()

    main.transcribe_file(file_path)
    print(main.Fore.CYAN + "\n[✔] Transcription completed. Exiting.")


if __name__ == "__main__":
    t()