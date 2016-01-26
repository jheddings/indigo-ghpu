#!/usr/bin/env python2.5

import os, httplib, urllib, plistlib
import xml.etree.ElementTree as ET

from ghpu import GitHubPluginUpdater

################################################################################
class Plugin(indigo.PluginBase):

    #---------------------------------------------------------------------------
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get('debug', False)
        self.updater = GitHubPluginUpdater('jheddings', 'indigo-ghpu', self)

    #---------------------------------------------------------------------------
    def __del__(self):
        indigo.PluginBase.__del__(self)

    #---------------------------------------------------------------------------
    def checkForUpdates(self):
        self.updater.checkForUpdate(str(self.pluginVersion))

    #---------------------------------------------------------------------------
    def toggleDebugging(self):
        self.debug = not self.debug
        self.pluginPrefs['debug'] = self.debug

    #---------------------------------------------------------------------------
    def closedPrefsConfigUi(self, values, canceled):
        if (not canceled):
            self.debug = values.get('debug', False)

