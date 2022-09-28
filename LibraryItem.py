class LibraryItem:
    """Represents a library item."""
    def __init__(self, library_item_id, title):
        """Creates a LibraryItem object with an id and title."""
        self._library_item_id = library_item_id
        self._title = title
        self._checked_out_by = None
        self._requested_by = None
        self._location = "ON_SHELF"
        self._date_checked_out = None

    def get_library_item_id(self):
        """Returns the library item id."""
        return self._library_item_id

    def get_title(self):
        """Returns the title of the library item."""
        return self._title

    def get_checked_out_by(self):
        """Returns the checked out by."""
        return self._checked_out_by

    def set_checked_out_by(self, patron):
        """Sets the checked out by status to the given patron."""
        self._checked_out_by = patron

    def get_requested_by(self):
        """Returns the requested by status of the library item."""
        return self._requested_by

    def set_requested_by(self, patron):
        """Sets the requested by status of the library item to the given patron."""
        self._requested_by = patron

    def get_location(self):
        """Returns the location of the library item."""
        return self._location

    def set_location(self, location):
        """Sets the location of the library item."""
        self._location = location

    def get_date_checked_out(self):
        """Returns the the date the library item was checked out."""
        return self._date_checked_out

    def set_date_checked_out(self, date):
        """Sets the checked out date for the library item."""
        self._date_checked_out = date