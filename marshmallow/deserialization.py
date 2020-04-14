from marshmallow import Schema, fields 

class BookSchema(Schema):
    author = fields.Str(required=True)
    title = fields.Str()
    description = fields.Str()

incoming_book_data = {
    "title": "Clean Code",
    "author" : "Bob Martin",
    #"description": "Book about clean code"
}

class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author

book_Schema=BookSchema()
book = book_Schema.load(incoming_book_data)
book_object = Book(**book)
#Json to Object
print(book)

print(book_object)