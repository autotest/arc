"""
  Copyright (c) 2007 Jan-Klaas Kollhof

  This file is part of jsonrpc.

  jsonrpc is free software; you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation; either version 2.1 of the License, or
  (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this software; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import json

URLLIB_FROM_PY3K = False
try:
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.request import Request, urlopen
    URLLIB_FROM_PY3K = True


__all__ = ['JSONRPCException',
           'ServiceProxy']


class JSONRPCException(Exception):
    """
    Error raised when data received from JSON RPC call is not valid
    """
    pass


class ServiceProxy(object):
    """
    Proxy to a given JSON RPC Server
    """
    def __init__(self, serviceURL, serviceName=None, headers=None):
        self.__serviceURL = serviceURL
        self.__serviceName = serviceName
        self.__headers = headers or {}


    def __getattr__(self, name):
        if self.__serviceName is not None:
            name = "%s.%s" % (self.__serviceName, name)
        return ServiceProxy(self.__serviceURL, name, self.__headers)


    def __call__(self, *args, **kwargs):
        postdata = json.dumps({"method": self.__serviceName,
                               'params': args + (kwargs,),
                               'id': 'jsonrpc'})
        if URLLIB_FROM_PY3K:
            try:
                postdata = bytes(postdata, 'utf-8')
            except:
                pass
        request = Request(self.__serviceURL, data=postdata,
                          headers=self.__headers)
        respdata = urlopen(request).read()
        if type(respdata) == bytes:
            respdata = respdata.decode()
        try:
            resp = json.loads(respdata)
        except ValueError:
            raise JSONRPCException('Error decoding JSON reponse:\n' + respdata)
        if resp['error'] is not None:
            error_message = (resp['error']['name'] + ': ' +
                             resp['error']['message'] + '\n' +
                             resp['error']['traceback'])
            raise JSONRPCException(error_message)
        else:
            return resp['result']
