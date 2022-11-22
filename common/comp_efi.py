#!/usr/bin/env python3
#coding=utf-8

"""
Copyright (C) 2022 Plato Mavropoulos
"""

from uefi_firmware import efi_compressor

from common.system import printer


def get_compress_sizes(data):    
    size_compress = int.from_bytes(data[0x0:0x4], 'little')
    size_original = int.from_bytes(data[0x4:0x8], 'little')
    
    return size_compress, size_original

def is_efi_compressed(data, strict=True):
    size_comp,size_orig = get_compress_sizes(data)
    
    check_diff = size_comp < size_orig
    
    if strict:
        check_size = size_comp + 0x8 == len(data)
    else:
        check_size = size_comp + 0x8 <= len(data)
    
    return check_diff and check_size

# EFI/Tiano Decompression via TianoCompress
def efi_decompress(compressed_buffer, padding=0, silent=False):
    if len(compressed_buffer) < 8:
        raise Exception('EFI_DECOMPRESS_ERROR')

    _, size_orig = get_compress_sizes(compressed_buffer)
    try:
        decompressed_data = efi_compressor.EfiDecompress(compressed_buffer, len(compressed_buffer))
        if len(decompressed_data) != size_orig:
            raise Exception('EFI_DECOMPRESS_ERROR')
    except Exception:
        if not silent:
            printer(f'Error: efi_compressor.EfiDecompress could not decompress file content!', padding)
        return bytes()

    if not silent:
        printer('Succesfull EFI decompression via efi_compressor.EfiDecompress!', padding)

    return decompressed_data
