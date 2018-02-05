import db
import warnings
from sqlalchemy import exc


# Check if user input is valid integer type
def check_int(user_input):
    try:
        int(user_input)
        return True
    except ValueError:
        return False


# Check if user input is valid float type
def check_float(user_input):
    try:
        float(user_input)
        return True
    except ValueError:
        return False

# Allow user to return to main menu option
print('\nWelcome to Merch Manager! \n'
    'Tip: Enter an invalid entry to return to the main options.\n')

# Begin program loop
while True:

    # Ask user which table they want to use, verify they provided a valid entry
    table_choice = input('Which table do you want to use? \n'
                         'Enter 1 - Merch\n'
                         'Enter 2 - Shows\n' 
                         'Enter 3 - Sales\n'
                         'Enter 4 - View Statistics\n'
                         'Enter 5 - Quit\n')
    if check_int(table_choice):
        if 5 >= int(table_choice) >= 1:
            # Ask user what they want to do with the table: View, Add, Delete, Edit
            # Verify user entered valid entry
            if table_choice == '1' or table_choice == '2' or table_choice == '3':
                action_choice = input('What do you want to do?\n'
                                      'Enter 1 - View All Entries\n'
                                      'Enter 2 - Add Entry\n'
                                      'Enter 3 - Search for an Entry\n')

            # Display statistics (ignore warning alerting that slight rounding errors may occur)
            elif table_choice == '4':
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=exc.SAWarning)
                    print(db.get_stats())
                    # Set action choice to invalid number so user returns to main options
                    action_choice = '6'

            # Quit program
            elif table_choice == '5':
                print("Goodbye!")
                break

            if check_int(action_choice):
                if 3 >= int(action_choice) >= 1:

                    # VIEW
                    if action_choice == '1':

                        if table_choice == '1':
                            merch = db.view_merch()
                            for item in merch:
                                print(merch)

                        elif table_choice == '2':
                            shows = db.view_shows()
                            for show in shows:
                                print(show)

                        elif table_choice == '3':
                            sales = db.view_sales()
                            for sale in sales:
                                print(sale)

                    # ADD
                    elif action_choice == '2':
                        # Add to Merch table
                        if table_choice == '1':
                            item = input("Item: \n")
                            price = input("Price: \n")
                            if check_float(price):
                                db.add_merch(item, price)
                            else:
                                print("Please try again with a valid price.")

                        # Add to Shows table
                        elif table_choice == '2':
                            date = input("Date: \n")
                            venue = input("Venue: \n")
                            db.add_show(date, venue)

                        # Add to Sales table
                        elif table_choice == '3':
                            show_id = input("Show ID: \n")
                            if check_int(show_id):
                                if db.check_id(show_id):
                                    item = input("Item: \n")
                                    if db.check_item(item):
                                        price = input("Price: \n")
                                        if check_float(price):
                                            if db.check_price(price):
                                                sold = input("Amount Sold: \n")
                                                if check_int(sold):
                                                    db.add_sale(show_id, item, sold)
                                            else:
                                                print("Please try again with a valid item.")
                                        else:
                                            print("Please try again with a valid price.")
                                    else:
                                        print("Please try again with a valid item.")
                                else:
                                    print("Please try again with a valid show ID.")
                            else:
                                print("Please try again with a valid number")

                    # SEARCH
                    elif action_choice == '3':

                        # Search Merch table
                        if table_choice == '1':
                            term = input("Search term: \n")
                            column = input('Enter 1 - Search by Item\n'
                                            'Enter 2 - Search by Price\n')
                            if column != '1' and column != '2':
                                print("Please try again with 1 or 2.")
                            else:
                                results = db.search_merch(term, column)
                                for item in results:
                                    print(item)

                        # Search Shows table
                        elif table_choice == '2':
                            term = input("Search term: \n")
                            column = input('Enter 1 - Item\n'
                                            'Enter 2 - Date\n'
                                            'Enter 3 - Venue\n')
                            if column != '1' and column != '2' and column != '3':
                                print("Please try again by entering 1, 2, or 3.")
                            else:
                                results = db.search_shows(term, column)
                                for item in results:
                                    print(item)
                                    
                        # Search Sales table            
                        elif table_choice == '3':
                            term = input("Search term: \n")
                            column = input('Enter 1 - Show ID\n'
                                            'Enter 2 - Item\n'
                                            'Enter 3 - Sold\n')
                            if column != '1' and column != '2' and column != '3':
                                print("Please try again by entering 1, 2, or 3.")
                            else:
                                results = db.search_sales(term, column)
                                for item in results:
                                    print(item)

                else:
                    print("Please try again with a valid number.")
            else:
                print("Please try again with a valid integer.")
        else:
            print("Please try again with a valid number.")
    else:
        print("Please try again with a valid integer.")
