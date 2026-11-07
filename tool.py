
#!/usr/bin/env python3

import os
import sys
import time
import random
import smtplib
import webbrowser
from pathlib import Path
from email.message import EmailMessage
from getpass import getpass

BASE = Path(__file__).resolve().parent
RED = "\033[1;31m"
GREEN = "\033[1;32m"
WHITE = "\033[1;37m"
CYAN = "\033[1;36m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"


def load_file(path):
    data = {}
    if not path.exists():
        return data

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()

    return data


CONFIG = load_file(BASE / "config.txt")
SECRETS = load_file(BASE / ".env")


def clear():
    os.system("clear")


def logo():
    clear()
    name = "ＴＨＥ　ＰＡＩＮ　ＴＤＬ"

    for _ in range(3):
        glitch = list(name)
        index = random.randrange(len(glitch))
        glitch[index] = random.choice(["▓", "▒", "█", "░"])
        print("\r" + RED + BOLD + "".join(glitch) + RESET,
              end="", flush=True)
        time.sleep(0.12)

    print("\r" + RED + BOLD + name + RESET)
    print(CYAN + "       CYBER GLITCH TERMINAL" + RESET)
    print(GREEN + "       [ SYSTEM ONLINE ]" + RESET)
    print(GRAY + "       VERSION 1.0.0" + RESET)
    print()


def pause():
    input(WHITE + "\nPress ENTER to continue..." + RESET)


def back():
    print(WHITE + "\n0. BACK" + RESET)
    return input("\nroot@the-pain:~$ ").strip() == "0"


def valid_phone(number):
    digits = "".join(c for c in number if c.isdigit())
    return 8 <= len(digits) <= 15


def open_form():
    url = CONFIG.get(
        "SUPPORT_FORM",
        "https://www.whatsapp.com/contact/"
    )
    print(GREEN + "\nOpening WhatsApp contact page..." + RESET)
    webbrowser.open(url)
    pause()


def send_email(subject, body):
    sender = SECRETS.get("GMAIL_ADDRESS", "")
    password = SECRETS.get("GMAIL_APP_PASSWORD", "")
    recipient = CONFIG.get("SUPPORT_EMAIL", "")

    if not sender or not password or not recipient:
        print(RED + "\nEmail is not configured." + RESET)
        print(WHITE + "Configure your private .env file and a verified")
        print("support email in config.txt." + RESET)
        pause()
        return

    print(CYAN + "\nEmail preview:" + RESET)
    print("From:", sender)
    print("To:", recipient)
    print("Subject:", subject)
    print("\n" + body)

    print(WHITE + "\n1. SEND THIS ONE EMAIL")
    print("2. CANCEL" + RESET)

    choice = input("\nroot@the-pain:~$ ").strip()

    if choice != "1":
        print(GRAY + "Cancelled. Nothing was sent." + RESET)
        pause()
        return

    confirm = input(
        RED + "Type SEND to confirm: " + RESET
    ).strip()

    if confirm != "SEND":
        print(GRAY + "Cancelled." + RESET)
        pause()
        return

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sender, password)
            smtp.send_message(message)

        print(GREEN + "\nEmail sent successfully." + RESET)

    except Exception as error:
        print(RED + "\nEmail could not be sent." + RESET)
        print("Check your Gmail setup and internet connection.")
        print(GRAY + str(error) + RESET)

    pause()


def request_tool(mode):
    logo()

    if mode == "BAN":
        print(RED + BOLD + "THE PAIN BAN TOOL" + RESET)
        print("Prepare a factual privacy complaint.")
    else:
        print(GREEN + BOLD + "THE PAIN UNBAN TOOL" + RESET)
        print("Prepare an account review request.")

    number = input(CYAN + "\nWhatsApp number (+country code): " + RESET)

    if not valid_phone(number):
        print(RED + "Invalid phone number." + RESET)
        pause()
        return

    reason = input(CYAN + "Explain the situation: " + RESET).strip()

    if not reason:
        print(RED + "An explanation is required." + RESET)
        pause()
        return

    if mode == "BAN":
        subject = "WhatsApp Privacy Concern"

        body = f"""Hello WhatsApp Support,

I would like to report a privacy concern for review.

Reported number: {number}

Details:
{reason}

Please assess this report according to your policies.
I understand that any decision is yours to make.

Thank you.
"""
    else:
        subject = "Request for WhatsApp Account Review"

        body = f"""Hello WhatsApp Support,

I would like to request a review of my account.

My WhatsApp number: {number}

Explanation:
{reason}

Please review my case and let me know if my account
can be restored.

Thank you.
"""

    logo()
    print(WHITE + BOLD + "REQUEST READY" + RESET)
    print("\nSubject:", subject)
    print("Number:", number)
    print("\nChoose a contact method:")
    print(RED + "1. SEND ONE EMAIL" + RESET)
    print(CYAN + "2. OPEN OFFICIAL CONTACT FORM" + RESET)
    print(WHITE + "3. CANCEL" + RESET)
    print(WHITE + "0. BACK" + RESET)

    choice = input("\nroot@the-pain:~$ ").strip()

    if choice == "1":
        send_email(subject, body)
    elif choice == "2":
        open_form()
    elif choice == "3" or choice == "0":
        return


def help_page():
    while True:
        logo()
        print(CYAN + BOLD + "HELP CENTER" + RESET)
        print("""
1. BAN TOOL:
   Prepare a genuine privacy complaint.

2. UNBAN TOOL:
   Request a review of your own suspended account.

3. EMAIL:
   Requires a private Gmail configuration.

4. CONTACT FORM:
   Opens the official WhatsApp contact page.

Only provide truthful information.
One carefully prepared request is sufficient.
""")
        if back():
            return


def about_page():
    while True:
        logo()
        print(RED + BOLD + "ABOUT THE DEVELOPER" + RESET)
        print("\nDeveloper:", CONFIG.get("DEVELOPER", "THE PAIN TDL"))
        print("WhatsApp:", CONFIG.get("DEVELOPER_NUMBER", "Not configured"))
        print("Channel:", CONFIG.get("WHATSAPP_CHANNEL", "Not configured"))
        print("Version:", CONFIG.get("VERSION", "1.0.0"))
        print("\nPOWERED BY THE PAIN TDL")

        if back():
            return


def main():
    while True:
        logo()

        print(RED + BOLD + "[1] THE PAIN BAN TOOL" + RESET)
        print(GREEN + BOLD + "[2] THE PAIN UNBAN TOOL" + RESET)
        print(WHITE + "[3] HELP" + RESET)
        print(WHITE + "[4] ABOUT" + RESET)
        print(WHITE + "[5] EXIT" + RESET)

        choice = input(GREEN + "\nroot@the-pain:~$ " + RESET).strip()

        if choice == "1":
            request_tool("BAN")
        elif choice == "2":
            request_tool("UNBAN")
        elif choice == "3":
            help_page()
        elif choice == "4":
            about_page()
        elif choice == "5":
            clear()
            print(RED + BOLD + "THE PAIN TDL - SYSTEM OFFLINE" + RESET)
            break
        else:
            print(RED + "Invalid option." + RESET)
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + RED + "Program stopped." + RESET)
        sys.exit(0)
