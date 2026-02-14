import os
import sys
import time
import subprocess

# -------------------------
# CONFIGURATION (default)
# -------------------------
boot_text = [
    "Initializing PythonOS...",
    "Loading kernel modules...",
    "Starting system services...",
    "Checking hardware...",
    "Welcome to PythonOS!"
]
boot_bg_color = "\033[40m"   # Black background
boot_text_color = "\033[92m" # Bright green text
reset_color = "\033[0m"

# -------------------------
# UTILITY FUNCTIONS
# -------------------------
def clear():
    os.system('clear')

def print_colored(text, color="", bg=""):
    print(f"{bg}{color}{text}{reset_color}")

# Boot screen animation
def boot_screen():
    clear()
    for line in boot_text:
        print_colored(line, boot_text_color, boot_bg_color)
        time.sleep(0.5)
    print_colored("\nBooting: [", boot_text_color, boot_bg_color)
    for _ in range(20):
        print_colored("█", boot_text_color, boot_bg_color)
        time.sleep(0.05)
    print_colored("] Done!\n", boot_text_color, boot_bg_color)
    time.sleep(0.3)
    clear()

# -------------------------
# COMMANDS
# -------------------------
def show_help():
    print("""
Available commands:
  help               - Show this help
  ver                - Show PythonOS version
  net                - Show Wi-Fi networks (requires nmcli)
  update             - Run update script (sudo bash ./update.sh)
  boottext           - Change booting text
  bootcolor          - Change boot background color
  boottextcolor      - Change boot text color
  echo <text>        - Echo text
  echo <text> <col>  - Echo text with color
  filefx             - Open real file manager (ranger or nautilus)
  exit               - Exit PythonOS
""")

def cmd_ver():
    print("PythonOS v0.3 (Terminal Edition)")

def cmd_net():
    try:
        subprocess.run(["nmcli", "dev", "wifi"], check=True)
    except FileNotFoundError:
        print("Error: nmcli not installed or Wi-Fi not available.")

def cmd_update():
    print("Running update script...")
    time.sleep(0.5)
    # Close PythonOS and run the script
    os.system("sudo bash ./update.sh")
    sys.exit()

def cmd_boottext():
    global boot_text
    print("Current boot text lines:", len(boot_text))
    boot_text = []
    print("Enter new boot lines (empty line to finish):")
    while True:
        line = input("> ")
        if line == "":
            break
        boot_text.append(line)
    print("Boot text updated!")

def cmd_bootcolor():
    global boot_bg_color
    print("Available colors: black, red, green, yellow, blue, magenta, cyan, white")
    color = input("Choose background color: ").strip().lower()
    colors = {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
    }
    boot_bg_color = colors.get(color, "\033[40m")
    print("Boot background color updated!")

def cmd_boottextcolor():
    global boot_text_color
    print("Available colors: black, red, green, yellow, blue, magenta, cyan, white, bright_green, bright_red")
    color = input("Choose text color: ").strip().lower()
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
    }
    boot_text_color = colors.get(color, "\033[92m")
    print("Boot text color updated!")

def cmd_echo(args):
    if not args:
        print("Usage: echo <text> [color]")
        return
    text = " ".join(args[:-1]) if len(args) > 1 else args[0]
    color_arg = args[-1] if len(args) > 1 else ""
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
    }
    color_code = colors.get(color_arg, "")
    print_colored(text, color_code)

def cmd_filefx():
    # Try to open ranger if installed, fallback to nautilus
    try:
        subprocess.run(["ranger"], check=True)
    except FileNotFoundError:
        try:
            subprocess.run(["nautilus"], check=True)
        except FileNotFoundError:
            print("No file manager found (ranger or nautilus).")

# -------------------------
# MAIN LOOP
# -------------------------
def main():
    boot_screen()
    show_help()
    while True:
        try:
            cmd_input = input("PythonOS> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting PythonOS...")
            sys.exit()
        if not cmd_input:
            continue
        parts = cmd_input.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "help":
            show_help()
        elif cmd == "ver":
            cmd_ver()
        elif cmd == "net":
            cmd_net()
        elif cmd == "update":
            cmd_update()
        elif cmd == "boottext":
            cmd_boottext()
        elif cmd == "bootcolor":
            cmd_bootcolor()
        elif cmd == "boottextcolor":
            cmd_boottextcolor()
        elif cmd == "echo":
            cmd_echo(args)
        elif cmd == "filefx":
            cmd_filefx()
        elif cmd == "exit":
            print("Shutting down PythonOS...")
            sys.exit()
        else:
            print(f"Unknown command '{cmd}'. Type 'help'.")

if __name__ == "__main__":
    main()
