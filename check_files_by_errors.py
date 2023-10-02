import os
import shutil


comnav_fail = 0
radio_fail = 0

def file_reader(file):
    with open(file, 'r') as f:
        for line in f:
            yield line


try:
    os.mkdir (os.path.join(os.path.dirname(__file__), 'to_look_at'))
except FileExistsError:
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'to_look_at'))
    os.mkdir(os.path.join(os.path.dirname(__file__), 'to_look_at'))

os.mkdir(os.path.join(os.path.dirname(__file__), 'to_look_at', 'failed_trials'))



files_list = os.listdir(os.path.dirname(__file__))
for i in range(len(files_list)-1,-1,-1):
    if not 'console' in files_list[i]:
        del files_list[i]

files_sorted = sorted(files_list, key=lambda x: int(os.path.splitext(x)[0].replace('console','')))

file_number = 0
file_name = 'results.txt'

while os.path.exists(os.path.abspath(file_name)):
    file_number += 1
    file_name = 'results.txt'+str(file_number)

result_file = open(file_name, 'a')

for file in files_sorted:
    for line in file_reader(file):
        if "Open error S" in line:
            # print (f'"Open error S" is found in {file}'+'\n\r')
            # result_file.write(f'"Open error S" is found in {file}'+'\n\r')
            shutil.copy2(file, os.path.join(os.path.dirname(__file__), 'to_look_at', 'radio_' + file))
            radio_fail += 1

        if "Open error P" in line:
            # print (f'"Open error P" is found in {file}'+'\n\r')
            # result_file.write(f'"Open error P" is found in {file}'+'\n\r')
            shutil.copy2(file, os.path.join(os.path.dirname(__file__), 'to_look_at', 'comnav_' + file))
            comnav_fail += 1
        if "runGnssScript file [/mnt/fw/comnav.sc]" in line:
            comnav_fail = 0



    if radio_fail == 1:
        # print (f'"Open error S" in {file} but eventually radio started'+'\n\r')
        # result_file.write(f'"Open error S" in {file} but eventually radio started'+'\n\r')
        radio_fail = 0
    elif radio_fail > 1:
        print(f'"Radio did not start in {file}'  + '\n\r')
        result_file.write(f'"Radio did not start in {file}'  + '\n\r')
        radio_fail = 0
        shutil.copy2(file, os.path.join(os.path.dirname(__file__), 'to_look_at', 'failed_trials', 'radio_' + file))

    # if comnav_fail != 0:
    #     print(f'"Open error P" in {file} but eventually Comnav statred' + '\n\r')
    #     result_file.write(f'"Open error P" in {file} but eventually Comnav statred' + '\n\r')
    if comnav_fail != 0:
        print(f'"Comnav did not start in {file}' + '\n\r')
        result_file.write(f'"Comnav did not start in {file}' + '\n\r')
        shutil.copy2(file, os.path.join(os.path.dirname(__file__), 'to_look_at', 'failed_trials', 'comnav_' + file))



problem_files = len([x for x in os.listdir(os.path.join(os.path.dirname(__file__), 'to_look_at')) if os.path.isfile(os.path.join(os.path.dirname(__file__),
                                                                                                                                 'to_look_at', x))])
failed_files = len (os.listdir(os.path.join(os.path.dirname(__file__), 'to_look_at', 'failed_trials')))
total_files = len(files_sorted)


print ('##############################################\n\r')
print (f'To look at: {problem_files} of {total_files} ---> {round((problem_files / total_files) * 100, 2)}%'+'\n\r')
print (f'Failed trials: {failed_files} of {total_files} ---> {round((failed_files / total_files) * 100, 2)}%'+'\n\r')
print ('##############################################\n\r')
result_file.write ('##############################################\n\r')
result_file.write (f'To look at: {problem_files} of {total_files} ---> {round((problem_files / total_files) * 100, 2)}%'+'\n\r')
result_file.write (f'Failed trials: {failed_files} of {total_files} ---> {round((failed_files / total_files) * 100, 2)}%'+'\n\r')
result_file.write ('##############################################\n\r')







