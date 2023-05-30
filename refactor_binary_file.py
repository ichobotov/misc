import time

file_source = 'bynav_data.log'
file_result_tmp = 'bynav_refactor_gga.log'
# file_result = 'bynav_ascii_gga.log'


# with open(file_source, 'rb') as orig, open(file_result_tmp, "w") as edited:
#     for line in orig:
#         try:
#             edited.write(line.decode(encoding='utf-8'))
#         except UnicodeDecodeError:
#             pass
#         except UnicodeEncodeError:
#             pass
#
# with open(file_result_tmp) as orig, open(file_result, "w") as edited:
#     for line in orig:
#         if line.strip():
#             edited.write(line)

start_time = time.time()


with open(file_source, 'rb') as orig, open(file_result_tmp, "w") as edited:
    '''
    читаем побайтово и тут же записываем.
    Такой переработанный файл потом нормально обрабатывается
    '''
    chunk = orig.read(1)
    while chunk:
        try:
            edited.write(chunk.decode(encoding='utf-8'))
        except UnicodeDecodeError:
            pass
        except UnicodeEncodeError:
            pass
        chunk = orig.read(1)

print("--- %s seconds ---" % (time.time() - start_time))