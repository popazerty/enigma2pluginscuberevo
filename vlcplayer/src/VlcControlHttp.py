from urllib import urlencode
from urllib2 import urlopen
from xml.dom.minidom import parse
from Components.config import config
import socket

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

class VlcControlHttp:
	defaultStreamName = "dreambox"
	
	def __init__(self, servernum):
		cfg = config.plugins.vlcplayer.servers[servernum]
		self.servercfg = cfg
		self.host = cfg.host.value + ":" + str(cfg.httpport.value)
		self.lastError = None
		try:
			self.defaultStreamName = "dream" + socket.gethostbyname(socket.gethostname()).split('.')[3]
		except Exception, e:
			pass

	def connect(self):
		pass

	def close(self):
		pass
	
	def xmlRequest(self, request, params):
		uri = "/requests/"+request+".xml"
		if params is not None: uri = uri + "?" + urlencode(params)
		#print "[VLC] SEND:", self.host+uri
		resp = urlopen("http://"+self.host+uri)
		return parse(resp)

	def playfile(self, filename, output):
		filename = filename.replace("\\", "\\\\")
		filename = filename.replace("'", "\\'")
		input = filename
		if output is not None:
			input += " :sout=" + output;
		print "[VLC] playfile", input
		xml = self.xmlRequest("status", {"command": "in_play", "input": input})
		error = xml.getElementsByTagName("error")
		if error is not None and len(error) > 0:
			self.lastError = getText(error[0].childNodes).strip()
			if len(self.lastError) == 0:
				self.lastError = None
			else:
				print "[VLC] VlcControl error:", self.lastError
		else:
			self.lastError = None
		return self.lastError

	def status(self):
		xml = self.xmlRequest("status", None)
		stats = {}
		for e in xml.documentElement.childNodes:
			if e.nodeType == e.ELEMENT_NODE:
				if e.firstChild is None:
					stats[e.nodeName.encode("latin_1", "replace")] = None
				else:
					stats[e.nodeName.encode("latin_1", "replace")] = e.firstChild.nodeValue.encode("latin_1", "replace")
		return stats

	def get_playlist(self):
		xml = self.xmlRequest("playlist", None)
		flist = []
		for e in xml.getElementsByTagName("leaf"):
			fentry = {}
			fentry["id"] = int(e.getAttribute("id"))
			fentry["current"] = e.hasAttribute("current")
			if e.hasAttribute("uri") is not None:
				fentry["name"] = e.getAttribute("uri").encode("latin_1", "replace")
			flist.append(fentry)
		return flist
	
	def get_current_id(self):
		flist = self.get_playlist()
		for f in flist:
			if f["current"]:
				return f["id"]
		return -1

	def play(self, listid=None):
		if listid is None:
			self.xmlRequest("status", {"command": "pl_pause"})
		else:
			self.xmlRequest("status", {"command": "pl_play", "id": str(listid)})
		
	def stop(self):
		self.xmlRequest("status", {"command": "pl_stop"})

	def pause(self):
		self.xmlRequest("status", {"command": "pl_pause"})
		
	def delete(self, listid=None):
		if listid is None:
			listid = self.get_current_id()
		self.xmlRequest("status", {"command": "pl_delete", "id": str(listid)})
		
	def seek(self, value):
		"""  Allowed values are of the form:
  [+ or -][<int><H or h>:][<int><M or m or '>:][<int><nothing or S or s or ">]
  or [+ or -]<int>%
  (value between [ ] are optional, value between < > are mandatory)
examples:
  1000 -> seek to the 1000th second
  +1H:2M -> seek 1 hour and 2 minutes forward
  -10% -> seek 10% back"""
		self.xmlRequest("status", {"command": "seek", "val": str(value)})
		