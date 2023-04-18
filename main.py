import smtplib
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

filename = "students.txt"
divider = ","

OCENA_3 = 51
OCENA_35 = 61
OCENA_4 = 71
OCENA_45 = 81
OCENA_5 = 91

studenci = {}


def wczytaj_dane():
    if not os.path.isfile(filename):
        return
    with open(filename, "r") as plik:
        for linia in plik:
            dane = linia.strip().split(divider)
            if len(dane) < 4:
                continue
            email, imie, nazwisko, punkty = dane[:4]
            if not email:
                continue
            punkty = int(punkty) if punkty else 0
            ocena, status = dane[4:] if len(dane) > 4 else ("", "")
            studenci[email] = {
                "imie": imie,
                "nazwisko": nazwisko,
                "punkty": punkty,
                "ocena": ocena,
                "status": status
            }


def zapisz_dane():
    with open(filename, "w") as plik:
        for email, dane in studenci.items():
            linia = f"{email}{divider}{dane['imie']}{divider}{dane['nazwisko']}{divider}{dane['punkty']}{divider}{dane['ocena']}{divider}{dane['status']}\n"
            plik.write(linia)


def wystaw_oceny():
    for email, dane in studenci.items():
        if dane["status"] != "":
            continue
        punkty = dane["punkty"]
        if punkty >= OCENA_5:
            dane["ocena"] = "bdb"
        elif punkty >= OCENA_45:
            dane["ocena"] = "db+"
        elif punkty >= OCENA_4:
            dane["ocena"] = "db"
        elif punkty >= OCENA_35:
            dane["ocena"] = "dst+"
        elif punkty >= OCENA_3:
            dane["ocena"] = "dst"
        else:
            dane["ocena"] = "ndst"
        dane["status"] = "GRADED"


def usun_studenta(email):
    if email in studenci:
        del studenci[email]


def dodaj_studenta(email, imie, nazwisko, punkty):
    if email in studenci:
        return False
    studenci[email] = {
        "imie": imie,
        "nazwisko": nazwisko,
        "punkty": int(punkty),
        "ocena": "",
        "status": ""
    }
    return True


wczytaj_dane()

while True:
    print("Co chcesz zrobić?")
    print("1 - Wystaw oceny")
    print("2 - Usuń studenta")
    print("3 - Dodaj studenta")
    print("4 - Wyślij email")
    print("5 - Wyjście")
    wybor = input("Twój wybór: ")

    if wybor == "1":
        wystaw_oceny()
        zapisz_dane()
        print("Oceny zostały wystawione.")
    elif wybor == "2":
        email = input("Podaj adres email studenta: ")
        usun_studenta(email)
        zapisz_dane()
        print("Student został usunięty.")
    elif wybor == "3":
        email = input("Podaj adres email studenta: ")
        imie = input("Podaj imię studenta: ")
        nazwisko = input("Podaj nazwisko studenta: ")
        punkty = input("Podaj liczbę uzyskanych punktów: ")
        if dodaj_studenta(email, imie, nazwisko, punkty):
            zapisz_dane()
            print("Student został dodany.")
        else:
            print("Student o podanym adresie email już istnieje.")
    elif wybor == "4":
        for email, dane in studenci.items():
            if dane["status"] != "MAILED":
                smtp_server = smtplib.SMTP("poczta.interia.pl", 587)
                smtp_server.starttls()
                smtp_server.login("pablo.sarmiento", "ReaktorWytrzymaXD")
                message = MIMEMultipart()
                message["From"] = "Pablo"
                message["To"] = dane["imie"]
                message["Subject"] = "GRADE"
                body = f"{dane['imie']} GRADE {dane['ocena']}"
                message.attach(MIMEText(body, "plain"))
                text = message.as_string()
                smtp_server.sendmail("pablo.sarmiento@interia.pl", email, text)
                smtp_server.quit()
                dane["status"] = "MAILED"
                zapisz_dane()
                print(f"Email został wysłany na adres {email}.")
            else:
                print(f"Błąd podczas wysyłania emaila na adres {email}.")

    elif wybor == "5":
        break
    else:
        print("Nieprawidłowy wybór.")
