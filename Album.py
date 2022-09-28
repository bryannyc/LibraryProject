from LibraryItem import LibraryItem


class Album(LibraryItem):
    """Represents an Album that inherits from the LibraryItem class."""
    def __init__(self, id, title, artist):
        """Creates an Album object with an artist."""
        super().__init__(id, title)
        self._check_out_length = 14
        self._artist = artist

    def get_check_out_length(self):
        return self._check_out_length

    def get_artist(self):
        """Returns the Album artist."""
        return self._artist