# -*- coding: UTF-8 -*-
# for localized messages
from . import _

from AutoTimerComponent import preferredAutoTimerComponent
from RecordTimer import AFTEREVENT
from Tools.XMLTools import stringToXML
from ServiceReference import ServiceReference

from enigma import eServiceReference

CURRENT_CONFIG_VERSION = "5"

def getValue(definitions, default):
	# Initialize Output
	ret = ""

	# How many definitions are present
	if isinstance(definitions, list):
		Len = len(definitions)
		if Len > 0:
			childNodes = definitions[Len-1].text
		else:
			childNodes = ""
	else:
		ret = definitions.text

	# Return stripped output or (if empty) default
	return ret.strip() or default

def parseConfig(configuration, list, version = None, uniqueTimerId = 0, defaultTimer = None):
	if version != CURRENT_CONFIG_VERSION:
		parseConfigOld(configuration, list, uniqueTimerId)
		return

	if defaultTimer is not None:
		# Read in defaults for a new timer
		for defaults in configuration.findall("defaults"):
			parseEntry(defaults, defaultTimer, True)

	for timer in configuration.findall("timer"):
		uniqueTimerId += 1
		baseTimer = preferredAutoTimerComponent(
			uniqueTimerId,
			'',
			'',
			True
		)

		if parseEntry(timer, baseTimer):
			list.append(baseTimer)

def parseEntry(element, baseTimer, defaults = False):
	if not defaults:
		# Read out match
		baseTimer.match = element.get("match", "").encode("UTF-8")
		if not baseTimer.match:
			print '[AutoTimer] Erroneous config is missing attribute "match", skipping entry'
			return False

		# Read out name
		baseTimer.name = element.get("name", "").encode("UTF-8")
		if not baseTimer.name:
			print '[AutoTimer] Timer is missing attribute "name", defaulting to match'
			baseTimer.name = baseTimer.match

		# Read out enabled
		enabled = element.get("enabled", "yes")
		if enabled == "no":
			baseTimer.enabled = False
		elif enabled == "yes":
			baseTimer.enabled = True
		else:
			print '[AutoTimer] Erroneous config contains invalid value for "enabled":', enabled,', disabling'
			baseTimer.enabled = False

		# Read timeframe
		before = element.get("before")
		after = element.get("after")
		if before and after:
			baseTimer.timeframe = (int(after), int(before))

	# Read out encoding (won't change if no value is set)
	baseTimer.encoding = element.get("encoding")

	# Read out search type/case
	baseTimer.searchType = element.get("searchType", baseTimer.searchType)
	baseTimer.searchCase = element.get("searchCase", baseTimer.searchCase)

	# Read out if we should change to alternative services
	baseTimer.overrideAlternatives = int(element.get("overrideAlternatives", baseTimer.overrideAlternatives))

	# Read out timespan
	start = element.get("from")
	end = element.get("to")
	if start and end:
		start = [int(x) for x in start.split(':')]
		end = [int(x) for x in end.split(':')]
		baseTimer.timespan = (start, end)

	# Read out max length
	maxduration = element.get("maxduration")
	if maxduration:
		baseTimer.maxduration = int(maxduration)*60

	# Read out recording path
	default = baseTimer.destination or ""
	baseTimer.destination = element.get("location", default).encode("UTF-8") or None

	# Read out offset
	offset = element.get("offset")
	if offset:
		offset = offset.split(",")
		if len(offset) == 1:
			before = after = int(offset[0] or 0) * 60
		else:
			before = int(offset[0] or 0) * 60
			after = int(offset[1] or 0) * 60
		baseTimer.offset = (before, after)

	# Read out counter
	baseTimer.matchCount = int(element.get("counter", 0))
	baseTimer.matchFormatString = element.get("counterFormat", "")
	if not defaults:
		baseTimer.matchLeft = int(element.get("left", baseTimer.matchCount))
		baseTimer.matchLimit = element.get("lastActivation", "")
		baseTimer.lastBegin = int(element.get("lastBegin", 0))

	# Read out justplay
	baseTimer.justplay = int(element.get("justplay", 0))

	# Read out avoidDuplicateDescription
	baseTimer.avoidDuplicateDescription = int(element.get("avoidDuplicateDescription", 0))

	# Read out allowed services
	l = element.findall("serviceref")
	if l:
		servicelist = []

		for service in l:
			value = service.text
			if value:
				myref = eServiceReference(str(value))
				if not (myref.flags & eServiceReference.isGroup):
					# strip all after last :
					pos = value.rfind(':')
					if pos != -1:
						if value[pos-1] == ':':
							pos -= 1
						value = value[:pos+1]

				servicelist.append(value)
		baseTimer.services = servicelist

	# Read out allowed bouquets
	l = element.findall("bouquet")
	if l:
		bouquets = []
		for bouquet in l:
			value = bouquet.text
			if value:
				bouquets.append(value)
		baseTimer.bouquets = bouquets

	# Read out afterevent
	l = element.findall("afterevent")
	if l:
		idx = {
			"none": AFTEREVENT.NONE,
			"deepstandby": AFTEREVENT.DEEPSTANDBY,
			"shutdown": AFTEREVENT.DEEPSTANDBY,
			"standby": AFTEREVENT.STANDBY,
			"auto": AFTEREVENT.AUTO
		}
		afterevents = []
		for afterevent in l:
			value = afterevent.text

			if idx.has_key(value):
				value = idx[value]
			else:
				print '[AutoTimer] Erroneous config contains invalid value for "afterevent":', afterevent,', ignoring definition'
				continue

			start = afterevent.get("from")
			end = afterevent.get("to")
			if start and end:
				start = [int(x) for x in start.split(':')]
				end = [int(x) for x in end.split(':')]
				afterevents.append((value, (start, end)))
			else:
				afterevents.append((value, None))
		baseTimer.afterevent = afterevents

	# Read out exclude
	l = element.findall("exclude")
	idx = {"title": 0, "shortdescription": 1, "description": 2, "dayofweek": 3}
	if l:
		excludes = ([], [], [], [])
		for exclude in l:
			where = exclude.get("where")
			value = exclude.text
			if not (value and where):
				continue

			if idx.has_key(where):
				excludes[idx[where]].append(value.encode("UTF-8"))
		baseTimer.exclude = excludes

	# Read out includes (use same idx)
	l = element.findall("include")
	if l:
		includes = ([], [], [], [])
		for include in l:
			where = include.get("where")
			value = include.text
			if not (value and where):
				continue

			if idx.has_key(where):
				includes[idx[where]].append(value.encode("UTF-8"))
		baseTimer.include = includes

	# Read out recording tags
	l =  element.findall("tag")
	if l:
		tags = []
		for tag in l:
			value = tag.text
			if not value:
				continue

			tags.append(value.encode("UTF-8"))
		baseTimer.tags = tags

	return True

def parseConfigOld(configuration, list, uniqueTimerId = 0):
	print "[AutoTimer] Trying to parse old config"

	# Iterate Timers
	for timer in configuration.findall("timer"):
		# Increment uniqueTimerId
		uniqueTimerId += 1

		# Get name (V2+)
		name = timer.get("name")
		if name:
			name = name.encode("UTF-8")
		# Get name (= match) (V1)
		else:
			# Read out name
			name = getValue(timer.findall("name"), "").encode("UTF-8")

		if not name:
			print '[AutoTimer] Erroneous config is missing attribute "name", skipping entry'
			continue

		# Read out match (V3+)
		match = timer.get("match")
		if match:
			# Read out match
			match = match.encode("UTF-8")
			if not match:
				print '[AutoTimer] Erroneous config contains empty attribute "match", skipping entry'
				continue
		# V2-
		else:
			# Setting match to name
			match = name


		# See if Timer is ensabled (V2+)
		enabled = timer.get("enabled")
		if enabled:
			if enabled == "no":
				enabled = False
			elif enabled == "yes":
				enabled = True
			else:
				print '[AutoTimer] Erroneous config contains invalid value for "enabled":', enabled,', skipping entry'
				enabled = False
		# V1
		else:
			elements = timer.findall("enabled")
			if elements:
				if getValue(elements, "yes") == "no":
					enabled = False
				else:
					enabled = True
			else:
				enabled = True

		# Read out timespan (V4+; Falling back on missing definition should be OK)
		start = timer.get("from")
		end = timer.get("to")
		if start and end:
			start = [int(x) for x in start.split(':')]
			end = [int(x) for x in end.split(':')]
			timetuple = (start, end)
		# V3-
		else:
			elements = timer.findall("timespan")
			Len = len(elements)
			if Len:
				# Read out last definition
				start = elements[Len-1].get("from")
				end = elements[Len-1].get("to")
				if start and end:
					start = [int(x) for x in start.split(':')]
					end = [int(x) for x in end.split(':')]
					timetuple = (start, end)
				else:
					print '[AutoTimer] Erroneous config contains invalid definition of "timespan", ignoring definition'
					timetuple = None
			else:
				timetuple = None

		# Read out allowed services (V*)
		elements = timer.findall("serviceref")
		if elements:
			servicelist = []
			for service in elements:
				value = service.text
				if value:
					myref = eServiceReference(str(value))
					if not (myref.flags & eServiceReference.isGroup):
						# strip all after last :
						pos = value.rfind(':')
						if pos != -1:
							if value[pos-1] == ':':
								pos -= 1
							value = value[:pos+1]

					servicelist.append(value)
		else:
			servicelist = None

		# Read out allowed bouquets (V* though officially supported since V4)
		bouquets = []
		for bouquet in timer.findall("bouquet"):
			value = bouquet.text
			if value:
				bouquets.append(value)

		# Read out offset (V4+)
		offset = timer.get("offset")
		if offset:
			offset = offset.split(",")
			if len(offset) == 1:
				before = after = int(offset[0] or 0) * 60
			else:
				before = int(offset[0] or 0) * 60
				after = int(offset[1] or 0) * 60
			offset = (before, after)
		# V3-
		else:
			elements = timer.findall("offset")
			Len = len(elements)
			if Len:
				value = elements[Len-1].get("both")
				if value == '':
					before = int(elements[Len-1].get("before", 0)) * 60
					after = int(elements[Len-1].get("after", 0)) * 60
				else:
					before = after = int(value) * 60
				offset = (before, after)
			else:
				offset = None

		# Read out counter
		counter = int(timer.get("counter", '0'))
		counterLeft = int(timer.get("left", counter))
		counterLimit = timer.get("lastActivation")
		counterFormat = timer.get("counterFormat", "")
		lastBegin = int(timer.get("lastBegin", 0))

		# Read out justplay
		justplay = int(timer.get("justplay", '0'))

		# Read out avoidDuplicateDescription
		avoidDuplicateDescription = int(timer.get("avoidDuplicateDescription", 0))

		# Read out afterevent (compatible to V* though behaviour for V3- is different as V4+ allows multiple afterevents while the last definication was chosen before)
		idx = {
			"none": AFTEREVENT.NONE,
			"deepstandby": AFTEREVENT.DEEPSTANDBY,
			"shutdown": AFTEREVENT.DEEPSTANDBY,
			"standby": AFTEREVENT.STANDBY,
			"auto": AFTEREVENT.AUTO
		}
		afterevent = []
		for element in timer.findall("afterevent"):
			value = element.text

			if idx.has_key(value):
				value = idx[value]
			else:
				print '[AutoTimer] Erroneous config contains invalid value for "afterevent":', afterevent,', ignoring definition'
				continue

			start = element.get("from")
			end = element.get("to")
			if start and end:
				start = [int(x) for x in start.split(':')]
				end = [int(x) for x in end.split(':')]
				afterevent.append((value, (start, end)))
			else:
				afterevent.append((value, None))

		# Read out exclude (V*)
		idx = {"title": 0, "shortdescription": 1, "description": 2, "dayofweek": 3}
		excludes = ([], [], [], [])
		for exclude in timer.findall("exclude"):
			where = exclude.get("where")
			value = exclude.text
			if not (value and where):
				continue

			if idx.has_key(where):
				excludes[idx[where]].append(value.encode("UTF-8"))

		# Read out includes (use same idx) (V4+ feature, should not harm V3-)
		includes = ([], [], [], [])
		for include in timer.findall("include"):
			where = include.get("where")
			value = include.text
			if not (value and where):
				continue

			if idx.has_key(where):
				includes[idx[where]].append(value.encode("UTF-8"))

		# Read out max length (V4+)
		maxlen = timer.get("maxduration")
		if maxlen:
			maxlen = int(maxlen)*60
		# V3-
		else:
			elements = timer.findall("maxduration")
			if elements:
				maxlen = getValue(elements, None)
				if maxlen is not None:
					maxlen = int(maxlen)*60
			else:
				maxlen = None

		# Read out recording path
		destination = timer.get("destination", "").encode("UTF-8") or None

		# Read out recording tags
		tags = []
		for tag in timer.findall("tag"):
			value = tag.text
			if not value:
				continue

			tags.append(value.encode("UTF-8"))

		# Finally append timer
		list.append(preferredAutoTimerComponent(
				uniqueTimerId,
				name,
				match,
				enabled,
				timespan = timetuple,
				services = servicelist,
				offset = offset,
				afterevent = afterevent,
				exclude = excludes,
				include = includes,
				maxduration = maxlen,
				destination = destination,
				matchCount = counter,
				matchLeft = counterLeft,
				matchLimit = counterLimit,
				matchFormatString = counterFormat,
				lastBegin = lastBegin,
				justplay = justplay,
				avoidDuplicateDescription = avoidDuplicateDescription,
				bouquets = bouquets,
				tags = tags
		))

def buildConfig(defaultTimer, timers, webif = False):
	# Generate List in RAM
	list = ['<?xml version="1.0" ?>\n<autotimer version="', CURRENT_CONFIG_VERSION, '">\n\n']

	# This gets deleted afterwards if we do not have set any defaults
	list.append(' <defaults')
	if webif:
		list.extend((' id="', str(defaultTimer.getId()),'"'))

	# Timespan
	if defaultTimer.hasTimespan():
		list.extend((' from="', defaultTimer.getTimespanBegin(), '" to="', defaultTimer.getTimespanEnd(), '"'))

	# Duration
	if defaultTimer.hasDuration():
		list.extend((' maxduration="', str(defaultTimer.getDuration()), '"'))

	# Destination
	if defaultTimer.hasDestination():
		list.extend((' location="', stringToXML(defaultTimer.destination), '"'))

	# Offset
	if defaultTimer.hasOffset():
		if defaultTimer.isOffsetEqual():
			list.extend((' offset="', str(defaultTimer.getOffsetBegin()), '"'))
		else:
			list.extend((' offset="', str(defaultTimer.getOffsetBegin()), ',', str(defaultTimer.getOffsetEnd()), '"'))

	# Counter
	if defaultTimer.hasCounter():
		list.extend((' counter="', str(defaultTimer.getCounter()), '"'))
		if defaultTimer.hasCounterFormatString():
			list.extend((' counterFormat="', str(defaultTimer.getCounterFormatString()), '"'))

	# Duplicate Description
	if defaultTimer.getAvoidDuplicateDescription():
		list.append(' avoidDuplicateDescription="1" ')

	# Only display justplay if true
	if defaultTimer.justplay:
		list.extend((' justplay="', str(defaultTimer.getJustplay()), '"'))

	# Only display encoding if != utf-8
	if defaultTimer.encoding != 'UTF-8':
		list.extend((' encoding="', str(defaultTimer.encoding), '"'))

	# Only display searchType if exact
	if defaultTimer.searchType == "exact":
		list.extend((' searchType="', str(defaultTimer.searchType), '"'))

	# Only display searchCase if sensitive
	if defaultTimer.searchCase == "sensitive":
		list.extend((' searchCase="', str(defaultTimer.searchCase), '"'))

	# Close still opened defaults tag
	list.append('>\n')

	if webif:
		# Services + Bouquets
		for serviceref in defaultTimer.services + defaultTimer.bouquets:
			ref = ServiceReference(str(serviceref))
			list.extend((
				'  <e2service>\n',
				'   <e2servicereference>', str(serviceref), '</e2servicereference>\n',
				'   <e2servicename>', stringToXML(ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')), '</e2servicename>\n',
				'  </e2service>\n',
			))
	else:
		# Services
		for serviceref in defaultTimer.services:
			ref = ServiceReference(str(serviceref))
			list.extend(('  <serviceref>', serviceref, '</serviceref>',
						' <!-- ', stringToXML(ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')), ' -->\n',
			))

		# Bouquets
		for bouquet in defaultTimer.bouquets:
			ref = ServiceReference(str(bouquet))
			list.extend(('  <bouquet>', str(bouquet), '</bouquet>',
						' <!-- ', stringToXML(ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')), ' -->\n',
			))

	# AfterEvent
	if defaultTimer.hasAfterEvent():
		idx = {
			AFTEREVENT.NONE: "none",
			AFTEREVENT.STANDBY: "standby",
			AFTEREVENT.DEEPSTANDBY: "shutdown",
			AFTEREVENT.AUTO: "auto"
		}
		for afterevent in defaultTimer.afterevent:
			action, timespan = afterevent
			list.append('  <afterevent')
			if timespan[0] is not None:
				list.append(' from="%02d:%02d" to="%02d:%02d"' % (timespan[0][0], timespan[0][1], timespan[1][0], timespan[1][1]))
			list.extend(('>', idx[action], '</afterevent>\n'))

	# Excludes
	for title in defaultTimer.getExcludedTitle():
		list.extend(('  <exclude where="title">', stringToXML(title), '</exclude>\n'))
	for short in defaultTimer.getExcludedShort():
		list.extend(('  <exclude where="shortdescription">', stringToXML(short), '</exclude>\n'))
	for desc in defaultTimer.getExcludedDescription():
		list.extend(('  <exclude where="description">', stringToXML(desc), '</exclude>\n'))
	for day in defaultTimer.getExcludedDays():
		list.extend(('  <exclude where="dayofweek">', stringToXML(day), '</exclude>\n'))

	# Includes
	for title in defaultTimer.getIncludedTitle():
		list.extend(('  <include where="title">', stringToXML(title), '</include>\n'))
	for short in defaultTimer.getIncludedShort():
		list.extend(('  <include where="shortdescription">', stringToXML(short), '</include>\n'))
	for desc in defaultTimer.getIncludedDescription():
		list.extend(('  <include where="description">', stringToXML(desc), '</include>\n'))
	for day in defaultTimer.getIncludedDays():
		list.extend(('  <include where="dayofweek">', stringToXML(day), '</include>\n'))

	# Tags
	if webif and defaultTimer.tags:
		list.extend(('  <e2tags>', stringToXML(' '.join(defaultTimer.tags)), '</e2tags>\n'))
	else:
		for tag in defaultTimer.tags:
			list.extend(('  <tag>', stringToXML(tag), '</tag>\n'))

	# Keep the list clean
	if len(list) == 5:
		list.pop() # >
		list.pop() # <defaults
	else:
		list.append(' </defaults>\n\n')

	# Iterate timers
	for timer in timers:
		# Common attributes (match, enabled)
		list.extend((' <timer name="', stringToXML(timer.name), '" match="', stringToXML(timer.match), '" enabled="', timer.getEnabled(), '"'))
		if webif:
			list.extend((' id="', str(timer.getId()),'"'))

		# Timespan
		if timer.hasTimespan():
			list.extend((' from="', timer.getTimespanBegin(), '" to="', timer.getTimespanEnd(), '"'))

		# Timeframe
		if timer.hasTimeframe():
			list.extend((' after="', str(timer.getTimeframeBegin()), '" before="', str(timer.getTimeframeEnd()), '"'))

		# Duration
		if timer.hasDuration():
			list.extend((' maxduration="', str(timer.getDuration()), '"'))

		# Destination
		if timer.hasDestination():
			list.extend((' location="', stringToXML(timer.destination), '"'))

		# Offset
		if timer.hasOffset():
			if timer.isOffsetEqual():
				list.extend((' offset="', str(timer.getOffsetBegin()), '"'))
			else:
				list.extend((' offset="', str(timer.getOffsetBegin()), ',', str(timer.getOffsetEnd()), '"'))

		# Counter
		if timer.hasCounter():
			list.extend((' lastBegin="', str(timer.getLastBegin()), '" counter="', str(timer.getCounter()), '" left="', str(timer.getCounterLeft()) ,'"'))
			if timer.hasCounterFormatString():
				list.extend((' lastActivation="', str(timer.getCounterLimit()), '"'))
				list.extend((' counterFormat="', str(timer.getCounterFormatString()), '"'))

		# Duplicate Description
		if timer.getAvoidDuplicateDescription():
			list.extend((' avoidDuplicateDescription="', str(timer.getAvoidDuplicateDescription()), '"'))

		# Only display justplay if true
		if timer.justplay:
			list.extend((' justplay="', str(timer.getJustplay()), '"'))

		# Only display encoding if != utf-8
		if timer.encoding != 'UTF-8':
			list.extend((' encoding="', str(timer.encoding), '"'))

		# Only display searchType if exact
		if timer.searchType == "exact":
			list.extend((' searchType="', str(timer.searchType), '"'))

		# Only display searchCase if sensitive
		if timer.searchCase == "sensitive":
			list.extend((' searchCase="', str(timer.searchCase), '"'))

		# Only display overrideAlternatives if true
		if timer.overrideAlternatives:
			list.extend((' overrideAlternatives="', str(timer.getOverrideAlternatives()), '"'))

		# Close still opened timer tag
		list.append('>\n')

		if webif:
			# Services + Bouquets
			for serviceref in timer.services + timer.bouquets:
				ref = ServiceReference(str(serviceref))
				list.extend((
					'  <e2service>\n',
					'   <e2servicereference>', str(serviceref), '</e2servicereference>\n',
					'   <e2servicename>', stringToXML(ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')), '</e2servicename>\n',
					'  </e2service>\n',
				))
		else:
			# Services
			for serviceref in timer.services:
				ref = ServiceReference(str(serviceref))
				list.extend(('  <serviceref>', serviceref, '</serviceref>',
							' <!-- ', stringToXML(ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')), ' -->\n',
				))

			# Bouquets
			for bouquet in timer.bouquets:
				ref = ServiceReference(str(bouquet))
				list.extend(('  <bouquet>', str(bouquet), '</bouquet>',
							' <!-- ', stringToXML(ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')), ' -->\n',
				))

		# AfterEvent
		if timer.hasAfterEvent():
			idx = {
				AFTEREVENT.NONE: "none",
				AFTEREVENT.STANDBY: "standby",
				AFTEREVENT.DEEPSTANDBY: "shutdown",
				AFTEREVENT.AUTO: "auto"
			}
			for afterevent in timer.afterevent:
				action, timespan = afterevent
				list.append('  <afterevent')
				if timespan[0] is not None:
					list.append(' from="%02d:%02d" to="%02d:%02d"' % (timespan[0][0], timespan[0][1], timespan[1][0], timespan[1][1]))
				list.extend(('>', idx[action], '</afterevent>\n'))

		# Excludes
		for title in timer.getExcludedTitle():
			list.extend(('  <exclude where="title">', stringToXML(title), '</exclude>\n'))
		for short in timer.getExcludedShort():
			list.extend(('  <exclude where="shortdescription">', stringToXML(short), '</exclude>\n'))
		for desc in timer.getExcludedDescription():
			list.extend(('  <exclude where="description">', stringToXML(desc), '</exclude>\n'))
		for day in timer.getExcludedDays():
			list.extend(('  <exclude where="dayofweek">', stringToXML(day), '</exclude>\n'))

		# Includes
		for title in timer.getIncludedTitle():
			list.extend(('  <include where="title">', stringToXML(title), '</include>\n'))
		for short in timer.getIncludedShort():
			list.extend(('  <include where="shortdescription">', stringToXML(short), '</include>\n'))
		for desc in timer.getIncludedDescription():
			list.extend(('  <include where="description">', stringToXML(desc), '</include>\n'))
		for day in timer.getIncludedDays():
			list.extend(('  <include where="dayofweek">', stringToXML(day), '</include>\n'))

		# Tags
		if webif and timer.tags:
			list.extend(('  <e2tags>', stringToXML(' '.join(timer.tags)), '</e2tags>\n'))
		else:
			for tag in timer.tags:
				list.extend(('  <tag>', stringToXML(tag), '</tag>\n'))

		# End of Timer
		list.append(' </timer>\n\n')

	# End of Configuration
	list.append('</autotimer>\n')

	return list

