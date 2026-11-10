def show_menu() -> None: #this function prints out the menu
    print()
    print("=" * 40)
    print(" CLI fundamentals")
    print("=" * 40)
    print(" 1. placeholder A")
    print(" 2. Placeholder B")
    print(" q. Quit")
    print("=" * 40) #this one *40 it multiplies  = sign into 40 times instead of typing it manually.

def get_choice() -> str:   #this function acts as input collector.
    return input("Choose an option: ").strip().lower()

def handle_choice(choice: str) -> bool:     # this function handles the logic of the menu so it look sat what you've typed and decides what to show you
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