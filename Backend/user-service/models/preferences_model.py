from mongoengine import Document, StringField

class Preference(Document):
    category = StringField(required=True, unique=True)
    description = StringField()