#-*- coding:utf-8 -*-
#from random import randrange
#from datetime import datetime
#import pickle
import os
from plone import api
from Products.ATContentTypes.lib import constraintypes
from Products.DCWorkflow.interfaces import *
#使用archetype content type做為相關的觸發條件
from Products.ATContentTypes.interfaces import folder
from Products.Archetypes.interfaces import *

from Products.PluggableAuthService.interfaces import events
from zope.lifecycleevent.interfaces import IObjectAddedEvent

#-------分隔線，以上是自已 import----------------------

from five import grok
'''
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


# Interface class; used to define content-type schema.

class IprogramSet(form.Schema, IImageScaleTraversable):
    """
    program set for babywithme
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/programset.xml to define the content type.

    form.model("models/programset.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class programSet(Container):
    grok.implements(IprogramSet)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# programset_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IprogramSet)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here

'''
#-------------以下自定義程式------------------------


#新註冊id,系統會開使用者家目錄，初始化這個目錄
@grok.subscribe(folder.IATFolder, IObjectAddedEvent)
def changeState(content, event):
    portal = api.portal.get()
    id = str(content.getId())
    uid = str(content.UID())
    if portal['Members'].has_key(id) and portal['Members'][id].UID() == uid:
        userHomeDir = portal['Members'][id]
        with open ('/home/plone/yyyyy','a') as yyyyy:
            yyyyy.write('成功了programSet!')
#排除於導覽外
    else:
        return
