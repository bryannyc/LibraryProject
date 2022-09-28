class Patron:
    """Represents a patron with id number and name."""
    def __init__(self, patron_id, name):
        """Creates a Patron object with id number and name."""
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0

    def get_patron_id(self):
        """Returns patron id."""
        return self._patron_id

    def get_patron_name(self):
        """Returns the patron name."""
        return self._name

    def get_checked_out_items(self):
        """Returns the list of the patron's currently checked out items."""
        return self._checked_out_items

    def get_fine_amount(self):
        """Returns the patron fine amount."""
        return self._fine_amount

    def add_library_item(self, library_item):
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """Removes the given library item from patron's checked out list of items."""
        self._checked_out_items.remove(library_item)

    def amend_fine(self, amount):
        """Adjusts the fine amount by given argument."""
        self._fine_amount += amount