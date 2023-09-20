#!/usr/bin/env python3
import os
import subprocess
import sys
from datetime import datetime
from multiprocessing import Process

TELESCOPE="C:/Users/ichobotov/TeleScope/telescope.exe"
PORT='T'

MGSORDER='PDIS'
MGSORDER2='NAV'

if len(sys.argv) < 2:
	print('Usage: '+sys.argv[0]+' atl_file')
	exit(1)

LOGFILE=sys.argv[1]
# LOGFILE='123.log'
PROJ= LOGFILE.rsplit(".")[0]+'_'+str(datetime.now().strftime("%Y%m%d_%H%M%S"))




if not os.path.exists(LOGFILE):
	print('Can not open: '+LOGFILE)
	exit(1)

FILE1=LOGFILE+'.inp_'+PORT
FILE2=FILE1+'.out'

os.system('atlproc -f'+PORT+' "'+LOGFILE+'"')
if not os.path.exists(FILE1):
	print('Can not open: '+FILE1)
	exit(1)

os.system('xordec "'+FILE1+'"')
if not os.path.exists(FILE2):
	print('Can not open: '+FILE2)
	exit(1)

os.system(TELESCOPE+' -new -d '+PROJ+' -i c_reader.dll "'+FILE2+'" -par "Message Order|'+MGSORDER+'"')
if not os.path.exists(PROJ+'.dp'):
	print('Can not open: '+PROJ+'.dp')
	exit(1)
os.system(TELESCOPE+' -d '+PROJ+' -i c_reader.dll "'+FILE2+'" -par "Message Order|'+MGSORDER2+'"')

subprocess.Popen([TELESCOPE, PROJ+'.dp'])

exit()

