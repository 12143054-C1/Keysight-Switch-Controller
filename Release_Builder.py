import os
import PyInstaller.__main__

# Define the path to the main script
main_script = 'c1sc.py'  # Replace with the actual name of your main script

# Define the name of the output executable
output_name = 'SwitchApp'

# Define the directory where the output executable will be saved
output_dir = 'output_folder'  # Replace with your desired output folder

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define additional data files to include (e.g., images, configs)
datas = [
    ('Keysight-Logo.png', '.'),
    ('switch_connector_name_dict.py', '.'),
    ('manual_switch_control.py', '.')
]

# Run PyInstaller with appropriate options
pyinstaller_args = [
    '--name=%s' % output_name,
    '--onefile',
    '--distpath=%s' % output_dir,
    '--windowed',
    '--log-level=INFO',
]

# Add the --add-data arguments
for src, dst in datas:
    pyinstaller_args.append('--add-data=%s;%s' % (src, dst))

# Add hidden imports to ensure all dependencies are included
hidden_imports = [
    'kivy',
    'kivy.core',
    'kivy.uix',
    'kivy.graphics',
    'kivy_deps.angle',
    'kivy_deps.glew',
    'kivy_deps.sdl2',
    'enchant'
]

for hidden_import in hidden_imports:
    pyinstaller_args.append('--hidden-import=%s' % hidden_import)

# Add the main script at the end
pyinstaller_args.append(main_script)

# Run PyInstaller with the specified arguments
PyInstaller.__main__.run(pyinstaller_args)

print(f'Executable created in {output_dir}')
