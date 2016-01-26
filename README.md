# indigo-ghpu

This is an Indigo plugin updater for plugins released on GitHub.  To help illustrate its
usage, this project also happens to be a plugin, although not a very useful one.

When creating releases for your plugins, you should use the `v{major}.{minor}.{revision}`
format.  This will help ensure compatibility with Indigo's versioning scheme.

## Installation

To install this in your plugin, simply copy the latest version of `ghpu.py` to your plugin
folder.  Check back occasionally to see if updates have been made.

## Usage

In your plugin, initialize the updater with your username and repository name:

    from ghpu import GitHubPluginUpdater
    ...
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        self.updater = GitHubPluginUpdater('jheddings', 'indigo-ghpu', self)

Of course, replace this repository with your own in the example above.  Providing the
`self` reference to the udpater allows it to use the current plugin's logging methods
and access to plugin properties.

Either as a menu option, during `runConcurrentThread`, or by whatever method you choose,
use the following method to check for new versions:

    self.updater.checkForUpdate()

This will instruct the updater to look for updates and notify the error log if any exist.
You may optionally provide the version you want to compare against, like this:

    self.updater.checkForUpdate(str(self.pluginVersion))

This form is required if you do not provide the plugin reference when constructing the
updater.
