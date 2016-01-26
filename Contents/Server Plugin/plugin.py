#!/usr/bin/env python2.5

import os, plistlib

from ghpu import GitHubPluginUpdater

################################################################################
class Plugin(indigo.PluginBase):

    #---------------------------------------------------------------------------
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get('debug', False)
        self.pluginPath = self.getPluginPath()
        self.updater = GitHubPluginUpdater('jheddings', 'indigo-ghpu', self)

    #---------------------------------------------------------------------------
    def __del__(self):
        indigo.PluginBase.__del__(self)

    #---------------------------------------------------------------------------
    def getPluginPath(self):
        self.debugLog('Looking for plugin installation: %s' % self.pluginId)

        # assume the plugin is installed under the standard installation folder...
        path = os.path.join(indigo.server.getInstallFolderPath(), 'Plugins', self.pluginDisplayName + '.indigoPlugin')
        self.debugLog('Calculated plugin path: %s' % path)

        plistFile = os.path.join(path, 'Contents', 'Info.plist')
        self.debugLog('Plugin info file: %s' % plistFile)

        if (not os.path.isfile(plistFile)):
            self.errorLog('File not found: %s' % plistFile)
            return None

        try:
            # make sure the plugin is the by reading the info file
            plist = plistlib.readPlist(plistFile)
            pluginId = plist.get('CFBundleIdentifier', None)
            self.debugLog('Found plugin: %s' % pluginId)

            if (self.pluginId == pluginId):
                self.debugLog('Verified plugin path: %s' % path)
            else:
                self.errorLog('Incorrect plugin ID in path: %s found, %s expected' % ( pluginId, self.pluginId ))
                path = None

        except Exception as e:
            self.errorLog('Error reading Info.plist: %s' % str(e))
            path = None

        return path

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

