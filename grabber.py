import os, platform, shutil
from concurrent.futures import ThreadPoolExecutor

target_extentions = ['.mp3', '.png', '.jpeg', '.jpg', '.pdf', '.docx']

def check_file_size(file):
    size = os.path.getsize(file)
    limit = 2 * 1024 * 1024

    if size > limit:
        return True
    else:
        return False

def grab_files(folder):
    if platform.system() == 'Linux':
        root_path = os.environ.get('HOME')
    elif platform.system() == 'Windows':
        user = os.environ['USERNAME']
        root_path = os.path.join("C:\\Users", user)

    categories = {
        ".png": "IMAGES",
        ".jpg": "IMAGES",
        ".jpeg": "IMAGES",
        ".pdf": "DOCUMENTS",
        ".docx": "DOCUMENTS",
        ".mp3": "MUSIC"
    }

    for c in set(categories.values()):
        os.makedirs(
            os.path.join(folder, c),
            exist_ok=True
        )
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            extention = os.path.splitext(file)[1].lower()
            if extention not in target_extentions:
                continue

            file_path = os.path.join(root, file)

            try:
                if check_file_size(file_path):
                    continue

                category = categories[extention]
                destination = os.path.join(folder, category, file)

                if os.path.exists(destination):
                    continue

                shutil.copy2(file_path, destination)
            except extention as e:
                return
            
    shutil.make_archive(folder, "zip")
    shutil.rmtree(folder)

if __name__ == "__main__":
    folder = "my_files"
    if os.path.exists(folder):
        grab_files(folder)
    else:
        os.mkdir(folder)
        grab_files(folder)