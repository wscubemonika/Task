import tkinter as tk
from tkinter import messagebox
import json
import os

# --- File Handling & Data Management ---

CONTACTS_FILE = "contacts.json"
contacts = {}

def load_contacts():
    """Loads contacts from the JSON file at startup."""
    global contacts
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, "r") as f:
                contacts = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {e}")
            contacts = {}
    else:
        contacts = {}

def save_contacts():
    """Saves the current contacts dictionary to the JSON file."""
    try:
        with open(CONTACTS_FILE, "w") as f:
            json.dump(contacts, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save contacts: {e}")

# --- GUI Logic & Functions ---

def update_listbox(contact_list=None):
    """Updates the listbox with contact names."""
    contact_listbox.delete(0, tk.END)
    data_to_display = contact_list if contact_list is not None else contacts
    
    for phone, details in data_to_display.items():
        display_text = f"{details['name']} ({phone})"
        contact_listbox.insert(tk.END, display_text)

def clear_fields():
    """Clears all input fields."""
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    contact_listbox.selection_clear(0, tk.END)
    entry_phone.config(state='normal') # Re-enable phone field for new additions

def on_contact_select(event):
    """Populates fields when a contact is selected from the list."""
    try:
        selected_text = contact_listbox.get(contact_listbox.curselection())
        # Extract phone number from the displayed text "Name (Phone)"
        phone = selected_text.split("(")[-1].strip(")")
        
        details = contacts.get(phone)
        if details:
            clear_fields()
            entry_name.insert(0, details['name'])
            entry_phone.insert(0, phone)
            entry_email.insert(0, details['email'])
            entry_address.insert(0, details['address'])
            # Disable phone field to prevent changing the unique key during update
            entry_phone.config(state='disabled') 
    except tk.TclError:
        pass # Handle case where listbox is clicked but no item is selected

def add_contact():
    """Adds a new contact to the dictionary and saves it."""
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    address = entry_address.get().strip()

    if not name or not phone:
        messagebox.showwarning("Warning", "Name and Phone Number are required.")
        return

    if phone in contacts:
        messagebox.showerror("Error", "A contact with this phone number already exists.")
        return

    contacts[phone] = {"name": name, "email": email, "address": address}
    save_contacts()
    update_listbox()
    clear_fields()
    messagebox.showinfo("Success", "Contact added successfully!")

def update_contact():
    """Updates the details of the selected contact."""
    try:
        # Get the original phone number from the disabled entry field
        original_phone = entry_phone.get()
        if original_phone not in contacts:
             messagebox.showwarning("Warning", "No contact selected to update.")
             return

        name = entry_name.get().strip()
        email = entry_email.get().strip()
        address = entry_address.get().strip()

        if not name:
             messagebox.showwarning("Warning", "Name cannot be empty.")
             return

        contacts[original_phone] = {"name": name, "email": email, "address": address}
        save_contacts()
        update_listbox()
        clear_fields()
        messagebox.showinfo("Success", "Contact updated successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def delete_contact():
    """Deletes the selected contact."""
    try:
        phone = entry_phone.get()
        if phone not in contacts:
            messagebox.showwarning("Warning", "No contact selected to delete.")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
        if confirm:
            del contacts[phone]
            save_contacts()
            update_listbox()
            clear_fields()
            messagebox.showinfo("Success", "Contact deleted.")
            
    except Exception as e:
         messagebox.showerror("Error", f"An error occurred: {e}")

def search_contact():
    """Filters the contact list based on the search term."""
    search_term = entry_search.get().strip().lower()
    if not search_term:
        update_listbox() # Show all if search is empty
        return

    filtered_contacts = {}
    for phone, details in contacts.items():
        if search_term in details['name'].lower() or search_term in phone:
            filtered_contacts[phone] = details
    
    update_listbox(filtered_contacts)

# --- GUI Setup ---

root = tk.Tk()
root.title("Contact Book")
root.geometry("700x500")
root.config(bg="#f0f0f0")

# Load data on start
load_contacts()

# --- Frames ---
left_frame = tk.Frame(root, bg="#f0f0f0", width=300, height=500, padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(root, bg="#ffffff", width=400, height=500, padx=20, pady=20, relief=tk.RIDGE, bd=2)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- Left Frame Widgets (Search & List) ---
tk.Label(left_frame, text="Search (Name or Phone):", bg="#f0f0f0", font=("Arial", 10)).pack(anchor=tk.W)
entry_search = tk.Entry(left_frame, font=("Arial", 12))
entry_search.pack(fill=tk.X, pady=(0, 5))
btn_search = tk.Button(left_frame, text="Search", command=search_contact, bg="#ddd")
btn_search.pack(fill=tk.X, pady=(0, 10))

tk.Label(left_frame, text="Contact List:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor=tk.W)
contact_listbox = tk.Listbox(left_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
contact_listbox.bind('<<ListboxSelect>>', on_contact_select)

# Scrollbar for listbox
scrollbar = tk.Scrollbar(left_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
contact_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=contact_listbox.yview)

# --- Right Frame Widgets (Details & Actions) ---
tk.Label(right_frame, text="Contact Details", font=("Arial", 16, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=(0, 20))

labels = ["Name:", "Phone No:", "Email:", "Address:"]
entries = []

for i, label_text in enumerate(labels):
    tk.Label(right_frame, text=label_text, font=("Arial", 11), bg="#ffffff").grid(row=i+1, column=0, sticky=tk.W, pady=5)
    entry = tk.Entry(right_frame, font=("Arial", 11), width=25)
    entry.grid(row=i+1, column=1, pady=5, padx=10)
    entries.append(entry)

entry_name, entry_phone, entry_email, entry_address = entries

# Action Buttons
btn_frame = tk.Frame(right_frame, bg="#ffffff")
btn_frame.grid(row=5, column=0, columnspan=2, pady=30)

btn_add = tk.Button(btn_frame, text="Add Contact", font=("Arial", 10), bg="#4CAF50", fg="white", width=12, command=add_contact)
btn_add.grid(row=0, column=0, padx=5)

btn_update = tk.Button(btn_frame, text="Update", font=("Arial", 10), bg="#2196F3", fg="white", width=10, command=update_contact)
btn_update.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(btn_frame, text="Delete", font=("Arial", 10), bg="#f44336", fg="white", width=10, command=delete_contact)
btn_delete.grid(row=0, column=2, padx=5)

btn_clear = tk.Button(right_frame, text="Clear Fields / New", font=("Arial", 10), command=clear_fields, bg="#ddd")
btn_clear.grid(row=6, column=0, columnspan=2, pady=10)

# Populate list initially
update_listbox()

root.mainloop()