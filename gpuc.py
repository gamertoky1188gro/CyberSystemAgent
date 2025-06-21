import torch

def main():
    print("CUDA available:", torch.cuda.is_available())
    print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")
    print("Supports half precision:", torch.cuda.get_device_capability(0) if torch.cuda.is_available() else "N/A")


if __name__ == "__main__":
    main()