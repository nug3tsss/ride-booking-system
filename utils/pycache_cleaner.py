import os
import shutil

class PycacheCleaner():
    @staticmethod
    def clear_pycache(directory):
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    pycache_path = os.path.join(root, dir_name)
                    shutil.rmtree(pycache_path)