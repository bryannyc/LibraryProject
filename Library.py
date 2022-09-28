class Library:
    """Represents a library with a dictionary of holdings, a dictionary of members and a current date."""
    def __init__(self):
        """Creates a Library object."""
        self._holdings = {}
        self._members = {}
        self._current_date = 0

    def get_holdings(self):
        """Returns the Library's dictionary of holdings."""
        return self._holdings

    def get_members(self):
        """Returns the Library's dictionary of members."""
        return self._members

    def get_current_date(self):
        """Returns the current date of the library."""
        return self._current_date

    def add_library_item(self, library_item):
        """Adds given library item to holdings dictionary."""
        library_item_id = library_item.get_library_item_id()
        self._holdings[library_item_id] = library_item

    def add_patron(self, patron):
        """Adds given patron to members dictionary."""
        patron_id = patron.get_patron_id()
        self._members[patron_id] = patron

    def lookup_library_item_from_id(self, library_item_id):
        """Returns the library item object corresponding to given library item id if found, if not returns None."""
        if library_item_id in self._holdings:
            return self._holdings[library_item_id]
        else:
            return None

    def lookup_patron_from_id(self, patron_id):
        """Returns the patron object corresponding to the given patron id if found, otherwise returns None."""
        if patron_id in self._members:
            return self._members[patron_id]
        else:
            return None

    def check_out_library_item(self, patron_id, library_item_id):
        """Checks if patron is a member, if not, it returns patron not found.
        Checks if item is in the library, if not, it returns item not found.
        Then checks if the item is already checked out and
        if the item was requested by either the patron or someone else.
        If available, it will update the library item's checked out by, date checked out and location and
        add the library item to the patron's list of checked out items."""
        if patron_id not in self._members:
            return "patron not found"
        if library_item_id not in self._holdings:
            return "item not found"

        library_item = self._holdings[library_item_id]
        patron = self._members[patron_id]

        if library_item.get_location() == "CHECKED_OUT":
            return "item already checked out"
        if library_item.get_location() == "ON_HOLD_SHELF" \
                and library_item.get_requested_by().get_patron_id() != patron.get_patron_id():
            return "item on hold by another patron"

        if library_item.get_requested_by() is not None and \
                library_item.get_requested_by().get_patron_id() == patron.get_patron_id():
            library_item.set_requested_by(None)

        library_item.set_checked_out_by(patron)
        library_item.set_date_checked_out(self._current_date)
        library_item.set_location("CHECKED_OUT")
        patron.add_library_item(library_item)
        return "check out successful"

    def return_library_item(self, library_item_id):
        """First checks if the library item is not in the holdings, if not returns item not found.
        Checks if item is not checked out and if it is not, it returns item already in library.
        Updates the patron's checked out items list, updates the library item's location,
        updates the library item's checked out by and returns return successful."""
        if library_item_id not in self._holdings:
            return "item not found"
        if self._holdings[library_item_id].get_location() != "CHECKED_OUT":
            return "item already in library"

        patron = self._holdings[library_item_id].get_checked_out_by()
        library_item = self._holdings[library_item_id]
        patron.remove_library_item(library_item)

        if library_item.get_requested_by() is not None:
            library_item.set_location("ON_HOLD_SHELF")
        else:
            library_item.set_location("ON_SHELF")
        library_item.set_checked_out_by = None
        return "return successful"

    def request_library_item(self, patron_id, library_item_id):
        """Checks if the given patron is a member, if not returns patron not found.
        Checks if library item is in holdings dictionary, if not, returns item not found.
        """
        if patron_id not in self._members:
            return "patron not found"
        if library_item_id not in self._holdings:
            return "item not found"

        library_item = self._holdings[library_item_id]
        if library_item.get_requested_by() is not None:
            return "item already on hold."

        patron = self._members[patron_id]
        library_item.set_requested_by(patron)

        if library_item.get_location() == "ON_SHELF":
            library_item.set_location("ON_HOLD_SHELF")
        return "request successful"

    def pay_fine(self, patron_id, pay_amount):
        """Checks if given patron id is a member,
        if so it calls the amend fine method on the patron and reduces by the pay amount."""
        if patron_id not in self._members:
            return "patron not found"
        self._members[patron_id].amend_fine(-pay_amount)
        return "payment successful"

    def increment_current_date(self):
        """Increments the current date for the library."""
        self._current_date += 1
        for (library_item_id, library_item) in self._holdings.items():
            if library_item.get_location() == "CHECKED_OUT":
                days_checked_out = self._current_date - library_item.get_date_checked_out()
                if days_checked_out > library_item.get_check_out_length():
                    patron = library_item.get_checked_out_by()
                    patron.amend_fine(.10)