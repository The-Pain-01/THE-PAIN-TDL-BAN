#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# THE PAIN TDL BAN

import smtplib
import time
import os
import random
import sys
from email.mime.text import MIMEText
from email.utils import formataddr

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE, "config.txt")
SUPPORT = "support@support.whatsapp.com"

R = "\033[1;31m"   # rouge gras
G = "\033[1;32m"
Y = "\033[1;33m"
C = "\033[1;36m"
W = "\033[1;37m"
X = "\033[0m"      # reset

BANNIERE = r"""
 ____  _   _ _____   ____    _    ___ _   _
|  _ \| | | | ____| |  _ \  / \  |_ _| \ | |
| |_) | |_| |  _|   | |_) |/ _ \  | ||  \| |
|  __/|  _  | |___  |  __// ___ \ | || |\  |
|_|   |_| |_|_____| |_|  /_/   \_\___|_| \_|

        ___  _   _   ____    _    _   _
       |_ _|| \ | | | __ )  / \  | \ | |
        | | |  \| | |  _ \ / _ \ |  \| |
        | | | |\  | | |_) / ___ \| |\  |
       |___||_| \_| |____/_/   \_\_| \_|
"""

SUJETS = [
    "Signalement compte spam",
    "Compte arnaque - liens douteux",
    "Signalement usurpation support WhatsApp",
    "Spam massif depuis ce numéro",
    "Compte envoie contenu gore / arnaque",
]

CORPS = """Bonjour l'équipe WhatsApp,

Je signale le compte suivant : {num}

Depuis plusieurs jours ce compte :
- envoie massivement des liens d'arnaque / faux concours
- diffuse du contenu gore
- se fait passer pour le support WhatsApp et réclame des codes

Merci de vérifier et de suspendre si nécessaire.
Rappel du numéro concerné : {num}

Cordialement,
Un utilisateur WhatsApp
"""


def clear():
    os.system("clear")


def ecrire_lent(texte, delai=0.002):
    for c in texte:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delai)
    print()


def banniere():
    clear()
    print(R + BANNIERE + X)
    print(R + "=" * 55 + X)
    print(R + "        THE PAIN TDL BAN  —  WHATSAPP EMAIL BAN" + X)
    print(R + "=" * 55 + X)
    print(C + "        [ signalement par emails — v1 ]" + X)
    print()


def charger_comptes():
    if not os.path.exists(CONFIG):
        return []
    out = []
    with open(CONFIG, "r", encoding="utf-8") as f:
        for l in f:
            l = l.strip()
            if not l or l.startswith("#"):
                continue
            if ":" in l:
                m, p = l.split(":", 1)
                out.append((m.strip(), p.strip()))
    return out


def envoyer(mail, pwd, numero, sujet, corps):
    msg = MIMEText(corps, "plain", "utf-8")
    msg["Subject"] = sujet
    msg["From"] = formataddr(("Utilisateur WhatsApp", mail))
    msg["To"] = SUPPORT

    hote = "smtp.gmail.com"
    if "outlook" in mail or "hotmail" in mail:
        hote = "smtp-mail.outlook.com"
    elif "yahoo" in mail:
        hote = "smtp.mail.yahoo.com"

    with smtplib.SMTP(hote, 587, timeout=30) as s:
        s.starttls()
        s.login(mail, pwd)
        s.send_message(msg)


def lancer(numero, n):
    comptes = charger_comptes()
    if not comptes:
        print(Y + "[!] Aucun compte dans config.txt" + X)
        return
    print(C + f"[+] Cible : {numero} | Envois : {n} | Comptes : {len(comptes)}" + X)
    time.sleep(1)
    ok = ko = 0
    for i in range(1, n + 1):
        m, p = random.choice(comptes)
        try:
            envoyer(m, p, numero, random.choice(SUJETS), CORPS.format(num=numero))
            ok += 1
            print(G + f"  [{i}/{n}] OK   {m}" + X)
        except Exception as e:
            ko += 1
            print(R + f"  [{i}/{n}] FAIL {m} :: {e}" + X)
        time.sleep(random.uniform(4, 12))
    print()
    print(G + f"Reussis : {ok}" + X, "|", R + f"Echecs : {ko}" + X)


def menu():
    banniere()
    print(W + " [1]" + X + " Lancer un signalement")
    print(W + " [2]" + X + " Voir mes comptes")
    print(W + " [3]" + X + " Quitter")
    print(R + "-" * 55 + X)
    return input(Y + " TDL-BAN > " + X).strip()


def main():
    while True:
        c = menu()
        if c == "1":
            num = input(" Numero (+2126XXXXXXX) > ").strip()
            if not num.startswith("+"):
                print(R + "[!] Mets le + devant" + X)
                time.sleep(2); continue
            try:
                n = int(input(" Nombre d'emails > ").strip())
            except ValueError:
                print(R + "[!] Nombre invalide" + X); time.sleep(2); continue
            lancer(num, n)
            input("\n Entree pour revenir...")
        elif c == "2":
            cs = charger_comptes()
            print(Y + f"\n {len(cs)} compte(s) :" + X)
            for m, _ in cs:
                print("  -", m)
            input("\n Entree...")
        elif c == "3":
            print(R + " Bye." + X); break


if __name__ == "__main__":
    main()
