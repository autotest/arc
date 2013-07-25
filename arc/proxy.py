import json


URLLIB_FROM_PY3K = False
try:
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.request import Request, urlopen
    URLLIB_FROM_PY3K = True


__all__ = ['DecodeError', 'RPCError', 'Proxy', 'Method']


class DecodeError(Exception):
    """
    Error raised when data can not be decoded into proper JSON
    """
    pass


class RPCError(Exception):
    """
    Error raised when JSON RPC call has errors
    """
    pass


class Proxy(object):
    """
    Service proxy to a JSON RPC Server
    """
    def __init__(self, uri):
        """
        Initializes a new proxy

        :param uri: the complete URI for the JSON RPC Server
        :type uri: str
        """
        self.uri = uri


    def __getattr__(self, name):
        """
        Returns the a method that will eventually be called by the client

        :param name: the name of the method
        :type name: str
        :returns: a method wrapper instance
        :rtype: :class:`Method`
        """
        return Method(self.uri, name)


class Method(object):
    """
    Class that wrapps an RPC Server Method
    """
    def __init__(self, uri, name):
        """
        Initializes a new method

        :param uri: the complete URI for the JSON RPC Server
        :type uri: str
        :param name: the name of the method
        :type name: str
        """
        self.uri = uri
        self.name = name


    @staticmethod
    def encode(data):
        """
        Encodes the data into bytes if necessary

        :param data: the data that will optionally be encoded as bytes
        :type data: str
        :returns: either data encoded as bytes or the original str
        :rtype: bytes or str
        """
        if URLLIB_FROM_PY3K:
            try:
                data = bytes(data, 'utf-8')
            except:
                data = data

        return data


    @staticmethod
    def decode(data):
        """
        Decodes into string if it's a byte array

        :param data: data to be decoded
        :type data: str or bytes
        :returns: the decode str
        :rtype: str
        """
        if type(data) == bytes:
            data = data.decode()
        return data


    def __call__(self, *args, **kwargs):
        post = json.dumps({"method": self.name,
                           'params': args + (kwargs,),
                           'id': 'jsonrpc'})

        # Send the request
        post = self.encode(post)
        request = Request(self.uri, data=post)

        # Receive the response
        response = urlopen(request).read()
        response = self.decode(response)

        try:
            response = json.loads(response)
        except ValueError:
            raise DecodeError('Error decoding JSON reponse: %s',
                              response)

        if response['error'] is not None:
            error = response['error']
            error_message = ("%s: %s\n%s" % (error['name'],
                                             error['message'],
                                             error['traceback']))
            raise RPCError(error_message)
        else:
            return response['result']
