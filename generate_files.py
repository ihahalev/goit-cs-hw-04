from pathlib import Path
from faker import Faker

fake = Faker()

def generate_text_files(dir: Path, amount):
    dir.mkdir(exist_ok=True, parents=True)

    for i in range(0, amount):
        file_name = f'file_{i}.txt'
        file_path = dir/file_name

        # Генеруємо випадковий текст
        random_text = fake.text(max_nb_chars=500)  

        # Записуємо текст у файл
        with open(str(file_path), 'w', encoding='utf-8') as f:
            f.write(random_text)

if __name__ == "__main__":
    
    dir = Path.cwd()/'texts'
    generate_text_files(dir, 10)
