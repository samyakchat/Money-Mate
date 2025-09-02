#Import All Libraries
import sqlite3
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import difflib
import certifi
import sendgrid
from sendgrid.helpers.mail import Mail
from collections import Counter
import google.generativeai as genai
load_dotenv()
API_KEY = os.getenv("GENAPI_KEY")
genai.configure(api_key=API_KEY)

DATABASE_PATH = 'Profile 1.db'
def quitp():
    quit()

# Initialize the Database
def initialize_database():
    # Connect to the Database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    # Execute the SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

#This writes the file for recent searches
def write_search():
    global file_path
    
    file_path = "/Users/samyakchatterjee/Documents/Javascript projects/FBLA/SEARCHES.txt"
    global slines
    if os.path.exists(file_path):
        #open and read
        with open(file_path, 'r') as file:
            slines = file.readlines()

#Help Center Code
def helpcenter():
    global qentry
    rlydestroy_all_widgets(root)
    menu()
    titleadd = tk.Label(root, text="Welcome, to Money-Mate", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
    titleadd.place(relx=0.55, rely=0.1, anchor="center")
    cc = tk.Label(root, text='''
Transactions are to be added with a Status (Income or Expense), Amount,
    Category, Date and an optional description. 
                  
Users can search these Transactions with SEARCH, and filter by date. 
    Last 10 recent searches are previewed.
                  
Users can also view all transactions with SHOW TRANSACTIONS. This will allow 
    you to edit and remove these transactions.
                  
Users can Generate Summaries as well, providing either a monthly or weekly summary
    These show things like total income and expense, 
    category distribution and more.
                  
Users can finally view their profile which shows activity and total balance.
''', font=("Shree Devangari 714", 17), fg="#ff5757")
    
    # Question and chatbot entry
    cc.place(relx = 0.18, rely = 0.14)
    cc.config()
    qq = tk.Label(root, text="Questions?", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
    qq.place(relx=0.55, rely=0.625, anchor="center")
    qlabel = tk.Label(root, text="Use our ChatBot!", font=("Shree Devangari 714", 17), fg="#ff5757")
    qlabel.place(relx=0.55, rely=0.678, anchor="center")
    emaillabel = tk.Label(root, text="", font=("Shree Devangari 714", 17), fg="#ff5757")
    emaillabel.place(relx=0.28, rely=0.78)
    emaillabel.config(justify='left')
    qentry = tk.Entry(root,font=("Shree Devangari 714", 17), highlightthickness=3, highlightcolor="#ff5757", highlightbackground="#ff5757", fg='gray28',width=41)
    qentry.place(relx = 0.28, rely = 0.72)

  

    def interactive_faq():
        global user_input, email_button
        faq = {
            #Sample Questions that the Chatbot will recognize
            "What does this app do?": "Track student finances and present summaries of transactions.",
            "How do I view the transactions?": "Click on the SHOW TRANSACTIONS button, and filter by choice.",
            "What is a way for me to search transactions?": "Go to SEARCH TRANSACTIONS, and filter by date. (Optional)",
            "How can I see the weekly summaries?": "Go to GENERATE SUMMARY, and pick weekly",
            "How can I see the monthly summaries?": "Go to GENERATE SUMMARY, and pick monthly"
        }
        #Using the Library to find the best match
        def find_best_match(user_input):
            #This function uses the Library to Execute AI Functions
            questions = list(faq.keys())
            matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)
            return matches[0] if matches else None

        user_input = qentry.get()
        user_input = user_input.strip()
        #We call the AI Function
        best_match = find_best_match(user_input)

        #Testing to see whether our features matched to a known question
        if best_match:
            emaillabel.config(text=f"{faq[best_match]}")
            email_button = tk.Button(root, text="Email Money-Mate", command=sendemail0, font=("Shree Devangari 714", 18), foreground='#ff5757')
            email_button.place(relx=0.55, rely=0.84, anchor="center")
        else:
            emaillabel.config(text="Sorry, I don't know. Please try rephrasing your question.")
            email_button = tk.Button(root, text="Email Money-Mate", command=sendemail0, font=("Shree Devangari 714", 18), foreground='#ff5757')
            email_button.place(relx=0.55, rely=0.84, anchor="center")

    def sendemail0():
        global senderentry, sendbut
        senderentry = tk.Entry(root,font=("Shree Devangari 714", 17), highlightthickness=3, highlightcolor="#ff5757", highlightbackground="#ff5757", fg='gray28')
        senderentry.place(relx = 0.42, rely = 0.87)
        senderentry.insert(0, "Provide email here")
        sendbut = tk.Button(root, text="Send", command=sendemail1, font=("Shree Devangari 714", 20), foreground='#ff5757')
        sendbut.place(relx=0.71, rely=0.89, anchor="center")


    def sendemail1():
        #Sending an email Through SENDGRID
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
        recemail = senderentry.get()
        load_dotenv()
        SENDGRRIDAPI_KEY = os.getenv("SENAPI_KEY")
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRRIDAPI_KEY)
        #This is the Actual Message, plugging in necesarry things
        message = Mail(
            from_email='moneymate.app.business@gmail.com',
            to_emails='moneymate.app.business@gmail.com',
            subject=f'MONEY BOT for {recemail}',
            
            html_content=f'Hello, Money Mate.<br><br>My question is: {user_input}<br>Recipient Email: {recemail}'
        )

        try:
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            senderentry.destroy()
            sendbut.destroy()
            email_button.destroy()
            qentry.delete(0, tk.END)
            emaillabel.config(text='')
        except Exception as e:
            print(e)


    button_searchd = tk.Button(root, text="Go", command=interactive_faq, font=("Shree Devangari 714", 23), foreground='#ff5757')
    button_searchd.place(relx=0.82, rely=0.74, anchor="center")

# Fetch existing categories from the database
def get_existing_categories():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM transactions')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

# Add transaction to the database
def add_transaction(transaction_type, amount, category, date, description):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (type, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (transaction_type, amount, category, date, description))
    conn.commit()
    conn.close()

def edit_transaction(transaction_id, date, transaction_type, category, amount, description):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions 
        SET date = ?, type = ?, category = ?, amount = ?, description = ?
        WHERE id = ?
    ''', (date, transaction_type, category, amount, description, transaction_id))
    conn.commit()
    conn.close()

def aitrans():
    
    rlydestroy_all_widgets(root)
    menu()
    def calc():
        z = aentry.get("1.0", tk.END)

        z = rungem(z)
        #This is the AI Function that plugs in the variables
        newlist = z.split("|")
        cleaned_list = []
        
        for item in newlist:
            # Remove leading/trailing whitespace
            item = item.strip()
            # Skip empty items
            if not item:
                continue
            cleaned_list.append(item)
            
        # Only keep the first 5 items (type, amount, category, date, description)
        cleaned_list = cleaned_list[:5]
        
        # Make sure we have exactly 5 items
        while len(cleaned_list) < 5:
            cleaned_list.append('None')
            
        # Add the transaction using the cleaned list
        try:
            add_transaction(
                transaction_type=cleaned_list[0].lower(),  # Convert type to lowercase
                amount=cleaned_list[1],
                category=cleaned_list[2], 
                date=cleaned_list[3],
                description=cleaned_list[4]
            )
            aentry.delete("1.0", tk.END)
            # Optionally add success message
        except Exception as e:
            print(f"Error adding transaction: {e}")
            # Optionally show error message to user
        
    def rungem(z):
        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction="i will type a sentence and you will create the SQL code by setting the variables type amount category date and description. This is a finance app and you have to dechiper my sentence into each variable. for type it can only be Income or Expense. for amount it has to be a number. for category it can be whatever. for date it has to be year-month-day. for description its optional, but can also be whatever. Here is the SQL code: INSERT INTO transactions (type, amount, category, date, description)\n        VALUES (?, ?, ?, ?, ?)\n All you have to do is give me the variables to plug in and I will do the rest. Please keep it in this format: the type | amount | category | date | description (do not include those words please)\n\nFOR EXAMPLE \nMy input: income on feb 23 i got lik 9 dollars for a bet it was pretty bad\nBad response: transaction_type: Income | amount: 9 | category: Bet | date: 2024-02-23 | description: it was pretty bad\nGood reponse: Income | 9 | Bet | 2025-02-23 | it was pretty bad\nSo for your output you will replace those words not keep them, and if there is no description keep it empty do NOT put something there. your ouput will NOT be transaction_type: Expense | amount: 9 | etc etc, instead it wil be expense | 8 etc etc\nIf something is wrong then when u give the error response first put the characters pops1 before ANY ERROR MESSAGE. So far the default year is 2025 if they do not say the year\n\n\n",
        )

        chat_session = model.start_chat(
        history=[
            {
            "role": "user",
            "parts": [
                "alr so like income 76 bucks for food on feb 26 this year and no desciprtion\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "transaction_type: Income | amount: 76 | category: Food | date: 2024-02-26 | description: None\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "expsnee 89 dollary doos feb 30 25 no desc\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "pops1: Invalid date. February only has 28 or 29 days in a leap year.\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "expesene on feb 23 i spent like 8 in like food idk and it was pretty goos\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "transaction_type: Expense | amount: 8 | category: Food | date: 2024-02-23 | description: it was pretty goos\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "expesene on feb 23 i spent like 8 in like food idk and it was pretty goos",
            ],
            },
            {
            "role": "model",
            "parts": [
                "transaction_type: Expense | amount: 8 | category: Food | date: 2024-02-23 | description: it was pretty goos\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "expesene on feb 23 i spent like 8 in like food idk and it was pretty goos\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "transaction_type: Expense | amount: 8 | category: Food | date: 2024-02-23 | description: it was pretty goos\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "income on feb 23 i got lik 9 dollars for a bet it was pretty bad",
            ],
            },
            {
            "role": "model",
            "parts": [
                "transaction_type: Income | amount: 9 | category: Bet | date: 2024-02-23 | description: it was pretty bad\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "income on feb 23 i got lik 9 dollars for a bet it was pretty bad\n\n\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "transaction_type: Income | amount: 9 | category: Bet | date: 2024-02-23 | description: it was pretty bad\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "income on feb 23 i got lik 9 dollars for a bet it was pretty bad\n\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Income | 9 | Bet | 2024-02-23 | it was pretty bad\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "expenasae on march 23 i spent 8 bucks on brisket and it was good\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Expense | 8 | Brisket | 2024-03-23 | it was good\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "i spent like 90 dolars on this rly good burger on march 23 2025\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Expense | 90 | Burger | 2025-03-23 | this rly good burger\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "i spent like 90 dolars on this rly good burger on march 23 2025\n\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Expense | 90 | Burger | 2025-03-23 | this rly good burger\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "i spent like 90 dolars on this rly good burger on march 23 \n\n\n\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Expense | 90 | Burger | 2025-03-23 | this rly good burger\n",
            ],
            },
            {
            "role": "user",
            "parts": [
                "i spent like 90 dolars on this rly good burger on march 23\n\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Expense | 90 | Burger | 2025-03-23 | this rly good burger\n",
            ],
            },
        ]
        )

        z = chat_session.send_message(z)
        return(z.text)
    
    qq = tk.Label(root, text="Tell us about the purchase!", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
    qq.place(relx=0.57, rely=0.325, anchor="center")
    qlabel = tk.Label(root, text="Make sure to include the date, amount, and our AI will do the rest!", font=("Shree Devangari 714", 17), fg="#ff5757")
    qlabel.place(relx=0.57, rely=0.378, anchor="center")
    aentry = tk.Text(root,font=("Shree Devangari 714", 17), highlightthickness=3, highlightcolor="#ff5757", highlightbackground="#ff5757", fg='gray28',width=47, height=3)
    aentry.place(relx = 0.28, rely = 0.42)

    submittrans = tk.Button(root, text="Submit ", command=calc, font=("Shree Devangari 714", 17), width=48)
    submittrans.place(relx=0.5715, rely=0.537, anchor="center")

# Add Transaction GUI with category dropdown
def add_transaction_gui():
    
    global trantype, tranlabel1, titleadd, date_var, day_var, month_var, year_var, amtlab, amtentry, catlab, datecheck
    def submit_transaction():
        
        transaction_type = type_var.get()
        amount_var = amtentry.get()
        amount = (amount_var)
        # amount = (amount_var.get())
        category = category_var.get()
        date = date_var.get()
        description = description_var.get()

        if not transaction_type or not amount or not category or not date:
            status_label.config(text="All fields except description are required!", fg="red")
            return

        try:
            add_transaction(transaction_type, amount, category, date, description)
            status_label.config(text="Transaction added successfully!", fg="green")
            trantype.set("")
            amtentry.delete(0, tk.END)
            category_dropdown.set("")
            k.delete(0, tk.END)
            status_label.pack_forget()
         


        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="white")

    rlydestroy_all_widgets(root)
    menu()
  
    datecheck = 0
   
    titleadd = tk.Label(root, text="Add Transaction", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
    titleadd.pack()
    titleadd.place(relx=0.55, rely=0.1, anchor="center")

    aibut = tk.Button(root, image=aiart, command=aitrans, font=("Shree Devangari 714", 17))
    aibut.pack()
    aibut.place(relx=0.245, rely=0.93, anchor="center")

    type_var = tk.StringVar()
    trantype = ttk.Combobox(root, textvariable=type_var, values=["income", "expense"], font=("Shree Devangari 714", 17), state="readonly")
    trantype.pack(side=tk.TOP)
    trantype.place(relx=0.66, rely=0.2, anchor="center")

    tranlabel1 = tk.Label(root, text="Transaction Type:", font=("Shree Devangari 714", 18), fg="#ff5757")
    tranlabel1.pack()
    tranlabel1.place(relx=0.426, rely=0.2, anchor="center")
    

    amtlab = tk.Label(root, text="Amount:", font=("Shree Devangari 714", 17), fg="#ff5757")
    amtlab.pack()
    amtlab.place(relx=0.47, rely=0.28, anchor="center")

    amount_var = 0.00
    print(type(amount_var))

    amtentry = tk.Entry(root, textvariable=amount_var,font=("Shree Devangari 714", 17), highlightthickness=3, highlightcolor="#ff5757", highlightbackground="#ff5757", fg='gray28')
    amtentry.pack()
    amtentry.place(relx=0.65, rely=0.28, anchor="center")
    

    catlab = tk.Label(root, text="Category:", font=("Shree Devangari 714", 17), fg="#ff5757")
    catlab.pack()
    catlab.place(relx=0.463, rely=0.36, anchor="center")

    category_var = tk.StringVar()
    existing_categories = get_existing_categories()  # Fetch categories from the database
    category_dropdown = ttk.Combobox(root, textvariable=category_var, values=existing_categories, font=("Shree Devangari 714", 17))
    category_dropdown.pack()
    category_dropdown.place(relx=0.66, rely=0.36, anchor='center')

    datetitle = tk.Label(root, text="Date:", font=("Shree Devangari 714", 17), fg="#ff5757")
    datetitle.pack()
    datetitle.place(relx=0.48, rely=0.46, anchor="center")

    years = [str(year) for year in range(1990, 2041)]
    months = [f"{month:02}" for month in range(1, 13)]
    days = [f"{day:02}" for day in range(1, 32)]


    yr = tk.OptionMenu(root, year_var, *years, command=lambda _: update_date_var())
    mr = tk.OptionMenu(root, month_var, *months, command=lambda _: update_date_var())
    dr = tk.OptionMenu(root, day_var, *days, command=lambda _: update_date_var())
    yr.pack()
    mr.pack()
    dr.pack()
    yr.place(relx=0.555, rely=0.46, anchor="center")
    mr.place(relx=0.625, rely=0.46, anchor="center")
    dr.place(relx=0.695, rely=0.46, anchor="center")    


    updatelabel = tk.Label(root, textvariable=date_var, font=("Shree Devangari 714", 17), fg="#ff5757")
    updatelabel.pack()
    updatelabel.place(relx=0.83, rely=0.46, anchor="center")

    yl = tk.Label(root, text='Year', font=("Shree Devangari 714", 13), fg="#ff5757")
    ml = tk.Label(root, text='Month', font=("Shree Devangari 714", 13), fg="#ff5757")
    dl = tk.Label(root, text='Day', font=("Shree Devangari 714", 13), fg="#ff5757")
    yl.pack()
    ml.pack()
    dl.pack()
    yl.place(relx=0.555, rely=0.495, anchor="center")
    ml.place(relx=0.625, rely=0.495, anchor="center")
    dl.place(relx=0.695, rely=0.495, anchor="center") 
    

    descl = tk.Label(root, text="Description:", font=("Shree Devangari 714", 17), fg="#ff5757")
    descl.pack()
    descl.place(relx=0.45, rely=0.54, anchor="center")

    description_var = tk.StringVar()
    k = tk.Entry(root, textvariable=description_var, font=("Shree Devangari 714", 17), fg="#ff5757", highlightthickness=3, highlightcolor="#ff5757", highlightbackground="#ff5757")
    k.pack()
    k.place(relx=0.65, rely=0.54, anchor="center")

    submittrans = tk.Button(root, text=" Submit ", command=submit_transaction, font=("Shree Devangari 714", 17))
    submittrans.pack()
    submittrans.place(relx=0.6, rely=0.65, anchor="center")

    # Status label to show success/error messages
    status_label = tk.Label(root, text="", fg="green", font=("Shree Devangari 714", 17))
    status_label.pack()
    status_label.place(relx=0.6, rely=0.69, anchor="center")

def edit_transaction_gui(transaction_data):
    global trantype, tranlabel1, titleadd, date_var, day_var, month_var, year_var, amtlab, amtentry, catlab
    
    def submit_transaction_edit():
        transaction_type = type_var.get()
        amount = amtentry.get()
        category = category_var.get()
        date = date_var.get()
        description = description_var.get()
        transaction_id = transaction_data[0]

        if not transaction_type or not amount or not category or not date:
            status_label.config(text="All fields except description are required!", fg="red")
            return

        try:
            edit_transaction(transaction_id, date, transaction_type, category, amount, description)
            status_label.config(text="Transaction updated successfully!", fg="green")
            show_transactions_gui()  # Return to transactions view
        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="white")

    rlydestroy_all_widgets(root)
    menudisabled()
    
    titleadd = tk.Label(root, text="Edit Transaction", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
    titleadd.pack()
    titleadd.place(relx=0.55, rely=0.1, anchor="center")

    # Pre-fill the form with existing transaction data
    type_var = tk.StringVar(value=transaction_data[1])  # type
    trantype = ttk.Combobox(root, textvariable=type_var, values=["income", "expense"], 
                           font=("Shree Devangari 714", 17), state="readonly")
    trantype.pack(side=tk.TOP)
    trantype.place(relx=0.66, rely=0.2, anchor="center")

    tranlabel1 = tk.Label(root, text="Transaction Type:", font=("Shree Devangari 714", 18), fg="#ff5757")
    tranlabel1.pack()
    tranlabel1.place(relx=0.426, rely=0.2, anchor="center")

    amtlab = tk.Label(root, text="Amount:", font=("Shree Devangari 714", 17), fg="#ff5757")
    amtlab.pack()
    amtlab.place(relx=0.47, rely=0.28, anchor="center")

    amtentry = tk.Entry(root, font=("Shree Devangari 714", 17), highlightthickness=3, 
                       highlightcolor="#ff5757", highlightbackground="#ff5757", fg='gray28')
    amtentry.insert(0, transaction_data[2])  # amount
    amtentry.pack()
    amtentry.place(relx=0.65, rely=0.28, anchor="center")

    catlab = tk.Label(root, text="Category:", font=("Shree Devangari 714", 17), fg="#ff5757")
    catlab.pack()
    catlab.place(relx=0.463, rely=0.36, anchor="center")

    category_var = tk.StringVar(value=transaction_data[3])  # category
    existing_categories = get_existing_categories()
    category_dropdown = ttk.Combobox(root, textvariable=category_var, values=existing_categories, 
                                   font=("Shree Devangari 714", 17))
    category_dropdown.pack()
    category_dropdown.place(relx=0.66, rely=0.36, anchor='center')

    # Date widgets
    datetitle = tk.Label(root, text="Date:", font=("Shree Devangari 714", 17), fg="#ff5757")
    datetitle.pack()
    datetitle.place(relx=0.48, rely=0.46, anchor="center")

    # Pre-fill date
    existing_date = transaction_data[4].split('-')
    year_var.set(existing_date[0])
    month_var.set(existing_date[1])
    day_var.set(existing_date[2])
    

    years = [str(year) for year in range(1990, 2041)]
    months = [f"{month:02}" for month in range(1, 13)]
    days = [f"{day:02}" for day in range(1, 32)]

    yr = tk.OptionMenu(root, year_var, *years, command=lambda _: update_date_var())
    mr = tk.OptionMenu(root, month_var, *months, command=lambda _: update_date_var())
    dr = tk.OptionMenu(root, day_var, *days, command=lambda _: update_date_var())
    yr.pack()
    mr.pack()
    dr.pack()
    yr.place(relx=0.555, rely=0.46, anchor="center")
    mr.place(relx=0.625, rely=0.46, anchor="center")
    dr.place(relx=0.695, rely=0.46, anchor="center")   
     

    updatelabel = tk.Label(root, textvariable=date_var, font=("Shree Devangari 714", 17), fg="#ff5757")
    updatelabel.pack()
    updatelabel.place(relx=0.83, rely=0.46, anchor="center")

    descl = tk.Label(root, text="Description:", font=("Shree Devangari 714", 17), fg="#ff5757")
    descl.pack()
    descl.place(relx=0.45, rely=0.54, anchor="center")

    description_var = tk.StringVar(value=transaction_data[5])  # description
    k = tk.Entry(root, textvariable=description_var, font=("Shree Devangari 714", 17), 
                 fg="#ff5757", highlightthickness=3, highlightcolor="#ff5757", highlightbackground="#ff5757")
    k.pack()
    k.place(relx=0.65, rely=0.54, anchor="center")

    submittrans = tk.Button(root, text="Update", command=submit_transaction_edit, 
                           font=("Shree Devangari 714", 17))
    submittrans.pack()
    submittrans.place(relx=0.6, rely=0.65, anchor="center")

    status_label = tk.Label(root, text="", fg="green", font=("Shree Devangari 714", 17))
    status_label.pack()
    status_label.place(relx=0.6, rely=0.69, anchor="center")
    update_date_var()


# Generate summary of transactions
def generate_summary(period):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    if period == 'Weekly':
        cursor.execute('''
            SELECT strftime('%W', date) AS week, 
                   SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS expenses,
                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS income,
                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) - 
                   SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS savings
            FROM transactions 
            GROUP BY week
        ''')
    elif period == 'Monthly':
        cursor.execute('''
            SELECT strftime('%Y-%m', date) AS month, 
                   SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS expenses,
                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS income,
                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) - 
                   SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS savings
            FROM transactions 
            GROUP BY month
        ''')
    results = cursor.fetchall()
    conn.close()
    return results

# Search transactions
def search_transactions(    temp, optemp,keyword):
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    if datecheck == 1:
        query = f'''
        SELECT * FROM transactions 
        WHERE description LIKE ? OR category LIKE ?
        '''
        #Plug in the search for both Categories and Descriptions
        cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
        #Each keyword is a string that we plug in
        results = cursor.fetchall()

               
        print('before:   '+str(results))
        for e in range(0,2):

            for i, row in enumerate(results):
                if date_var.get() == row[4]:
                    print('accepted: '+str(row[4]))
                    continue
                else:
                    print('removed: '+str(row[4]))
                    results.remove(row)
                    

        print(results)
        print(date_var.get())



    else:
        query = '''
        SELECT * FROM transactions 
        WHERE description LIKE ? OR category LIKE ? OR date LIKE ?
        '''
        #Plug in the search for both Categories, Descriptions and Dates
        cursor.execute(query, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        #Same thing occurs except we plug in the date as well
        results = cursor.fetchall()
    conn.close()
    return results
optemp = 'id'

# Remove transaction from the database
def remove_transaction(transaction_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()

# Show Transactions GUI
def show_transactions_gui():
    global showtable, op_var, optemp
    rlydestroy_all_widgets(root)
    menu()
    titleshow = tk.Label(root, text="Show Transactions", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
    titleshow.pack()
    titleshow.place(relx=0.55, rely=0.1, anchor="center")
    
    # Function to fetch and display transactions in the GUI

            
    def show_transactions():
        op1op = ['Id', 'Type', 'Amount', 'Category', 'Date', 'Description']
        op1 = tk.OptionMenu(root, op_var, *op1op, command=lambda _: update_op1_var())
        op1.pack()
        op1.place(relx=0.45, rely=0.2, anchor="center")
        root.update()
        op1label = tk.Label(root, text="Order by:", font=("Shree Devangari 714", 17), fg="#ff5757")
        op1label.pack()
        op1label.place(relx=0.45, rely=0.17, anchor="center")
        op2label = tk.Label(root, text="Filter by:", font=("Shree Devangari 714", 17), fg="#ff5757")
        op2label.pack()
        op2label.place(relx=0.65, rely=0.17, anchor="center")

        op2op = get_existing_categories()
        op2op.append('all')

        op2 = tk.OptionMenu(root, fromvar, *op2op, command=lambda _: update_op1_var())
        op2.pack()
        op2.place(relx=0.65, rely=0.2, anchor="center")
        
        #int(op1.winfo_x)-int(op1.winfo_width)-10
    
        global transactions
        showtable = ttk.Treeview(root, columns=("num", "transaction", "amount", "category", "date", "description"),
                              show='headings', style="Custom.Treeview", height=25)
        
        # Create buttons (initially hidden)
        edit_button = tk.Button(
            root,
            text='Edit',
            command=lambda: edit_selected_transaction(),
            font=("Shree Devangari 714", 15),
            fg='#ff5757'
        )
        remove_button = tk.Button(
            root,
            text='Remove',
            command=lambda: remove_selected_transaction(),
            font=("Shree Devangari 714", 15),
            fg='#ff5757'
        )
        
        def on_row_select(event):
            # Get selected item
            selected_items = showtable.selection()
            if selected_items:
                # Show buttons above table
                edit_button.place(x=150, y=180)
                remove_button.place(x=190, y=180)
            else:
                # Hide buttons if no selection
                edit_button.place_forget()
                remove_button.place_forget()
        
        def edit_selected_transaction():
            selected_item = showtable.selection()[0]
            row_data = showtable.item(selected_item)['values']
            edit_transaction_gui(row_data)
        
        def remove_selected_transaction():
            selected_item = showtable.selection()[0]
            transaction_id = showtable.item(selected_item)['values'][0]
            
            # Remove from database
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
            conn.close()
            
            # Remove from treeview
            showtable.delete(selected_item)
            
            # Hide buttons after removal
            edit_button.place_forget()
            remove_button.place_forget()

        # Bind selection event to table
        showtable.bind('<<TreeviewSelect>>', on_row_select)
        
        # Create and populate table as before
        showtable.heading("num", text="#")
        showtable.heading("transaction", text="Type")
        showtable.heading("amount", text="Amount")
        showtable.heading("category", text="Category")
        showtable.heading("date", text="Date")
        showtable.heading("description", text="Description")


        showtable.column("num", anchor=tk.CENTER, width=50)
        showtable.column("transaction", anchor=tk.CENTER, width=100)
        showtable.column("amount", anchor=tk.CENTER, width=100)
        showtable.column("category", anchor=tk.CENTER, width=100)
        showtable.column("date", anchor=tk.CENTER, width=170)
        showtable.column("description", anchor=tk.CENTER, width=240)


        transactions = get_transactions(optemp, fromvartemp)
        for row in transactions:
            showtable.insert("", tk.END, values=row)
        
        showtable.pack(fill=tk.BOTH, expand=True)
        showtable.place(x=130, y=220)


            
       
        def update_op1_var():
            root.update()

            
            def regen():
                for item in showtable.get_children():
                    showtable.delete(item)

                transactions = get_transactions(optemp, fromvartemp)
                
                for row in transactions:
                    showtable.insert("", tk.END, values=row)
                
                # Hide the edit/remove buttons when regenerating the table
                edit_button.place_forget()
                remove_button.place_forget()
            
            optemp = (op_var.get())
            print(optemp)
            fromvartemp0 = (fromvar.get())
            print(fromvartemp0)
            if fromvartemp0 == 'all':
                fromvartemp = ''
            else:
                fromvartemp = fromvartemp0
            print(fromvartemp)
            regen()

    
    # Function to remove a selected transaction and refresh the list

    def remove_selected_transaction(transaction_id):
        try:
            # Call a function to remove the transaction (assumes remove_transaction() exists)
            remove_transaction(transaction_id)
            for item in showtable.get_children():
                if showtable.item(item, 'values')[0] == transaction_id:
                    showtable.delete(item)
                    
                    # Connect to the SQLite database
                    conn = sqlite3.connect(DATABASE_PATH)
                    cursor = conn.cursor()

                    # Execute DELETE query to remove the transaction with the given ID
                    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

                    # Commit the changes to the database
                    conn.commit()
                    
                    # Update the status label to indicate success
                    status_label.config(text="Transaction removed successfully!", fg="green")

                    break

        
            

        except Exception as e:
            # Display an error message in the status label if an exception occurs
            status_label.config(text=f"Error: {e}", fg="white")

        show_transactions()
    
    


    # Status label to display success or error messages
    status_label = tk.Label(root, text="", fg="green")
    status_label.pack()

    show_transactions()

# Get all transactions for the show GUI
def get_transactions(optemp, fromvartemp):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(f'''
                   SELECT * FROM transactions 
                   WHERE category = '{fromvartemp}' OR '{fromvartemp}' = ''
                   ORDER BY {optemp}
                   
                   
                   ''') 
    
    transactions = cursor.fetchall()
    print(transactions)
    conn.close()
    return transactions

# View Balance GUI
def profileupdate():
    global DATABASE_PATH
    profile = prof.get()
    if profile == 'Profile 1':
        DATABASE_PATH = 'Profile 1.db'
        
    elif profile == 'Profile 2':
        DATABASE_PATH = 'Profile 2.db'

    elif profile == 'Profile 3':
        DATABASE_PATH = 'Profile 3.db'
    initialize_database()
    view_balance_gui()
    print("New DATABASE_PATH:", DATABASE_PATH)
        


def view_balance_gui():
    global prof
    rlydestroy_all_widgets(root)
    menu()
    titletext1 = tk.Label(root, text="Your Balance is:", font=("DIN Alternate", 30, 'bold'), fg="#ff5757")
    titletext1.place(relx=0.46, rely=0.06)
    prframe = Frame(root, width=150, height=75, bg='gray93')
    prframe.pack()
    prframe.place(relx=0.24, rely=0.09, anchor="center")
    status_label = tk.Label(root, text="sigm", font=("DIN Alternate", 80, 'bold'), fg="#ff5757")
    profilevar = ['Profile 1', 'Profile 2', 'Profile 3']
    pr1 = tk.OptionMenu(root, prof, *profilevar, command=lambda _: profileupdate())
    pr1.pack()
    pr1.place(relx=0.24, rely=0.11, anchor="center")
    op1label = tk.Label(root, text="Switch Profiles:", font=("DIN Alternate", 17), fg="white",bg='Indianred1', width=16)
    op1label.pack()
    op1label.place(relx=0.24, rely=0.06, anchor="center")

    root.update()

    def exwidget():

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT SUM(amount) AS total_spent
        FROM transactions
        WHERE date >= DATE('now', 'start of month')
        AND type = 'expense'


        ''')
        feels = cursor.fetchall()
        if feels != 'None':
            feels = str(feels[0])
            feels = feels[1:]
            feels = feels.strip(',)')
            feels = '$'+str(feels)
        else:
            feels = '$0.00'
        
        conn.close()

        
        frame2 = Frame(root, width=298, height=200, bg='gray93')
        frame2.pack()
        frame2.place(x=210,y=250)

        vis_label = Label(root, text='This months spending!', bg='Indianred1', fg='white', cursor='xterm', font=('Futura 25'), width=18)
        vis_label.pack()
        vis_label.place(x=210,y=250)

        vis_miles = Label(frame2, text=feels, bg='gray93', fg='gray13', cursor='xterm', font=('Futura 50'))
        vis_miles.pack()
        vis_miles.place(relx=0.5, rely=0.55, anchor='center')
    def incwidget():

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT SUM(amount) AS total_spent
        FROM transactions
        WHERE date >= DATE('now', 'start of month')
        AND type = 'income'


        ''')
        inc = cursor.fetchall()
        inc = str(inc[0])
        inc = inc[1:]
        inc = inc.strip(',)')
        if inc != 'None':

            inc = '$'+str(inc)
        else:
            inc = '$0.00'
        conn.close()


        incwid_frame = Frame(root, width=298, height=200, bg='gray93')
        incwid_frame.pack()
        incwid_frame.place(x=520,y=250)

        inctitle = Label(root, text='This months earnings!', bg='Indianred1', fg='white', cursor='xterm', font=('Futura 25'), width=18)
        inctitle.pack()
        inctitle.place(x=520,y=250)

        labelinc = Label(incwid_frame, text=inc, bg='gray93', fg='gray13', cursor='xterm', font=('Futura 50'))
        labelinc.pack()
        labelinc.place(relx=0.5, rely=0.55, anchor='center')
    def topex():
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT category, SUM(amount) AS total_spent
        FROM transactions
        WHERE date >= DATE('now', 'start of month')
        AND type = 'expense'
        GROUP BY category
        ORDER BY total_spent DESC
        LIMIT 1;
        ''')
        top_category = cursor.fetchone()
        if not top_category:
            top1 = 'None'
            top2 = '0.00'
        else:
            
            top_category = str(top_category)
            top_category = top_category.split()
            top1 = top_category[0][2:]
            top1 = top1.strip("',)")
            top2 = top_category[1]
            top2 = top2.strip(")")
            top2 = "at $"+top2
        conn.close()
        extop_frame = Frame(root, width=298, height=200, bg='gray93')
        extop_frame.pack()
        extop_frame.place(x=210,y=465)

        extitle = Label(root, text='This months top expense', bg='Indianred1', fg='white', cursor='xterm', font=('Futura 25'), width=18)
        extitle.pack()
        extitle.place(x=210,y=465)

        labeltopex = Label(extop_frame, text=top1, bg='gray93', fg='gray13', cursor='xterm', font=('Futura 40'))
        labeltopex.pack()
        labeltopex.place(relx=0.5, rely=0.44, anchor='center')

        labeltopex2 = Label(extop_frame, text=top2, bg='gray93', fg='gray13', cursor='xterm', font=('Futura 30'))
        labeltopex2.pack()
        labeltopex2.place(relx=0.5, rely=0.68, anchor='center')
    def topinc():
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT category, SUM(amount) AS total_spent
        FROM transactions
        WHERE date >= DATE('now', 'start of month')
        AND type = 'income'
        GROUP BY category
        ORDER BY total_spent DESC
        LIMIT 1;
        ''')
        top_2category = cursor.fetchone()
        if not top_2category:
            topinc1 = 'None'
            topinc2 = '$0.00'
        else:
        
            top_2category = str(top_2category)
            top_2category = top_2category.split()
            topinc1 = top_2category[0][2:]
            topinc1 = topinc1.strip("',)")
            topinc2 = top_2category[1]
            topinc2 = topinc2.strip(")")
            topinc2 = "at $"+topinc2
        conn.close()
        extop_frame = Frame(root, width=298, height=200, bg='gray93')
        extop_frame.pack()
        extop_frame.place(x=520,y=465)

        inctitle = Label(root, text='This months best earning', bg='Indianred1', fg='white', cursor='xterm', font=('Futura 25'), width=18)
        inctitle.pack()
        inctitle.place(x=520,y=465)

        labeltopinc = Label(extop_frame, text=topinc1, bg='gray93', fg='gray13', cursor='xterm', font=('Futura 40'))
        labeltopinc.pack()
        labeltopinc.place(relx=0.5, rely=0.44, anchor='center')

        labeltopinc2 = Label(extop_frame, text=topinc2, bg='gray93', fg='gray13', cursor='xterm', font=('Futura 30'))
        labeltopinc2.pack()
        labeltopinc2.place(relx=0.5, rely=0.68, anchor='center')
    
    incwidget()
    exwidget()
    topex()
    topinc()

    status_label.place(relx=0.58, rely=0.18,anchor='center')
    root.update()


    balance = view_balance()
    status_label.config(text=f"${balance:.2f}")

# Summary GUI
def summary_gui():
    def weekplot(week_number):
        # Create a new frame for the plot if it doesn't exist
        for widget in root.winfo_children():
            if isinstance(widget, ttk.Frame) and widget.winfo_name() == 'plot_frame':
                widget.destroy()

        plot_frame = ttk.Frame(root, name='plot_frame')
        plot_frame.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.4)

        # Connect to the database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Query to get all categories for a specific week
        query = """
        SELECT category 
        FROM transactions
        WHERE strftime('%W', date) = ?;
        """

        cursor.execute(query, (week_number,))
        rows = cursor.fetchall()

        # Extract category names from tuples
        categories = [row[0] for row in rows]

        # Print categories (one per line)
        print("\nCategories for Week", week_number)
        catlistplot = []
        perlistplot = []
        for category in categories:
            print(category)
            if category in catlistplot:
                perlistplot[catlistplot.index(category)] = perlistplot[catlistplot.index(category)]+1
            else:
                catlistplot.append(category)
                perlistplot.append(1)
        print(catlistplot)
        print(perlistplot)

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            perlistplot,
            labels=catlistplot,
            autopct='%1.1f%%',
            startangle=90
        )
        
        # Create canvas and embed it in the plot frame
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Close the connection
        conn.close()

    def show_summary(*args):  # Added *args to handle both button clicks and dropdown changes
        rlydestroy_all_widgets(root)
        menu()
        
        period = period_var.get()
        results = generate_summary(period)

        titlesum = tk.Label(root, text=f"{period} Summaries", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
        titlesum.pack()
        titlesum.place(relx=0.5, rely=0.07, anchor="center")

        # Add the period selector dropdown at the top
        tran = ttk.Combobox(root, textvariable=period_var, values=["Weekly", "Monthly"], 
                           font=("Shree Devangari 714", 17), state="readonly")
        tran.pack(side=tk.TOP)
        tran.place(relx=0.3, rely=0.15, anchor="center")

        # Create a frame for the table
        table_frame = ttk.Frame(root)
        table_frame.place(relx=0.14, rely=0.2)  # Moved down slightly to accommodate dropdown

        wmTable = ttk.Treeview(table_frame, columns=(f"Week", "Total Expenses", "Total Income", "Savings"),
                              show='headings', style="Custom.Treeview", height=5)
        wmTable.heading("Week", text=f"{period[:-2]}")
        wmTable.heading("Total Expenses", text="Total Expenses")
        wmTable.heading("Total Income", text="Total Income")
        wmTable.heading("Savings", text="Savings")

        wmTable.column("Week", anchor=tk.CENTER, width=50)
        wmTable.column("Total Expenses", anchor=tk.CENTER, width=100)
        wmTable.column("Total Income", anchor=tk.CENTER, width=100)
        wmTable.column("Savings", anchor=tk.CENTER, width=100)
        wmTable.bind("<ButtonRelease-1>", lambda e: on_row_click(e))
        
        for i, row in enumerate(results, start=1):
            wmTable.insert("", tk.END, values=row)
        
        wmTable.pack(fill=tk.BOTH, expand=True)

    def on_row_click(event):
        # Get the selected row index
        selected_item = event.widget.selection()[0]
        
        # Get the values of the selected row
        row_values = event.widget.item(selected_item, 'values')
        
        
        # Extract the value of week/month
        value_a = row_values[0]
        if period_var.get() == 'Weekly':
            weekplot(value_a)

    # Initial setup
    rlydestroy_all_widgets(root)
    menu()
    period_var = tk.StringVar(value="Weekly")  # Set default value to Weekly
    period_var.trace('w', show_summary)  # Add trace to update when dropdown changes
    weekplot('00')
    
    # Show initial weekly summary
    
    show_summary()

# Search Transactions GUI
def search_transactions_gui():
    global datecheck, date_search, updatelabel
    datecheck = 9
    rlydestroy_all_widgets(root)
    menu()






    def on_label_click(event, clicked_label):
    # Print the text of the clicked label
        l = (clicked_label.cget('text'))
        box_search.delete(0, tk.END)
        box_search.insert(0, str(l)[5:][:-1])
        button_search.invoke()
    
    def addate():
        global datecheck
        datecheck = 1
   
        date_search.destroy()
        updatelabel.destroy()

    def show_results():
        print('ecenprior: '+str(datecheck))
        keyword = keyword_var.get()
        box_search.delete(0, tk.END)
        if os.path.exists(file_path):
            #open and read
            with open(file_path, 'r') as file:
                slines = file.readlines()

            slines.pop()
            slines.insert(0, str(keyword)+'\n')  # Add a new line at the top

            #open again and read
            with open(file_path, 'w') as file:
                file.writelines(slines)
            print("".join(slines))

        rlydestroy_all_widgets(root)
        menu()

        titleshow = tk.Label(root, text="Search Results", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
        titleshow.pack()
        titleshow.place(relx=0.55, rely=0.1, anchor="center")
   
        op1op = ['Id', 'Type', 'Amount', 'Category', 'Date', 'Description']
        op1 = tk.OptionMenu(root, op_var2, *op1op, command=lambda _: updatesearch_var())
        op1.pack()
        op1.place(relx=0.45, rely=0.2, anchor="center")
        root.update()
        op1label = tk.Label(root, text="Order by:", font=("Shree Devangari 714", 17), fg="#ff5757")
        op1label.pack()
        op1label.place(relx=0.45, rely=0.17, anchor="center")
        op2label = tk.Label(root, text="Filter by:", font=("Shree Devangari 714", 17), fg="#ff5757")
        op2label.pack()
        op2label.place(relx=0.65, rely=0.17, anchor="center")

        op2op = get_existing_categories()
        op2op.append('all')

        op2 = tk.OptionMenu(root, fromvar2, *op2op, command=lambda _: updatesearch_var())
        op2.pack()
        op2.place(relx=0.65, rely=0.2, anchor="center")
        
        #TREE
        sshowtable = ttk.Treeview(root, columns=("num", "transaction", "amount", "category", "date", "description"),show='headings', style="Custom.Treeview", height=25)
        sshowtable.heading("num", text="#")
        sshowtable.heading("transaction", text="Type")
        sshowtable.heading("amount", text="Amount")
        sshowtable.heading("category", text="Category")
        sshowtable.heading("date", text="Date")
        sshowtable.heading("description", text="Description")
        #-----
        sshowtable.column("num",  anchor=tk.CENTER, width=50)
        sshowtable.column("transaction",  anchor=tk.CENTER, width=100)
        sshowtable.column("amount",  anchor=tk.CENTER, width=127)
        sshowtable.column("category",  anchor=tk.CENTER, width=100)
        sshowtable.column("date",  anchor=tk.CENTER, width=200)
        sshowtable.column("description",  anchor=tk.CENTER, width=135)
        # sshowtable.bind("<Button-1>", on_column_click)
            
        print('prior: '+str(datecheck))
        results = search_transactions(fromvartemp2, optemp2, keyword)

        

        # Create buttons (initially hidden)
        edit_button = tk.Button(
            root,
            text='Edit',
            command=lambda: edit_selected_transaction(),
            font=("Shree Devangari 714", 15),
            fg='#ff5757'
        )
        remove_button = tk.Button(
            root,
            text='Remove',
            command=lambda: remove_selected_transaction(),
            font=("Shree Devangari 714", 15),
            fg='#ff5757'
        )
        
        def on_row_select(event):
            # Get selected item
            selected_items = sshowtable.selection()
            if selected_items:
                # Show buttons above table
                edit_button.place(x=150, y=180)
                remove_button.place(x=190, y=180)
            else:
                # Hide buttons if no selection
                edit_button.place_forget()
                remove_button.place_forget()
        
        def edit_selected_transaction():
            selected_item = sshowtable.selection()[0]
            row_data = sshowtable.item(selected_item)['values']
            edit_transaction_gui(row_data)
        
        def remove_selected_transaction():
            selected_item = sshowtable.selection()[0]
            transaction_id = sshowtable.item(selected_item)['values'][0]
            
            # Remove from database
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
            conn.close()
            
            # Remove from treeview
            sshowtable.delete(selected_item)
            
            # Hide buttons after removal
            edit_button.place_forget()
            remove_button.place_forget()

        # Bind selection event to table
        sshowtable.bind('<<TreeviewSelect>>', on_row_select)

        def updatesearch_var():
            root.update()

            
            def regen():
                for item in sshowtable.get_children():
                    sshowtable.delete(item)

                sear = search_transactions(fromvartemp2, optemp2, keyword)
                
                for row in sear:
                    sshowtable.insert("", tk.END, values=row)
                
                # Hide the edit/remove buttons when regenerating the table
                edit_button.place_forget()
                remove_button.place_forget()
            
            optemp2 = (op_var2.get())
            print(optemp2)
            fromvartemp0 = (fromvar2.get())
            print(fromvartemp0)
            if fromvartemp0 == 'all':
                fromvartemp2 = ''
            else:
                fromvartemp2 = fromvartemp0
            print(fromvartemp2)
            regen()
        
        # Create and populate table as before
        for e, row in enumerate(results, start=0):
            sshowtable.insert("", tk.END, values=row)
            sshowtable.pack(fill=tk.BOTH, expand=True)
            sshowtable.place(x=150, y=220)


            
        


    write_search()

    titlesearch = tk.Label(root, text="Search Transactions", font=("DIN Alternate", 40, 'bold'), fg="#ff5757")
    titlesearch.pack()
    titlesearch.place(relx=0.55, rely=0.1, anchor="center")

    box_lab = tk.Label(root, text="Search by date:", font=("Shree Devangari 714", 18), fg="#ff5757")
    box_lab.pack()
    box_lab.place(relx=0.42, rely=0.16, anchor="center")

    years = [str(year) for year in range(1990, 2041)]
    months = [f"{month:02}" for month in range(1, 13)]
    days = [f"{day:02}" for day in range(1, 32)]


    yr = tk.OptionMenu(root, year_var, *years, command=lambda _: update_date_var())
    mr = tk.OptionMenu(root, month_var, *months, command=lambda _: update_date_var())
    dr = tk.OptionMenu(root, day_var, *days, command=lambda _: update_date_var())
    yr.pack()
    mr.pack()
    dr.pack()
    yr.place(relx=0.535, rely=0.16, anchor="center")
    mr.place(relx=0.60, rely=0.16, anchor="center")
    dr.place(relx=0.655, rely=0.16, anchor="center")    

    updatelabel = tk.Label(root, textvariable=date_var, font=("Shree Devangari 714", 17), fg="#ff5757")




    keyword_var = tk.StringVar()

    box_search = tk.Entry(root, textvariable=keyword_var, font=("Shree Devangari 714", 17), fg="#ff5757", highlightthickness=3, highlightcolor="#ff5757", highlightbackground="#ff5757", width=46)
    box_search.pack()
    box_search.place(relx=0.55, rely=0.225, anchor="center")

    
    button_search = tk.Button(root, text="Go", command=show_results, font=("Shree Devangari 714", 23), foreground='#ff5757')
    button_search.place(relx=0.863, rely=0.225, anchor="center")

    date_search = tk.Button(root, text="+", command=addate, font=("Shree Devangari 714", 23), foreground='#ff5757')
    

    
    for i, li in enumerate(slines, start=0):
            but = tk.Label(root, text=str(i+1)+'.   '+li, font=("Shree Devangari 714", 18), fg="#ff5757")
            but.place(relx=0.26, y=200+(i*45))
            but.bind("<Button-1>", lambda e, label=but: on_label_click(e, label))
    ##fc5d5d

# View current balance
def view_balance():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) AS balance FROM transactions
    ''')
    balance = cursor.fetchone()[0]
    conn.close()
    return balance if balance else 0.0


# Main Application
date_var = 0

root = tk.Tk()

#Year Updater
def update_date_var():
    # Combine year, month, and day into a single string
    date_var.set(f"{year_var.get()}-{month_var.get()}-{day_var.get()}")
    updatelabel.place(relx=0.755, rely=0.16, anchor="center")
    if datecheck == 9:
        date_search.place(relx=0.833, rely=0.16, anchor="center")
#Year String System
date_var = tk.StringVar()
year_var = tk.StringVar(value="1990")
month_var = tk.StringVar(value="01")
day_var = tk.StringVar(value="01")


#ALL THE ART
addtrans_art = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/buttonArt/ADDTRANS.png")
profile = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/buttonArt/BALANCEANDPROFILE.png")
search = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/buttonArt/SEARCH.png")
show = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/buttonArt/SHOW.png")
gen = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/buttonArt/GEN.png")
help = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/buttonArt/HELP.png")
d_addtrans_art = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/dis_buttonArt/ADDTRANS copy.png")
d_profile = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/dis_buttonArt/BALANCEANDPROFILE copy.png")
d_search = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/dis_buttonArt/SEARCH copy.png")
d_show = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/dis_buttonArt/SHOW copy.png")
d_gen = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/dis_buttonArt/GEN copy.png")
d_help = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/dis_buttonArt/HELP copy.png")
intr = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/buttonArt/intro.png")
aiart = PhotoImage(file=r"/Users/samyakchatterjee/Documents/Javascript projects/FBLA/buttonArt/TRYAIBUTFINAL.png")





#Initalize Boundaries And Properties
root.title("Money-Mate")
initialize_database()
root.geometry("900x750") 
root.resizable(False, False)

#Setting Starting Picture
def intro():
    ss = tk.Label(root, image=intr)
    ss.place(x=120)
    
#Destroy ALL Elements
def rlydestroy_all_widgets(parent):
    #Destroys All elements on screen
    for widget in parent.winfo_children():
        widget.destroy()

#Set Menu
def menu():
    def on_hover_addtrans(event):
    # Display the label for Button 2
        addhovlabel.config(text=" Add Transaction ")
        addhovlabel.place(x=add.winfo_x()+120, y=add.winfo_y() + add.winfo_height()/2-13) 
    def on_leave_addtrans(event):
        # Hide the label for Button 2
        addhovlabel.place_forget()
    def on_hover_search(event):
        # Display the label for Button 2
        searchlabel.config(text=" Search Transactions ")
        searchlabel.place(x=searchbut.winfo_x()+120, y=searchbut.winfo_y() + searchbut.winfo_height()/2-13)
    def on_leave_seaerch(event):
        # Hide the label for Button 2
        searchlabel.place_forget()
    def on_hover_profile(event):
        # Display the label for Button 2
        profilehov.config(text=" Profile ")
        profilehov.place(x=v_balance.winfo_x()+120, y=v_balance.winfo_y() + v_balance.winfo_height()/2-13)
    def on_leave_profile(event):
        # Hide the label for Button 2
        profilehov.place_forget()
    def on_hover_show(event):
        # Display the label for Button 2
        showlabel.config(text=" Show Transactions ")
        showlabel.place(x=showbut.winfo_x()+120, y=showbut.winfo_y() + showbut.winfo_height()/2-13)
    def on_leave_show(event):
        # Hide the label for Button 2
        showlabel.place_forget()
    def on_hover_gen(event):
        # Display the label for Button 2
        genlabel.config(text=" Generate Summary ")
        genlabel.place(x=genbut.winfo_x()+120, y=genbut.winfo_y() + genbut.winfo_height()/2-13)
    def on_leave_gen(event):
        # Hide the label for Button 2
        genlabel.place_forget()
    def on_hover_help(event):
        # Display the label for Button 2
        helplabel.config(text=" Help/Info ")
        helplabel.place(x=helpbut.winfo_x()+120, y=helpbut.winfo_y() + helpbut.winfo_height()/2-13)
    def on_leave_help(event):
        # Hide the label for Button 2
        helplabel.place_forget()

    canvas = tk.Canvas(width=122, height=root.winfo_screenheight(), bg="#ff5757", borderwidth=0, highlightthickness=0)
    canvas.pack()
    canvas.place(x=0)

    quitbut = tk.Button(
    root,
    text='Quit',
    command=lambda: quitp(),
    font=("Shree Devangari 714", 15),
    fg='#ff5757'
)
    quitbut.place(relx=0.95, rely=0.95)

    helpbut = tk.Button(image=help, command=helpcenter,highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    helpbut.pack()
    helpbut.place(x=0, y=500)
    helpbut.bind("<Enter>", on_hover_help)
    helpbut.bind("<Leave>", on_leave_help)
    helplabel = tk.Label(text="", font=("Shree Devangari 714", 17), fg="white", bg='#ff5757')

    add = tk.Button(image=addtrans_art, command=add_transaction_gui,highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    add.pack()
    add.place(x=0)
    add.bind("<Enter>", on_hover_addtrans)
    add.bind("<Leave>", on_leave_addtrans)
    addhovlabel = tk.Label(text="", font=("Shree Devangari 714", 17), fg="white", bg='#ff5757')

    v_balance = tk.Button(image=profile, command=view_balance_gui,highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    v_balance.pack()
    v_balance.place(x=0,y=630)
    v_balance.bind("<Enter>", on_hover_profile)
    v_balance.bind("<Leave>", on_leave_profile)
    profilehov = tk.Label(text="", font=("Shree Devangari 714", 17), fg="white", bg='#ff5757')

    searchbut = tk.Button(image=search, command=search_transactions_gui,highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    searchbut.pack()
    searchbut.place(x=0,y=125)
    searchbut.bind("<Enter>", on_hover_search)
    searchbut.bind("<Leave>", on_leave_seaerch)
    searchlabel = tk.Label(root, text="", font=("Shree Devangari 714", 17), fg="white", bg='#ff5757',highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)

    showbut = tk.Button(image=show, command=show_transactions_gui,highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    showbut.pack()
    showbut.place(x=0,y=250)
    showbut.bind("<Enter>", on_hover_show)
    showbut.bind("<Leave>", on_leave_show)
    showlabel = tk.Label(root, text="", font=("Shree Devangari 714", 17), fg="white", bg='#ff5757',highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)

    genbut = tk.Button(image=gen, command=summary_gui,highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    genbut.pack()
    genbut.place(x=0,y=375)
    genbut.bind("<Enter>", on_hover_gen)
    genbut.bind("<Leave>", on_leave_gen)
    genlabel = tk.Label(root, text="", font=("Shree Devangari 714", 17), fg="white", bg='#ff5757',highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)

#Set Menu When Disabled
def menudisabled():
    canvas = tk.Canvas(width=122, height=root.winfo_screenheight(), bg="#8f8f8f", borderwidth=0, highlightthickness=0)
    canvas.pack()
    canvas.place(x=0)
    
    add = tk.Button(image=d_addtrans_art, highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    add.pack()
    add.place(x=0)


    helpbut = tk.Button(image=d_help,highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    helpbut.pack()
    helpbut.place(x=0, y=500 )



    v_balance = tk.Button(image=d_profile, highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    v_balance.pack()
    v_balance.place(x=0,y=630)
  
    searchbut = tk.Button(image=d_search, highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    searchbut.pack()
    searchbut.place(x=0,y=125)

    showbut = tk.Button(image=d_show, highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    showbut.pack()
    showbut.place(x=0,y=250)

    genbut = tk.Button(image=d_gen,highlightthickness=0,highlightbackground='#ff5757', borderwidth=0)
    genbut.pack()
    genbut.place(x=0,y=375)


#Define All String Variables and tables
op_var = StringVar(root)
op_var2 = StringVar(root)
prof = StringVar(root)
prof.set('Profile 1')
op_var.set('Id')
monk = StringVar(root)
monk.set('Id')
optemp = 'id'
fromvar = StringVar(root)
fromvar2 = StringVar(root)
fromvar.set('all')
fromvartemp = ''
fromvartemp2 = ''
optemp2 = 'id'
profilevar = 'Profile 1'
style = ttk.Style()
style.configure("Custom.Treeview", font=("Shree Devangari 714", 13), rowheight=25) 
showtable = ttk.Treeview(root, columns=("num", "transaction", "amount", "category", "date", "description"),show='headings', style="Custom.Treeview", height=25)
sshowtable = ttk.Treeview(root, columns=("num", "transaction", "amount", "category", "date", "description"),show='headings', style="Custom.Treeview", height=25)
wmTable = ttk.Treeview(root, columns=("Week", "Expense", "Income", "Savings"),show='headings', style="Custom.Treeview")

#STARTING COMMANDS
intro()
menu()
root.mainloop()
