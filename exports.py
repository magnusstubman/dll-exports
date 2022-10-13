#!/usr/bin/env python3

import sys
import glob
import json
import pefile

from prettytable import PrettyTable


el = sys.argv[1]
print('binary: ' + el)

pe = pefile.PE(el)

imageBase = pe.OPTIONAL_HEADER.ImageBase

print('image base: ' + '0x' + hex(imageBase)[2:].zfill(16) + ' (' + str(imageBase) + ')')

is32bit = hex(pe.FILE_HEADER.Machine) == '0x14c'

if is32bit:
  print('architecture: 32-bit')
else:
  print('architecture: 64-bit')

d = [pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]]

pe.parse_data_directories(directories=d)
exports = [(e) for e in pe.DIRECTORY_ENTRY_EXPORT.symbols]

x = PrettyTable()
x.field_names = ['name', 'address (imagebase + relative)', 'relative address', 'ordinal']

for n in x.field_names:
  x.align[n] = "l"

for e in exports:

  if is32bit:
    address = '0x' + hex(imageBase + e.address)[2:].zfill(8)
  else:
    address = '0x' + hex(imageBase + e.address)[2:].zfill(16)

  if e.forwarder:
    address = str(e.forwarder.decode())

  name = ''

  if e.name:
    name = str(e.name.decode())

  x.add_row([name, address, '0x' + hex(e.address)[2:].zfill(8), str(e.ordinal) + ' (' + hex(e.ordinal) + ')'])

print(x)
