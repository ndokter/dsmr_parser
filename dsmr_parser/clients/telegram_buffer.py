import re


class TelegramBuffer(object):
    """
    Used as a buffer for a stream of telegram data. Constructs full telegram
    strings from the buffered data and returns it.
    """

    def __init__(self):
        self._buffer = ''

    def get_all(self):
        """
        Remove complete telegrams from buffer and yield them.
        :rtype generator:
        """
        for telegram in self._find_telegrams():
            self._remove(telegram)
            yield telegram

    def append(self, data):
        """
        Add telegram data to buffer.
        :param str data: chars, lines or full telegram strings of telegram data
        """
        self._buffer += data

    def _remove(self, telegram):
        """
        Remove telegram from buffer and incomplete data preceding it. This
        is easier than validating the data before adding it to the buffer.
        :param str telegram:
        :return:
        """
        # Remove data leading up to the telegram and the telegram itself.
        index = self._buffer.index(telegram) + len(telegram)

        self._buffer = self._buffer[index:]

    def _find_telegrams(self):
        """
        Find complete telegrams in buffer from  start ('/') till ending
        checksum ('!AB12\r\n').
        :rtype: list
        """
        # - Match all characters after start of telegram except for the start
        # itself again '^\/]+', which eliminates incomplete preceding telegrams.
        # - Do non greedy match using '?' so start is matched up to the first
        # checksum that's found.
        # - The checksum is optional '{0,4}' because not all telegram versions
        # support it.
        return re.findall(
            r'\/[^\/]+?\![A-F0-9]{0,4}\0?\r\n',
            self._buffer,
            re.DOTALL
        )
