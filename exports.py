#!/usr/bin/env python3

import sys
import glob
import json
import pefile
import argparse

from prettytable import PrettyTable

parser = argparse.ArgumentParser(description='Tool to show exports of a given DLL.')

parser.add_argument('filename', help='filename of binary to analyse',type=argparse.FileType('r'))
#parser.add_argument('-d', '--deff', help='Output in DEF format instead of pretty table', required=False, action='store_true')
parser.add_argument("-d", "--deff", metavar='<forwardtarget>', help="Instead of pretty table, print a DEF file with exports to a given target", required=False, action='store', default=None, type=str)

args = parser.parse_args()



def printTable(pe):
  print('binary: ' + args.filename.name)

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


def printDeff(pe):
  print('EXPORTS')

  d = [pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]]
  pe.parse_data_directories(directories=d)
  exports = [(e) for e in pe.DIRECTORY_ENTRY_EXPORT.symbols]

  for export in exports:
    export = export.name.decode('utf-8')
    print('  ' + export + '="' + args.deff[:-4] + '".' + export)



pe = pefile.PE(args.filename.name)

if args.deff:
  printDeff(pe)
else:
  printTable(pe)
