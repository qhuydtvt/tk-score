from mongoengine import *

class Score(Document):
    name = StringField()
    score = IntField()
    added_time = DateTimeField()