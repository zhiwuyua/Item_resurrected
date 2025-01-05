# Reuse Items Application
#### This is a Python-based application that allows users to manage a list of reusable items. The application lets users add, delete, search, and display items, along with storing item information such as the name, description, contact type (Phone or WeChat), and contact information (Phone number or WeChat ID).

The application provides a simple GUI using tkinter.

## Features
**Add Item**: Allows users to add a new item with its name, description, contact type (Phone or WeChat), and contact information.
**Delete Item**: Allows users to delete an item by its ID.
**Search Item**: Users can search for items by their name. It supports:
**Exact Match**: Displays items that exactly match the input name.
**Partial Match**: Displays items that contain any character(s) from the input name.
**Display All Items**: Displays a list of all items stored in the application.
## Prerequisites
Python 3.x
tkinter library (usually comes pre-installed with Python)
Basic knowledge of Python programming and tkinter for GUI applications.
## Installation
Ensure Python 3.x is installed on your machine.
Clone or download the repository to your local machine.
Open a terminal and navigate to the directory where the script is located.
Run the Python script:
python main.py
## How to Use
**Add Item:**
Click the Add Item button in the GUI. Enter the item name, description, and select the contact type (Phone or WeChat). Enter the contact information. If Phone is selected, it will check that the phone number is exactly 11 digits. The item will be saved and displayed in the list.

**Delete Item:**
Click the Delete Item button. Enter the item ID you want to delete, and it will be removed from the list.

**Search Item:**
Click the Find Item button. Enter the item name (it supports both exact and partial matching). If there are any exact matches, they will be displayed under Exact Matches. If there are any partial matches, they will be displayed under Partial Matches (but not duplicate exact matches).

**Display All Items:**
Click the Display All Items button to view all items saved in the application.

**Exit:**
Click the Exit button to close the application.
