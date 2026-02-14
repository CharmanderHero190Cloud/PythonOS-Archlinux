import time
import os
import sys

# Utility: clear screen
def clear():
    os.system('clear')

# Boot screen animation
def boot_screen():
    clear()
    boot_messages = [
        "Initializing PythonOS...",
        "Loading kernel modules...",
        "Starting system services...",
        "Checking hardware...",
        "Welcome to PythonOS v0.2!"
    ]
    for msg in boot_messages:
        print(msg)
        time.sleep(0.7)
    # Fake loading bar
    print("\nBooting: [", end="")
    for i in range(20):
        print("█", end="", flush=True)
        time.sleep(0.1)
    print("] Done!\n")
    time.sleep(0.5)

# Show help
def show_help():
    print("""
Available commands:
  help      - Show this help message
  time      - Show current date and time
  echo      - Echo back your message
  apps      - List simple apps
  run <app> - Run an app
  clear     - Clear the screen
  exit      - Exit PythonOS
""")

# Simple apps dictionary
def app_clock():
    try:
        while True:
            clear()
            print("=== PythonOS Clock App ===\n")
            print("Current time:", time.strftime("%H:%M:%S"))
            print("\nPress Ctrl+C to exit app.")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def app_guess_number():
    import random
    number = random.randint(1, 10)
    print("=== Guess the Number App ===")
    print("I chose a number between 1 and 10. Try to guess it!")
    while True:
        guess = input("Your guess: ")
        if not guess.isdigit():
            print("Please enter a number!")
            continue
        guess = int(guess)
        if guess == number:
            print("🎉 Correct! You win!")
            break
        elif guess < number:
            print("Too low!")
        else:
            print("Too high!")

apps = {
    "clock": app_clock,
    "guess": app_guess_number
}

# Main terminal loop
def main():
    boot_screen()
    show_help()
    while True:
        command = input("PythonOS> ").strip()
        if command == "help":
            show_help()
        elif command == "time":
            print("Current time:", time.strftime("%Y-%m-%d %H:%M:%S"))
        elif command.startswith("echo "):
            print(command[5:])
        elif command == "clear":
            clear()
        elif command == "apps":
            print("Available apps:", ", ".join(apps.keys()))
        elif command.startswith("run "):
            app_name = command[4:].strip()
            if app_name in apps:
                apps[app_name]()
            else:
                print(f"App '{app_name}' not found.")
        elif command == "exit":
            print("Shutting down PythonOS...")
            sys.exit()
        elif command == "":
            continue
        else:
            print("Unknown command. Type 'help' for commands.")

if __name__ == "__main__":
    main()
