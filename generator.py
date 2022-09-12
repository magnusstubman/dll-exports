import os
import sys
import ntpath
import pefile


def getDLLsinFolder(folder):
  dlls = []
  try:
    path = os.walk(folder)
    for root, directories, files in path:
      #for directory in directories:
      #  print(directory)
      for f in files:
        if f[-4:].lower() == '.dll':
          dlls.append(os.path.join(folder, f))
  except:
    pass

  return dlls
       

def getExports(f):
  exports = []

  try:
    pe = pefile.PE(f, fast_load=True)
    pe.parse_data_directories()

    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
      for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if exp.name:
          #exports.append(exp.name.decode('ascii'))
          exports.append(exp.name.decode('utf-8'))

  except pefile.PEFormatError:
    print(f + ' is apparently not a PE file. SKIPPED')
  except FileNotFoundError:
    print(f + ' is not found. SKIPPED')

  return exports 


def getFileName(path):
  head, tail = ntpath.split(path)
  return tail or ntpath.basename(head)

def createFolder(f):
  try:
    os.makedirs(f)
  except FileExistsError:
    pass


def doFolder(folder, outFolder):
  createFolder(outFolder)
  dlls = getDLLsinFolder(folder)
  
  for dll in dlls:
    fileName = getFileName(dll)
    print(dll)
    exports = getExports(dll)

    if len(exports) > 0:
      f = open(os.path.join(outFolder, fileName + '.cpp'), 'w')
      defF = open(os.path.join(outFolder, fileName + '.def'), 'w')
      defF.write('EXPORTS' + '\n')

      for export in exports:
        line = '#pragma comment(linker, "/export:' + export + '=\\"' + dll.replace('\\', '\\\\')[:-3] + export + '\\"")'
        f.write(line + '\n')

        defLine = '  ' + export + '="' + dll[:-4] + '".' + export
        defF.write(defLine + '\n')

      f.close()
      defF.close()


if __name__ == "__main__":
  parentFolder = 'win10.19044'
  createFolder(parentFolder)
  doFolder('C:\\Windows\\SysWOW64', os.path.join(parentFolder, 'SysWOW64'))
  doFolder('C:\\Windows\\System32', os.path.join(parentFolder, 'System32'))


