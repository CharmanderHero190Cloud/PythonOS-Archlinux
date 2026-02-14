import os
import datetime
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    print("""
Available commands:
  help      - Show this help message
  time      - Show current date and time
  echo      - Echo back your message
  clear     - Clear the screen
  exit      - Exit PythonOS
""")

def main():
    clear()
    print("=== Welcome to PythonOS v0.1 ===")
    print("Type 'help' to see available commands.\n")

    while True:
        command = input("PythonOS> ").strip()

        if command == "help":
            show_help()

        elif command == "time":
            now = datetime.datetime.now()
            print("Current date & time:", now)

        elif command.startswith("echo "):
            print(command[5:])

        elif command == "clear":
            clear()

        elif command == "exit":
            print("Shutting down PythonOS...")
            sys.exit()

        elif command == "":
            continue

        else:
            print("Unknown command. Type 'help' for list of commands.")

if __name__ == "__main__":
    main()

