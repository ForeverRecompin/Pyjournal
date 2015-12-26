import datetime

from peewee import *

db = SqliteDatabase('diary.db')
 

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db

def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)

def menu_loop():
    pass

def add_entry():
    pass

def view_entries():
    pass

def delete_entry():
    pass

if __name__ == '__main__':
    initialize()
    menu_loop()
