import json
import random
import time

# Function to load names from the JSON file
def load_names(filename):
    try:
        with open(filename, 'r') as file:
            names = json.load(file)
        return names
    except FileNotFoundError:
        return []

# Function to save names to the JSON file
def save_names(filename, names):
    with open(filename, 'w') as file:
        json.dump(names, file, indent=2)

# Function to select a random name
def select_random_name(names):
    if not names:
        print("No names available. It is Christmas!")
        return None

    print("Selecting a random name...")
    time.sleep(1)  # Animation: Wait for 1 second
    print("...")
    time.sleep(1)  # Animation: Wait for 1 second
    print("...")
    time.sleep(1)  # Animation: Wait for 1 second

    return random.choice(names)

# Function to ask the user if they appreciate the presented name
def ask_user_preference(name):
    user_input = input(f"Is '{name}' present? (yes/no): ")
    return user_input.lower() == 'yes'

# Main function
def main():
    filename = 'names.json'

    # Load existing names from the file
    names = load_names(filename)

    # Select a random name
    selected_name = select_random_name(names)

    if selected_name is not None:
        while True:
            # Ask user for appreciation
            if ask_user_preference(selected_name):
                print(f"Great choice! '{selected_name}' can choose a gift!")
                # Remove the selected name from the list
                names.remove(selected_name)
                # Save the updated names to the file
                save_names(filename, names)
                break
            else:
                print(f"No worries! '{selected_name}' is not present, trying again.")
                # Select a new random name without removing the previous one
                selected_name = select_random_name(names)

if __name__ == "__main__":
    main()