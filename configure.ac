AC_INIT([enigma2-plugins],[3.0.0],[enigma2-devel@lists.elitedvb.net])
AM_INIT_AUTOMAKE([dist-bzip2 foreign no-define tar-pax])
AC_CONFIG_HEADERS([enigma2-plugins-config.h])

# Silent rules are available since 1.11, but older versions
# are still in use. So don't use them unconditionally.
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

AC_USE_SYSTEM_EXTENSIONS
AC_SYS_LARGEFILE

AC_PROG_CC
AC_PROG_CXX
m4_ifdef([LT_INIT], [LT_INIT], [AC_PROG_LIBTOOL])
AC_CONFIG_MACRO_DIR([m4])

AC_PATH_PROG(MSGFMT, msgfmt, AC_MSG_ERROR(Could not find msgfmt))

AM_PATH_PYTHON
AX_PYTHON_DEVEL
AX_PTHREAD

TUXBOX_APPS_DVB

PKG_CHECK_MODULES(ENIGMA2, enigma2)
PKG_CHECK_MODULES(GSTREAMER, gstreamer-0.10 gstreamer-pbutils-0.10)
PKG_CHECK_MODULES(LIBCRYPTO, libcrypto)

AC_ARG_WITH(debug,
	AS_HELP_STRING([--without-debug],[disable debugging code]),
	[with_debug="$withval"],[with_debug="yes"])
if test "$with_debug" = "yes"; then
	DEBUG_CFLAGS="-ggdb3"
	AC_DEFINE([DEBUG],[1],[Define to 1 to enable debugging code])
fi

AC_ARG_WITH(po,
	AS_HELP_STRING([--with-po],[enable updating of po files]),
	[with_po="$withval"],[with_po="no"])
if test "$with_po" = "yes"; then
	AC_PATH_PROG(MSGINIT, msginit)
	AC_PATH_PROG(MSGMERGE, msgmerge)
	AC_PATH_PROG(MSGUNIQ, msguniq)
	AC_PATH_PROG(XGETTEXT, xgettext)
	if test -z "$MSGINIT" -o -z "$MSGMERGE" -o -z "$MSGUNIQ" -o -z "$XGETTEXT"; then
		AC_MSG_ERROR([Could not find required gettext tools])
	fi
fi
AM_CONDITIONAL(UPDATE_PO, test "$with_po" = "yes")

CPPFLAGS="$CPPFLAGS $PYTHON_CPPFLAGS -include Python.h -include enigma2-plugins-config.h"
CFLAGS="$CFLAGS $DEBUG_CFLAGS -Wall"
CXXFLAGS="$CXXFLAGS $DEBUG_CFLAGS -Wall $ENIGMA2_CFLAGS $PTHREAD_CFLAGS"

AC_CONFIG_FILES([
Makefile

aihdcontroler/Makefile
aihdcontroler/meta/Makefile
aihdcontroler/src/Makefile
aihdcontroler/src/comp/Makefile
aihdcontroler/src/data/Makefile

antiscrollbar/Makefile
antiscrollbar/meta/Makefile
antiscrollbar/src/Makefile

audiosync/Makefile
audiosync/img/Makefile
audiosync/meta/Makefile
audiosync/po/Makefile
audiosync/src/Makefile

automatictimerlistcleanup/Makefile
automatictimerlistcleanup/meta/Makefile
automatictimerlistcleanup/po/Makefile
automatictimerlistcleanup/src/Makefile

automaticvolumeadjustment/Makefile
automaticvolumeadjustment/meta/Makefile
automaticvolumeadjustment/src/Makefile

autoresolution/Makefile
autoresolution/meta/Makefile
autoresolution/src/Makefile

autotimer/Makefile
autotimer/meta/Makefile
autotimer/po/Makefile
autotimer/src/Makefile
autotimer/src/webinterface/Makefile

babelzapper/Makefile
babelzapper/etc/Makefile
babelzapper/meta/Makefile
babelzapper/src/Makefile

bitrateviewer/Makefile
bitrateviewer/meta/Makefile
bitrateviewer/src/Makefile
bitrateviewer/src/bitratecalc/Makefile

bonjour/Makefile
bonjour/meta/Makefile
bonjour/src/Makefile

cdinfo/Makefile
cdinfo/meta/Makefile
cdinfo/src/Makefile

dreamirc/Makefile
dreamirc/meta/Makefile
dreamirc/src/Makefile
dreamirc/src/protocols/Makefile

dreammediathek/Makefile
dreammediathek/src/Makefile

dvdbackup/Makefile
dvdbackup/meta/Makefile
dvdbackup/po/Makefile
dvdbackup/src/Makefile

dyndns/Makefile
dyndns/src/Makefile
dyndns/meta/Makefile

easyinfo/Makefile
easyinfo/meta/Makefile
easyinfo/src/Makefile

easymedia/Makefile
easymedia/meta/Makefile
easymedia/po/Makefile
easymedia/src/Makefile

eibox/Makefile
eibox/meta/Makefile
eibox/po/Makefile
eibox/src/Makefile
eibox/src/images/Makefile

elektro/Makefile
elektro/meta/Makefile
elektro/po/Makefile
elektro/src/Makefile

emailclient/Makefile
emailclient/meta/Makefile
emailclient/po/Makefile
emailclient/src/Makefile

epgrefresh/Makefile
epgrefresh/meta/Makefile
epgrefresh/po/Makefile
epgrefresh/src/Makefile
epgrefresh/src/webinterface/Makefile

epgsearch/Makefile
epgsearch/meta/Makefile
epgsearch/po/Makefile
epgsearch/src/Makefile

fancontrol2/Makefile
fancontrol2/meta/Makefile
fancontrol2/po/Makefile
fancontrol2/src/Makefile
fancontrol2/src/data/Makefile

filebrowser/Makefile
filebrowser/meta/Makefile
filebrowser/src/Makefile

fritzcall/Makefile
fritzcall/meta/Makefile
fritzcall/po/Makefile
fritzcall/src/Makefile
fritzcall/src/images/Makefile

ftpbrowser/Makefile
ftpbrowser/meta/Makefile
ftpbrowser/po/Makefile
ftpbrowser/src/Makefile
ftpbrowser/src/images/Makefile

genuinedreambox/Makefile
genuinedreambox/meta/Makefile
genuinedreambox/src/Makefile

googlemaps/Makefile
googlemaps/meta/Makefile
googlemaps/src/Makefile

growlee/Makefile
growlee/meta/Makefile
growlee/src/Makefile

httpproxy/Makefile
httpproxy/meta/Makefile
httpproxy/src/Makefile

imdb/Makefile
imdb/meta/Makefile
imdb/po/Makefile
imdb/src/Makefile

kiddytimer/Makefile
kiddytimer/img/Makefile
kiddytimer/meta/Makefile
kiddytimer/po/Makefile
kiddytimer/src/Makefile

lastfm/Makefile
lastfm/meta/Makefile
lastfm/src/Makefile

letterbox/Makefile
letterbox/src/Makefile
letterbox/meta/Makefile

logomanager/Makefile
logomanager/logodir_hdd/Makefile
logomanager/meta/Makefile
logomanager/src/Makefile

mediadownloader/Makefile
mediadownloader/meta/Makefile
mediadownloader/po/Makefile
mediadownloader/src/Makefile

merlinepg/Makefile
merlinepg/meta/Makefile
merlinepg/src/Makefile

merlinmusicplayer/Makefile
merlinmusicplayer/meta/Makefile
merlinmusicplayer/src/Makefile
merlinmusicplayer/src/images/Makefile
merlinmusicplayer/src/merlinmp3player/Makefile

meteoitalia/Makefile
meteoitalia/meta/Makefile
meteoitalia/src/Makefile

mosaic/Makefile
mosaic/meta/Makefile
mosaic/po/Makefile
mosaic/src/Makefile

moviecut/Makefile
moviecut/meta/Makefile
moviecut/src_cc/Makefile
moviecut/src_py/Makefile

movielistpreview/Makefile
movielistpreview/meta/Makefile
movielistpreview/po/Makefile
movielistpreview/src/Makefile

movieretitle/Makefile
movieretitle/meta/Makefile
movieretitle/po/Makefile
movieretitle/src/Makefile

movieselectionquickbutton/Makefile
movieselectionquickbutton/meta/Makefile
movieselectionquickbutton/po/Makefile
movieselectionquickbutton/src/Makefile

movietagger/Makefile
movietagger/etc/Makefile
movietagger/meta/Makefile
movietagger/src/Makefile

multirc/Makefile
multirc/src/Makefile
multirc/meta/Makefile

mytube/Makefile
mytube/meta/Makefile
mytube/src/Makefile

netcaster/Makefile
netcaster/meta/Makefile
netcaster/src/Makefile
netcaster/src/bin/Makefile
netcaster/src/bin/interface/Makefile
netcaster/src/etc/Makefile

networkbrowser/Makefile
networkbrowser/meta/Makefile
networkbrowser/src/Makefile
networkbrowser/src/icons/Makefile
networkbrowser/src/lib/Makefile

ncidclient/Makefile
ncidclient/meta/Makefile
ncidclient/po/Makefile
ncidclient/src/Makefile

ofdb/Makefile
ofdb/meta/Makefile
ofdb/po/Makefile
ofdb/src/Makefile

orfat/Makefile
orfat/meta/Makefile
orfat/src/Makefile

orfteletext/Makefile
orfteletext/meta/Makefile
orfteletext/src/Makefile

partnerbox/Makefile
partnerbox/meta/Makefile
partnerbox/po/Makefile
partnerbox/src/Makefile
partnerbox/src/icons/Makefile
partnerbox/src/servicewebts/Makefile

passwordchanger/Makefile
passwordchanger/meta/Makefile
passwordchanger/po/Makefile
passwordchanger/src/Makefile

permanentclock/Makefile
permanentclock/meta/Makefile
permanentclock/po/Makefile
permanentclock/src/Makefile

podcast/Makefile
podcast/etc/Makefile
podcast/meta/Makefile
podcast/po/Makefile
podcast/src/Makefile

porncenter/Makefile
porncenter/meta/Makefile
porncenter/po/Makefile
porncenter/src/Makefile
porncenter/src/Additions/Makefile

quickbutton/Makefile
quickbutton/meta/Makefile
quickbutton/po/Makefile
quickbutton/src/Makefile

reconstructapsc/Makefile
reconstructapsc/meta/Makefile
reconstructapsc/src_cc/Makefile
reconstructapsc/src_py/Makefile

remotetimer/Makefile
remotetimer/meta/Makefile
remotetimer/src/Makefile

rsdownloader/Makefile
rsdownloader/meta/Makefile
rsdownloader/po/Makefile
rsdownloader/src/Makefile
rsdownloader/src/container/Makefile

seekbar/Makefile
seekbar/meta/Makefile
seekbar/po/Makefile
seekbar/src/Makefile

serienfilm/Makefile
serienfilm/meta/Makefile
serienfilm/po/Makefile
serienfilm/src/Makefile
serienfilm/src/icons/Makefile

setpasswd/Makefile
setpasswd/meta/Makefile
setpasswd/po/Makefile
setpasswd/src/Makefile

shoutcast/Makefile
shoutcast/meta/Makefile
shoutcast/po/Makefile
shoutcast/src/Makefile

simplerss/Makefile
simplerss/meta/Makefile
simplerss/po/Makefile
simplerss/src/Makefile

startupservice/Makefile
startupservice/meta/Makefile
startupservice/po/Makefile
startupservice/src/Makefile

startuptostandby/Makefile
startuptostandby/meta/Makefile
startuptostandby/src/Makefile

svdrp/Makefile
svdrp/meta/Makefile
svdrp/src/Makefile

tageditor/Makefile
tageditor/meta/Makefile
tageditor/po/Makefile
tageditor/src/Makefile

trafficinfo/Makefile
trafficinfo/meta/Makefile
trafficinfo/src/Makefile

tvcharts/Makefile
tvcharts/meta/Makefile
tvcharts/src/Makefile

unwetterinfo/Makefile
unwetterinfo/meta/Makefile
unwetterinfo/src/Makefile

valixdcontrol/Makefile
valixdcontrol/meta/Makefile
valixdcontrol/src/Makefile
valixdcontrol/src/comp/Makefile
valixdcontrol/src/data/Makefile

virtualzap/Makefile
virtualzap/meta/Makefile
virtualzap/po/Makefile
virtualzap/src/Makefile

vlcplayer/Makefile
vlcplayer/meta/Makefile
vlcplayer/po/Makefile
vlcplayer/src/Makefile
vlcplayer/src/servicets/Makefile

weatherplugin/Makefile
weatherplugin/meta/Makefile
weatherplugin/po/Makefile
weatherplugin/src/Makefile

webcamviewer/Makefile
webcamviewer/meta/Makefile
webcamviewer/src/Makefile

webbouqueteditor/Makefile
webbouqueteditor/src/Makefile
webbouqueteditor/meta/Makefile
webbouqueteditor/src/web/Makefile
webbouqueteditor/src/web-data/Makefile
webbouqueteditor/src/WebChilds/Makefile
webbouqueteditor/src/WebComponents/Makefile
webbouqueteditor/src/WebComponents/Sources/Makefile
webbouqueteditor/src/WebScreens/Makefile

webinterface/Makefile
webinterface/meta/Makefile
webinterface/po/Makefile
webinterface/src/Makefile
webinterface/src/etc/Makefile
webinterface/src/mobile/Makefile
webinterface/src/web/Makefile
webinterface/src/web-data/Makefile
webinterface/src/web-data/gfx/Makefile
webinterface/src/web-data/img/Makefile
webinterface/src/web-data/lib/Makefile
webinterface/src/web-data/tpl/Makefile
webinterface/src/web-data/tpl/default/Makefile
webinterface/src/web-data/tpl/default/streaminterface/Makefile
webinterface/src/web-data/tpl/default/streaminterface/img/Makefile
webinterface/src/WebChilds/Makefile
webinterface/src/WebChilds/External/Makefile
webinterface/src/WebComponents/Makefile
webinterface/src/WebComponents/Converter/Makefile
webinterface/src/WebComponents/Sources/Makefile

werbezapper/Makefile
werbezapper/meta/Makefile
werbezapper/po/Makefile
werbezapper/src/Makefile

youtubeplayer/Makefile
youtubeplayer/meta/Makefile
youtubeplayer/src/Makefile
youtubeplayer/src/Nemesis.GlassLine_Mod/Makefile

zaphistorybrowser/Makefile
zaphistorybrowser/meta/Makefile
zaphistorybrowser/po/Makefile
zaphistorybrowser/src/Makefile

zapstatistic/Makefile
zapstatistic/meta/Makefile
zapstatistic/po/Makefile
zapstatistic/src/Makefile

zdfmediathek/Makefile
zdfmediathek/meta/Makefile
zdfmediathek/src/Makefile

])
AC_OUTPUT
