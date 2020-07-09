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
dest = os.path.splitext(filename)[0] + '.zip'

# XOR key and shuffle index arrays for decryption
CHUNK_SIZE = 8
key = bytearray([(0x8D + i) for i in range(CHUNK_SIZE)])
indices = [5, 3, 6, 7, 4, 2, 0, 1]

debug('chunk size = {}, key = {}, indices = {}'.format(CHUNK_SIZE, key, indices))
debug('filename = {}, dest = {}'.format(filename, dest))

with open(filename, 'rb') as file, open(dest, 'wb') as output:
  while True:
    # Read in a chunk of raw data
    chunk = file.read(CHUNK_SIZE)
    if not chunk:
      break

    # Need a full 8-byte chunk to decrypt.
    if(len(chunk) == CHUNK_SIZE):
      out = bytearray(CHUNK_SIZE)

      # Decrypt the chunk.
      for i in range(CHUNK_SIZE):
        out[i] = chunk[indices[i]] ^ key[i]
    else:
      out = chunk

    debug('out = {}'.format(out))
    output.write(out)

print('Decrypted {} to {}'.format(filename, dest))
