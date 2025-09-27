import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# ---------------- Functions ----------------

# Create a new file
def new_file():
    text_area.delete(1.0, tk.END)

# Open an existing file
def open_file():
    file = filedialog.askopenfilename(defaultextension=".txt",
                                      filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file:
        text_area.delete(1.0, tk.END)
        with open(file, "r") as f:
            text_area.insert(tk.END, f.read())

# Save file
def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(file, "w") as f:
            f.write(text_area.get(1.0, tk.END))
        messagebox.showinfo("Saved", f"File saved: {file}")

# Exit the app
def exit_app():
    root.destroy()

# Change Font Size
def change_font_size():
    size = simpledialog.askinteger("Font Size", "Enter new font size:", minvalue=8, maxvalue=72)
    if size:
        text_area.config(font=("Arial", size))

# Toggle Dark Mode
dark_mode = False
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        text_area.config(bg="black", fg="white", insertbackground="white")
        status_bar.config(bg="black", fg="white")
    else:
        text_area.config(bg="white", fg="black", insertbackground="black")
        status_bar.config(bg="lightgray", fg="black")

# Word Count
def update_word_count(event=None):
    content = text_area.get(1.0, 'end-1c')
    words = len(content.split())
    chars = len(content)
    status_bar.config(text=f"Words: {words}  |  Characters: {chars}")

# Find and Replace
def find_replace():
    def do_replace():
        find_text = find_entry.get()
        replace_text = replace_entry.get()
        content = text_area.get(1.0, tk.END)
        new_content = content.replace(find_text, replace_text)
        text_area.delete(1.0, tk.END)
        text_area.insert(1.0, new_content)
        find_window.destroy()

    find_window = tk.Toplevel(root)
    find_window.title("Find and Replace")
    find_window.geometry("300x120")
    tk.Label(find_window, text="Find:").pack(pady=2)
    find_entry = tk.Entry(find_window, width=30)
    find_entry.pack()

    tk.Label(find_window, text="Replace:").pack(pady=2)
    replace_entry = tk.Entry(find_window, width=30)
    replace_entry.pack()

    tk.Button(find_window, text="Replace All", command=do_replace).pack(pady=5)


# ---------------- GUI Setup ----------------

root = tk.Tk()
root.title("Notepad 📝")
root.geometry("600x400")

# Text Area
text_area = tk.Text(root, wrap="word", font=("Arial", 12))
text_area.pack(expand=True, fill="both")
text_area.bind("<KeyRelease>", update_word_count)

# Status Bar
status_bar = tk.Label(root, text="Words: 0  |  Characters: 0", anchor='w', bg="lightgray")
status_bar.pack(fill='x', side='bottom')

# Menu Bar
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Find and Replace", command=find_replace)
edit_menu.add_command(label="Change Font Size", command=change_font_size)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
menu_bar.add_cascade(label="View", menu=view_menu)

# Set Menu
root.config(menu=menu_bar)

# Initialize word count
update_word_count()

# Run App
root.mainloop()
