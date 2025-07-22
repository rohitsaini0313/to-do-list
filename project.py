#FRONT END DONE BY ROHIT AND BACKEND DONE BY AYUSH
import tkinter
from tkinter import messagebox
from tinydb import TinyDB, Query

# --- 1. BACKEND SETUP ---
# Initialize the database. This creates a 'tasks.json' file to store data.
db = TinyDB('tasks.json')
TaskQuery = Query()


# --- 2. LOGIC FUNCTIONS (Combines Backend and Frontend) ---

def add_task(entry_widget, listbox_widget):
    """Adds a task to the database and updates the UI listbox."""
    task_text = entry_widget.get()

    if not task_text:
        messagebox.showwarning("Warning", "You must enter a task.")
        return

    # Add the raw task text to the database
    db.insert({'task': task_text})
    
    # Add the formatted task (with bullet point) to the UI
    listbox_widget.insert(tkinter.END, f"• {task_text}")
    
    # Clear the entry box
    entry_widget.delete(0, tkinter.END)

def delete_task(listbox_widget):
    """Deletes a task from the listbox and the database."""
    try:
        # Get the full text of the selected item (e.g., "• Buy groceries")
        selected_item_text = listbox_widget.get(listbox_widget.curselection())
        
        # Remove the bullet point and space ("• ") to get the raw task text
        raw_task_text = selected_item_text.lstrip("• ")
        
        # Remove the task from the database using the raw text
        db.remove(TaskQuery.task == raw_task_text)
        
        # Delete the item from the UI listbox
        listbox_widget.delete(listbox_widget.curselection())
        
    except IndexError:
        # This error happens if the delete button is clicked with no item selected
        messagebox.showwarning("Warning", "You must select a task to delete.")

def load_tasks_on_startup(listbox_widget):
    """Loads all tasks from the database and displays them in the listbox on startup."""
    # Clear the listbox to prevent duplicates when reloading
    listbox_widget.delete(0, tkinter.END)

    # Get all tasks from the database
    all_tasks = db.all()
    
    # Insert each task into the UI listbox with a bullet point
    for task in all_tasks:
        listbox_widget.insert(tkinter.END, f"• {task['task']}")


# --- 3. FRONTEND UI ---

def create_gui():
    """Creates and configures the main GUI window and all its widgets."""
    window = tkinter.Tk()
    window.title("Final To-Do List")
    window.geometry("400x350")
    window.resizable(False, False)
    window.configure(bg="#f0f0f0")

    input_frame = tkinter.Frame(window, bg="#f0f0f0")
    input_frame.pack(pady=10)

    task_entry = tkinter.Entry(input_frame, width=30, font=("Helvetica", 12))
    task_entry.pack(side=tkinter.LEFT, padx=(10, 5))

    list_frame = tkinter.Frame(window)
    list_frame.pack(pady=10, padx=10, fill=tkinter.BOTH, expand=True)
    
    task_listbox = tkinter.Listbox(
        list_frame, height=10, width=50, font=("Helvetica", 12),
        selectbackground="#a6a6a6", selectforeground="white"
    )
    task_listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    scrollbar = tkinter.Scrollbar(list_frame)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
    
    task_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=task_listbox.yview)

    # --- Buttons (with fixes applied) ---
    
    add_button = tkinter.Button(
        input_frame, text="Add Task", font=("Helvetica", 10, "bold"),
        bg="#4CAF50", padx=10, # Removed fg="white" for Mac readability
        command=lambda: add_task(task_entry, task_listbox)
    )
    add_button.pack(side=tkinter.LEFT, padx=(0, 10))
    
    delete_button = tkinter.Button(
        window, text="Delete Selected Task", font=("Helvetica", 10, "bold"),
        bg="#f44336", padx=10, pady=5, # Removed fg="white" for Mac readability
        command=lambda: delete_task(task_listbox)
    )
    delete_button.pack(pady=10)
    
    # --- Load existing data when the app starts ---
    load_tasks_on_startup(task_listbox)
    
    # Start the application loop
    window.mainloop()


# --- 4. RUN THE APPLICATION ---

if __name__ == "__main__":
    create_gui()
