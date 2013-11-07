###
# Copyright (c) 2013, James Scott
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.registry as registry

import requests
import json
import winds

class Flight(callbacks.Plugin):
    """Add the help for "@plugin help Flight" here
    This should describe *how* to use this plugin."""
    threaded = True


    def __init__(self, irc):
        self.__parent = super(Flight, self)
        self.__parent.__init__(irc)

        self.flightapi = self.registryValue('flghtapi_url') + '%s'

    def _api_request(self, request_type, endpoint, data=None):
        response = None
        url = self.flightapi % (endpoint, )
        if request_type == 'get':
            response = requests.get(url)
        elif request_type == 'put':
            headers = {'content-type': 'application/json'}
            response = requests.put(url,
                                    data=json.dumps(data),
                                    headers=headers)
        if response is not None:
            if response.code == 200:
                return response.json()
            else:
                return {'error': response.code}

    def _api_get_request(self, endpoint):
        return self._api_request('get', endpoint)

    def _api_put_request(self, endpoint, data):
        return self._api_request('put', endpoint, data=data)

    def metar(self, irc, msg, args):
        """ Returns the metar for a station """
        if len(args) > 0:
            response = self._api_get_request('/metar/%s' % args[0])
            try:
                irc.reply(response['metar'])
            except KeyError:
                irc.reply('Failed to pull weather for: %s' % args[0])
        else:
            irc.reply(self.metar.__doc__)

    def taf(self, irc, msg, args):
        """ Returns the taf for a station """
        if len(args) > 0:
            response = self._api_get_request('/metar/%s' % args[0])
            try:
                irc.reply(response['taf'])
            except KeyError:
                irc.reply('Failed to pull TAF for: %s' % args[0])
        else:
            irc.reply(self.metar.__doc__)

    def expandroute(self, irc, msg, args):
        """ This returns the entire flown route """
        route = ' '.join(args)
        route = self._api_put_request('/route', data={'route': route})
        if route is not None:
            try:
                irc.reply(route['expanded_route'])
            except:
                irc.reply('Unabled to parse route')
        irc.reply('Unable to parse route')

    def apt(self, irc, msg, args):
        """ Returns information about an airport """
        airport = args[0].upper()
        skyvector = 'http://skyvector.com/airport/%s' % (airport, )
        metar = self._api_get_request('/longmetar/%s' % (airport, ))
        airport = self._api_get_request('/airport/%s' % (airport, ))

    def zulu(self, irc, msg, args):
        irc.reply(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

Class = Flight


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
