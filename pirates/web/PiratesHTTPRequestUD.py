from direct.directnotify import DirectNotifyGlobal

import traceback

class PiratesHTTPRequestUD(object):
    """
    Represents an HTTP request in queue
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesHTTPRequestUD')

    def __init__(self, rest, request_id, channel, ram_file, callback=None):
        self._rest = rest
        self._request_id = request_id
        self._channel = channel
        self._callback = callback
        self._ram_file = ram_file
    
    @property
    def requestId(self):
        return self._request_id

    @property
    def channel(self):
        return self._channel

    @property
    def ramFile(self):
        return self._ram_file

    def update(self):
        """
        Performs the run operations and finishing callbacks
        for the request's channel instance
        """

        if self._channel == None:
            return

        done = not self._channel.run()
        if done:
            self.notify.debug('Completed request: %s' % self._request_id)
            
            if self._callback != None:
                try:
                    self._callback(self._ram_file.get_data())
                except:
                    self.notify.warning('Exception occured processing callback')
                    self.notify.warning(traceback.format_exc())

            self._rest.removeRequest(self._request_id)