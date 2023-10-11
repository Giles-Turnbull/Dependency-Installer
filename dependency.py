import os
import subprocess
import sys
import importlib.util

def get_script_dependencies(script_path):
    try:
        spec = importlib.util.spec_from_file_location("temp_module", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error loading the script: {e}")
        return []

    try:
        import pkg_resources
        return [pkg for pkg in module.__dict__.keys() if pkg_resources.working_set.by_key.get(pkg) is None]
    except ImportError:
        print("pkg_resources module not found. Make sure you have setuptools installed.")
        return []

def install_dependencies(dependencies):
    if not dependencies:
        print("No missing dependencies found.")
        return
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + dependencies)
        
        # Print the list of installed dependencies
        print("Installed dependencies:")
        for dep in dependencies:
            print(dep)

        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")


def find_downloads_folder():
    # Platform-specific method to find the user's downloads folder
    if sys.platform == "win32":
        # Windows
        return os.path.expanduser("~/Downloads")
    elif sys.platform == "darwin":
        # macOS
        return os.path.expanduser("~/Downloads")
    else:
        # Linux or other platforms
        return os.path.expanduser("~/Downloads")

def process_new_python_file(file_path):
    if not file_path.endswith(".py"):
        return  # Ignore non-Python files

    missing_dependencies = get_script_dependencies(file_path)

    if missing_dependencies:
        install_dependencies(missing_dependencies)

    # Optionally, you can also print a message indicating that the file has been processed.
    print(f"Processed: {file_path}")

if __name__ == "__main__":
    # Find the downloads folder automatically
    downloads_folder = find_downloads_folder()

    # Continuous monitoring code (use a library like watchdog)
    # Here, we'll simulate it by listing files once and checking for new ones
    initial_files = set(os.listdir(downloads_folder))

    while True:
        current_files = set(os.listdir(downloads_folder))
        new_files = current_files - initial_files

        for new_file in new_files:
            new_file_path = os.path.join(downloads_folder, new_file)
            process_new_python_file(new_file_path)

        initial_files = current_files