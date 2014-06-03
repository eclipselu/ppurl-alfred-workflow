#coding=utf-8

import urllib2
import urllib
from xml.dom.minidom import Document
from bs4 import BeautifulSoup


def get_search_results():
    params = urllib.urlencode({"s": "{query}"})
    search = urllib2.urlopen('http://www.ppurl.com/?'+params).read()
    html = BeautifulSoup(search)
    results = html.find('div', id="search-book-list")
    return results


'''
The xml output looks like this:

<?xml version="1.0"?>
<items>
  <item uid="desktop" arg="~/Desktop" valid="YES" autocomplete="Desktop" type="file">
    <title>Desktop</title>
    <subtitle>~/Desktop</subtitle>
    <icon type="fileicon">~/Desktop</icon>
  </item>
</items>
'''

def xml_results(results):
    doc = Document()
    items = doc.createElement("items")

    if not results:
        xmlitem = doc.createElement("item")
        attr = doc.createElement("title")
        attr.appendChild(doc.createTextNode(u'哇哦，什么也没找到，←_← '))
        xmlitem.appendChild(attr)
        items.appendChild(xmlitem)
    else:
        for item in results.find('ul').findAll('li'):
            for t in item.findAll('div', attrs={ 'class' : 'info' }):
                title = t.find('a').get_text()
                infos = t.find_all('p')
                subtitle = ' | '.join([i.get_text() for i in infos[1:]])
                url = t.find('a').get('href', '')

                xmlitem = doc.createElement("item")
                xmlitem.setAttribute("uid", url)
                xmlitem.setAttribute("arg", url)
                xmlitem.setAttribute("autocomplete", title)
                xmlitem.setAttribute("valid", "YES")
                attr = doc.createElement("title")
                attr.appendChild(doc.createTextNode(title))
                xmlitem.appendChild(attr)

                attr = doc.createElement("subtitle")
                attr.appendChild(doc.createTextNode(subtitle))
                xmlitem.appendChild(attr)

                attr = doc.createElement("icon")
                attr.appendChild(doc.createTextNode("icon.png"))
                xmlitem.appendChild(attr)

                items.appendChild(xmlitem)

    doc.appendChild(items)
    return doc.toxml().encode('utf-8')

print xml_results(get_search_results())