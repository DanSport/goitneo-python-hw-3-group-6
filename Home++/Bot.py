from Origin import AddressBook, Record
from datetime import datetime
import time
import art


rows = art.h.split("\n")  # Розділити рядок за символом нового рядка
for row in rows:
    print(row)
    time.sleep(0.2)

MENU = """
    * Available commands:
        #1 or hello
        #2 or add 
        #3 or change
        #4 or phone
        #5 or all
        #6 add-birthday
        #7 show-birthday
        #8 birtdays
        #9 or close or exit or bye
         
"""


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid input. Please provide name and phone number separated by space."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    print("\nWelcome to the assistant bot!")
    address_book = AddressBook()
    address_book.load_from_file()
    print(MENU)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "bye", "9"]:
            rows = art.a.split("\n")
            for row in rows:
                print(row)
                time.sleep(0.1)
            print(
                "Goodbye! I hope I was useful. Thank you for using me.! See you soon.\n"
            )
            address_book.save_to_file()
            break
        elif command in ["hello", "1"]:
            print("\n*****************************\nHow can I help you?")
        elif command in ["add", "2"]:
            if len(args) != 2:
                print("Invalid input. Please provide name and phone number separated by space.")
                continue
            name, phone = args   
            record = address_book.find(name)
            if record:
                record.add_phone(phone)
                print(f"Phone number added for {name}.")
            else:
                record = Record(name)
                record.add_phone(phone)
                address_book.add_record(record)
                print("Contact added.")
        elif command in ["change", "3"]:
            if len(args) != 3:
                print(
                    "Invalid input. Please provide name and phone number separated by space."
                )
                continue
            name, old_phone, new_phone = args
            record = address_book.find(name)
            if record:
                record.edit_phone(old_phone, new_phone)
                print(f"Phone number changed for {name}.")
            else:
                print(f"Contact {name} not found.")
        elif command in ["phone", "4"]:
            if len(args) != 1:
                print("Invalid input. Please provide a name or a phone number.")
                continue
            search_term = args[0]
            found_contact = False
            for record in address_book.data.values():
                if search_term.lower() in [record.name.value.lower()] + [
                    phone.value.lower() for phone in record.phones
                ]:
                    print(record)
                    found_contact = True
                    break
            if not found_contact:
                print(f"Contact {search_term} not found.")
        elif command in ["all", "5"]:
            for record in address_book.data.values():
                print(record)
        elif command in ["add-birthday", "6"]:
            if len(args) != 2:
                print(
                    "Invalid input. Please provide name and birthday separated by space in DD.MM.YYYY format."
                )
                continue
            name, birthday = args
            try:
                datetime.strptime(birthday, "%d.%m.%Y")
            except ValueError:
                print("Invalid date format. Use DD.MM.YYYY")
                continue
            record = address_book.find(name)
            if record:
                record.add_birthday(birthday)
                print(f"Birthday added for {name}.")
            else:
                print(f"Contact {name} not found.")
        elif command in ["show-birthday", "7"]:
            if len(args) != 1:
                print("Invalid input. Please provide a name.")
                continue
            name = args[0]
            record = address_book.find(name)
            if record:
                print(record.show_birthday())
            else:
                print(f"Contact {name} not found.")
        elif command in ["birthdays", "8"]:
            address_book.get_birthdays_per_week()
        else:
            print("Invalid command.\n")

        print(MENU)


if __name__ == "__main__":
    main()
