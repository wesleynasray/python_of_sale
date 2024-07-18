import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def main():
    initialize_firebase()

    menu_option = -1
    offers_reference = db.reference("item-offers")

    while menu_option != 0:
        menu_option = request_menu_option()

        if menu_option == 1: 
            list_offers(offers_reference)

        elif menu_option == 2:
            prompt_add_offer(offers_reference)

        elif menu_option == 3:
            prompt_remove_offer(offers_reference)

    return

def request_menu_option():
    print()
    print("1 - List item offers")
    print("2 - Add item offer")
    print("3 - Remove item offer")
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

def list_offers(offers_reference):
    offers_dictionary = offers_reference.get()
    if offers_dictionary:
        for item, price in offers_dictionary.items():
            print(f"- {item}: $ {price:.2f}")
    else:
        print(offers_dictionary)


def initialize_firebase():
    cred = credentials.Certificate("./python-of-sale-firebase-adminsdk-pgjxf-92ea74ad68.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://python-of-sale-default-rtdb.firebaseio.com/"
    })

if __name__ == "__main__":
    main()