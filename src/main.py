#Этап 1: Каркас (Импорты + точка входа + main)
import sys
import os
import time
import hashlib
# Этап 3: Дубликаты (Функция calculate_hash для хэширования)
def calculate_hash(file_path, chunk_size=4096):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
def print_tree(folder_path, level=0):
    #Рекурсивно выводит структуру папок с отступами
    try:
        items = os.listdir(folder_path)
        items.sort()
        for item in items:
            full_path = os.path.join(folder_path, item)
            indent = "    " * level
            if os.path.isdir(full_path):
                print(indent + item + "/")
                print_tree(full_path, level + 1)
            else:
                print(indent + item)          
    except PermissionError:
        print("    " * level + "Нет доступа")
# Этап 2: Сканирование (Функция scan_folder)
def scan_folder(folder_path, extension=None):
    file_count = 0
    hash_map = {}
    try:
        items = os.listdir(folder_path)
    except PermissionError:
        return file_count, hash_map
    for item in items:
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path):
            sub_count, sub_map = scan_folder(full_path, extension)
            file_count += sub_count
            for h, paths in sub_map.items():
                if h in hash_map:
                    hash_map[h].extend(paths)
                else:
                    hash_map[h] = paths
        else:
            #Фильтрация
            if extension is not None:
                if not full_path.lower().endswith(extension.lower()):
                    continue
            
            size = os.path.getsize(full_path)
            mod_time = os.path.getmtime(full_path)
            mod_time_str = time.ctime(mod_time)
            print(f"Файл: {full_path}")
            print(f"Размер: {size} байт")
            print(f"Изменён: {mod_time_str}")
            file_hash = calculate_hash(full_path)
            print(f"  Хэш: {file_hash[:8]}...")
            if file_hash in hash_map:
                hash_map[file_hash].append(full_path)
            else:
                hash_map[file_hash] = [full_path]
            file_count += 1
    return file_count, hash_map
# Этап 4: Резервная копия (Функция get_files_info)
def get_files_info(folder_path):
    files_info = {}
    try:
        items = os.listdir(folder_path)
    except PermissionError:
        return files_info
    for item in items:
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path):
            sub_info = get_files_info(full_path)
            files_info.update(sub_info)
        else:
            rel_path = os.path.relpath(full_path, folder_path)
            size = os.path.getsize(full_path)
            file_hash = calculate_hash(full_path)  # ← ТЕПЕРЬ ХЭШ!
            files_info[rel_path] = (size, file_hash)
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
            orig_hash = orig_info[1]   # ← ХЭШ
            back_hash = back_info[1]   # ← ХЭШ
            if orig_hash != back_hash: # ← СРАВНИВАЕМ ХЭШИ!
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
#Этап 1: Каркас (Основная функция main)
def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к папке")
        return
    
    folder_path = sys.argv[1]
    extension = None
    
    if len(sys.argv) >= 3 and sys.argv[2].startswith('.'):
        extension = sys.argv[2]
        print(f"Фильтр: только файлы с расширением {extension}")
    
    if not os.path.isdir(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует")
        return
    
    # Стуктурирование
    print_tree(folder_path)
    
    if len(sys.argv) == 2 or (len(sys.argv) == 3 and extension):
        print(f"Программа запущена. Папка для сканирования: {folder_path}")
        file_count, hash_map = scan_folder(folder_path, extension)
        
        print(f"\nВсего файлов найдено: {file_count}")
        print("\nДубликаты")
        duplicates_found = False
        for file_hash, paths in hash_map.items():
            if len(paths) > 1:
                duplicates_found = True
                print(f"Группа дубликатов (хэш: {file_hash[:16]}...):")
                for path in paths:
                    print(f"  - {path}")
                print()
        
        if not duplicates_found:
            print("Дубликатов не найдено")
    
    elif len(sys.argv) == 3 and not extension:
        backup_path = sys.argv[2]
        if not os.path.isdir(backup_path):
            print(f"Ошибка: папка бэкапа '{backup_path}' не существует.")
            return
        print(f"Оригинал: {folder_path}")
        print(f"Бэкап: {backup_path}")
        compare_folders(folder_path, backup_path)
    
    else:
        print("Ошибка: слишком много аргументов.")