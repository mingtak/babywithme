from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from plone.app.content.interfaces import INameFromTitle
from random import randrange
from time import time

class Ichangeid(Interface):
    """Marker interface to enable name from creation date behavior"""

class changeid(object):
    implements(INameFromTitle)
    adapts(Ichangeid)

    def __new__(cls, context):
        instance = super(changeid, cls).__new__(cls)
        newId = "%s%s" % (str(time()).replace('.',''), str(randrange(100,1000)))
        instance.title = newId
        return instance

    def __init__(self, context):
        self.context = context
