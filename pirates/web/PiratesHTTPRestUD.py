from panda3d.core import HTTPClient, HTTPChannel, DocumentSpec
from panda3d.core import Ramfile, UniqueIdAllocator, ConfigVariableInt

from direct.directnotify import DirectNotifyGlobal

from pirates.web.PiratesHTTPRequestUD import PiratesHTTPRequestUD

import json

class PiratesHTTPRestUD(object):
    """
    Primary class for handling GET/POST requests with Panda's HTTPClient object
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesHTTPRestUD')
    notify.setInfo(True)

    def __init__(self, air):
        self._air = air
        self._http_client = HTTPClient()

        max_http_requests = ConfigVariableInt('http-max-requests', 900).value
        self._request_allocator = UniqueIdAllocator(0, max_http_requests)
        self._requests = {}
        self.notify.info('%s going online' % self.__class__.__name__)
        taskMgr.add(self.updateTask, 'http-rest-update-task')

    def updateTask(self, task):
        """
        Performs update operations on the PandaHTTP instance
        """

        for request_id in list(self._requests):

            # Check that this id is still valid
            if request_id not in self._requests:
                continue

            request = self._requests[request_id]
            request.update()

        return task.again

    def destroy(self):
        """
        Performs destruction operations on the PandaHTTP instance
        """
    
        for request_id in list(self._requests):
            self.removeRequest(request_id)

    def removeRequest(self, request_id):
        """
        Removes the request id form the PandaHTTP request list
        """
        
        if request_id not in self._requests:
            return

        self._request_allocator.free(request_id)
        del self._requests[request_id]

    def getRequestStatus(self, request_id):
        """
        Returns the requests current status
        """

        return not request_id in self._requests

    def getRequest(self, request_id):
        """
        Returns the requested request if its present
        """

        return self._requests.get(request_id, None)

    def performGetRequest(self, url, headers={}, content_type=None, callback=None):
        """
        Performs an HTTP restful GET call and returns the request's unique itentifier
        """

        self.notify.debug('Sending GET request: %s' % url)

        request_channel = self._http_client.make_channel(True)

        if content_type != None:
            request_channel.set_content_type(content_type)

        for header_key in headers:
            header_value = headers[header_key]
            request_channel.send_extra_header(header_key, header_value)

        request_channel.begin_get_document(DocumentSpec(url))

        ram_file = Ramfile()
        request_channel.download_to_ram(ram_file, False)

        request_id = self._request_allocator.allocate()
        http_request = PiratesHTTPRequestUD(self, request_id, request_channel, ram_file, callback)
        self._requests[request_id] = http_request

        return request_id

    def performJsonGetRequest(self, url, headers={}, callback=None):
        """
        """

        def json_wrapper(data):
            """
            Wraps the callback to automatically perform json.load
            on the resulting data
            """

            try:
                data = json.loads(data)
            except:
                self.notify.warning('Received invalid JSON results: %s' % data)
                
            callback(data)

        return self.performGetRequest(
            url=url, 
            content_type='application/json',
            headers=headers,
            callback=json_wrapper)

    def performPostRequest(self, url, headers={}, content_type=None, post_body={}, callback=None):
        """
        """

        self.notify.debug('Sending POST request: %s' % url)

        request_channel = self._http_client.make_channel(True)

        if content_type != None:
            request_channel.set_content_type(content_type)

        for header_key in headers:
            header_value = headers[header_key]
            request_channel.send_extra_header(header_key, header_value)

        post_body = json.dumps(post_body)
        request_channel.begin_post_form(DocumentSpec(url), post_body)

        ram_file = Ramfile()
        request_channel.download_to_ram(ram_file, False)

        request_id = self._request_allocator.allocate()
        http_request = PiratesHTTPRequestUD(self, request_id, request_channel, ram_file, callback)
        self._requests[request_id] = http_request

        return request_id

    def performJsonPostRequest(self, url, headers={}, post_body={}, callback=None):
        """
        """

        def json_wrapper(data):
            """
            Wraps the callback to automatically perform json.load
            on the resulting data
            """

            try:
                data = json.loads(data)
            except:
                self.notify.warning('Received invalid JSON results: %s' % data)

            callback(data)

        return self.performPostRequest(
            url=url, 
            content_type='application/json',
            headers=headers,
            post_body=post_body, 
            callback=json_wrapper)