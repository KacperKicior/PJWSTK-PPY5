import smtplib
import os.path

# Stałe z danymi dotyczącymi pliku
NAZWA_PLIKU = "students.txt"
ROZDZIELACZ = ","

# Stałe z danymi dotyczącymi ocen
OCENA_MINIMALNA = 30
OCENA_DOBRA = 60
OCENA_BARDZO_DOBRA = 90

# Słownik przechowujący dane studentów
studenci = {}

# Funkcja wczytująca dane z pliku
def wczytaj_dane():
    if not os.path.isfile(NAZWA_PLIKU):
        return
    with open(NAZWA_PLIKU, "r") as plik:
        for linia in plik:
            dane = linia.strip().split(ROZDZIELACZ)
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

# Funkcja zapisująca dane do pliku
def zapisz_dane():
    with open(NAZWA_PLIKU, "w") as plik:
        for email, dane in studenci.items():
            linia = f"{email}{ROZDZIELACZ}{dane['imie']}{ROZDZIELACZ}{dane['nazwisko']}{ROZDZIELACZ}{dane['punkty']}{ROZDZIELACZ}{dane['ocena']}{ROZDZIELACZ}{dane['status']}\n"
            plik.write(linia)

# Funkcja automatycznie wystawiająca ocenę studentom
def wystaw_oceny():
    for email, dane in studenci.items():
        if dane["status"] != "":
            continue
        punkty = dane["punkty"]
        if punkty >= OCENA_BARDZO_DOBRA:
            dane["ocena"] = "bdb"
        elif punkty >= OCENA_DOBRA:
            dane["ocena"] = "db"
        elif punkty >= OCENA_MINIMALNA:
            dane["ocena"] = "dst"
        else:
            dane["ocena"] = "ndst"
        dane["status"] = "GRADED"

# Funkcja usuwająca studenta
def usun_studenta(email):
    if email in studenci:
        del studenci[email]

# Funkcja dodająca studenta
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


# Funkcja wysyłająca email
def wyslij_email(email, tresc):
    # Dane dotyczące serwera SMTP i konta
    SMTP_SERVER = "smtp.wp.pl"
    SMTP_PORT = 465
    EMAIL_ADRES = "antoniodelgado@wp.pl"
    EMAIL_HASLO = "ZAQ!2wsx"
    EMAIL_NADAWCA = "Antonio Delgado Mexico Cartel"

    # Tworzenie wiadomości email
    msg = f"From: {EMAIL_NADAWCA} <{EMAIL_ADRES}>\n"
    msg += f"To: {email}\n"
    msg += "Subject: Ocena z przedmiotu Podstawy Programowania Python\n\n"
    msg += tresc

    # Wysyłanie wiadomości email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADRES, EMAIL_HASLO)
        server.sendmail(EMAIL_ADRES, email, msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Błąd podczas wysyłania emaila na adres {email}: {str(e)}")
        return False


# Wczytanie danych z pliku
wczytaj_dane()

# Główna pętla programu
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
        tresc = input("Podaj treść wiadomości: ")
        for email, dane in studenci.items():
            if dane["status"] != "MAILED":
                if wyslij_email(email, tresc):
                    dane["status"] = "MAILED"
                    zapisz_dane()
                    print(f"Email został wysłany na adres {email}.")
                else:
                    print(f"Błąd podczas wysyłania emaila na adres {email}.")
    elif wybor == "5":
        break
    else:
        print("Nieprawidłowy wybór.")
