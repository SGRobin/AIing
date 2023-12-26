class booki:

    def __init__(self, bookname):
        self.name = bookname

    def printbook(self):
        print(self.name)


class shelf:

    def __init__(self):
        self.books = []

    def addbook(self, book):
        self.books.append(booki(book))

    def removebook(self, book):
        self.books.remove(booki(book))

    def printshelf(self):
        for i in range(0, len(self.books)):
            self.books[i].printbook()


class libra:

    def __init__(self, now=None):
        if now is None:
            now = []
        self.types = []
        self.shelves = now

    def addbook(self, booktype, bookname):
        for i in range(0, len(self.types)):
            if self.types[i] == booktype:
                self.shelves[i].addbook(bookname)
                return
        self.shelves.append(shelf())
        self.shelves[-1].addbook(bookname)
        self.types.append(booktype)

    def removebook(self, booktype, bookname):
        for i in range(0, len(self.types)):
            if self.types[i] == booktype:
                self.shelves[i].removebook(bookname)

    def printlibrary(self):
        for i in range(0, len(self.shelves)):
            print("books from type: " + i)
            for b in range(0, len(i)):
                print(b)


lib = libra()
while True:
    x = input()
    if x == 1:
        y = input()
        z = input()
        lib.addbook(y, z)
    elif x == 2:
        y = input()
        z = input()
        lib.removebook(y, z)
    else:
        lib.printlibrary()
