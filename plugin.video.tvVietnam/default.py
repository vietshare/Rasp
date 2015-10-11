# -*- coding: utf-8 -*-
import urllib, urllib2, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, re, urlfetch, hashlib

from BeautifulSoup import BeautifulSoup


AddonID = 'plugin.video.tvVietnam'
__settings__ = xbmcaddon.Addon(id='plugin.video.tvVietnam')
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')

addonDir = Addon.getAddonInfo('path').decode("utf-8")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common

addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)
	

playlistsFile = os.path.join(addon_data_dir, "playLists.txt")
tmpListFile = os.path.join(addon_data_dir, 'tempList.txt')
htvListFile = os.path.join(addon_data_dir, 'htvList.txt')
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
htvFile = os.path.join(addon_data_dir, 'htv.m3u')
fptFile = os.path.join(addon_data_dir, 'fpt.m3u')
vietFile = os.path.join(addon_data_dir, 'viet.m3u')
if  not (os.path.isfile(favoritesFile)):
	f = open(favoritesFile, 'w') 
	f.write('[]') 
	f.close() 

def home():
    apilink = "http://api.htvonline.com.vn/tv_channels"
    reqdata = '{"pageCount":200,"category_id":"-1","startIndex":0}'
    data = getContent ( apilink , reqdata)
#    f = open(htvFile, "w")
#    f.write("#EXTM3U\n")
#    f2 = open(vietFile, "w")
#    f2.write("#EXTM3U\n")

    htvList = []
    for d in data ["data"] :
        res = d["link_play"][0]["resolution"]
        img = d["image"]
        title = d["name"]+' ('+res+')'
        link = d["link_play"][0]["mp3u8_link"]
	unicodestr = title.encode('utf-8').strip()
#	f.write("#EXTINF:-1,%s\n" %unicodestr)
#        f.write("%s\n" %link)

	hashCode = hashlib.md5(unicodestr).hexdigest()
	#htvList.append({"url": link, "image": "", "name": unicodestr})
	htvList.append({"url": link, "image": img, "name": unicodestr.decode("utf-8"), "hashcode": hashCode})
	
#	f2.write("#EXTINF:-1 tvg-logo=\"%s\"," %img)
#	f2.write("%s\n" %unicodestr)
#	htvLink = "http://hplus.vn//" + hashCode
#        f2.write("%s\n" %htvLink )
#    f.close()
#    f2.close()
    
    #print htvList
    common.SaveList(htvListFile, htvList)



def getContent(url, requestdata):
    req = urllib2 . Request(urllib . unquote_plus(url))
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Authorization', 'Basic YXBpaGF5aGF5dHY6NDUlJDY2N0Bk')
    req.add_header('User-Agent', 'Apache-HttpClient/UNAVAILABLE (java 1.4)')
    link = urllib . urlencode({'request': requestdata})
    resp = urllib2 . urlopen(req, link, 120)
    content = resp . read()
    resp . close()
    content = '' . join(content . splitlines())
    data = json . loads(content)
    return data



def getChannels():

    crawurl= 'http://fptplay.net/livetv'	

    f = open(fptFile, "w")
    f.write("#EXTM3U\n")

    result = None
    result = urlfetch.fetch(
        crawurl,
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
            })
    if result.status_code != 200 :
        print 'Something wrong when get list fpt play channel !'
        return
    soup = BeautifulSoup(result.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    
    items = soup.findAll('div', {'class' : 'item_view'})
    for item in items:
            
        ac = item.find('a', {'class' : 'tv_channel '})
        
        if ac == None :
            ac = item.find('a', {'class' : 'tv_channel active'})
            if ac == None :
                continue
        
        lock = item.find('img', {'class' : 'lock'})
        
        if lock != None :
            continue
        
        dataref = ac.get('data-href')
        
        if dataref == None :
            continue
        
        img = ac.find('img', {'class' : 'img-responsive'})
        
        imgthumbnail = ''
        title = ""

        if img != None :
            imgthumbnail = img.get('data-original')
            title = img.get('title')
		
            
        if not dataref.startswith(crawurl) :
            continue
            
        channelid = dataref[26:]
        
        if not channelid :
            continue
            
        link = "http://fptplay.vn//" + channelid

	unicodestr = title.encode('utf-8').strip()

	f.write("#EXTINF:-1 tvg-logo=\"%s\"," %imgthumbnail)
	f.write("%s\n" %unicodestr)

        f.write("%s\n" %link )

    
    f.close()

	
def Categories():
	#repoCheck.UpdateRepo()

	
	list = common.ReadList(playlistsFile)
	for item in list:
		mode = 1 if item["url"].find(".plx") > 0 else 2
		name = common.GetEncodeString(item["name"])
		AddDir("[COLOR blue]{0}[/COLOR]".format(name) ,item["url"], mode, "")

	AddDir("[COLOR blue]{0}[/COLOR]".format("US"),"http://pastebin.com/raw.php?i=csh2HJi2", 4, "")
	AddDir("[COLOR blue]{0}[/COLOR]".format("Vietnam(from US)"),"http://pastebin.com/raw.php?i=x7iMAwhF", 4, "")
	AddDir("[COLOR blue]{0}[/COLOR]".format("Vietnam(from hplus.vn)"),"http://pastebin.com/raw.php?i=mh93beYk" , 4, "")
	AddDir("[COLOR blue]{0}[/COLOR]".format("Vietnam(fptplay.vn)"),"http://pastebin.com/raw.php?i=mTdWEhjD", 4, "")
	#AddDir("[COLOR blue]{0}[/COLOR]".format("Vietnam(fptplay.vn)"),fptFile, 4, "")
	AddDir("[COLOR blue]{0}[/COLOR]".format("Vietnam(vtvplus.vn)"),"http://pastebin.com/raw.php?i=PrJcL7zS", 4, "")
	#VideoChannel()
	addShowDir("Hoài Linh","http://hieuhien.vn/XBMC/LIVESHOW/HOAILINH.xml",50,"http://i.imgur.com/ZtRIhmO.jpg")
	addShowDir("Trường Giang","http://hieuhien.vn/XBMC/LIVESHOW/TRUONGGIANG.xml",50,"http://i.imgur.com/AosVicV.jpg")
	AddDir("[COLOR white][B]{0}[/B][/COLOR]".format(localizedString(10003).encode('utf-8')), "favorites" ,30 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"))
	AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10001).encode('utf-8')), "settings" , 20, os.path.join(addonDir, "resources", "images", "NewList.ico"), isFolder=False)
	AddDir("[COLOR white][B]{0}[/B][/COLOR]".format("Exit"), "Exit" ,99 ,os.path.join(addonDir, "resources", "images", "shutdown.png"), isFolder=False)

def AddNewList():
	listName = GetKeyboardText(localizedString(10004).encode('utf-8')).strip()
	if len(listName) < 1:
		return

	method = GetSourceLocation(localizedString(10002).encode('utf-8'), [localizedString(10016).encode('utf-8'), localizedString(10017).encode('utf-8')])	
	#print method
	if method == -1:
		return
	elif method == 0:
		listUrl = GetKeyboardText(localizedString(10005).encode('utf-8')).strip()
	else:
		listUrl = xbmcgui.Dialog().browse(int(1), localizedString(10006).encode('utf-8'), 'myprograms','.plx|.m3u').decode("utf-8")
		if not listUrl:
			return
	
	if len(listUrl) < 1:
		return


	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == listUrl.lower():

			xbmc.executebuiltin('Notification({0}, "{1}" {2}, 5000, {3})'.format(AddonName, listName, localizedString(10007).encode('utf-8'), icon))
			return
	list.append({"name": listName.decode("utf-8"), "url": listUrl})
	if common.SaveList(playlistsFile, list):
		#xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
		xbmc.executebuiltin("XBMC.Container.Refresh()")
	
	
def RemoveFromLists(url):
	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == url.lower():
			list.remove(item)
			if common.SaveList(playlistsFile, list):
				xbmc.executebuiltin("XBMC.Container.Refresh()")
			break
			
def PlxCategory(url):
	tmpList = []
	list = common.plx2list(url)
	background = list[0]["background"]
	for channel in list[1:]:
		iconimage = "" if not channel.has_key("thumb") else common.GetEncodeString(channel["thumb"])
		name = common.GetEncodeString(channel["name"])
		if channel["type"] == 'playlist':
			AddDir("[COLOR blue][{0}][/COLOR]".format(name) ,channel["url"], 1, iconimage, background=background)
		else:
			AddDir(name, channel["url"], 3, iconimage, isFolder=False, background=background)
			tmpList.append({"url": channel["url"], "image": iconimage, "name": name.decode("utf-8")})
			
	common.SaveList(tmpListFile, tmpList)
			
def m3uCategory(url):	
	tmpList = []
	list = common.m3u2list(url)

	for channel in list:

		name = common.GetEncodeString(channel["display_name"])
		AddDir(name ,channel["url"], 3, channel["logo"], isFolder=False)
		tmpList.append({"url": channel["url"], "image": channel["logo"], "name": name.decode("utf-8"), "hashcode": hashlib.md5(name).hexdigest()})

	common.SaveList(tmpListFile, tmpList)
		
def PlayUrl(name, url, iconimage=None):
	print '--- Playing "{0}". {1}'.format(name, url)

	if url.find("viettv") > 0 :
		vIndex = url.index("//",7)
		vIndex = vIndex + 2
		titleName = url[vIndex :]


		vLink = "http://www.viettv24.com/main/getStreamingServerWeb.php"
		vFile = urllib.urlopen(vLink )
		resp = vFile.read()
		data = json.loads(resp)
		url = data[0]['streamApp'] + titleName +  "/playlist.m3u8?" + data[0]['key']

	elif url.find("fptplay.vn") > 0 :
		vIndex = url.index("//",7)
		vIndex = vIndex + 2
		id = url[vIndex :]

		result = urlfetch.post(
        		'http://fptplay.net/show/getlinklivetv',
			data=	{"id": id,
				"quality": __settings__.getSetting('quality'),"mobile": "web"
				},
			headers=	{
					'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
					'X-Requested-With': 'XMLHttpRequest',
					'Referer': 'http://fptplay.net/livetv'
					}
			)

		if result.status_code != 200 :
			url = None
		else :
			info = json.loads(result.content)
			url = info['stream']

	elif url.find("hplus.vn") > 0 :
		vIndex = url.index("//",7)
		vIndex = vIndex + 2
		hashcode = url[vIndex :]

		htvList = common.ReadList(htvListFile)	
		for item in htvList:
	
			if hashcode  ==  item["hashcode"]:
				url = item["url"]
				break		
	elif 'htvonline' in url:
		content = Get_Url(url)	
		url = re.compile('data\-source=\"([^\"]*)\"').findall(content)[0]
	elif 'hplus.com' in url:
		content = Get_Url(url)	
		url = re.compile('iosUrl\s*=\s*\"([^\"]*)\"').findall(content)[0]

	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage, description="", isFolder=True, background=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)

	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
	if background:
		liz.setProperty('fanart_image', background)
	if mode == 1 or mode == 2:
		liz.addContextMenuItems(items = [('{0}'.format(localizedString(10008).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=22)'.format(sys.argv[0], urllib.quote_plus(url)))])
	elif mode == 3:
		liz.setProperty('IsPlayable', 'true')
		liz.addContextMenuItems(items = [('{0}'.format(localizedString(10009).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
	elif mode == 4:
		liz.setProperty('IsPlayable', 'true')
	elif mode == 32:
		liz.setProperty('IsPlayable', 'true')
		liz.addContextMenuItems(items = [('{0}'.format(localizedString(10010).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=33&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
		
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text =  "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, list):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list)
	return answer
	

def AddFavorites2(url, iconimage, name):

	favList = common.ReadList(favoritesFile)
	#use url find hash code, url = http://hplus.vn//hashcode
	#for item in favList:
	#	if item["url"].lower() == url.lower():
	#		xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10011).encode('utf-8'), icon))
	#		return
    
	list = common.ReadList(tmpListFile)	
	
	for channel in list:
		if channel["url"].lower() == url.lower():
			print "hashcode " +  channel["hashcode"] + ", url: " + channel["url"]
			url = channel["url"]	
			iconimage = channel["image"]
			if url.find("cdnviet.com") > 0 :
				url = "http://hplus.vn//" + channel["hashcode"]
			break
			
	if not iconimage:
		iconimage = ""
		
	data = {"url": url, "image": iconimage, "name": name.decode("utf-8")}
	
	favList.append(data)

	common.SaveList(favoritesFile, favList)
	xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10012).encode('utf-8'), icon))


def AddFavorites(url, iconimage, name):
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10011).encode('utf-8'), icon))
			return
    
	list = common.ReadList(tmpListFile)	

			
	if not iconimage:
		iconimage = ""
		
	data = {"url": url, "image": iconimage, "name": name.decode("utf-8")}
	
	favList.append(data)
	common.SaveList(favoritesFile, favList)
	xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10012).encode('utf-8'), icon))
	
def ListFavorites():
	#AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10013).encode('utf-8')), "favorites" ,34 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"), isFolder=False)
	list = common.ReadList(favoritesFile)
	for channel in list:
		name = channel["name"].encode("utf-8")
		iconimage = channel["image"].encode("utf-8")
		AddDir(name, channel["url"], 32, iconimage, isFolder=False) 
		
def RemoveFavorties(url):
	list = common.ReadList(favoritesFile) 
	for channel in list:
		if channel["url"].lower() == url.lower():
			list.remove(channel)
			break
			
	common.SaveList(favoritesFile, list)
	xbmc.executebuiltin("XBMC.Container.Refresh()")
	
def AddNewFavortie():
	chName = GetKeyboardText("{0}".format(localizedString(10014).encode('utf-8'))).strip()
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText("{0}".format(localizedString(10015).encode('utf-8'))).strip()
	if len(chUrl) < 1:
		return
		
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, localizedString(10011).encode('utf-8'), icon))
			return
			
	data = {"url": chUrl, "image": "", "name": chName.decode("utf-8")}
	
	favList.append(data)
	if common.SaveList(favoritesFile, favList):
		xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}?mode=30&url=favorites')".format(AddonID))






def TVChannel(url):
    xmlcontent = GetUrl(url)
    names = re.compile('<name>(.+?)</name>').findall(xmlcontent)
    if len(names) == 1:
        items = re.compile('<item>(.+?)</item>').findall(xmlcontent)
        for item in items:
            thumb=""
            title=""
            link=""
            if "/title" in item:
                title = re.compile('<title>(.+?)</title>').findall(item)[0]
            if "/link" in item:
                link = re.compile('<link>(.+?)</link>').findall(item)[0]
            if "/thumbnail" in item:
                thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
            add_Link(title, link, thumb)
        #xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)		
    else:
        for name in names:
            addShowDir('' + name + '', url+"?n="+name, 52, '')
        #xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)

def VideoChannel():
    content = Get_Url("http://www.hieuhien.vn/XBMC/LIVESHOW/MenuLiveShow.xml")
    match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)	
    for title,url,thumbnail in match:
		addShowDir(title,url,50,thumbnail)	
    #xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)	
	
def resolveUrl(url):
	if 'xemphimso' in url:
		content = Get_Url(url)	
		url = urllib.unquote_plus(re.compile("file=(.+?)&").findall(content)[0])
	elif 'vtvplay' in url:
		content = Get_Url(url)
		url = content.replace("\"", "")
		url = url[:-5]
	elif 'vtvplus' in url:
		content = Get_Url(url)
		url = re.compile('var responseText = "(.+?)";').findall(content)[0]		
	elif 'htvonline' in url:
		content = Get_Url(url)	
		url = re.compile('data\-source=\"([^\"]*)\"').findall(content)[0]
	elif 'hplus' in url:
		content = Get_Url(url)	
		url = re.compile('iosUrl = "(.+?)";').findall(content)[0]		
	else:
		url = url
	item=xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	  
	return

    
def GetUrl(url):
    link = ""
    if os.path.exists(url)==True:
        link = open(url).read()
    else:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    link = ''.join(link.splitlines()).replace('\'','"')
    link = link.replace('\n','')
    link = link.replace('\t','')
    link = re.sub('  +',' ',link)
    link = link.replace('> <','><')
    return link
	
def add_Link(name,url,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=51"  
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable', 'true')  
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  


def addShowDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok	
	




def Get_Url(url):
    try:
		req=urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)')
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()  
		return link
    except:
		pass


def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?','')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0].lower()] = splitparams[1]
	return param

	
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass
try:        
	print "================mode " + params["mode"] 
	#mode = int(params["mode"])
	mode = params["mode"]
except:
	print "================Error"
	pass
try:       
	description = urllib.unquote_plus(params["description"])
except:
	pass

	
if mode == None or url == None or len(url) < 1:
	home()
	#getChannels()
	Categories()
elif mode == '1':
	PlxCategory(url)
elif mode == '2' or mode == '4':
	m3uCategory(url)
elif mode == '3' or mode == '32':
	PlayUrl(name, url, iconimage)
elif mode == '20':
	AddNewList()
elif mode == '22':
	RemoveFromLists(url)
elif mode == '30':
	ListFavorites()
elif mode == '31': 
	AddFavorites(url, iconimage, name) 
elif mode == '33':
	RemoveFavorties(url)
elif mode == '34':
	AddNewFavortie()
elif mode == '99':
	#turnOff(url, iconimage, name)
	xbmc.executebuiltin("XBMC.Quit()")
	sys.exit()
	#xbmc.executebuiltin("System.Exec(Notepad)")
elif mode == '40':
	common.DelFile(playlistsFile)
	sys.exit()
elif mode == '41':
	common.DelFile(favoritesFile)
	sys.exit()
elif mode == '50':
	print "========Viet 50"
	TVChannel(url)	
elif mode=='51':
	print "========Viet 51"
	PlayUrl(name, url, iconimage)
	#resolveUrl(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
