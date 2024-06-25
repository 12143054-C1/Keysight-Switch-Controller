import os
import subprocess
import sys

class PyToExe:
    def __init__(self, script_path, external_files=None, dest_folder=None, onefile=True, windowed=True, icon_path=None, app_name=None):
        """
        Initialize the PyToExe object with the required parameters.

        :param script_path: Path to the main Python script to compile.
        :param external_files: List of tuples containing (source_path, destination_path_within_exe) for external files.
        :param dest_folder: Destination folder for the compiled executable.
        :param onefile: Boolean to indicate if the output should be a single file.
        :param windowed: Boolean to indicate if the output should be windowed (no console).
        :param icon_path: Path to the icon file to use for the executable.
        :param app_name: Name of the compiled application.
        """
        self.script_path = script_path
        self.external_files = external_files if external_files else []
        self.dest_folder = dest_folder if dest_folder else os.getcwd()
        self.onefile = onefile
        self.windowed = windowed
        self.icon_path = icon_path
        self.app_name = app_name

    def compile(self):
        """
        Compile the Python script to an executable using PyInstaller.
        """
        cmd = [sys.executable, '-m', 'PyInstaller', self.script_path]

        if self.onefile:
            cmd.append('--onefile')
        if self.windowed:
            cmd.append('--windowed')
        if self.icon_path:
            cmd.extend(['--icon', self.icon_path])
        if self.app_name:
            cmd.extend(['--name', self.app_name])

        for src, dest in self.external_files:
            cmd.extend(['--add-data', f'{src};{dest}'])

        cmd.extend(['--distpath', self.dest_folder, '--clean'])

        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

# Example usage
if __name__ == '__main__':
    script_path = 'c1sc_tkinter.py'
    external_files = [('remote-control.ico','.')]
    dest_folder = 'Release'
    icon_path = 'remote-control.ico'
    app_name = 'Switch Controller'

    compiler = PyToExe(script_path, external_files, dest_folder, icon_path=icon_path, app_name=app_name)
    compiler.compile()
