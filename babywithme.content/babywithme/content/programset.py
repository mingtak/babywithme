#-*- coding:utf-8 -*-

#event handle
from Products.DCWorkflow.interfaces import *
from Products.ATContentTypes.interfaces import folder
from Products.Archetypes.interfaces import *
from Products.PluggableAuthService.interfaces import events
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from five import grok

#import Dexterity content type
from babywithme.content import album, playgroup

#program libary
import os
from plone import api
from datetime import datetime
from random import randrange
from Products.ATContentTypes.lib import constraintypes

''' 以下暫擱置
#變更id,格式：yyyyMMddhhmm + random(3)
def changeContentId(content):
    newId = "%s%s" % (str(datetime.now().strftime('%Y%m%d%H%M')),
                      str(randrange(100,1000)))
    contentObject = api.content.get(UID=content.UID())
    api.content.rename(obj=content, new_id=newId)


#babywithme.content.album，變更名稱改以時間格式
@grok.subscribe(album.IAlbum, IObjectAddedEvent)
def changeIAlbumId(content, event):
    changeContentId(content)


#babywithme.content.playgroup，變更名稱改以時間格式
@grok.subscribe(playgroup.IPlaygroup, IObjectAddedEvent)
def changeIAlbumId(content, event):
    changeContentId(content)

以上暫擱置
'''

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
