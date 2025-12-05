class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status   # shows if issued or not

    def toLine(self):
        # saving the book in a single line format
        return self.title + "|" + self.author + "|" + self.isbn + "|" + self.status


def bookFromLine(line):
    parts = line.strip().split("|")
    if len(parts) != 4:
        return None
    # making a book object back from line
    return Book(parts[0], parts[1], parts[2], parts[3])


class LibraryInventory:
    def __init__(self, filename="inventory.txt"):
        self.filename = filename
        self.books = []
        self.loadFile()

    def loadFile(self):
        try:
            f = open(self.filename, "r")
            for line in f:
                b = bookFromLine(line)
                if b != None:
                    self.books.append(b)
            f.close()
        except:
            # if file doesn't exist, make an empty one
            file = open(self.filename, "w")
            file.close()

    def saveFile(self):
        try:
            f = open(self.filename, "w")
            for b in self.books:
                f.write(b.toLine() + "\n")
            f.close()
        except:
            print("Error while saving file")

    def addBook(self, title, author, isbn):
        # checking if isbn already there
        for b in self.books:
            if b.isbn == isbn:
                return False

        newb = Book(title, author, isbn)
        self.books.append(newb)
        self.saveFile()
        return True

    def searchTitle(self, title):
        found = []
        for b in self.books:
            if title.lower() in b.title.lower():
                found.append(b)
        return found

    def searchISBN(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None


def menu():
    print("\n=== Library Inventory ===")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. Show All Books")
    print("5. Search by Title")
    print("6. Exit")
    return input("Enter your choice: ")


def main():
    inv = LibraryInventory()

    while True:
        ch = menu()

        if ch == "1":
            t = input("Book title: ")
            a = input("Author name: ")
            isbn = input("ISBN: ")

            if inv.addBook(t, a, isbn):
                print("Book added.")
            else:
                print("ISBN already exists.")

        elif ch == "2":
            isbn = input("Enter ISBN to issue: ")
            b = inv.searchISBN(isbn)
            if b != None:
                if b.status == "available":
                    b.status = "issued"
                    inv.saveFile()
                    print("Book issued.")
                else:
                    print("Already issued.")
            else:
                print("Book not found.")

        elif ch == "3":
            isbn = input("Enter ISBN to return: ")
            b = inv.searchISBN(isbn)
            if b != None:
                if b.status == "issued":
                    b.status = "available"
                    inv.saveFile()
                    print("Book returned.")
                else:
                    print("This book was not issued.")
            else:
                print("Book not found.")

        elif ch == "4":
            if len(inv.books) == 0:
                print("No books available.")
            else:
                for b in inv.books:
                    print("Title:", b.title, "| Author:", b.author,
                          "| ISBN:", b.isbn, "| Status:", b.status)

        elif ch == "5":
            t = input("Enter title to find: ")
            res = inv.searchTitle(t)
            if len(res) > 0:
                for b in res:
                    print("Title:", b.title, "| Author:", b.author,
                          "| ISBN:", b.isbn, "| Status:", b.status)
            else:
                print("No matching books.")

        elif ch == "6":
            print("Exiting program.")
            break

        else:
            print("Invalid choice!")
            

if __name__ == "__main__":
    main()
