import binascii
from struct import *

sector_size = 512
relative_key_pos = 12254

# open file handle
fh = open( 'C:\\disk.img', "rb")
# read mbr from file/disk
mbr = fh.read(512)

# section  -> int64  (15-22 bytes)
# signatur -> char[] (510-512 bytes)
section, signatur = unpack('=14xq488x2s', mbr)

# last two bytes of the MBR are 0x55AA on a little endian system
if binascii.hexlify(signatur) != b'55aa':
    print( "No MBR was found... exit" )
    exit(1)

# section needs to be multiplied by the sector size to get the real section address
# (section contains the real boot code of DiskCryptor, including the keyfile)
section *= sector_size

fh.seek(section)
startBootcode = fh.read(5)

# 2FDE = 12254
fh.seek( section + relative_key_pos )
key = fh.read( 64 )

if key == (b"\x00" * 64):
    print( "No embedded keyfile" )
else:
    print( "Key found:" )
    print( binascii.hexlify(key) )
