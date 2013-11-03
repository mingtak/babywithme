#-*- coding:utf-8 -*-
from Products.ATContentTypes.lib import constraintypes
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from plone import api

from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from babywithme.content import MessageFactory as _



#寫入測試，寫到/home/plone/yyyyy
def writeinTest(string='please give me a text string'):
    with open('/home/plone/yyyyy', 'a') as yyyyy:
        yyyyy.write(string + '\n')


# Interface class; used to define content-type schema.

class IAlbum(form.Schema, IImageScaleTraversable):
    """
    Album for user
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/album.xml to define the content type.

    form.model("models/album.xml")

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Album(Container):
    grok.implements(IAlbum)
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# album_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IAlbum)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here

'''
#新增Album,初始化這個目錄,只能新增image
@grok.subscribe(IAlbum, IObjectAddedEvent)
def initialAlbum(content, event):
    writeinTest(str(content.UID()))
    portal = api.portal.get()
#    id = str(content.getId())
    uid = str(content.UID())
    newAlbum = portal['Members']['ddddd']['ffg']['ddddd'] #  api.content.get(UID=uid)

    #將Album設定只允許Image
    newAlbum.setConstrainTypesMode(constraintypes.ENABLED)
    newAlbum.setLocallyAllowedTypes(["Image"])
    newAlbum.setImmediatelyAddableTypes(["Image"])
    writeinTest(str(content.getId()))
    #將Album設為「排除於導覽樹外」
#    userHomeDir.setExcludeFromNav(True)
        #reindex
'''
