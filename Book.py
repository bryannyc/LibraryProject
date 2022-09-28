from LibraryItem import LibraryItem


class Book(LibraryItem):
    """Represents a Book that inherits from the LibraryItem class."""
    def __init__(self, id, title, author):
        """Creates a Book object with an author."""
        super().__init__(id, title)
        self._check_out_length = 21
        self._author = author

    def get_check_out_length(self):
        return self._check_out_length

    def get_author(self):
        """Returns the author of the book."""
        return self._author
