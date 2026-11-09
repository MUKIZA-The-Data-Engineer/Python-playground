def show_menu() -> None:
    print()
    print("=" * 40)
    print(" CLI fundamentals")
    print("=" * 40)
    print(" 1. placeholder A")
    print(" 2. Placeholder B")
    print(" q. Quit")
    print("=" * 40)

def get_choice() -> str:
    return input("Choose an option: ").strip().lower()

def handle_choice(choice: str) -> bool:
    """Return True to Keep looping, False to quit"""
    if choice == "1":
        print("[stub] you Picked A. ")
    elif choice == "2":
        print("[stub] You picked B. ")
    elif choice == "q":
        return False
    else:
        print(f"[!] Unkown option: {choice!r}")
    return True

def main()-> None:
    print("Welcome. Press q to quit. ")
    running =True
    while running:
        show_menu()
        choice = get_choice()
        running = handle_choice(choice)
        print("Good bye")
        
if __name__ == "__main__":
        try:
            main()
        except KeyboardInterrupt: 
            print("\nInterrupted. Goodbye. ")