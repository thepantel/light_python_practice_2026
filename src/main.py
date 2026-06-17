import sys
import os

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