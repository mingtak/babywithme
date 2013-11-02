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


#寫入測試，寫到/home/plone/yyyyy
def writeinTest(string='please give me a text string'):
    with open('/home/plone/yyyyy', 'a') as yyyyy:
        yyyyy.write(string + '\n')



#切換blog的workflow狀態
def changeBlogState(blogFolder, new_state):
    catalog = api.portal.get_tool(name='portal_catalog')
    ownerId= str(blogFolder.getOwner())
    if new_state == 'published':
        searchState = 'tempStat'
    elif new_state == 'private':
        searchState = 'published'
    items = catalog.searchResults({'Creator':ownerId,
                                   'review_state':searchState,
                                   'portal_type':['babywithme.content.album', 
                                                  'babywithme.content.playgroup', 
                                                  'Document']})
    writeinTest(str(type(items)))
    writeinTest(str(len(items)))
    if len(items) == 0:
        return

    writeinTest('len(items)>0')

    if new_state == 'private':
        for item in items:
            contentObject = api.content.get(UID=item.UID)
            api.content.transition(obj=contentObject, transition="toTempStat")
            contentObject.reindexObject()
    elif new_state == 'published':
        for item in items:
            contentObject = api.content.get(UID=item.UID)
            api.content.transition(obj=contentObject, transition="publish")
            contentObject.reindexObject()



#部落格關閉時，將該部落格下面所有published的content改為tmpStat,
#部落格重新啟動後，tmpStat再回到published
@grok.subscribe(folder.IATFolder, IAfterTransitionEvent)
def blogCloseOrReopen(blog, event):
    portal = api.portal.get()
    id = str(blog.getId())
    uid = str(blog.UID())

    #確認這個目錄是個部落格，而不是其他的，才執行
    if portal['Members'].has_key(id) and portal['Members'][id].UID() == uid:
        writeinTest('有call changeBlogState')
        changeBlogState(blogFolder=blog, new_state=event.new_state.id)




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
