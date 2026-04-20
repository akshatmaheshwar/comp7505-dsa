"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Compression Utilities for Task 4.
"""

from pathlib import Path
from typing import Any
import sys
import hashlib

def file_to_bytes(path: str) -> bytes:
    """
    Read a file into a byte array
    """
    with open(path, 'rb') as f:
        data = f.read()
    return data

def bytes_to_file(path: str, data: bytes) -> None:
    """
    Write a sequence of bytes to a file
    """
    with open(path, 'wb') as f:
        f.write(data)

def my_compressor(in_bytes: bytes) -> bytes:
    """
    Your compressor takes a bytes object and returns a compressed
    version of the bytes object. We have put xz here just as a 
    baseline general purpose compression tool.
    """
    # Implement me!
    pass

def my_decompressor(compressed_bytes: bytes) -> bytes:
    """
    Your decompressor is given a compressed bytes object (from your own
    compressor) and must recover and return the original bytes.
    Once again, we've just used xz.
    """ 
    # Implement me!
    pass

def compress_file(in_path: str, out_path: str) -> None:
    """
    Consume a file from in_path, compress it, and write it to out_path.
    """
    in_size = Path(in_path).stat().st_size
    in_data = file_to_bytes(in_path)
   
    compressed = my_compressor(in_data)
    
    bytes_to_file(out_path, compressed)
    out_size = Path(out_path).stat().st_size

    print("Compression Benchmark...")
    print("Input File:", in_path)
    print("Input Size:", in_size)
    print("Output File:", out_path)
    print("Output Size:", out_size)
    print("Ratio:", out_size/in_size)

def decompress_file(compressed_path: str, out_path: str) -> None:
    """
    Consume a compressed file from compressedpath, decompress it, and
    write it to outpath.
    """
    compressed_data = file_to_bytes(compressed_path)
    
    decompressed = my_decompressor(compressed_data)

    bytes_to_file(out_path, decompressed)

def recovery_check(in_path: str, compressed_path: str) -> bool:

    original = file_to_bytes(in_path)
    expected_checksum = hashlib.md5(original).hexdigest()

    decompress_file(compressed_path, "tmp")
    recovered = file_to_bytes("tmp")
    recovered_checksum = hashlib.md5(recovered).hexdigest()

    assert expected_checksum == recovered_checksum, "Uh oh!"


if __name__ == "__main__":
    compress_file(sys.argv[1], sys.argv[2])
    recovery_check(sys.argv[1], sys.argv[2])
