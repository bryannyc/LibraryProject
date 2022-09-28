from LibraryItem import LibraryItem


class Movie(LibraryItem):
    """Represents a Movie that inherits from LibraryItem."""
    def __init__(self, id, title, director):
        """Creates a Movie object with a director."""
        super().__init__(id, title)
        self._check_out_length = 7
        self._director = director

    def get_check_out_length(self):
        return self._check_out_length

    def get_director(self):
        """Returns the director of the movie."""
        return self._director