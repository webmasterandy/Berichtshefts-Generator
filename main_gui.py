import json
import random
from datetime import datetime, timedelta
import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk, ImageSequence
import markdown2
from tkhtmlview import HTMLLabel

# Pfad zur config.json-Datei
cp = os.getcwd()
config_path = os.path.join(cp, 'config', 'config.json')


# Daten aus der config.json-Datei lesen
with open(config_path, 'r', encoding='utf-8') as file:
    config_data = json.load(file)

# Pfade aus der config.json-Datei extrahieren
json_paths = config_data['paths']

# Funktion zum Laden der ausgewählten JSON-Datei
def load_json_file(selected_file):
    with open(selected_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Standardmäßig die erste JSON-Datei laden
data = load_json_file(json_paths[0])

# Deutsche Wochentage
wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

# Stellen Sie sicher, dass der Exportordner existiert
if not os.path.exists('export'):
    os.makedirs('export')

def generate_schedule():
    selected_days = [day for day, var in day_vars.items() if var.get()]
    start_date = cal.selection_get()
    
    if not selected_days:
        result_label.config(text="Bitte wählen Sie mindestens einen Wochentag aus.")
        return

    result = "Vorschau der Konfiguration:\n"
    for i, day in enumerate(wochentage):
        if day in selected_days:
            date = start_date + timedelta(days=i)
            result += f'{day} [{date.strftime("%d.%m.%Y")}]\n'
            events = random.sample(data, min(random.randint(6, 8), len(data)))
            result += '--Tätigkeiten (7)\n'
            for event in events:
                result += '- ' + event + '\n'
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)
    generate_msg.config(text="Bericht erfolgreich generiert!")
    # Nachricht nach 5 Sekunden verschwinden lassen
    root.after(5000, lambda: generate_msg.config(text=""))

def save_schedule():
    selected_days = [day for day, var in day_vars.items() if var.get()]
    start_date = cal.selection_get()
    
    if not selected_days:
        result_label.config(text="Bitte wählen Sie mindestens einen Wochentag aus.")
        return

    with open(os.path.join('export', f'output_{start_date.strftime("%d%m%Y")}.txt'), 'w', encoding='utf-8') as f:
        for i, day in enumerate(wochentage):
            if day in selected_days:
                date = start_date + timedelta(days=i)
                f.write(f'{day} [{date.strftime("%d.%m.%Y")}]\n')
                events = random.sample(data, min(random.randint(6, 8), len(data)))
                f.write('--Tätigkeiten (7)\n')
                for event in events:
                    f.write('- ' + event + '\n')
    
    result_label.config(text="Konfiguration gespeichert.")
    save_msg.config(text="Bericht erfolgreich gespeichert!")
    # Nachricht nach 5 Sekunden verschwinden lassen
    root.after(5000, lambda: save_msg.config(text=""))

def disable_non_mondays(event):
    selected_date = cal.selection_get()
    if selected_date.weekday() != 0:  # 0 entspricht Montag
        cal.selection_set(None)
        result_label.config(text="Bitte wählen Sie einen Montag aus.")

def animate_gif(label, gif):
    frames = []
    for img in ImageSequence.Iterator(gif):
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            # Change all white (also shades of whites)
            # to transparent
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        frames.append(ImageTk.PhotoImage(img))

    def update_frame(frame_index):
        frame = frames[frame_index]
        frame_index = (frame_index + 1) % len(frames)
        label.config(image=frame)
        root.after(100, update_frame, frame_index)
    update_frame(0)

def on_json_select(event):
    global data
    selected_file = json_var.get()
    data = load_json_file(selected_file)

def show_info():
    # Pfad zur .ico-Datei
    icon_path = os.path.join(cp, 'config', 'book.ico')
    
    # Pfad zur Info1.txt-Datei
    info_path = os.path.join(cp, 'config', 'Info1.txt')
    
    # Lade den Inhalt der Info-Datei
    with open(info_path, 'r', encoding='utf-8') as file:
        info_content = file.read()
    
    # Konvertiere den Inhalt zu Markdown
    info_content_md = markdown2.markdown(info_content)
    
    # Erstelle ein neues Toplevel-Fenster
    info_window = tk.Toplevel(root)
    info_window.title("Allgemeine Hinweise")
    
    # Versuche das Icon zu setzen, wenn der Pfad existiert
    if os.path.exists(icon_path):
        info_window.iconbitmap(icon_path)
    else:
        print(f"Icon-Datei nicht gefunden: {icon_path}")
    
    # Label für den Titel
    info_label = tk.Label(info_window, text="Allgemeine Hinweise", font=('Arial', 16, 'bold'), pady=10)
    info_label.pack()

    # Frame für den HTML-Inhalt und die Scrollleiste
    content_frame = tk.Frame(info_window)
    content_frame.pack(fill="both", expand=True)

    # Scrollleiste hinzufügen
    scrollbar = tk.Scrollbar(content_frame)
    scrollbar.pack(side="right", fill="y")

    # HTMLLabel zur Anzeige des Info-Inhalts
    info_html = HTMLLabel(content_frame, html=info_content_md, yscrollcommand=scrollbar.set)
    info_html.pack(fill="both", expand=True)
    scrollbar.config(command=info_html.yview)

    # Schließen-Button hinzufügen
    close_button = tk.Button(info_window, text="Schließen", command=info_window.destroy, bg='#FF0000', fg='white', font=('Arial', 12, 'bold'))
    close_button.pack(pady=10)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(result_text.get("1.0", tk.END))
    root.update()  # Dies stellt sicher, dass die Zwischenablage aktualisiert wird
    copy_msg.config(text="Inhalt erfolgreich kopiert!")
    # Nachricht nach 5 Sekunden verschwinden lassen
    root.after(5000, lambda: copy_msg.config(text=""))

# GUI erstellen
root = tk.Tk()
root.title("Berichtsheft Generator by Andreas Behfus | V1.0")
root.geometry("680x750")  # Fensterbreite erhöhen

# Icon Path
icon_path = os.path.join(cp, 'config','book.ico')
root.iconbitmap(icon_path)

# Frame für Kalender und Checkboxen
frame = tk.Frame(root, padx=20, pady=20, bg='white')  # Rand hinzufügen und Hintergrundfarbe setzen
frame.pack(pady=20)

# GIF laden und animieren
gif = Image.open("config/animated.gif")
gif_label = tk.Label(frame, bg='white', bd=0)  # Hintergrundfarbe setzen und Rahmen entfernen
gif_label.grid(row=0, column=0, padx=10)
animate_gif(gif_label, gif)

# Kalender
cal = Calendar(frame, selectmode='day', date_pattern='dd.mm.yyyy')
cal.grid(row=0, column=1, padx=20, pady=10)
cal.bind("<<CalendarSelected>>", disable_non_mondays)

# Frame für die Checkboxen
checkbox_frame = tk.Frame(frame, bg='white')  # Hintergrundfarbe setzen
checkbox_frame.grid(row=1, column=0, columnspan=2, pady=10)

# Checkboxen für Wochentage
day_vars = {day: tk.BooleanVar() for day in wochentage}
for i, (day, var) in enumerate(day_vars.items()):
    chk = tk.Checkbutton(checkbox_frame, text=day, variable=var, bg='white')  # Hintergrundfarbe setzen
    chk.grid(row=0, column=i, padx=5)

# Dropdown-Menü zum Auswählen der JSON-Datei
json_var = tk.StringVar(value=json_paths[0])
json_dropdown = ttk.Combobox(root, textvariable=json_var)
json_dropdown['values'] = json_paths
json_dropdown.bind("<<ComboboxSelected>>", on_json_select)
json_dropdown.pack(pady=10)

# Frame für die Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Button zum Generieren des Berichts
generate_btn = tk.Button(button_frame, text="Bericht generieren", command=generate_schedule, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'))
generate_btn.grid(row=0, column=0, padx=5)
generate_msg = tk.Label(button_frame, text="", fg='green')
generate_msg.grid(row=1, column=0)

# Button zum Speichern des Berichts
save_btn = tk.Button(button_frame, text="Bericht speichern", command=save_schedule, bg='#2196F3', fg='white', font=('Arial', 12, 'bold'))
save_btn.grid(row=0, column=1, padx=5)
save_msg = tk.Label(button_frame, text="", fg='green')
save_msg.grid(row=1, column=1)

# Button zum Anzeigen der Info
info_btn = tk.Button(button_frame, text="Info", command=show_info, bg='#FFC107', fg='black', font=('Arial', 12, 'bold'))
info_btn.grid(row=0, column=2, padx=5)

# Button zum Kopieren des Textinhalts
copy_btn = tk.Button(button_frame, text="Inhalt kopieren", command=copy_to_clipboard, bg='#FF5722', fg='white', font=('Arial', 12, 'bold'))
copy_btn.grid(row=0, column=3, padx=5)
copy_msg = tk.Label(button_frame, text="", fg='green')
copy_msg.grid(row=1, column=3)

# Textfeld zur Anzeige des Ergebnisses
result_text = tk.Text(root, height=20, width=58)  # Breite des Textfelds erhöhen
result_text.pack(pady=20)

# Label zur Anzeige von Nachrichten
result_label = tk.Label(root, text="", justify='left')
result_label.pack(pady=10)

root.mainloop()
