# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.launcher.procapi
import ctypes
from ctypes.wintypes import *
TH32CS_SNAPPROCESS = 2
INVALID_HANDLE_VALUE = -1
cwk = ctypes.windll.kernel32

class PROCESSENTRY32(ctypes.Structure):
    __module__ = __name__
    _fields_ = [('dwSize', DWORD), ('cntUsage', DWORD), ('th32ProcessID', DWORD), ('th32DefaultHeapId', HANDLE), ('th32ModuleID', DWORD), ('cntThreads', DWORD), ('th32ParentProcessID', DWORD), ('pcPriClassBase', LONG), ('dwFlags', DWORD), ('szExeFile', c_char * MAX_PATH)]


class ProcessEntryPY:
    __module__ = __name__

    def __init__(self, name, pid):
        self.name = name
        self.pid = pid


def getProcessList():
    hProcessSnap = cwk.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    processList = []
    if hProcessSnap != INVALID_HANDLE_VALUE:
        pe32 = PROCESSENTRY32()
        pe32.dwSize = sizeof(pe32)
        if cwk.Process32First(hProcessSnap, ctypes.byref(pe32)):
            while 1:
                processList.append(ProcessEntryPY(pe32.szExeFile.lower(), int(pe32.th32ProcessID)))
                if not cwk.Process32Next(hProcessSnap, ctypes.byref(pe32)):
                    break

        cwk.CloseHandle(hProcessSnap)
    return processList
# okay decompiling .\otp\launcher\procapi.pyc
