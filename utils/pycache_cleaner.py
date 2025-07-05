import os
import shutil
import stat

"""Utility class to clear Python bytecode cache files (.pyc) and __pycache__ directories.
This class provides a method to recursively search through a directory and remove all .pyc files"""

class PycacheCleaner:
    @staticmethod
    def clear_pycache(root_dir="."):
        pyc_count = 0
        folder_count = 0

        def remove_readonly(func, path, _):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception as e:
                print(f"[ERROR] Could not change permissions for: {path} — {e}")

        for foldername, subfolders, filenames in os.walk(root_dir, topdown=False):
            # Skip .venv folders completely
            if ".venv" in foldername:
                continue

            # Delete .pyc files
            for file in filenames:
                if file.endswith(".pyc"):
                    file_path = os.path.join(foldername, file)
                    try:
                        os.remove(file_path)
                        pyc_count += 1
                    except Exception as e:
                        print(f"[ERROR] Failed to delete file {file_path}: {e}")

            # Delete __pycache__ folders
            if os.path.basename(foldername) == "__pycache__":
                try:
                    shutil.rmtree(foldername, onerror=remove_readonly)
                    folder_count += 1
                except Exception as e:
                    print(f"[ERROR] Failed to delete folder {foldername}: {e}")

        return pyc_count, folder_count # Returns the count of deleted .pyc files and __pycache__ folders
