import os
import sys
import time
import datetime
import subprocess
import curses
import threading

# -------------------------
# CONFIGURATION
# -------------------------
boot_text = [
    "Initializing PythonOS...",
    "Loading kernel modules...",
    "Starting system services...",
    "Checking hardware...",
    "Welcome to PythonOS!"
]
boot_bg_color = "\033[40m"
boot_text_color = "\033[92m"
reset_color = "\033[0m"
version = "PythonOS v0.4 Terminal Edition"

# -------------------------
# UTILITY FUNCTIONS
# -------------------------
def clear():
    os.system('clear')

def print_colored(text, color="", bg=""):
    print(f"{bg}{color}{text}{reset_color}")

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
  net                - Show Wi-Fi networks
  update             - Run update script
  boottext           - Change booting text
  bootcolor          - Change boot background color
  boottextcolor      - Change boot text color
  echo <text> [col]  - Print text (optional color)
  filefx             - Open real file manager
  games              - Open games menu
  clock              - Open clock app
  pythonmaker        - Open PythonMaker editor
  exit               - Exit PythonOS
""")

def cmd_ver():
    print(version)

def cmd_net():
    try:
        subprocess.run(["nmcli", "dev", "wifi"], check=True)
    except FileNotFoundError:
        print("Error: nmcli not installed or Wi-Fi not available.")

def cmd_update():
    print("Running update script...")
    time.sleep(0.5)
    os.system("sudo bash ./update.sh")
    sys.exit()

def cmd_boottext():
    global boot_text
    print("Current boot lines:", len(boot_text))
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
    print("Colors: black, red, green, yellow, blue, magenta, cyan, white")
    color = input("Choose background color: ").strip().lower()
    colors = {
        "black":"\033[40m", "red":"\033[41m", "green":"\033[42m",
        "yellow":"\033[43m", "blue":"\033[44m", "magenta":"\033[45m",
        "cyan":"\033[46m", "white":"\033[47m"
    }
    boot_bg_color = colors.get(color, "\033[40m")
    print("Boot background color updated!")

def cmd_boottextcolor():
    global boot_text_color
    print("Colors: black, red, green, yellow, blue, magenta, cyan, white, bright_red, bright_green")
    color = input("Choose text color: ").strip().lower()
    colors = {
        "black":"\033[30m","red":"\033[31m","green":"\033[32m","yellow":"\033[33m",
        "blue":"\033[34m","magenta":"\033[35m","cyan":"\033[36m","white":"\033[37m",
        "bright_red":"\033[91m","bright_green":"\033[92m"
    }
    boot_text_color = colors.get(color, "\033[92m")
    print("Boot text color updated!")

def cmd_echo(args):
    if not args: 
        print("Usage: echo <text> [color]"); return
    text = " ".join(args[:-1]) if len(args)>1 else args[0]
    color_arg = args[-1] if len(args)>1 else ""
    colors = {
        "black":"\033[30m","red":"\033[31m","green":"\033[32m","yellow":"\033[33m",
        "blue":"\033[34m","magenta":"\033[35m","cyan":"\033[36m","white":"\033[37m",
        "bright_red":"\033[91m","bright_green":"\033[92m"
    }
    print_colored(text, colors.get(color_arg,""))

def cmd_filefx():
    try:
        subprocess.run(["ranger"], check=True)
    except FileNotFoundError:
        try:
            subprocess.run(["nautilus"], check=True)
        except FileNotFoundError:
            print("No file manager found (ranger/nautilus).")

# -------------------------
# GAMES
# -------------------------
def run_game_guess_number():
    import random
    number = random.randint(1,10)
    print("=== Guess the Number Game ===")
    while True:
        guess = input("Guess 1-10: ")
        if not guess.isdigit(): continue
        guess = int(guess)
        if guess == number: print("🎉 Correct!"); break
        print("Too low!" if guess<number else "Too high!")

def run_clock():
    try:
        while True:
            os.system('clear')
            print("=== Clock App ===")
            print(datetime.datetime.now().strftime("%H:%M:%S"))
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def games_menu():
    while True:
        print("\nGames Menu:\n1. Guess Number\n2. Back")
        choice = input("> ").strip()
        if choice=="1": run_game_guess_number()
        elif choice=="2": break

# -------------------------
# PYTHONMAKER EDITOR
# -------------------------
def python_maker(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    editor_win = curses.newwin(max_y, max_x//2, 0, 0)
    console_win = curses.newwin(max_y, max_x//2, 0, max_x//2)
    console_win.scrollok(True)
    console_win.idlok(True)
    code_lines = []
    running = [False]
    process_thread = [None]
    line_no = 0

    def run_code():
        try:
            local_vars={}
            exec("\n".join(code_lines), {}, local_vars)
        except Exception as e:
            console_win.addstr(f"Error: {e}\n"); console_win.refresh()

    def start_code():
        if running[0]: return
        running[0]=True
        console_win.addstr("Starting code...\n"); console_win.refresh()
        process_thread[0]=threading.Thread(target=run_code); process_thread[0].start()

    def stop_code():
        if not running[0]: return
        running[0]=False
        console_win.addstr("Stopped code.\n"); console_win.refresh()
        process_thread[0]=None

    def install_module():
        curses.echo()
        console_win.addstr("Module name: "); console_win.refresh()
        name = stdscr.getstr().decode("utf-8")
        console_win.addstr(f"Installing python-{name}...\n"); console_win.refresh()
        os.system(f"sudo pacman -S python-{name}")
        curses.noecho()

    while True:
        editor_win.clear()
        for i, line in enumerate(code_lines): editor_win.addstr(i,0,line)
        editor_win.addstr(line_no,0,""); editor_win.refresh(); console_win.refresh()
        key = stdscr.getch()
        if key==27:
            next_key = stdscr.getch()
            if next_key==49: start_code()
            elif next_key==50: stop_code()
            elif next_key==51: install_module()
        elif key in (curses.KEY_BACKSPACE,127):
            if code_lines and code_lines[line_no]: code_lines[line_no]=code_lines[line_no][:-1]
        elif key==curses.KEY_ENTER or key==10:
            code_lines.insert(line_no+1,""); line_no+=1
        elif key==curses.KEY_UP:
            if line_no>0: line_no-=1
        elif key==curses.KEY_DOWN:
            if line_no<len(code_lines)-1: line_no+=1
        elif key==27: break
        else:
            if line_no>=len(code_lines): code_lines.append("")
            code_lines[line_no]+=chr(key)

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
            print("\nExiting PythonOS..."); sys.exit()
        if not cmd_input: continue
        parts = cmd_input.split(); cmd = parts[0].lower(); args = parts[1:]

        if cmd=="help": show_help()
        elif cmd=="ver": cmd_ver()
        elif cmd=="net": cmd_net()
        elif cmd=="update": cmd_update()
        elif cmd=="boottext": cmd_boottext()
        elif cmd=="bootcolor": cmd_bootcolor()
        elif cmd=="boottextcolor": cmd_boottextcolor()
        elif cmd=="echo": cmd_echo(args)
        elif cmd=="filefx": cmd_filefx()
        elif cmd=="games": games_menu()
        elif cmd=="clock": run_clock()
        elif cmd=="pythonmaker": curses.wrapper(python_maker)
        elif cmd=="exit": print("Shutting down PythonOS..."); sys.exit()
        else: print(f"Unknown command '{cmd}'. Type 'help'.")

if __name__=="__main__":
    main()
