"""
Classes for managing tag connections
"""

from .utils import *
import io

format_map = {
    0x12: 144,  # NTAG-213
    0x3E: 504,  # NTAG-215
    0x6D: 888,  # NTAG-216
}

class TagIO(io.RawIOBase):
    def __init__(self, reader, mem_size: int = None):
        """
        I/O class for reading and writing to tags
        :param reader: The TagBit reader class of the tag.
        :param mem_size: The full size of the tag's memory. Auto-detected by default.
        """
        self.reader = reader

        if mem_size:
            self.mem_size = mem_size

        else:
            cc = self.reader.send_command('FF:B0:00:03')

            if cc[2] not in format_map.keys():
                raise TypeError('Tag format or size not supported')

            self.mem_size = format_map[cc[2]]

        self.offset = 0
        self.buffer = {}

    def read(self, size: int = -1) -> bytes:
        """
        Reads bytes from the tag.
        :param size: Size (in bytes) to read from the tag
        :return: Data read from tag.
        """

        if size < 0:
            read_size = self.mem_size
        else:
            read_size = size

        buffer = bytearray()

        for i in range(read_size):
            if self.offset >= self.mem_size:
                break

            address, page_offset = find_page(self.offset)

            if address in self.buffer.keys():
                page = self.buffer[address]

            else:
                page = self.reader.read_address(address)
                self.buffer[address] = page

            buffer.append(page[page_offset])
            self.offset += 1

        return buffer

    def write(self, data: bytes):
        """
        Write bytes to the tag.
        :return: Bytes data.
        """

        if self.offset + len(data) >= self.mem_size:
            raise IOError('Data exceeds available memory')

        for i in range(0, len(data), 4):
            octets = data[i:i+4]

            address, page_offset = find_page(self.offset)

            if page_offset != 0:
                raise IOError('IO offset must be a multiple of 4')  # This is not an ideal solution.

            if len(octets) < 4:
                existing_octets = self.reader.read_address(address)
                octets += existing_octets[len(octets):]

            self.reader.write_address(address, octets)
            self.offset += len(octets)

        return

    def seek(self, offset: int, whence: int = 0):
        """
        Moves the I/O pointer.
        :param offset: The offset to move the pointer to
        :param whence: Where to start from. 0 = start of the stream, 1 = current stream position, 2 = end of the stream.
        :return:
        """
        if whence == 0:
            self.offset = offset
        elif whence == 1:
            self.offset += offset
        elif whence == 2:
            self.offset = self.mem_size + offset
        else:
            raise ValueError('invalid whence ({}, should be 0, 1, or 2)'.format(whence))
        return max(offset, 0)

    def empty_buffer(self):
        """
        Empties the buffer.
        """
        self.buffer = {}

    def reset(self):
        """
        Sets offset back to zero and empties the buffer.
        """
        self.seek(0)
        self.buffer = {}

class AmiiboHandler:
    def __init__(self, reader):
        """
        Class for handling connections to Amiibos
        :param reader: The NFC Reader device class
        """
        self.reader = reader

    def write(self, data: bytes):
        """
        Write to the amiibo
        """
        raise NotImplementedError('This feature is not yet implemented! Check again in a later version.')

    def dump(self):
        """
        Create a dump of the amiibo
        :return:
        """
        chunks = bytearray()

        itr = 0
        while True:
            data = self.reader.read_address(itr)
            if itr > 131:
                break
            chunks[itr * 4: itr * 4 + 16] = bytearray(data)
            itr += 1
        return chunks

    def get_id(self):
        """
        Returns the ID of the Amiibo
        :return:
        """
        return self.reader.read_address(20)[4:-4]


class NDEFHandler:
    def __init__(self, reader):
        """
        Class for handling connections to NDEF tags
        :param reader: The NFC Reader device class
        """
        self.reader = reader
        self.io = TagIO(self.reader)

    def read(self) -> list:
        """
        Read NDEF records from the tag.
        :return: NDEF Records in a list
        """
        self.io.reset()

        records = ndef_load(self.io)

        self.io.seek(0)
        return records

    def write(self, records: list):
        """
        Writes NDEF records to a tag.
        :param records: NDEF Records in a list
        :return:
        """

        buffer = io.BytesIO()
        ndef_dump(records, buffer)
        octets = buffer.getvalue()

        self.io.write(octets)
        self.io.reset()
