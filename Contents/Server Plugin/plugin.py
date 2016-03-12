#!/usr/bin/env python2.5

import os

from ghpu import GitHubPluginUpdater

################################################################################
class Plugin(indigo.PluginBase):

    #---------------------------------------------------------------------------
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get('debug', False)
        self.updater = GitHubPluginUpdater(self)

    #---------------------------------------------------------------------------
    def __del__(self):
        indigo.PluginBase.__del__(self)

    #---------------------------------------------------------------------------
    def selfInstall(self):
        self.updater.install()

    #---------------------------------------------------------------------------
    def forceUpdate(self):
        self.updater.update(currentVersion='0.0.0')

    #---------------------------------------------------------------------------
    def updatePlugin(self):
        self.updater.update()

    #---------------------------------------------------------------------------
    def checkForUpdates(self):
        self.updater.checkForUpdate()

    #---------------------------------------------------------------------------
    def checkRateLimit(self):
        limiter = self.updater.getRateLimit()
        indigo.server.log('RateLimit {limit:%d remaining:%d resetAt:%d}' % limiter)

    #---------------------------------------------------------------------------
    def testUpdateCheck(self):
        indigo.server.log('-- BEGIN testUpdateCheck --')

        self.updater.checkForUpdate()
        self.updater.checkForUpdate('0.0.0')

        emptyUpdater = GitHubPluginUpdater('jheddings', 'indigo-ghpu')
        emptyUpdater.checkForUpdate()
        emptyUpdater.checkForUpdate('0.0.0')
        emptyUpdater.checkForUpdate(str(self.pluginVersion))

        indigo.server.log('-- END testUpdateCheck --')

    #---------------------------------------------------------------------------
    def toggleDebugging(self):
        self.debug = not self.debug
        self.pluginPrefs['debug'] = self.debug

    #---------------------------------------------------------------------------
    def closedPrefsConfigUi(self, values, canceled):
        if (not canceled):
            self.debug = values.get('debug', False)

    #---------------------------------------------------------------------------
    def runConcurrentThread(self):
        while True:
            # this checks for any updates on a regular interval
            self.updater.checkForUpdate()

            # we are checking every 300 seconds (5 minutes) here as an example
            # in practice, this should not be less than 3600 seconds (1 hour)
            self.sleep(300)

