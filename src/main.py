import sys
import os
from scan import scan_folder
from compare import compare_folders

def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к папке")
        return
    
    folder_path = sys.argv[1]
    extension = None
    # Проверяем, передан ли фильтр
    if len(sys.argv) >= 3 and sys.argv[2].startswith('.'):
        extension = sys.argv[2]
        print(f"Фильтр: только файлы с расширением {extension}")
    # Проверка существования папки
    if not os.path.isdir(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует")
        return
    # Режим сканирования (1 аргумент ИЛИ аргумент + фильтр)
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
    
    # Режим сравнения с бэкапом (2 аргумента, второй - папка)
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

if __name__ == "__main__":
    main()