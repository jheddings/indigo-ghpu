#!/usr/bin/env python2.5

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# for the latest version and documentation, visit https://github.com/jheddings/indigo-ghpu

import json
import httplib
import indigo

################################################################################
class GitHubPluginUpdater(object):

    #---------------------------------------------------------------------------
    def __init__(self, owner, repo, plugin=None):
        self.owner = owner
        self.repo = repo
        self.plugin = plugin

    #---------------------------------------------------------------------------
    # returns the URL for an update if there is one
    def checkForUpdate(self, currentVersion=None):
        self._log('Checking for updates...')

        currentVersion = self._resolveCurrentVersion(currentVersion)
        if (currentVersion == None): return False

        update = self.getUpdate(currentVersion)

        if (update == None):
            self._log('No updates are available')
            return False

        self._error('A new version is available: %s' % update['html_url'])

        return True

    #---------------------------------------------------------------------------
    # returns the update package, if there is one
    def getUpdate(self, currentVersion):
        self._debug('Current version is: %s' % currentVersion)

        update = self.getLatestRelease()

        if (update == None):
            self._debug('No release available')
            return None

        # assume the tag is the release version
        latestVersion = update['tag_name'].lstrip('v')
        self._debug('Latest release is: %s' % latestVersion)

        if (ver(currentVersion) >= ver(latestVersion)):
            return None

        return update

    #---------------------------------------------------------------------------
    # returns the latest release information from a given user / repo
    # https://developer.github.com/v3/repos/releases/
    def getLatestRelease(self):
        return self._GET('/repos/' + self.owner + '/' + self.repo + '/releases/latest')

    #---------------------------------------------------------------------------
    # returns a tuple for the current rate limit: (limit, remaining, resetTime)
    # https://developer.github.com/v3/rate_limit/
    # NOTE this does not count against the current limit
    def getRateLimit(self):
        limiter = self._GET('/rate_limit')

        remain = int(limiter['rate']['remaining'])
        limit = int(limiter['rate']['limit'])
        resetAt = int(limiter['rate']['reset'])

        return (limit, remain, resetAt)

    #---------------------------------------------------------------------------
    # should really only be used for testing and development...
    def testBadRequest(self): self._GET('/undefined')

    #---------------------------------------------------------------------------
    # form a GET request to api.github.com and return the parsed JSON response
    def _GET(self, requestPath):
        self._debug('GET %s' % requestPath)

        headers = {
            'User-Agent': 'Indigo-Plugin-Updater',
            'Accept': 'application/vnd.github.v3+json'
        }

        data = None

        try:
            conn = httplib.HTTPSConnection('api.github.com')
            conn.request('GET', requestPath, None, headers)

            resp = conn.getresponse()
            self._debug('HTTP %d %s' % (resp.status, resp.reason))

            if (resp.status == 200):
                data = json.loads(resp.read())
            elif (400 <= resp.status < 500):
                error = json.loads(resp.read())
                self._error('Client Error: %s' % error['message'])
            else:
                self._error('Unhandled Error: %s' % resp.reason)

        except Exception as e:
            self._error('Unhandled Exception: %s' % str(e))
            return None

        return data

    #---------------------------------------------------------------------------
    # verifies and returns the current version based on user-supplied args
    def _resolveCurrentVersion(self, currentVersion):
        if ((currentVersion == None) and (self.plugin == None)):
            self._error('Must provide either currentVersion or plugin reference')
            return None
        elif (currentVersion == None):
            currentVersion = str(self.plugin.pluginVersion)
            self._debug('Plugin version detected: %s' % currentVersion)
        else:
            self._debug('Plugin version provided: %s' % currentVersion)

        return currentVersion

    #---------------------------------------------------------------------------
    # convenience method for log messages
    def _log(self, msg):
        indigo.server.log(msg)

    #---------------------------------------------------------------------------
    # convenience method for debug messages
    def _debug(self, msg):
        if self.plugin:
            self.plugin.debugLog(msg)

    #---------------------------------------------------------------------------
    # convenience method for error messages
    def _error(self, msg):
        if self.plugin:
            self.plugin.errorLog(msg)

################################################################################
# maps the standard version string as a tuple for comparrison
def ver(vstr): return tuple(map(int, (vstr.split('.'))))
