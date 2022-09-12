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


#### References

- https://silentbreaksecurity.com/adaptive-dll-hijacking/
