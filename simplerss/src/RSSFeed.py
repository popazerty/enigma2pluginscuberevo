from sets import Set

from urlparse import urlsplit

class BaseFeed:
	"""Base-class for all Feeds. Initializes needed Elements."""
	MAX_HISTORY_ELEMENTS = 100

	def __init__(self, uri, autoupdate, stripper):
		# Set URI (used as Identifier)
		self.uri = uri

		# Determine URI Elements
		remote = urlsplit(uri)
		self.hostname = remote.hostname
		self.port = remote.port or 80
		self.path = '?'.join([remote.path, remote.query])
		print "[SimpleRSS] determined hostname:", self.hostname, ", port:", self.port, ", path:", self.path

		# Set Autoupdate
		self.autoupdate = autoupdate

		# Set Stripper
		self.stripper = stripper

		# Initialize
		self.title = uri.encode("UTF-8")
		self.description = ""
		self.last_update = None
		self.last_ids = set()
		self.history = []

class AtomFeed(BaseFeed):
	"""Parses an Atom-Feed into expected format."""
	def gotDom(self, dom):
		try:
			# Try to read when feed was last updated, if time equals return empty list. else fetch new items
			updated = dom.getElementsByTagName("updated")[0].childNodes[0].data
			if self.last_update == updated:
				return [ ]
			self.last_update = updated
		except:
			pass
		return AtomFeed.parse(self, dom.getElementsByTagName("entry"))

	def parse(self, items):
		new_items = []
		for item in items:
			enclosure = []
			link = ""
			
			# Try to read title, continue if none found
			try:
				title = self.stripper.strip(item.getElementsByTagName("title")[0].childNodes[0].data)
			except:
				continue

			# Try to read id, continue if none found (invalid feed, should be handled differently) or to be excluded
			try:
				id = item.getElementsByTagName("id")[0].childNodes[0].data
				if id in self.last_ids:
					continue
			except:
				continue

			# Read out enclosures and link
			for current in item.getElementsByTagName("link"):
				# Enclosure
				if current.getAttribute("rel") == "enclosure":
					enclosure.append((
							current.getAttribute("href").encode("UTF-8"),
							current.getAttribute("type").encode("UTF-8")
					))
				# No Enclosure, assume its a link to the item
				else:
					link = current.getAttribute("href")
			
			# Try to read summary, empty if none
			try:
				summary = self.stripper.strip_readable(item.getElementsByTagName("summary")[0].childNodes[0].data)
			except:
				summary = ""

			# Update Lists
			new_items.append((
					title.encode("UTF-8"),
					link.encode("UTF-8"),
					summary.encode("UTF-8"),
					enclosure
			))
			self.last_ids.add(id)

		 # Append known Items to new Items and eventually cut it
		self.history = new_items + self.history
		self.history[:self.MAX_HISTORY_ELEMENTS]

		return new_items

class RSSFeed(BaseFeed):
	"""Parses an RSS-Feed into expected format."""
	def gotDom(self, dom):
		# Try to read when feed was last updated, if time equals return empty list. else fetch new items
		try:
			updated = dom.getElementsByTagName("lastBuildDate")[0].childNodes[0].data
			if self.last_update == updated:
				return [ ]
			self.last_update = updated
		except:
			pass
		return RSSFeed.parse(self, dom.getElementsByTagName("item"))

	def parse(self, items):
		new_items = []
		for item in items:
			enclosure = []

			# Try to read title, continue if none found
			try:
				title = self.stripper.strip(item.getElementsByTagName("title")[0].childNodes[0].data)
			except:
				continue

			# Try to read link, empty if none
			try:
				link = item.getElementsByTagName("link")[0].childNodes[0].data
			except:
				link = ""
			
			# Try to read guid, link if none (RSS 1.0 or invalid RSS 2.0)
			try:
				guid = item.getElementsByTagName("guid")[0].childNodes[0].data
			except:
				guid = link

			# Continue if item is to be excluded
			if guid in self.last_ids:
				continue

			# Try to read summary (description element), empty if none
			try:
				summary = self.stripper.strip_readable(item.getElementsByTagName("description")[0].childNodes[0].data)
			except:
				summary = ""

			# Read out enclosures
			for current in item.getElementsByTagName("enclosure"):
				enclosure.append((
						current.getAttribute("url").encode("UTF-8"),
						current.getAttribute("type").encode("UTF-8")
				))

			# Update Lists
			new_items.append((
					title.encode("UTF-8"),
					link.encode("UTF-8"),
					summary.encode("UTF-8"),
					enclosure
			))
			
			self.last_ids.add(guid)

		# Append known Items to new Items and eventually cut it
		self.history = new_items + self.history
		self.history[:self.MAX_HISTORY_ELEMENTS]

		return new_items

class UniversalFeed(BaseFeed, RSSFeed, AtomFeed):
	"""Universal Feed which on first run determines its type and calls the correct parsing-functions"""
	def __init__(self, uri, autoupdate, stripper):
		BaseFeed.__init__(self, uri, autoupdate, stripper)
		self.type = None

	def gotDom(self, dom):
		if self.type is None:
			# RSS 2.0
			if dom.documentElement.getAttribute("version") in ["2.0", "0.94", "0.93", "0.92", "0.91"]:
				self.type = "rss"
				try:
					self.title = dom.getElementsByTagName("channel")[0].getElementsByTagName("title")[0].childNodes[0].data
					self.description = dom.getElementsByTagName("channel")[0].getElementsByTagName("description")[0].childNodes[0].data
				except:
					pass
			# RSS 1.0 (NS: http://www.w3.org/1999/02/22-rdf-syntax-ns#)
			elif dom.documentElement.localName == "RDF":
				self.type = "rss"
				try:
					self.title = dom.getElementsByTagName("channel")[0].getElementsByTagName("title")[0].childNodes[0].data
					self.description = dom.getElementsByTagName("channel")[0].getElementsByTagName("description")[0].childNodes[0].data
				except:
					pass
			# Atom (NS: http://www.w3.org/2005/Atom)
			elif dom.documentElement.localName == "feed":
				self.type = "atom"
				try:
					self.title = dom.getElementsByTagName("title")[0].childNodes[0].data
					self.description = dom.getElementsByTagName("subtitle")[0].childNodes[0].data
				except:
					pass
			else:
				raise NotImplementedError, 'Unsupported Feed: %s' % dom.documentElement.localName
			self.title = self.stripper.strip(self.title).encode("UTF-8")
			self.description = self.stripper.strip_readable(self.description).encode("UTF-8")
		if self.type == "rss":
			print "[SimpleRSS] type is rss"
			return RSSFeed.gotDom(self, dom)
		elif self.type == "atom":
			print "[SimpleRSS] type is atom"
			return AtomFeed.gotDom(self, dom)