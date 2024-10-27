import tkinter as tk          # Import the tkinter module as tk
from tkinter import ttk        # Import the ttk submodule from tkinter for themed widgets
import json                 # Import the json module for JSON data handling

class FinanceTrackerGUI:
    def __init__(self, root):
        # Set the root window
        self.root = root

        self.root.title("Personal Finance Tracker")       # Set the window title
        self.root.iconbitmap("finance tracker.ico")        # Set the window icon

        # Call the method to create GUI widgets
        self.create_widgets()

        # Set window dimensions and position it at the center of the screen
        width,height = 700,300      # Define the window width and height
        display_width = root.winfo_screenwidth()    # Get the width of the screen
        display_height = root.winfo_screenheight()   # Get the height of the screen
        left = int(display_width/2 - width/2)    # Calculate the left position of the window
        top = int(display_height/2 - height/2)     # Calculate the top position of the window
        self.root.geometry(f'{width}x{height}+{left}+{top}')     # Set the window geometry

         # Disable window resizing                   
        self.root.resizable(False, False)

          # Load transactions from JSON file
        self.transactions = self.load_transactions("transactions.json")

        
    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)     # Create a main frame within the root window
        self.main_frame.pack()       # Pack the main frame into the root window

        # Frame for table and scrollbar
        self.frame = ttk.Frame(self.main_frame)     # Create a frame within the main frame for the table and scrollbar
        self.frame.pack(side=tk.LEFT)     # Pack the frame to the left side of the main frame

        # Treeview for displaying transactions
        self.tree = ttk.Treeview(self.frame, columns=("Category", "Amount", "Date"), show="headings")  # Create a Treeview widget within the frame

        # Set headings for columns and define sorting behavior
        self.tree.heading("Category", text="Category", command=lambda: self.sort_by_column("Category", False))
        self.tree.heading("Amount", text="Amount", command=lambda: self.sort_by_column("Amount", False))
        self.tree.heading("Date", text="Date", command=lambda: self.sort_by_column("Date", False))
        self.tree.pack(side=tk.LEFT)    # Pack the Treeview to the left side of the frame


        # Scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)  # Create a vertical scrollbar within the frame
        self.scrollbar.pack(side="right", fill="y")  # Pack the scrollbar to the right side of the frame and fill it vertically
        self.tree.configure(yscrollcommand=self.scrollbar.set)    # Configure the Treeview to use the scrollbar for vertical scrolling

        # Search bar and button
        self.search_var = tk.StringVar()  # Create a StringVar to store search input

        self.search_entry = ttk.Entry(self.root, textvariable=self.search_var)   # Create an entry widget for search input
        self.search_entry.pack()  # Pack the search entry widget

        self.search_button = ttk.Button(self.root, text="Search", command=self.search_transactions)  # Create a button to trigger search
        self.search_button.pack()    # Pack the search button

         # Variables to track sorting state
        self.sorted_column = None    # Track the column currently sorted
        self.sort_reverse = False     # Track if sorting is in reverse order


    def load_transactions(self, filename):
       try:
          with open(filename, "r") as file:  # Open the JSON file for reading
            data = json.load(file)  # Load transactions from the file
            transactions = [] 
            for category, items in data.items():  # Iterate over each category and its associated items in the loaded data
                for item in items:  # Iterate over each item in the category
                    # Append a dictionary representing the transaction to the transactions list
                    transactions.append({"Category": category, "Amount": item["amount"], "Date": item["date"]})
            return transactions  # Return the list of transactions
       except FileNotFoundError:  # Handle the case where the file is not found
          print("File not found")
          return []  

    def display_transactions(self, transactions):
        # Remove existing entries
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Add transactions to the treeview
        for transaction in transactions:
            # Insert a new row into the Treeview with transaction details
            self.tree.insert("", "end", values=(transaction["Category"], transaction["Amount"], transaction["Date"]))

    def search_transactions(self):
        # Get the search term from the search entry, strip leading/trailing whitespace, and convert to lowercase
        search_term = self.search_var.get().strip().lower()

        # Check if the search term is not empty
        if search_term:

            # Filter transactions based on the search term
            filtered_transactions = [transaction for transaction in self.transactions
                                     if search_term in transaction["Category"].lower()  # Check if the search term is in the category (case-insensitive)
                                     or search_term in str(transaction["Amount"])  # Check if the search term is in the amount (as a string)
                                     or search_term in transaction["Date"]]    # Check if the search term is in the date
            
            # Display the filtered transactions in the Treeview
            self.display_transactions(filtered_transactions)

        else:
             # If the search term is empty, display all transactions
            self.display_transactions(self.transactions)
    def sort_by_column(self, col, reverse):
        # Get data from Treeview and store in a list of tuples with item value and item ID
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children("")]

        # Sort the data based on the item values, converting to int if possible, and using reverse flag
        data.sort(key=lambda x: (int(x[0]) if x[0].isdigit() else x[0]), reverse=reverse)

        # Reorder Treeview items based on the sorted data
        for index, item in enumerate(data):
            self.tree.move(item[1], "", index)

        # Update sorting state variables
        self.sorted_column = col
        self.sort_reverse = reverse

        # Update heading command to toggle sorting direction
        self.tree.heading(col, command=lambda col=col: self.sort_by_column(col, not self.sort_reverse))

def main():
    # Initialize GUI
    root = tk.Tk()  # Create the main application window
    app = FinanceTrackerGUI(root)  # Create an instance of the FinanceTrackerGUI class
    app.display_transactions(app.transactions)  # Display transactions in the GUI
    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main()  # Call the main function if the script is executed directly
