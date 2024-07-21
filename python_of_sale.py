import time
import firebase_admin
from datetime import datetime
from firebase_admin import credentials
from firebase_admin import db

def main():
    initialize_firebase()

    offers_reference = db.reference("offers")
    events_reference = db.reference("events")

    menu_option = -1
    while menu_option != 0:
        menu_option = prompt_menu_option()

        if menu_option == 1: 
            print_offers_list(offers_reference)
        
        elif menu_option == 2:
            prompt_add_offer(offers_reference)

        elif menu_option == 3:
            prompt_remove_offer(offers_reference)

        elif menu_option == 4:
            print_events_list(events_reference)

        elif menu_option == 5:
            toggle_event_availability(events_reference)

        elif menu_option == 6:
            event_name = input("Type event name: ")
            cashier_loop(event_name)

def cashier_loop(event_name: str):
    while True:
        print()
        print(f"event: {event_name}")
        print("=== NEW ORDER ===")

        order_sentence = prompt_order_sentence()
        if order_sentence == "exit":
            return

        order_dictionary = get_order_dictionary(order_sentence)

        available_offers_dictionary = db.reference("offers").get()
        total_price = get_order_total_price(order_dictionary, available_offers_dictionary)
        print_order_review(order_dictionary, total_price)

        payment_option = prompt_payment_option()
        client_name = input("Type client's name: ").title()

        payment_confirmation = prompt_payment_confirmation()
        if payment_confirmation == "cancel":
            return
        
        register_payment(event_name, 
                         order_dictionary, 
                         total_price,
                         payment_option, 
                         client_name)

def initialize_firebase():
    cred = credentials.Certificate("./python-of-sale-firebase-adminsdk-pgjxf-92ea74ad68.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://python-of-sale-default-rtdb.firebaseio.com/"
    })

def prompt_menu_option():
    print()
    print("1 - List item offers")
    print("2 - Add item offer")
    print("3 - Remove item offer")
    print("4 - List events")
    print("5 - Toogle event availability")
    print("6 - Start cashier routine")
    print("0 - Exit program")
    print()
    menu_option = int(input("Type desired option: "))
    print()
    return menu_option

def print_offers_list(offers_reference: db.Reference):
    offer_items = get_items_from_reference(offers_reference)
    if not offer_items:
        print("None")
    else:
        for item, price in get_items_from_reference(offers_reference):
            print(f"- {item}: {price:.2f}")

def get_items_from_reference(database_reference: db.Reference):
    items_dictionary = database_reference.get()
    return items_dictionary.items() if items_dictionary else []

def prompt_add_offer(offers_reference: db.Reference):
    offer_name = input("Name of the new item: ")
    offer_price = float(input("Price of the new item: "))
    offers_reference.child(offer_name).set(offer_price)
    print(f"Added item offer for {offer_name} = $ {offer_price:.2f}")

def prompt_remove_offer(offers_reference:db.Reference):
    item_to_delete = input("Name of item offer to remove: ")
    offers_reference.child(item_to_delete).delete()
    print(f"{item_to_delete} offer deleted")

def print_events_list(events_reference: db.Reference):
    event_items = get_items_from_reference(events_reference)
    if not event_items:
        print("None")
    else:
        for event, is_active in event_items: 
            status = "ACTIVE" if is_active else "inactive"
            print(f"- {event}: {status}")

def toggle_event_availability(events_reference: db.Reference):
    event_name = input("Type the name of the event: ").upper()
            
    chosen_event_ref = events_reference.child(event_name)
    new_availability = not chosen_event_ref.get()
    chosen_event_ref.set(new_availability)
            
    status_name = "ACTIVE" if new_availability == True else "inactive"
    print(f"Event \"{event_name}\" is now {status_name}")

def prompt_order_sentence():
    order_sentence = ""
    while not is_valid_order_sentence(order_sentence):
        print("Enter order sentence or \"exit\" (example: \"2 kebab 1 soda 4 water\"): ")
        order_sentence = input()
        
        if order_sentence.strip().lower() == "exit":
            return "exit"
    
    return order_sentence

def is_valid_order_sentence(order_sentence):
    if not order_sentence:
        return False

    order_dictionary = get_order_dictionary(order_sentence)

    if not order_dictionary:
        return False    

    available_offers = db.reference("offers").get().keys()

    for item, quantity in order_dictionary.items():
        if item not in available_offers:
            print(f"Invalid item \"{item}\" in order sentence, please try again.")
            return False
    
    return True

def get_order_dictionary(order_sentence: str):
    order_parts = order_sentence.split()
    order_dictionary = {}
    part_index = 0

    while part_index < len(order_parts) - 1:
        name = order_parts[part_index + 1]
        quantity = int(order_parts[part_index])

        if name not in order_dictionary:
            order_dictionary[name] = 0

        order_dictionary[name] += quantity

        part_index += 2
    return order_dictionary

def get_order_total_price(order_dictionary: dict, available_offers_dictionary: dict):
    total_price = 0
    for item, quantity in order_dictionary.items():
        total_price += quantity * available_offers_dictionary[item]
    return total_price

def print_order_review(order_dictionary: dict, total_price: float):
    print()
    print("ORDER REVIEW:")
    for name, quantity in order_dictionary.items():
        print(f"- {quantity} x {name}")
    print(f"TOTAL: $ {total_price:.2f}")

def prompt_payment_option():
    print()
    print("What is the payment method? ")
    print("1 - Pix")
    print("2 - Debit Card")
    print("3 - Credit Card")
    print("4 - Cash")
    print("0 - Cancel order")
    print()
    return input("Type desired payment option: ")

def prompt_payment_confirmation():
    print("Waiting payment operation ", end="", flush="True")
    for char in "5...4...3...2...1...":
        print(char, end="", flush=True)
        time.sleep(.25)
    print()

    finishing_option = ""
    while finishing_option not in ["yes", "cancel"]:
        finishing_option = input("Is payment complete? (yes/cancel): ").strip().lower()
    return finishing_option

def register_payment(event_name, order_dictionary, total_price, payment_option, client_name):
    event_name = event_name.strip().upper().replace(" ", "")
    payment_data = {
            "datetime": datetime.now().isoformat(),
            "event": event_name,
            "method": payment_option,
            "client": client_name,
            "amount": total_price,
            "items": order_dictionary
        }
    db.reference("payments").push(payment_data)
    print("Payment registered!")

if __name__ == "__main__":
    main()