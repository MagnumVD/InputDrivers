import bpy
import subprocess
import sys
import os
from typing import Optional

def get_install_folder(internal_folder):
    return os.path.join(bpy.context.preferences.addons[__package__.removesuffix('.functions')].preferences.dependencies_path, internal_folder)

def ensure_package_path():
    # Add the python path to the dependencies dir if missing
    target = get_install_folder("py_packages")
    if os.path.isdir(target) and target not in sys.path:
        print('InputDrivers: Found missing deps path in sys.path, appending...')
        sys.path.append(target)
        print('InputDrivers: Deps path has been appended to sys.path')

def install_packages(override: Optional[bool] = False):
    python_exe = sys.executable
    target = get_install_folder("py_packages")
    
    subprocess.run([python_exe, '-m', 'ensurepip'])
    subprocess.run([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip', '-t', target])
    
    if override:
        subprocess.run([python_exe, '-m', 'pip', 'install', '--upgrade', '--force-reinstall', 'XInput-Python', '-t', target])
    else:
        subprocess.run([python_exe, '-m', 'pip', 'install', '--upgrade', 'XInput-Python', '-t', target])
        
    ensure_package_path()
    print('FINISHED')

def test_packages():
    try:
        import XInput
        del XInput
    except ImportError as e:
        print('InputDrivers: An ImportError occured when importing the dependencies')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        return False
    except Exception as e:
        print('InputDrivers: Something went very wrong importing the dependencies, please get that checked')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        return False
    else:
        return True

def register():
    ensure_package_path()
    if test_packages():
        return {'REGISTERED'}
    else:
        print("InputDrivers: Some dependencies are not installed, please install them using the button in the Preferences.")
        return {'FAILED'}

def unregister():
    if test_packages():
        return {'UNREGISTERED'}
    else:
        print("InputDrivers: Some dependencies are not installed, please install them using the button in the Preferences.")
        return {'FAILED'}
    