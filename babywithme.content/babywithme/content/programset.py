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

from five import grok


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
