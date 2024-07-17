import os
import shutil

# Path to the sector file and the directory containing downloaded Excel files
sector_file_path = '/Users/huseyin/Downloads/sector_by_sector.txt'
download_directory = '/Users/huseyin/Documents/DATA_RAW'

# Function to parse the sector file and create a mapping of firms to sectors
def parse_sector_file(sector_file_path):
    firm_to_sectors = {}
    with open(sector_file_path, 'r', encoding='utf-8') as file:
        current_sector = None
        for line in file:
            line = line.strip()
            if line.endswith('Sektörü'):
                current_sector = line
            elif line:
                if line not in firm_to_sectors:
                    firm_to_sectors[line] = []
                firm_to_sectors[line].append(current_sector)
    return firm_to_sectors

# Function to create folders for each sector and copy the Excel files
def organize_files_by_sector(firm_to_sectors, download_directory):
    for file_name in os.listdir(download_directory):
        if file_name.endswith('.xlsx'):
            firm_name = file_name.split(' ')[0]
            if firm_name in firm_to_sectors:
                for sector in firm_to_sectors[firm_name]:
                    sector_folder = os.path.join(download_directory, sector)
                    if not os.path.exists(sector_folder):
                        os.makedirs(sector_folder)
                    src_file_path = os.path.join(download_directory, file_name)
                    dest_file_path = os.path.join(sector_folder, file_name)
                    if not os.path.exists(dest_file_path):
                        shutil.copy2(src_file_path, dest_file_path)
                        print(f"Copied {file_name} to {sector_folder}")
                    else:
                        print(f"File {file_name} already exists in {sector_folder}, skipping copy.")

# Parse the sector file
firm_to_sectors = parse_sector_file(sector_file_path)

# Organize the downloaded Excel files into sector folders
organize_files_by_sector(firm_to_sectors, download_directory)

print("Files have been organized by sector.")
