import os

class PycacheCleaner:
    @staticmethod
    def clear_pycache(root_dir="."):
        count = 0
        for foldername, subfolders, filenames in os.walk(root_dir):
            for file in filenames:
                if file.endswith(".pyc"):
                    file_path = os.path.join(foldername, file)
                    try:
                        os.remove(file_path)
                        count += 1
                    except Exception:
                        pass
        return count
