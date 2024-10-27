import json  # Import the json module for handling JSON data
import tkinter as tk
from GUI import FinanceTrackerGUI


# Global dictionary to store transactions
transactions = {}

# Function to load transactions from a JSON file
def load_transactions():
    global transactions  # Access the global 'transactions' dictionary
    try:
        with open("transactions.json", "r") as file:  # Open the JSON file for reading
            data = json.load(file)  # Load JSON data from the file
            transactions.update(data)  # Update the 'transactions' dictionary with data from the file
    except FileNotFoundError:  # Handle the case where the file is not found
        print("File not found!")  # Print a message indicating that the file is not found
        transactions = {}  # Reset the 'transactions' dictionary to an empty dictionary

# Function to save transactions to a JSON file
def save_transactions():
    with open("transactions.json", "w") as file:  # Open the JSON file for writing
        json.dump(transactions, file, indent=2)  # Write the 'transactions' dictionary to the file with indentation for readability


def read_bulk_transactions_from_file(filename):
    # Open and read the file, then parse each line to add to the transactions dictionary
    global transactions    # Access the global 'transactions' dictionary
    try:
        with open(filename, "r") as file:    # Open the specified file for reading
            if not file:   # Check if the file is empty
                print("No data on file")    # Print a message indicating that there is no data in the file
                return  # Return from the function
            
            for line in file:   # Iterate over each line in the file
                data = json.load(line.strip())   # Parse JSON data from the line and strip any leading/trailing whitespace
                
                
                for key in data:   # Iterate over each key in the parsed data
                    if key not in transactions.keys():   # Check if the key is not already in the 'transactions' dictionary
                        transactions[key] = []    # Initialize an empty list for the key if it doesn't exist

                
                    transactions[key].append(data[key])  # Append the value associated with the key to the list in the 'transactions' dictionary

            
            print("Data added successfully !")    # Print a message indicating that the data was added successfully
        
    except Exception as n:  # Handle any exceptions that occur during file reading
        print("File not found!",n)    # Print an error message indicating the specific exception that occurred

# Feature implementations for adding a transaction
def add_transaction():
    print("\n__________Add Transaction__________\n")
    print("1. Import transaction from file")  # Option to import transactions from a file
    print("2. Add transaction")  # Option to manually add a transaction

    choice = input("Enter choice: ")  # Prompt the user to choose an option

    if choice == "1":  # If the user chooses to import transactions from a file
        filename = input("Enter file name: ")  # Prompt the user to enter the filename
        read_bulk_transactions_from_file(filename)  # Call the function to read transactions from the file
        save_transactions()  # Save the transactions to the file after importing

    elif choice == "2":  # If the user chooses to manually add a transaction
        while True:
            try:
                amount = float(input("Enter the transaction amount: "))  # Prompt the user to enter the transaction amount
                break
            except ValueError as e:  # Handle the case where the input is not a valid number
                print("Invalid input. Try again!", e)

        category = input("Enter the category of transaction: ")  # Prompt the user to enter the category of the transaction

        while True:
            transaction_type = input("Enter the transaction type (Income/Expense): ").capitalize()  # Prompt the user to enter the transaction type
            if transaction_type in ["Income", "Expense"]:  # Check if the transaction type is valid
                break
            else:
                print("Please enter 'Income' or 'Expense'")  # Print a message indicating that the input is invalid

        date = input("Enter the date (YYYY-MM-DD): ")  # Prompt the user to enter the date of the transaction

        # Storing transaction as a dictionary
        transaction = {"amount": amount, "type": transaction_type, "date": date}  # Create a dictionary representing the transaction

        if category not in transactions:  # Check if the category is not already in the transactions dictionary
            transactions[category] = []  # Initialize an empty list for the category if it doesn't exist

        transactions[category].append(transaction)  # Add the transaction to the list for the category
        print("Transaction added successfully!")  # Print a message indicating that the transaction was added successfully
        save_transactions()  # Save the updated transactions to the file

    else:
        print("Invalid input")  # Print a message indicating that the input is invalid if the user enters an invalid choice



def view_transactions():
   
    # Initialize GUI
    root = tk.Tk()  # Create the main application window
    app = FinanceTrackerGUI(root)  # Create an instance of the FinanceTrackerGUI class
    app.display_transactions(app.transactions)  # Display transactions in the GUI
    root.mainloop()  # Start the Tkinter event loop

def update_transaction():
    print("\n__________Update Transaction__________")
    # Update a transaction in the 'transactions' list

    # Display all transactions to the user
    view_transactions()

    # Request the user to input the index of the transaction to update
    while True:
        try:
            index = int(input("Enter the index of the transaction to update: ")) - 1

            # Check if the index is inside the range of the transactions list.
            if 0 <= index < len(transactions):
                break
            else:
                # Handle the case when the user enters an invalid input for index
                print("Invalid index. Please enter a valid index.")
        except ValueError as e:
            # Handle the case when the user enters an invalid input for index
            print("Please enter a valid integer index.", e)

    # Ask the user to enter the updated amount and handle invalid input.
    while True:
        try:
            new_amount = float(input("Enter the new amount: "))
            break
        except ValueError as e:
            # Handle the case when the user enters an invalid input for amount
            print("Invalid input for amount. Please enter a valid number.", e)

    # Prompt the user to input the category of the transaction and store it as a string
    new_category = input("Enter the new category: ")

    while True:
        new_transaction_type = input("Enter the new transaction type (Income/Expense): ").capitalize()
        if new_transaction_type in ["Income", "Expense"]:
            break
        else:
            # Handle the case when the user enters an invalid transaction type
            print("Please enter 'Income' or 'Expense'.")

    # Request the user to input the new date in the format (YYYY-MM-DD)
    new_date = input("Enter the new date (YYYY-MM-DD): ")

    # Update the transaction details in the 'transactions' list with the new values
    transactions[index] = {"amount" : new_amount , "category" : new_category , "type" : new_transaction_type , "date" : new_date}
    # Save the updated transactions to the file
    save_transactions()

    # Print a success message
    print("Transaction updated successfully.")

      

def delete_transaction():
    print("\n_____Delete Transaction____")  # Print a header for the delete transaction section
    #Delete a transaction from the 'transactions' list.

    # Display all transactions to the user
    view_transactions()
    try:
        
        category = input("Enter category: ")   # Prompt the user to enter the category of the transaction to delete


        if category not in transactions:  # Check if the entered category is not in the transactions dictionary
            print("No category found !")  # Print a message indicating that the category is not found
            return

        # Request the user to input the index of the transaction to delete
        index = int(input("Enter the index of the transaction to delete: "))

         # Delete the transaction at the specified index from the 'transactions' list
        del transactions[category][index - 1]

        # Save the updated transactions to the file
        save_transactions()

         # Print a success message
        print("Transaction deleted successfully.")
    except Exception as n:
        # Handle the case when the user enters an invalid index
        print("Invalid index .",n)
  


def display_summary():
    print("\n__________Display Summary__________")
    #Display summary information based on transactions.

    # Placeholder for summary display logic
    total_income = 0
    total_expense = 0

    # Iterate through each transaction in the 'transactions' list
    for transaction in transactions:
        # Check the transaction type and add the total income and expenses.
        if transaction[2] == 'Income':  
            total_income += transaction[0] # Add transaction amount to total income
        elif transaction[2] == 'Expense': 
            total_expense += transaction[0]  # Add transaction amount to total expense
    

    # Print summary information
    print("\nSummary : ")
    print("Total Income:", total_income)
    print("Total Expense:", total_expense)
    print("Net Balance:", total_income - total_expense)

# Define a function to display the main menu of the personal finance tracker
def main_menu():
    while True:      # Loop to continuously display the menu until the user chooses to exit
        print("\n===== Personal Finance Tracker =====")
        print("1. Add Transaction")  # Option to add a new transaction
        print("2. View Transactions")  # Option to view  transactions
        print("3. Update Transaction")  # Option to update transactions
        print("4. Delete Transaction")  # Option to delete transactions
        print("5. Display Summary")  # Option to display summary of transactions
        print("6. Exit")     # Option to exit the program
        choice = input("Enter your choice: ")  # Prompt the user to enter their choice
        if choice == "1":   # If user chooses to add a transaction                   
            add_transaction()     # Call the add_transaction function
        elif choice == "2":   # If user chooses to view transactions
            view_transactions()  # Call the view_transactions function
        elif choice == "3":   # If user chooses to update a transaction
            update_transaction()  # Call the update_transaction function
        elif choice == "4":    # If user chooses to delete a transaction
            delete_transaction()  # Call the delete_transaction function
        elif choice == "5":    # If user chooses to display a summary
            display_summary()   # Call the display_summary function
        elif choice == "6":   # If user chooses to exit
            print("Exiting...")    # Display a message indicating exiting
            break   # Exit the while loop and end the program
        else:  # If user enters an invalid choice
            print("Invalid choice.")  # Display a message indicating an invalid choice

# Check if the script is being run directly and not imported as a module
if __name__ == "__main__":
    main_menu() # Call the main_menu function to start the program
