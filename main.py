import os
from bs4 import BeautifulSoup
import pandas as pd


# Создаем пустой DataFrame
columns = ["Имя", "Телефон"]  # Замените этот список на реальные названия полей
df = pd.DataFrame(columns=columns)

columns_1 = ["Телефон"]
df_without_number = pd.DataFrame(columns=columns_1)

# Путь к вашему каталогу с HTML файлами
directory_path = "/Users/user/Desktop/valeria_excel"

# Проходим по каждому файлу в каталоге
for file_name in os.listdir(directory_path):
    file_path = os.path.join(directory_path, file_name)
    
    # Проверяем, является ли объект файлом и имеет расширение .html
    if os.path.isfile(file_path) and file_name.endswith(".html"):
        with open(file_path, "r", encoding="utf-8") as file:
            # Читаем содержимое HTML файла
            html_content = file.read()
            
            # Используем BeautifulSoup для парсинга HTML
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Извлекаем контактные данные (пример)
            name_tag = soup.find("td", class_="label", string="ФИО:")
            name = name_tag.find_next("td", class_="editable").text.strip() if name_tag else ""

            phone_tag = soup.find("td", class_="label", string="Телефон:")
            phone = phone_tag.find_next("td", class_="editable").text.strip() if phone_tag else ""
            
            # Добавляем данные в DataFrame
            df = df._append({"Имя": name, "Телефон": phone}, ignore_index=True)
            df_without_number = df_without_number._append({"Телефон": phone}, ignore_index=True)

# Сохраняем DataFrame в Excel файл
output_excel_path = "/Users/user/Desktop/contact_info.xlsx"
output_excel_path1 = "/Users/user/Desktop/contact_info_without_number.xlsx"

df.to_excel(output_excel_path, index=False)
df_without_number.to_excel(output_excel_path1, index=False)

print(f"Таблица успешно создана и сохранена в {output_excel_path}")
print(f"Таблица без имени успешно создана и сохранена в {output_excel_path1}")
