import json
import unittest

from Album import Album
from Book import Book
from Library import Library
from LibraryItem import LibraryItem
from Movie import Movie
from Patron import Patron


class LibraryTester(unittest.TestCase):
    def test_library_item(self):
        library_item = LibraryItem("abc", "the thing")
        patron = Patron("123", "John")
        self.assertEqual(library_item.get_library_item_id(), "abc")
        self.assertEqual(library_item.get_title(), "the thing")
        self.assertEqual(library_item.get_checked_out_by(), None)
        self.assertEqual(library_item.set_checked_out_by(patron), None)
        self.assertEqual(library_item.get_requested_by(), None)
        self.assertEqual(library_item.get_date_checked_out(), None)

    def test_patron(self):
        library_item_1 = LibraryItem("abc", "the thing")
        library_item_2 = LibraryItem("aaa", "titanic")
        patron = Patron("123", "John")

        self.verify_patron_checkout(patron, library_item_1, library_item_2)

        self.verify_patron_fines(patron)

    def verify_patron_checkout(self, patron, library_item_1, library_item_2):
        # No items checked out yet
        self.assertEqual(patron.get_checked_out_items(), [])

        # Verify checked out item appears in patron's checked out items list
        patron.add_library_item(library_item_1)
        self.assertEqual(patron.get_checked_out_items(), [library_item_1])

        # Verify all checked items appear
        patron.add_library_item(library_item_2)
        self.assertEqual(patron.get_checked_out_items(), [library_item_1, library_item_2])

        # Verify item is removed properly
        patron.remove_library_item(library_item_1)
        self.assertEqual(patron.get_checked_out_items(), [library_item_2])

    def verify_patron_fines(self, patron):
        # Testing fine
        patron.amend_fine(20)
        self.assertEqual(patron.get_fine_amount(), 20)

        patron.amend_fine(-5)
        self.assertEqual(patron.get_fine_amount(), 15)

        patron.amend_fine(.2)
        self.assertEqual(patron.get_fine_amount(), 15.20)

    def test_library(self):
        library = Library()
        library_item_1 = LibraryItem("abc", "the thing")
        library_item_2 = LibraryItem("aaa", "titanic")
        patron_1 = Patron("123", "John")
        patron_2 = Patron("124", "George")

        self.verify_library_members(library, patron_1, patron_2)

        self.verify_library_holdings(library, library_item_1, library_item_2)

        self.verify_library_transactions(library, patron_2, library_item_1, library_item_2)

    def verify_library_holdings(self, library, library_item_1, library_item_2):
        # Start date should be 0
        self.assertEqual(library.get_current_date(), 0)

        # Assert library can store a library item
        library.add_library_item(library_item_1)
        self.assertEqual(library.get_holdings(), {"abc": library_item_1})

        # Assert library can store multiple library items
        library.add_library_item(library_item_2)
        self.assertEqual(library.get_holdings(), {"abc": library_item_1, "aaa": library_item_2})

        # Look up library item tests
        self.assertEqual(library.lookup_library_item_from_id("aaa"), library_item_2)
        self.assertEqual(library.lookup_library_item_from_id("111"), None)

        self.assertEqual(library.check_out_library_item("101", "aaa"), "patron not found")
        self.assertEqual(library.check_out_library_item("123", "bbb"), "item not found")

    def verify_library_members(self, library, patron_1, patron_2):
        # Test add patron
        library.add_patron(patron_1)
        self.assertEqual(library.get_members(), {"123": patron_1})

        # Test add another patron
        library.add_patron(patron_2)
        self.assertEqual(library.get_members(), {"123": patron_1, "124": patron_2})

        # Look up patron tests
        self.assertEqual(library.lookup_patron_from_id("123"), patron_1)
        self.assertEqual(library.lookup_patron_from_id("125"), None)

    def verify_library_transactions(self, library, patron, library_item_1, library_item_2):
        library_item_1.set_location("CHECKED_OUT")
        self.assertEqual(library.check_out_library_item("123", "abc"), "item already checked out")

        library_item_1.set_location("ON_HOLD_SHELF")
        library_item_1.set_requested_by(patron)
        self.assertEqual(library.check_out_library_item("123", "abc"), "item on hold by another patron")

        library.check_out_library_item("124", "abc")
        self.assertEqual(library_item_1.get_checked_out_by(), patron)
        self.assertEqual(patron.get_checked_out_items(), [library_item_1])
        self.assertEqual(library.check_out_library_item("124", "aaa"), "check out successful")
        self.assertEqual(library.return_library_item("ccc"), "item not found")

        library_item_2.set_location("ON_SHELF")
        self.assertEqual(library.return_library_item("aaa"), "item already in library")

    def test_library_polymorhpism(self):
        # import info from book json to create book objects
        book_list = []
        with open('books.json', 'r') as book_file:
            book_data = json.load(book_file)
        for book in book_data:
            id = book["Id"]
            title = book["Title"]
            author = book["Author"]
            book_object = Book(id, title, author)
            book_list.append(book_object)

        # import info from movie json to create movie objects
        movie_list = []
        with open('movies.json', 'r') as movie_file:
            movie_data = json.load(movie_file)
        for movie in movie_data:
            id = movie["Id"]
            title = movie["Title"]
            director = movie["Director"]
            movie_object = Movie(id, title, director)
            movie_list.append(movie_object)

        # import info from album json to create album objects
        album_list = []
        with open('albums.json', 'r') as album_file:
            album_data = json.load(album_file)
        for album in album_data:
            id = album["Id"]
            title = album["Title"]
            artist = album["Artist"]
            album_object = Album(id, title, artist)
            album_list.append(album_object)

        # import info from patron json to create patron objects
        patron_list = []
        with open('patrons.json', 'r') as patron_file:
            patron_data = json.load(patron_file)
        for patron in patron_data:
            id = patron["Id"]
            name = patron["Name"]
            patron_object = Patron(id, name)
            patron_list.append(patron_object)

        # create library object, add library items and patrons
        lib = Library()
        for book in book_list:
            lib.add_library_item(book)
        for album in album_list:
            lib.add_library_item(album)
        for movie in movie_list:
            lib.add_library_item(movie)

        self.assertEqual(len(lib.get_holdings()), len(book_list) + len(album_list) + len(movie_list))

        for patron in patron_list:
            lib.add_patron(patron)

        self.assertEqual(len(lib.get_members()), len(patron_list))

    def verify_item_location(self, library, library_item):
        library.check_out_library_item("bcd", "456")
        location = library_item.get_location()
        self.assertEqual()

        # add to check fine
        for i in range(57):
            lib.increment_current_date()  # 57 days pass
        p2_fine = p2.get_fine_amount()
        lib.pay_fine("bcd", p2_fine)

        # add to library transaction
        lib.return_library_item("456")

if __name__ == "__main__":
    unittest.main()