import os
import shutil

comnav_size = 2772
radio_size = 100

comnav_files = 0
radio_files = 0
comnav_fail = 0
radio_fail = 0

try:
    os.mkdir (os.path.join(os.path.dirname(__file__), 'failed_trials'))
except FileExistsError:
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'failed_trials'))
    os.mkdir(os.path.join(os.path.dirname(__file__), 'failed_trials'))
for file in os.listdir(os.path.dirname(__file__)):
    if 'comnav_' in file:
        comnav_files += 1
        if os.path.getsize(file) < comnav_size:
            shutil.copy2(file, os.path.join(os.path.dirname(__file__), 'failed_trials'))
            comnav_fail += 1
    if 'radio_' in file:
        radio_files += 1
        # if os.path.getsize(file) < radio_size or os.path.getsize(file) > radio_size:
        if os.path.getsize(file) < radio_size:
            shutil.copy2(file, os.path.join(os.path.dirname(__file__), 'failed_trials'))
            radio_fail += 1

print (f'Failed comnav files: {comnav_fail} ---> {round((comnav_fail / comnav_files) * 100, 2)}%')
print (f'Failed radio files: {radio_fail} ---> {round((radio_fail / radio_files) * 100, 2)}%')

with open ('result.txt', 'w') as f:
    f.write(f'Failed comnav files: {comnav_fail} of {comnav_files}---> {round((comnav_fail / comnav_files) * 100, 2)}%'+'\n\r')
    f.write(f'Failed radio files: {radio_fail} of {radio_files} ---> {round((radio_fail / radio_files) * 100, 2)}%')





