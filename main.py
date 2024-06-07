import os
import winapps
import json

# Function to list applications in a directory
def list_apps_in_directory(directory):
    try:
        return [entry.name for entry in os.scandir(directory) if entry.is_dir()]
    except FileNotFoundError:
        return []

# Function to get Steam games from the 'common' directory
def get_steam_games():
    steam_apps = []
    steam_common_path = os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Steam', 'steamapps', 'common')

    if not os.path.exists(steam_common_path):
        print(f"Steam common path does not exist: {steam_common_path}")
        return steam_apps

    steam_apps = list_apps_in_directory(steam_common_path)
    return steam_apps

# Function to get Epic Games
def get_epic_games():
    epic_apps = []
    epic_path = os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'Epic', 'EpicGamesLauncher', 'Data', 'Manifests')

    if not os.path.exists(epic_path):
        print(f"Epic Games manifest path does not exist: {epic_path}")
        return epic_apps

    for manifest in os.listdir(epic_path):
        if manifest.endswith('.item'):
            with open(os.path.join(epic_path, manifest), 'r', encoding='utf-8') as f:
                app_info = json.load(f)
                epic_apps.append(app_info['DisplayName'])

    return epic_apps

# Get list of installed applications from winapps
installed_apps = []
for app in winapps.list_installed():
    installed_apps.append(f"{app.name} ({app.version})")

# Get list of applications in Program Files and Program Files (x86)
program_files_dirs = [
    os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
    os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')
]

program_files_apps = []
for directory in program_files_dirs:
    program_files_apps.extend(list_apps_in_directory(directory))

# Get Steam and Epic Games
steam_games = get_steam_games()
epic_games = get_epic_games()

# Write to file
with open('installed_apps.txt', 'w', encoding='utf-8') as file:
    file.write("Applications from winapps:\n")
    file.write("\n".join(installed_apps))
    file.write("\n\nApplications from Program Files directories:\n")
    file.write("\n".join(program_files_apps))
    file.write("\n\nSteam games:\n")
    file.write("\n".join(steam_games))
    file.write("\n\nEpic Games:\n")
    file.write("\n".join(epic_games))

print("List of installed applications has been saved to installed_apps.txt")
