#
# author : jiankaiwang (https://welcome-jiankaiwang.rhcloud.com/)
# project : seed (https://github.com/jiankaiwang/seed)
# reference : seed (https://www.gitbook.com/book/jiankaiwang/seed/details)
#

# coding: utf-8

#
# desc : unicode to utf8 from dictionary
# retn : a utf8-encoding dictionary
# e.g. : unicode2utf8FromDict({ u'\u4e3b\u8981' : u'\u4e3b\u8981' }) 
#
def unicode2utf8FromDict(getDict):
    newData = {}
    for k, v in getDict.iteritems():
        newData[k] = unicode(v).encode('utf-8')
    return newData

#
# desc : unicode to utf8 from string
# retn : a utf8-encoding string
# e.g. : unicode2utf8FromStr(u'\u4e3b\u8981')
#       
def unicode2utf8FromStr(getStr):
    return unicode(getStr).encode('utf-8')