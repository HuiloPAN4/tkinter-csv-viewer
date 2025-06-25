import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

table_frame = None
current_df = None
filter_frame = None
button_frame = None
search_entry = None
search_frame = None


def show_table(df, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    xscrollbar = tk.Scrollbar(frame, orient='horizontal')
    yscrollbar = tk.Scrollbar(frame, orient='vertical')
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(
        frame,
        yscrollcommand=yscrollbar.set,
        xscrollcommand=xscrollbar.set
    )
    tree.pack(fill='both', expand=True)

    yscrollbar.config(command=tree.yview)
    xscrollbar.config(command=tree.xview)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='w', width=150)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))


def filter_white_products():
    global table_frame, current_df
    current_df['Название'] = current_df['Название'].astype(str).str.strip()
    filtered_df = current_df[current_df['Название'].str.contains("БЕЛЫЙ", case=False, na=False)]
    show_table(filtered_df, table_frame)


def pants():
    global table_frame, current_df
    current_df['Название'] = current_df['Название'].astype(str).str.strip()
    filtered_df = current_df[current_df['Название'].str.contains("Трусы", case=False, na=False)]
    show_table(filtered_df, table_frame)


def pants_size_42_44():
    global table_frame, current_df
    current_df['Название'] = current_df['Название'].astype(str).str.strip()
    filtered_df = current_df[current_df['Название'].str.contains("Трусы", case=False, na=False) &
                             current_df['Название'].str.contains("42-44", case=False, na=False)]
    show_table(filtered_df, table_frame)


def filter_price_max_2000():
    global current_df, table_frame
    filtered_df = current_df[current_df['Цена'] <= 2000.00]
    show_table(filtered_df, table_frame)


def show_most_expensive_product():
    global current_df, table_frame
    max_price = current_df['Цена'].max()
    most_expensive = current_df[current_df['Цена'] == max_price]
    show_table(most_expensive, table_frame)


def show_most_lowprice_product():
    global current_df, table_frame
    min_price = current_df['Цена'].min()
    most_cheap = current_df[current_df['Цена'] == min_price]
    show_table(most_cheap, table_frame)


def reset_filters():
    global table_frame, current_df
    show_table(current_df, table_frame)


def search_by_keyword():
    global current_df, table_frame, search_entry

    if current_df is None:
        messagebox.showwarning("Нет данных", "Сначала загрузите CSV файл.")
        return

    keyword = search_entry.get().strip().lower()
    if not keyword:
        messagebox.showinfo("Поиск", "Введите слово для поиска.")
        return

    current_df['Название'] = current_df['Название'].astype(str).str.lower()
    filtered_df = current_df[current_df['Название'].str.contains(keyword, na=False)]

    if filtered_df.empty:
        messagebox.showinfo("Поиск", "Совпадений не найдено.")
    else:
        show_table(filtered_df, table_frame)


def import_csv():
    global table_frame, current_df
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Выберите CSV файл"
    )
    if not file_path:
        return

    df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['Цена'] = df['Цена'].astype(str).str.replace(' ', '')
    df['Цена'] = df['Цена'].str.replace(',', '.')
    df['Цена'] = pd.to_numeric(df['Цена'], errors='coerce')

    current_df = df
    show_table(df, table_frame)
    show_filter_buttons()


def show_filter_buttons():
    global filter_frame, search_frame

    for widget in filter_frame.winfo_children():
        widget.destroy()

    filter_frame.pack(side=tk.LEFT, padx=20)
    search_frame.pack(side=tk.LEFT, padx=10)

    btn_filter_white = tk.Button(filter_frame, text="Показать только БЕЛУЮ одежду", command=filter_white_products)
    btn_filter_white.pack(side=tk.LEFT, padx=5)

    btn_pants = tk.Button(filter_frame, text="Показать позиции Трусов", command=pants)
    btn_pants.pack(side=tk.LEFT, padx=5)

    btn_pants_size = tk.Button(filter_frame, text="Трусы 42-44", command=pants_size_42_44)
    btn_pants_size.pack(side=tk.LEFT, padx=5)

    btn_filter_price = tk.Button(filter_frame, text="Цена ≤ 2000", command=filter_price_max_2000)
    btn_filter_price.pack(side=tk.LEFT, padx=5)

    btn_most_expensive = tk.Button(filter_frame, text="Самый дорогой товар", command=show_most_expensive_product)
    btn_most_expensive.pack(side=tk.LEFT, padx=5)

    btn_most_cheap = tk.Button(filter_frame, text="Самый дешевый товар", command=show_most_lowprice_product)
    btn_most_cheap.pack(side=tk.LEFT, padx=5)

    btn_reset_filters = tk.Button(filter_frame, text="Сбросить фильтры", command=reset_filters)
    btn_reset_filters.pack(side=tk.LEFT, padx=5)


def create_app():
    global table_frame, filter_frame, button_frame, search_entry, search_frame

    root = tk.Tk()
    root.title("Импорт из Excel просмотр и сортировка данных")
    root.geometry("1400x600")

    button_frame = tk.Frame(root)
    button_frame.pack(fill='x', padx=10, pady=10)

    btn_import = tk.Button(button_frame, text="Импорт CSV", command=import_csv)
    btn_import.pack(side=tk.LEFT, padx=5)


    search_frame = tk.Frame(button_frame)

    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)

    btn_search = tk.Button(search_frame, text="Поиск", command=search_by_keyword)
    btn_search.pack(side=tk.LEFT, padx=5)


    filter_frame = tk.Frame(button_frame)


    table_frame = tk.Frame(root)
    table_frame.pack(fill='both', expand=True)

    root.mainloop()


create_app()
