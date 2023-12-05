import json
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Function to ask the user if they appreciate the presented name via email
def ask_user_preference_via_email(name, email):
    # You might want to customize the email template
    subject = "Secret Santa Assignment"
    body = f"Hi,\n\nIs '{name}' present? (yes/no)\n\nBest regards,\nSecret Santa Bot"

    msg = MIMEMultipart()
    msg['From'] = 'your_email@gmail.com'  # Your Gmail address
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Use your Gmail credentials
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('sectercyberneticsanta@gmail.com', '##########')  # Your Gmail password
        smtp.sendmail('pederbs1@gmail.com', email, msg.as_string())

    user_input = input(f"An email has been sent to {email}. Please check your email and respond (yes/no): ")
    return user_input.lower() == 'yes'

# Main function
def main():
    filename = 'names_email.json'

    # Load existing names and emails from the file
    data = load_names(filename)
    names = data["names"]
    emails = data["emails"]

    # Select a random name
    selected_name = select_random_name(names)

    if selected_name is not None:
        while True:
            # Ask user for appreciation via email
            if selected_name in emails:
                email = emails[selected_name]
                if ask_user_preference_via_email(selected_name, email):
                    print(f"Great choice! '{selected_name}' can choose a gift!")
                    # Remove the selected name from the list
                    names.remove(selected_name)
                    # Save the updated names to the file
                    save_names(filename, {"names": names, "emails": emails})
                    break
                else:
                    print(f"No worries! '{selected_name}' is not present, trying again.")
                    # Select a new random name without removing the previous one
                    selected_name = select_random_name(names)
            else:
                print(f"No email found for '{selected_name}', trying again.")
                # Select a new random name without removing the previous one
                selected_name = select_random_name(names)

if __name__ == "__main__":
    main()
