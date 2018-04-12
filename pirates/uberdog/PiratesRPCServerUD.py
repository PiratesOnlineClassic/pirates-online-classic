from rpyc import Service
from rpyc.utils.server import ThreadedServer
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.stdpy import threading

activeConnections = set()

class PiratesService(Service):
    notify = directNotify.newCategory('PiratesService')
    notify.setInfo(True)

    def __init__(self, conn, air):
        self._air = air
        Service.__init__(self, conn)

    @property
    def air(self):
        return self._air

    def on_connect(self):
        self.token = None

    def on_disconnect(self):
        if self.token:
            self.exposed_disconnect()

    def exposed_authenticate(self, token):
        client_ip = self._conn._config['endpoints'][1]
        if self.token:
            raise ValueError('Connection already authenticated')
        elif self.__verifyToken(token):
            self.token = token

            self.notify.info('Received new RPC connection from %s:%s' % client_ip)
            self.air.writeServerEvent('rpc-connection',
                message='Success!',
                client_ip=client_ip[0])
        else:
            self.notify.warning('Received an invalid rpc token from %s:%s!' % client_ip)
            self.air.writeServerEvent('rpc-connection',
                message='Invalid authentication token',
                client_ip=client_ip[0])
            raise ValueError('Invalid authentication token')

    def __verifyToken(self, token):
        return token == 'test_token' #TODO

    def __verifyConnection(self):
        if self.token is None:
            raise Exception('Connection has not been authenticated')

    def exposed_disconnect(self):
        self._callback = None
        activeConnections.discard(self)

        # Log RPC activity
        self.air.writeServerEvent('rpc-disconnect',
            client_ip=self._conn._config['endpoints'][1][0])

    def exposed_ping(self, incoming):
        """
        Summary:
            Responds with the [data] that was sent. This method exists only for
            testing purposes.
        Parameters:
            [any data] = The data to be given back in response.
        Example response: 'pong'
        """
        self.__verifyConnection()

        return incoming

    def exposed_systemMessage(self, message, channel=10):
        """
        Summary:
            Broadcasts a [message] to any client whose Client Agent
            is subscribed to the provided [channel]. Channel 10
            is a global broadcast
        Parameters:
            [int channel] = The channel to direct the message to.
            [str message] = The message to broadcast.
        """
        self.__verifyConnection()

        self.air.systemMessage(message, channel)
        return True

    def kickChannel(self, channel, reason=1, message=''):
        """
        Summary:
            Kicks any users whose CAs are subscribed to a particular [channel] with a [code].
        Parameters:
            [int channel] = The channel to direct the message to.
            [int code] = An optional code to kick.
            [string reason] = An optional reason.
        """

        try:
            self.air.kickChannel(channel, reason, message)
        except Exception as e:
            raise Exception('Failed to kick channel, An unexpected error occured: %s' % repr(e))

        return True

class PiratesRPCFactory:
    notify = directNotify.newCategory('PiratesRPCFactory')

    def __init__(self, air):
        self._air = air

    def get_service_name(self):
        return 'PiratesService'

    def get_service_aliases(self):
        return ('PIRATES',)

    def __call__(self, conn):
        return PiratesService(conn, self._air)

class PiratesRPCServerUD:
    notify = directNotify.newCategory('PiratesRPCServerUD')
    notify.setInfo(True)
    
    def __init__(self, air):
        self._server = None
        self._air = air

    @property
    def server(self):
        return self._server

    @property
    def air(self):
        return self._air

    def start(self):
        port = config.GetInt('rpc-server-port', 19912)
        self._server = ThreadedServer(PiratesRPCFactory(self._air), port=port)

        self.notify.info('Starting RPC server on port %d' % port)
        t = threading.Thread(target=self._server.start)
        t.daemon = True
        t.start()