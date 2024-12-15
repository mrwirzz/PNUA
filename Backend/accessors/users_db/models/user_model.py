from mongoengine import Document, StringField, ListField, ReferenceField

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    preferences = ListField(ReferenceField('Preference'))  # Ссылка на предпочтения