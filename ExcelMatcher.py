import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import os

def select_file():
    file_path = filedialog.askopenfilename(
        title="Оберіть Excel-файл",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if file_path:
        process_file(file_path)

def process_file(file_path):
    try:
        df = pd.read_excel(file_path)
        
        if 'Номер' not in df.columns:
            messagebox.showerror("Помилка", "У файлі не знайдено колонку 'Номер'!")
            return
        
        # Шукаємо дублікати
        duplicates = df[df.duplicated(subset=['Номер'], keep=False)]
        
        # Очищуємо поле перед виведенням нового результату
        # щось для тсту
        # 
        # 
        # 'normal' дозволяє програмі змінювати текст
        txt_area.config(state='normal')
        txt_area.delete('1.0', tk.END)
        
        if not duplicates.empty:
            unique_dups = duplicates['Номер'].unique()
            
            txt_area.insert(tk.INSERT, f"Знайдено дублікатів: {len(duplicates)}\n")
            txt_area.insert(tk.INSERT, "Список номерів, що повторюються:\n")
            txt_area.insert(tk.INSERT, "-"*30 + "\n")
            for num in unique_dups:
                txt_area.insert(tk.INSERT, f"{num}\n")
            
    
        else:
            txt_area.insert(tk.INSERT, "Дублікатів не знайдено.")
        
        # state='normal' залишаємо, щоб ви могли виділяти та копіювати текст
        
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {e}")
def copy_to_clipboard():
    text = txt_area.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(text)
   

# Інтерфейс
root = tk.Tk()
root.title("Аналіз дублікатів")
root.geometry("400x400")
copy_btn = tk.Button(root, text="Копіювати все", command=copy_to_clipboard)
copy_btn.pack(pady=5)

btn = tk.Button(root, text="Обрати файл для перевірки", command=select_file)
btn.pack(pady=10)

# Поле для результатів
txt_area = scrolledtext.ScrolledText(root, width=40, height=15)
txt_area.pack(pady=10, padx=10)

root.mainloop()