#-*- coding:utf-8 -*-

#event handle
from Products.DCWorkflow.interfaces import *
from Products.ATContentTypes.interfaces import folder
from Products.Archetypes.interfaces import *
from Products.PluggableAuthService.interfaces import events
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from five import grok

#program libary
import os
from plone import api
from Products.ATContentTypes.lib import constraintypes


#新註冊id,系統會新增使用者家目錄，初始化這個目錄
@grok.subscribe(folder.IATFolder, IObjectAddedEvent)
def initialUserHome(content, event):
    portal = api.portal.get()
    id = str(content.getId())
    uid = str(content.UID())

    #確認Members目錄中有這個目錄，而且就是新增的這個目錄
    if portal['Members'].has_key(id) and portal['Members'][id].UID() == uid:
        userHomeDir = portal['Members'][id]
        #同時將user家目錄改設定只允許Album, Document, playgroup
        userHomeDir.setConstrainTypesMode(constraintypes.ENABLED)
        userHomeDir.setLocallyAllowedTypes(["Document",
                                            "babywithme.content.album",
                                            "babywithme.content.playgroup"])
        userHomeDir.setImmediatelyAddableTypes(["Document",
                                                "babywithme.content.album",
                                                "babywithme.content.playgroup"])
        #將使用者家目錄設為「排除於導覽樹外」
        userHomeDir.setExcludeFromNav(True)
        #reindex
        userHomeDir.reindexObject("exclude_from_nav")
    else:
        return
