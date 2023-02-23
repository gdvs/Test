import os
import datetime
import shutil
import ctypes

# specify the directory path where the files are located
directory_path = ""

# create a list to store the unique years in the directory
years = []

# iterate through all the files and directories in the specified directory and its subdirectories
for root, dirs, files in os.walk(directory_path):
    for filename in files:
        # check if the file is a photo or video file (you can customize the extensions to include other file types)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.mov', '.avi', '.mts')):
            # get the modified date of the file
            modified_time = os.path.getmtime(os.path.join(root, filename))
            modified_datetime = datetime.datetime.fromtimestamp(modified_time)

            # add the year to the list of unique years if it doesn't already exist
            year = modified_datetime.year
            if year not in years:
                years.append(year)

            # create a new filename using the modified date (year, month, day) and time (hour, minute, second)
            new_filename = modified_datetime.strftime("%m-%d-%Y_%H-%M-%S") + os.path.splitext(filename)[1]

            # check if the new filename already exists in the directory
            if os.path.exists(os.path.join(root, new_filename)):
                # if it does, add a unique identifier to the filename based on the time (hour, minute, second)
                i = 1
                while True:
                    new_filename = f"{modified_datetime.strftime('%m-%d-%Y_%H-%M-%S')}_{i}{os.path.splitext(filename)[1]}"
                    if not os.path.exists(os.path.join(root, new_filename)):
                        break
                    i += 1

            # rename the file with the new filename
            try:
                os.rename(os.path.join(root, filename), os.path.join(root, new_filename))
                print(f"Renamed {filename} to {new_filename}")
            except PermissionError:
                print(f"Cannot rename {filename}, skipping")

# create a new folder for each year in the directory
for year in years:
    year_folder = os.path.join(directory_path, str(year))
    if not os.path.exists(year_folder):
        os.mkdir(year_folder)

# move the files into their respective year folders
for root, dirs, files in os.walk(directory_path):
    for filename in files:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.mov', '.avi', '.mts')):
            modified_time = os.path.getmtime(os.path.join(root, filename))
            modified_datetime = datetime.datetime.fromtimestamp(modified_time)
            year_folder = os.path.join(directory_path, str(modified_datetime.year))
            try:
                shutil.move(os.path.join(root, filename), os.path.join(year_folder, filename))
                print(f"Moved {filename} to {year_folder}")
            except PermissionError:
                print(f"Cannot move {filename} to {year_folder}, skipping")
