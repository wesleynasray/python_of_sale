import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def main():
    initialize_firebase()

    menu_option = -1
    offers_reference = db.reference("offers")
    events_reference = db.reference("events")

    while menu_option != 0:
        menu_option = request_menu_option()

        if menu_option == 1: 
            offers = get_reference_items(offers_reference)
            if not offers:
                print("None")
            else:
                for item, price in get_reference_items(offers_reference):
                    print(f"- {item}: {price:.2f}")

        elif menu_option == 2:
            prompt_add_offer(offers_reference)

        elif menu_option == 3:
            prompt_remove_offer(offers_reference)

        elif menu_option == 4:
            events = get_reference_items(events_reference)
            if not events:
                print("None")
            else:
                for event, is_active in events: 
                    status = "ACTIVE" if is_active else "inactive"
                    print(f"- {event}: {status}")

        elif menu_option == 5:
            event_name = input("Type the name of the event: ").upper()
            
            chosen_event_ref = events_reference.child(event_name)
            new_availability = not chosen_event_ref.get()
            chosen_event_ref.set(new_availability)
            
            status_name = "ACTIVE" if new_availability == True else "inactive"
            print(f"Event \"{event_name}\" is now {status_name}")



def request_menu_option():
    print()
    print("1 - List item offers")
    print("2 - Add item offer")
    print("3 - Remove item offer")
    print("4 - List events")
    print("5 - Toogle event availability")
    print("0 - Exit program")
    menu_option = int(input("Type desired option: "))
    print()
    return menu_option

def prompt_remove_offer(offers_reference):
    item_to_delete = input("Name of item offer to remove: ")
    offers_reference.child(item_to_delete).delete()
    print(f"{item_to_delete} offer deleted")

def prompt_add_offer(offers_reference):
    offer_name = input("Name of the new item: ")
    offer_price = float(input("Price of the new item: "))
    offers_reference.child(offer_name).set(offer_price)
    print(f"Added item offer for {offer_name} = $ {offer_price:.2f}")

def get_reference_items(database_reference):
    items_dictionary = database_reference.get()
    return items_dictionary.items() if items_dictionary else []


def initialize_firebase():
    cred = credentials.Certificate("./python-of-sale-firebase-adminsdk-pgjxf-92ea74ad68.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://python-of-sale-default-rtdb.firebaseio.com/"
    })

if __name__ == "__main__":
    main()