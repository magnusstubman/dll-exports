# dll-exports
Collection of DLL function export forwards for DLL export function proxying.

Typical usecase is for backdooring applications for persistence purposes. E.g:

1. inspect the target application you wish to backdoor with procmon, see which DLLs it loads via the static IAT. You can clearly see this as the application tries to load Windows DLLs first from the applications own folder before attempting to load them from System32/SysWOW64.
2. pick one, a common target is `C:\Windows\System32\version.dll`
3. fire up Visual Studio, generate a new DLL project
4. add the code from here https://github.com/magnusstubman/dll-exports/blob/main/win10.19042/System32/version.dll.cpp
5. add your own maliciousness e.g. malware, e.g. as I did in https://dumpco.re/blog/alternative-to-lsass-dumping
6. compile - remember to compile for correct architecture
7. copy your newly compiled DLL to the target application's home directory
8. restart application and see it load your code, while preserving functionality


`generator.py` generates a list of DLLs in the target folders and use `pefile` to generate a list of exported functions for each, that are written to individual files containing relevant linker directives. E.g. for C:\Windows\System32\version.dll:


https://github.com/magnusstubman/dll-exports/blob/main/win10.19044/System32/version.dll.cpp
```c
#pragma comment(linker, "/export:GetFileVersionInfoA=\"C:\\Windows\\System32\\version.GetFileVersionInfoA\"")
#pragma comment(linker, "/export:GetFileVersionInfoByHandle=\"C:\\Windows\\System32\\version.GetFileVersionInfoByHandle\"")
#pragma comment(linker, "/export:GetFileVersionInfoExA=\"C:\\Windows\\System32\\version.GetFileVersionInfoExA\"")
#pragma comment(linker, "/export:GetFileVersionInfoExW=\"C:\\Windows\\System32\\version.GetFileVersionInfoExW\"")
#pragma comment(linker, "/export:GetFileVersionInfoSizeA=\"C:\\Windows\\System32\\version.GetFileVersionInfoSizeA\"")
#pragma comment(linker, "/export:GetFileVersionInfoSizeExA=\"C:\\Windows\\System32\\version.GetFileVersionInfoSizeExA\"")
#pragma comment(linker, "/export:GetFileVersionInfoSizeExW=\"C:\\Windows\\System32\\version.GetFileVersionInfoSizeExW\"")
#pragma comment(linker, "/export:GetFileVersionInfoSizeW=\"C:\\Windows\\System32\\version.GetFileVersionInfoSizeW\"")
#pragma comment(linker, "/export:GetFileVersionInfoW=\"C:\\Windows\\System32\\version.GetFileVersionInfoW\"")
#pragma comment(linker, "/export:VerFindFileA=\"C:\\Windows\\System32\\version.VerFindFileA\"")
#pragma comment(linker, "/export:VerFindFileW=\"C:\\Windows\\System32\\version.VerFindFileW\"")
#pragma comment(linker, "/export:VerInstallFileA=\"C:\\Windows\\System32\\version.VerInstallFileA\"")
#pragma comment(linker, "/export:VerInstallFileW=\"C:\\Windows\\System32\\version.VerInstallFileW\"")
#pragma comment(linker, "/export:VerLanguageNameA=\"C:\\Windows\\System32\\version.VerLanguageNameA\"")
#pragma comment(linker, "/export:VerLanguageNameW=\"C:\\Windows\\System32\\version.VerLanguageNameW\"")
#pragma comment(linker, "/export:VerQueryValueA=\"C:\\Windows\\System32\\version.VerQueryValueA\"")
#pragma comment(linker, "/export:VerQueryValueW=\"C:\\Windows\\System32\\version.VerQueryValueW\"")
```

Are DEF files yout thing? 
https://github.com/magnusstubman/dll-exports/blob/main/win10.19044/System32/version.dll.def

```
EXPORTS
  GetFileVersionInfoA="C:\Windows\System32\version".GetFileVersionInfoA
  GetFileVersionInfoByHandle="C:\Windows\System32\version".GetFileVersionInfoByHandle
  GetFileVersionInfoExA="C:\Windows\System32\version".GetFileVersionInfoExA
  GetFileVersionInfoExW="C:\Windows\System32\version".GetFileVersionInfoExW
  GetFileVersionInfoSizeA="C:\Windows\System32\version".GetFileVersionInfoSizeA
  GetFileVersionInfoSizeExA="C:\Windows\System32\version".GetFileVersionInfoSizeExA
  GetFileVersionInfoSizeExW="C:\Windows\System32\version".GetFileVersionInfoSizeExW
  GetFileVersionInfoSizeW="C:\Windows\System32\version".GetFileVersionInfoSizeW
  GetFileVersionInfoW="C:\Windows\System32\version".GetFileVersionInfoW
  VerFindFileA="C:\Windows\System32\version".VerFindFileA
  VerFindFileW="C:\Windows\System32\version".VerFindFileW
  VerInstallFileA="C:\Windows\System32\version".VerInstallFileA
  VerInstallFileW="C:\Windows\System32\version".VerInstallFileW
  VerLanguageNameA="C:\Windows\System32\version".VerLanguageNameA
  VerLanguageNameW="C:\Windows\System32\version".VerLanguageNameW
  VerQueryValueA="C:\Windows\System32\version".VerQueryValueA
  VerQueryValueW="C:\Windows\System32\version".VerQueryValueW
```

#### Note

I havn't taken `KnownDLLs` into account.
Keep in mind that the DLLs listed in `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs` *and any* DLL that they load is also considered to be a known DLL, thus the standard search order does not apply.


#### `exports.py`

`exports.py` is a small util script for showing what exports a given DLL has:

```
$ ./exports.py version.dll 
binary: version.dll
image base: 0x0000000180000000 (6442450944)
architecture: 64-bit
+----------------------------+--------------------------------+------------------+-----------+
| name                       | address (imagebase + relative) | relative address | ordinal   |
+----------------------------+--------------------------------+------------------+-----------+
| GetFileVersionInfoA        | 0x00000001800010f0             | 0x000010f0       | 1 (0x1)   |
| GetFileVersionInfoByHandle | 0x0000000180002370             | 0x00002370       | 2 (0x2)   |
| GetFileVersionInfoExA      | 0x0000000180001e90             | 0x00001e90       | 3 (0x3)   |
| GetFileVersionInfoExW      | 0x0000000180001070             | 0x00001070       | 4 (0x4)   |
| GetFileVersionInfoSizeA    | 0x0000000180001010             | 0x00001010       | 5 (0x5)   |
| GetFileVersionInfoSizeExA  | 0x0000000180001eb0             | 0x00001eb0       | 6 (0x6)   |
| GetFileVersionInfoSizeExW  | 0x0000000180001090             | 0x00001090       | 7 (0x7)   |
| GetFileVersionInfoSizeW    | 0x00000001800010b0             | 0x000010b0       | 8 (0x8)   |
| GetFileVersionInfoW        | 0x00000001800010d0             | 0x000010d0       | 9 (0x9)   |
| VerFindFileA               | 0x0000000180001ed0             | 0x00001ed0       | 10 (0xa)  |
| VerFindFileW               | 0x0000000180002560             | 0x00002560       | 11 (0xb)  |
| VerInstallFileA            | 0x0000000180001ef0             | 0x00001ef0       | 12 (0xc)  |
| VerInstallFileW            | 0x0000000180003320             | 0x00003320       | 13 (0xd)  |
| VerLanguageNameA           | KERNEL32.VerLanguageNameA      | 0x00004e6c       | 14 (0xe)  |
| VerLanguageNameW           | KERNEL32.VerLanguageNameW      | 0x00004e97       | 15 (0xf)  |
| VerQueryValueA             | 0x0000000180001030             | 0x00001030       | 16 (0x10) |
| VerQueryValueW             | 0x0000000180001050             | 0x00001050       | 17 (0x11) |
+----------------------------+--------------------------------+------------------+-----------+
```


#### References

- https://silentbreaksecurity.com/adaptive-dll-hijacking/
