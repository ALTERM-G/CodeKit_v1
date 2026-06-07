from PyInstaller.utils.hooks import collect_data_files

# Tell PyInstaller to collect all data files from the pyfiglet package
datas = collect_data_files('pyfiglet')