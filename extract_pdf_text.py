#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import fitz  # PyMuPDF


def extract_text_from_pdfs_in_current_folder():
    """
    Извлекает текст из всех PDF-файлов в текущей директории,
    минимизируя объём выходных .txt файлов:
    - Каждая страница → одна строка без внутренних переносов
    - Лишние пробелы и пустые строки удалены
    - Без разделителей страниц
    """
    current_directory = os.getcwd()

    pdf_files = [
        f for f in os.listdir(current_directory)
        if os.path.isfile(os.path.join(current_directory, f)) and f.lower().endswith('.pdf')
    ]

    if not pdf_files:
        print("В текущей папке не найдено PDF-файлов.")
        return

    print(f"Найдено {len(pdf_files)} PDF-файлов для обработки:\n")

    for pdf_filename in pdf_files:
        pdf_path = os.path.join(current_directory, pdf_filename)
        txt_filename = os.path.splitext(pdf_filename)[0] + '.txt'
        txt_path = os.path.join(current_directory, txt_filename)

        try:
            document = fitz.open(pdf_path)
            lines = []

            for page_number in range(len(document)):
                page = document[page_number]
                page_text = page.get_text()

                # Удаляем переносы строк внутри страницы → заменяем на пробел
                line = page_text.replace('\n', ' ').replace('\r', ' ')

                # Сжимаем множественные пробелы в один
                line = re.sub(r'\s+', ' ', line).strip()

                # Добавляем только непустые строки
                if line:
                    lines.append(line)

            document.close()

            # Объединяем все страницы через один перенос строки (минимальный разделитель)
            compact_text = '\n'.join(lines)

            # Сохраняем результат
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(compact_text)

            original_size = os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
            result_size = len(compact_text.encode('utf-8'))

            print(f"✓ {pdf_filename}")
            print(f"  → {txt_filename} ({result_size / 1024:.1f} КБ)")
            if original_size:
                print(f"  → Сжатие: {100 - (result_size / original_size * 100):.1f}% меньше исходного PDF\n")
            else:
                print()

        except Exception as e:
            print(f"✗ Ошибка при обработке {pdf_filename}: {str(e)}\n")

    print("Обработка завершена.")


if __name__ == "__main__":
    extract_text_from_pdfs_in_current_folder()
