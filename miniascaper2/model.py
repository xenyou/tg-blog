from turbogears.database import PackageHub
from sqlobject import *

hub = PackageHub("miniascaper2")
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass

class Article(SQLObject):
    entryid = IntCol(alternateID=True)
    subject = UnicodeCol()
    body = UnicodeCol()
    author = UnicodeCol()
    year = IntCol(notNone=True)
    month = IntCol(notNone=True)
    day = IntCol(notNone=True)
    attached_files = MultipleJoin('Attached')
    trackbacks = MultipleJoin('Trackback')
    category = ForeignKey('Category', cascade=None)

class Category(SQLObject):
    name = UnicodeCol(length=50, alternateID=True)
    articles = MultipleJoin('Article')

class Attached(SQLObject):
    name = UnicodeCol(length=100)
    onfsname = StringCol(alternateID=True, length=200)
    article = ForeignKey('Article', cascade='null')

class Trackback(SQLObject):
    title = UnicodeCol()
    url = StringCol()
    excerpt = UnicodeCol()
    blog_name = UnicodeCol()
    posttime = IntCol()
    article = ForeignKey('Article', cascade=True)

class Msg(SQLObject):
    poster = UnicodeCol()
    body = UnicodeCol()
    posttime = IntCol()
    client = StringCol(length=16)
    signature = UnicodeCol()

class Webinfo(SQLObject):
    name = UnicodeCol()
    url = StringCol()

class User(SQLObject):
    user = UnicodeCol(length=10, alternateID=True)
    password = UnicodeCol()
    privilege = IntCol()

class Access(SQLObject):
    ipaddress = StringCol(length=16)
    accesstime =  DateTimeCol()

class Statistics(SQLObject):
    counter = IntCol()

class AccessBlock(SQLObject):
    ipaddress = StringCol(length=16)

