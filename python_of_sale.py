import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def main():
    initialize_firebase()

    menu_option = -1
    item_offers_ref = db.reference("item-offers")

    while menu_option != 0:
        print()
        print("1 - List item offers")
        print("2 - Add item offer")
        print("3 - Remove item offer")
        print("0 - Exit program")
        menu_option = int(input("Type desired option: "))
        print()

        if menu_option == 1:
            offers_dict = item_offers_ref.get()
            if offers_dict:
                for item, price in offers_dict.items():
                    print(f"- {item}: $ {price:.2f}")
            else:
                print(offers_dict)

        elif menu_option == 2:
            new_name = input("Name of the new item: ")
            new_price = float(input("Price of the new item: "))
            item_offers_ref.child(new_name).set(new_price)
            print(f"Added item offer for {new_name} = $ {new_price:.2f}")

        elif menu_option == 3:
            item_to_delete = input("Name of item offer to remove: ")
            item_offers_ref.child(item_to_delete).delete()
            print(f"{item_to_delete} offer deleted")

    return

def initialize_firebase():
    cred = credentials.Certificate("./python-of-sale-firebase-adminsdk-pgjxf-92ea74ad68.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://python-of-sale-default-rtdb.firebaseio.com/"
    })

if __name__ == "__main__":
    main()