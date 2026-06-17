import sys
import os
import time

def scan_folder(folder_path):
    file_count = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            mod_time = os.path.getmtime(file_path)
            mod_time_str = time.ctime(mod_time)
            
            print(f"Файл: {file_path}")
            print(f"  Размер: {size} байт")
            print(f"  Изменён: {mod_time_str}")
            file_count += 1
    
    print(f"Всего файлов найдено: {file_count}")

def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к папке")
        print("Пример: python main.py C:/путь/к/папке")
        return
    
    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует")
        return
    
    print(f"Программа запущена. Папка: {folder_path}")

if __name__ == "__main__":
    main()