import os
import re
import sys
'''
Исходные данные:
- файл с командами управления питанием
- папка для каждого юнита с файлами с системным временем. Поиск папок по "U" ключу

Работа скрипта:
- поиск времени подачи события на включение
- поиск соответствующего файла для данной итерации
- поиск времени старта файла
- сопоставление времени

'''

def find_string(line, reg_expr):
    if re.findall(reg_expr, line):
        return True


def read_file(file):
    with open(file, 'r') as f:
        for line in f:
            yield line

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)



def func_to_split(file):
    try:
        index = int(file.split('.')[-1])
        return index
    except ValueError:
        pass



dirname = os.path.dirname(__file__)
with os.scandir(dirname) as files:
    subdir = [file.name for file in files if file.is_dir()]
    subdir = [dir for dir in subdir if "U" in dir]


failed_trials = []


for line in read_file(sys.argv[1]):
    if "Ignition ON" in line:
        time = line.rstrip().split(' ')[-2]
        time = time.split(':')
        hh = int(time[0]) - 3
        if hh < 0:
            hh = str(hh+24)
        time[0] = str(hh)
        ignition_start_time = get_sec(':'.join(time))
        continue
    if "$PASHR,PWR,2,ON," in line:
        trial_index = int(line.rstrip().split(',')[-1].split('.')[0])
        for i in subdir:
            for time_line in read_file(os.path.join(dirname, i, f"cpu.log.{trial_index}")):
                start_file_time = time_line.rstrip().split(' ')[-4]
                start_file_time = get_sec(start_file_time)
                if start_file_time - ignition_start_time < -60: # handle day roll-over
                    start_file_time = start_file_time+86400
                if start_file_time - ignition_start_time < 0 or start_file_time - ignition_start_time > 30: # make sure start_file_time is later than ignition_start_time
                    failed_trials.append(f"{i}+cpu.log.{trial_index}")
                break

if len(failed_trials) == 0:
    print ('OK!')
else:
    print (failed_trials)


# for dir in subdir:
#     if "U" in dir:
#         files_list = []
#         for item in os.listdir(dir):
#             if func_to_split(item) is None:
#                 continue
#             else:
#                 files_list.append(item)
#
#         for file in sorted(files_list, key=func_to_split):
#             if 'cpu' in file:
#                for line in read_file(file):
#                    time = line.rstrip().split(' ')[-4]
#                    file_start_time = get_sec(time)
#
#
#         # print (func_to_split(file))
# #         files_sorted = sorted(os.listdir(os.path.join(dirname, 'U#2')), key=func_to_split)


