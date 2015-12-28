from collections import OrderedDict
import datetime
import sys
import os

from peewee import *

db = SqliteDatabase('journal.db')

class Entry(Model):
    content = TextField()
    tag = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db

def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)

def clear():
    os.system("cls" if os.name == 'nt' else "clear")

def menu_loop():
    """Show the menu."""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}> {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()

def add_entry():
    """Add an entry."""
    formatting_var_len = 33
    entry_tag = input("Enter a tag (Work, School..).\nDefault tag is Personal: ")
    print('Enter your entry. Press ctrl+d when done.')
    print('='*formatting_var_len)
    data = sys.stdin.read().strip()
    print('\n')

    if data:
        if input('Save entry? [Y/n]: ').lower() != 'n':
            Entry.create(content=data, tag=entry_tag)
            print('Saved successfully!')

def view_entries(search_query=None):
    """View previous entries."""
    formatting_var_len = 33 # Same as timestamp's length
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query)) 

    if entries.count() == 0: # There are no entries. Retreat. 
        return

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M %p')
        tag = entry.tag
        if tag == '':
            tag = 'Personal'
        content =  entry.content
        clear()
        print(timestamp)
        print('='*formatting_var_len)
        print('Tag: ', tag)
        print(content)
        print("\n\n")
        print('='*formatting_var_len)
        print('n> Next entry.')
        print('q> Return to main menu.')
        print('d> Delete entry.')

        next_action = input('Action [Nqd]: ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def search_entries():
    """Search entries by their contents"""
    view_entries(input("Search query: "))

def delete_entry(entry):
    """Delete an entry."""
    if input('Are you sure? [yN]: ').lower() == 'y':
        entry.delete_instance()
        print('Entry deleted.')

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])

if __name__ == '__main__':
    initialize()
    menu_loop()
