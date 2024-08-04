import shutil
import os

path = "./data/scene13/radar_0/"
# List of original files
original_file = '000000.csv'

# Create 297 new files with content from original files
# for i in range(1, 297):
#     # Determine the new file name
#     new_file = f'{i:06}.csv'
#     # Copy content from the original file to the new file
#     shutil.copyfile(path+original_file, path+new_file)

# print("Files copied successfully.")



# Loop through the files from 000001.csv to 000296.csv
for i in range(1, 297):
    # Determine the file name
    file_name = f'{i:06}.csv'
    # Change the file permission to read and write for the user
    os.chmod(path+file_name, 0o664)

print("File permissions changed successfully.")

