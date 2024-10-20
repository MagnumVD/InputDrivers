import subprocess
import sys
import os


def install_packages():
    python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
    target = os.path.join(sys.prefix, 'lib', 'site-packages')
    
    subprocess.call([python_exe, '-m', 'ensurepip'])
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])
    
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'XInput-Python', '-t', target])
    print('FINISHED')


def register():
    try:
        import XInput
    except ImportError:
        print("InputDrivers: XInput is not installed, please install it using the button in the Preferences with Blender opened as administrator.")
        return {'FAILED'}
    else:
        return {'REGISTERED'}

def unregister():
    try:
        import XInput
    except ImportError:
        print("InputDrivers: XInput is not installed, please install it using the button in the Preferences with Blender opened as administrator.")
        return {'FAILED'}
    else:
        return {'UNREGISTERED'}
    