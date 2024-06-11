from mongoengine import StringField, Document, ListField, ReferenceField, BooleanField

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    message_sent = BooleanField(default=False)
    
    def __str__(self):
        return f'{self.fullname},{self.born_date},{self.born_location},{self.description}'
    


class Quotes(Document):
    quote = StringField()
    author = StringField()
    # author = ReferenceField(Author, reverse_delete_rule='CASCADE')
    tags = ListField(StringField())
    
    
    
    def __str__(self):
        return f'{self.quote},{self.author},{self.tags}'