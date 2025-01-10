"""
Python interface for the NFC reader
"""

from smartcard.System import readers
from smartcard.Exceptions import NoCardException

from tagbit.handlers import *
from tagbit.utils import *
from tagbit.status import *

import time

class Reader:
    def __init__(self, reader=None):
        if reader:
            self.reader = reader
        else:
            self.reader = readers(["SCard$DefaultReaders"])[0]

        self.connection = self.reader.createConnection()

    def send_command(self, command: str | bytes | bytearray | list[int], raise_status=True, blocking=True) -> bytes:
        """
        Sends a command to the tag.

        BE CAREFUL! - You can damage your tag if you
        don't know what you're doing.

        :param command: The command to send to the card
        :param raise_status: If true, raise `TagStatusError()` for errors in connecting to the tag.
        :param blocking: If true, when no tag is found wait until a tag is found. Otherwise, raise `NoTagError()`
        :return: The data received.
        """
        if not blocking:
            try:
                self.connection.connect()
            except NoCardException:
                raise NoTagError

        while True:
            try:
                self.connection.connect()
                break
            except NoCardException:
                time.sleep(0.1)
                continue

        if isinstance(command, str):
            instr = from_notation(command)
        else:
            instr = bytearray(command)

        data, sw1, sw2 = self.connection.transmit(instr)

        if raise_status:
            raise_for_status((sw1, sw2))

        return bytes(data)

    def read_address(self, page: int) -> bytes:
        """
        Reads a 16-byte page from the tag.
        :param page: The page address
        :return: The data from the page
        """
        page = min(0xFF, page)
        return self.send_command(f'FF:B0:00:{page:02X}')

    def write_address(self, page: int, data: bytes):
        """
        Writes a 4-byte page to the tag.

        BE CAREFUL! - You can damage your tag if you
        don't know what you're doing.

        :param page: The page address
        :param data: Four bytes to write to the tag.
        """
        page = min(0xFF, page)
        self.send_command(f'FF:D6:00:{page:02X}:04:{to_notation(data[:4])}')

    def get_tag(self, blocking=True):
        """
        Returns a handler for reading and writing to the tags
        :param blocking: If true, when no tag is found wait until a tag is found. Otherwise, raise `NoTagError()`
        :return: A new handler instance for interacting with the tag.
        """
        cc = self.send_command('FF:B0:00:03', blocking=blocking)

        if cc[0] == 0xF1:
            return AmiiboHandler(self)

        elif cc[0] == 0xE1:
            return NDEFHandler(self)

        else:
            raise NotImplementedError("This tag format is not yet supported.")
