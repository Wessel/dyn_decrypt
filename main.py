import sys
import os

def debug(msg):
  if (len(sys.argv) > 2):
    if (sys.argv[2] == 'debug'):
      print(msg)

if (len(sys.argv) < 2):
  print('Usage: {} file.dyn [debug]'.format(sys.argv[0]))
  sys.exit(1)

filename = sys.argv[1]
dest = os.path.splitext(filename)[0] + ('.zip' if (isDecrypt := os.path.splitext(filename)[1] == '.dyn') else '.dyn')

# XOR key and shuffle index arrays for convert
CHUNK_SIZE = 16
key = bytearray([(0x8D + i%8) for i in range(CHUNK_SIZE)])
indices = (indices := [5, 3, 6, 7, 4, 2, 0, 1]) + [i+8 for i in indices]

debug('chunk size = {}, key = {}, indices = {}'.format(CHUNK_SIZE, key, indices))
debug('filename = {}, dest = {}'.format(filename, dest))

with open(filename, 'rb') as file, open(dest, 'wb') as output:
  while True:
    # Read in a chunk of raw data
    chunk = file.read(CHUNK_SIZE)
    if not chunk:
      break

    # Need a full 8-byte chunk to convert.
    if len(chunk) == CHUNK_SIZE:
      out = bytearray(CHUNK_SIZE)

      # Convert the chunk.
      for i in range(CHUNK_SIZE):
        out[i if isDecrypt else indices[i]] = chunk[indices[i] if isDecrypt else i] ^ key[i]
    else:
      out = chunk

    debug('out = {}'.format(out))
    output.write(out)

print('{} {} to {}'.format('Decrypted' if isDecrypt else 'Encrypted', filename, dest))