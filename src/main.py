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

def get_files_info(folder_path):
    files_info = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, folder_path)
            size = os.path.getsize(file_path)
            mod_time = os.path.getmtime(file_path)
            files_info[rel_path] = (size, mod_time)
    return files_info

def compare_folders(original_path, backup_path):
    print("\nСравнение с резервной копией")
    
    original_files = get_files_info(original_path)
    backup_files = get_files_info(backup_path)
    
    missing_in_backup = set(original_files.keys()) - set(backup_files.keys())
    if missing_in_backup:
        print("\nФайлы, отсутствующие в бэкапе:")
        for file in sorted(missing_in_backup):
            print(f"  - {file}")
    else:
        print("\nВсе файлы из оригинала есть в бэкапе.")
    
    changed_files = []
    for rel_path, orig_info in original_files.items():
        if rel_path in backup_files:
            back_info = backup_files[rel_path]
            if orig_info != back_info:
                changed_files.append(rel_path)
    
    if changed_files:
        print("\nИзменённые файлы:")
        for file in sorted(changed_files):
            print(f"  - {file}")
    else:
        print("\nВсе файлы совпадают.")
    
    extra_in_backup = set(backup_files.keys()) - set(original_files.keys())
    if extra_in_backup:
        print("\nЛишние файлы в бэкапе:")
        for file in sorted(extra_in_backup):
            print(f"  - {file}")
    else:
        print("\nВ бэкапе нет лишних файлов.")

def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к папке")
        print("\nПримеры запуска:")
        print("1.Сканирование:python main.py C:/путь/к/папке")
        print("2.Сравнение с бэкапом:python main.py C:/оригинал D:/бэкап")
        return
    
    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует")
        return
    
    if len(sys.argv) == 2:
        print(f"Программа запущена. Папка для сканирования: {folder_path}")
        scan_folder(folder_path)
    
    elif len(sys.argv) == 3:
        backup_path = sys.argv[2]
        if not os.path.isdir(backup_path):
            print(f"Ошибка: папка бэкапа '{backup_path}' не существует.")
            return
        print(f"Оригинал: {folder_path}")
        print(f"Бэкап: {backup_path}")
        compare_folders(folder_path, backup_path)
    
    else:
        print("Ошибка: слишком много аргументов.")


if __name__ == "__main__":
    main()