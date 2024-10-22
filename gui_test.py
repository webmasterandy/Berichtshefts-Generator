import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkhtmlview import HTMLLabel
import markdown2

cp = os.getcwd()

# Laden der Konfigurationsdatei
config_path = os.path.join(cp, 'config', 'config.json')
with open(config_path, 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
    file_paths = [os.path.join(cp, path) for path in config['paths']]
    info_text = config.get('info_text', '')

def add_elements_to_json(file_name, elements):
    # Lesen Sie die vorhandene JSON-Datei
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Fügen Sie neue Elemente zur JSON-Datei hinzu
    data.extend(elements)

    # Speichern Sie die aktualisierte JSON-Datei
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # Löschen Sie die Einträge aus dem Textfeld
    entry.delete('1.0', tk.END)

def add_elements():
    file_name = combo.get()
    elements = entry.get('1.0', 'end-1c')  # Abrufen des gesamten Textes im Eingabefeld

    # Fügen Sie Spiegelstriche in der ersten Zeile und nach jedem Zeilenumbruch hinzu
    elements_with_bullets = "- " + elements.replace('\n', '\n- ')

    # Fügen Sie die Elemente mit Spiegelstrichen in das Textfeld ein
    entry.delete('1.0', tk.END)
    entry.insert(tk.END, elements_with_bullets)

    # Bereinigen Sie die Spiegelstriche, bevor Sie sie zur JSON-Datei hinzufügen
    elements_without_bullets = elements.split('\n')

    add_elements_to_json(file_name, elements_without_bullets)
    update_listbox(file_name)

def update_listbox(file_name):
    # Lesen Sie die vorhandene JSON-Datei
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Löschen Sie die vorhandenen Einträge in der Listbox
    listbox.delete(0, tk.END)

    # Fügen Sie die Elemente aus der JSON-Datei zur Listbox hinzu
    for item in data:
        listbox.insert(tk.END, f"- {item}")

def on_combo_select(event):
    file_name = combo.get()
    update_listbox(file_name)

def on_listbox_double_click(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index)
        show_item_details(selected_item)

def show_item_details(item):
    detail_window = tk.Toplevel(root)
    detail_window.title("Eintragsdetails")
    detail_window.geometry("400x300")
    detail_window.iconbitmap(icon_path)

    item_label = tk.Label(detail_window, text="Eintragsdetails", font=("Arial", 14))
    item_label.pack(pady=10)

    item_text = tk.Text(detail_window, height=10, width=40)
    item_text.pack(pady=10)
    item_text.insert(tk.END, item)
    item_text.config(state=tk.DISABLED)

    button_frame = tk.Frame(detail_window)
    button_frame.pack(pady=10)

    delete_button = tk.Button(button_frame, text="Löschen", command=lambda: delete_item(item, detail_window), bg='#FF0000', fg='white', font=('Arial', 12, 'bold'))
    delete_button.pack(side=tk.LEFT, padx=5)

    cancel_button = tk.Button(button_frame, text="Abbrechen", command=detail_window.destroy, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'))
    cancel_button.pack(side=tk.LEFT, padx=5)

def delete_item(item, window):
    file_name = combo.get()
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    item_text = item[2:]  # Entfernen des Spiegelstrichs und des Leerzeichens
    if item_text in data:
        data.remove(item_text)
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        update_listbox(file_name)
        window.destroy()
    else:
        messagebox.showerror("Fehler", "Eintrag nicht gefunden.")

def show_info():
    info_window = tk.Toplevel(root)
    info_window.title("Allgemeine Hinweise")
    info_window.geometry("700x800")
    info_window.iconbitmap(icon_path)

    info_label = tk.Label(info_window, text="Allgemeine Hinweise", font=("Arial", 14))
    info_label.pack(pady=10)

    # Konvertieren von Markdown in HTML
    info_html_content = markdown2.markdown(info_text)
    info_html = HTMLLabel(info_window, html=info_html_content)
    info_html.pack(pady=10, fill="both", expand=True)

    close_button = tk.Button(info_window, text="Schließen", command=info_window.destroy)
    close_button.pack(pady=10)

root = tk.Tk()
root.title("Berichtsheft Item Manager by Andreas Behfus | V1.0")
root.geometry("700x400")  # Setzen Sie die Größe des Fensters auf 700x400

# Setzen Sie das Icon für das Fenster
icon_path = os.path.join(cp, 'config/book.ico')
root.iconbitmap(icon_path)

# Erstellen Sie eine Überschrift
label = tk.Label(root, text="BH Item Manager", font=("Arial", 30))
label.place(x=220, y=15)  # Setzen Sie die Position der Überschrift

label1 = tk.Label(root, text="Bitte Datei auswählen", font=("Arial", 12))
label1.place(x=120, y=70)  # Setzen Sie die Position der Überschrift

# Erstellen Sie ein Dropdown-Menü
combo = ttk.Combobox(root, values=file_paths)
combo.place(x=130, y=100)
combo.bind("<<ComboboxSelected>>", on_combo_select)  # Bind the selection event to the function

# Erstellen Sie ein Eingabefeld
entry = tk.Text(root, height=10, width=25)  # Setzen Sie die Größe des Eingabefelds auf 200x400
entry.place(x=100, y=130)

# Erstellen Sie einen Button
button = tk.Button(root, text="Elemente hinzufügen", command=add_elements, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'))
button.place(x=130, y=310)  # Setzen Sie die Position des Buttons

# Erstellen Sie eine Überschrift für die Listbox
label2 = tk.Label(root, text="Alle Einträge", font=("Arial", 12))
label2.place(x=350, y=100)  # Setzen Sie die Position der Überschrift

# Erstellen Sie eine Listbox für die Übersicht
listbox = tk.Listbox(root, height=10, width=45)
listbox.place(x=350, y=130)
listbox.bind("<Double-Button-1>", on_listbox_double_click)  # Bind double-click event to the function

# Erstellen Sie einen Info-Button
info_button = tk.Button(root, text="Info", command=show_info, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
info_button.place(x=460, y=310)  # Setzen Sie die Position des Info-Buttons

root.mainloop()
