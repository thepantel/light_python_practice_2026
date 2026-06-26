import os
from utils import calculate_hash

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
            file_hash = calculate_hash(full_path)
            files_info[rel_path] = (size, file_hash)
    
    return files_info

def compare_folders(original_path, backup_path):
    print("\nСравнение с резервной копией")
    original_files = get_files_info(original_path)
    backup_files = get_files_info(backup_path)
    
    # 1. Файлы, отсутствующие в бэкапе
    missing_in_backup = set(original_files.keys()) - set(backup_files.keys())
    if missing_in_backup:
        print("\nФайлы, отсутствующие в бэкапе:")
        for file in sorted(missing_in_backup):
            print(f"  - {file}")
    else:
        print("\nВсе файлы из оригинала есть в бэкапе.")
    
    # 2. Изменённые файлы (по хэшу)
    changed_files = []
    for rel_path, orig_info in original_files.items():
        if rel_path in backup_files:
            back_info = backup_files[rel_path]
            orig_hash = orig_info[1]
            back_hash = back_info[1]
            if orig_hash != back_hash:
                changed_files.append(rel_path)
    
    if changed_files:
        print("\nИзменённые файлы:")
        for file in sorted(changed_files):
            print(f"  - {file}")
    else:
        print("\nВсе файлы совпадают.")
    
    # 3. Лишние файлы в бэкапе
    extra_in_backup = set(backup_files.keys()) - set(original_files.keys())
    if extra_in_backup:
        print("\nЛишние файлы в бэкапе:")
        for file in sorted(extra_in_backup):
            print(f"  - {file}")
    else:
        print("\nВ бэкапе нет лишних файлов.")