import sys
import os
import time
import hashlib

def calculate_hash(file_path, chunk_size=4096):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def scan_folder(folder_path):
    file_count = 0
    hash_map = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            mod_time = os.path.getmtime(file_path)
            mod_time_str = time.ctime(mod_time)
            
            print(f"Файл: {file_path}")
            print(f"  Размер: {size} байт")
            print(f"  Изменён: {mod_time_str}")
            file_hash = calculate_hash(file_path)
            print(f"  Хэш: {file_hash[:8]}...")
            if file_hash in hash_map:
                hash_map[file_hash].append(file_path)
            else:
                hash_map[file_hash] = [file_path]
            file_count += 1
    
    print(f"Всего файлов найдено: {file_count}")
    print("\nДубликаты")
    duplicates_found = False
    for file_hash, paths in hash_map.items():
        if len(paths) > 1: 
            duplicates_found = True
            print(f"Группа дубликатов (хэш: {file_hash}):")
            for path in paths:
                print(f"  - {path}")
            print()
    
    if not duplicates_found:
        print("Дубликатов не найдено")

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