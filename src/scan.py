import os
import time
from utils import calculate_hash

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
            # Рекурсивно обходим подпапки
            sub_count, sub_map = scan_folder(full_path, extension)
            file_count += sub_count
            # Объединяем словари
            for h, paths in sub_map.items():
                if h in hash_map:
                    hash_map[h].extend(paths)
                else:
                    hash_map[h] = paths
        else:
            # Фильтрация по расширению
            if extension is not None:
                if not full_path.lower().endswith(extension.lower()):
                    continue
            
            size = os.path.getsize(full_path)
            mod_time = os.path.getmtime(full_path)
            mod_time_str = time.ctime(mod_time)
            print(f"Файл: {full_path}")
            print(f"  Размер: {size} байт")
            print(f"  Изменён: {mod_time_str}")
            file_hash = calculate_hash(full_path)
            print(f"  Хэш: {file_hash[:8]}...")
            
            if file_hash in hash_map:
                hash_map[file_hash].append(full_path)
            else:
                hash_map[file_hash] = [full_path]
            
            file_count += 1
    
    return file_count, hash_map