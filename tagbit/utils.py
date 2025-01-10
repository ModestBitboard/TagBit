"""
Some utilities to help our endeavours
"""

import ndef

def from_notation(string: str) -> list[int]:
    """
    Converts colon-delimited bytes into a list.
    :param string: Colon-delimited notation of bytes
    :return: A list of bytes represented as integers
    """
    return [int(s, base=16) for s in string.split(':')]

def to_notation(data: bytes | bytearray | list[int]) -> str:
    """
    Converts a byte list into colon-delimited notation.
    :param data: The byte-like data to convert to notation
    :return: Colon-delimited notation
    """
    return bytearray(data).hex(sep=':').upper()

def ndef_load(fp) -> list:
    """
    Loads NDEF data from an I/O object.
    :param fp: I/O object
    :return: NDEF records
    """
    tlv = fp.read(2)
    if tlv[0] != 0x03:
        raise RuntimeError("Not in NDEF format.")

    if tlv[1] == 0:
        raise RuntimeError("No NDEF Message detected.")

    return list(ndef.message_decoder(fp))

def ndef_dump(records: list, fp):
    """
    Dumps NDEF data to an I/O object.
    :param records: NDEF records
    :param fp: I/O object
    :return:
    """
    fp.write(b'\x03')
    octets = b''.join(list(ndef.message_encoder(records)))
    fp.write(len(octets).to_bytes())
    fp.write(octets)
    fp.write(b'\xFE')

def find_page(offset: int):
    """
    Returns the page number based off of the byte offset.
    :param offset: The offset in the file object
    :return: The page number and the offset within the page.
    """

    page_offset = offset % 4
    address = int((offset - page_offset) / 4)
    address += 4

    return address, page_offset
