#!/usr/bin/env python
# coding=utf-8
import os   
import pdb
import subprocess as sb 
from lib.common import analysis_file

class File_Analysis:
    def __init__(self):
        pass 

    def check_command(self):
        count = 0
        results = []
        white_list = ('/etc/ssh/sshd_config')
        command_list = ['ls','ps','netstat','ss','top','lsattr','chattr','find','lsof','cat','chkconfig','crontab','ssh']
        package_list = ['coreutils','procps-ng','net-tools','iproute','procps-ng','findutils','lsof','coreutils','chkconfig','cronie','openssh-server']
        for package in package_list:
            result = sb.Popen('./bin/rpm -V {}'.format(package),shell=True,stdout=sb.PIPE).communicate()[0].strip()
            if result:
                if result.split()[-1] not in white_list:
                    count += 1 
                    results.append(result)
        if 0 < count < 10:
            print('  [1]关键命令完整性检测    [ 存在风险 ]')
            print('  ' + str(results))
        else:
            print('  [1]关键命令完整性检测    [ OK ]')

    def check_tmp(self):
        tmp_list = ['/tmp/','/var/tmp/','/dev/shm/'] 
        try:
            for dir in tmp_list:
                if not os.path.exists(dir):
                    continue
                else:
                    files = [os.path.join(dir,f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
                    for f in files:
                        result = analysis_file(f) 
                        if result:
                            print('  [2]临时目录恶意文件检测    [ 存在风险 ]') 
                            print(result)
                        else:
                            print('  [2]临时目录恶意文件检测    [ OK ]')
        except Exception,e:
            print(e)

    def run(self):
        print("\n文件安全检测开始")
        self.check_command()
        self.check_tmp()
