import webapp2
import globals
import gaesessions

from openid import yadis
from openid.store import gaecache
from openid.consumer import consumer, discover
from openid.extensions import sreg, ax

from src.controllers import base_handler

class OpenIdAuthenticator(base_handler.BaseHandler):
    dataype2ax_schema = {
        'username': 'http://axschema.org/namePerson/friendly',
        'email': 'http://axschema.org/contact/email',
        'country': 'http://openid.net/schema/contact/country/home',
    }

    sreg_attributes = {
        'required': {
            'email': 'email',
            'nickname': 'username',
            'fullname': 'real_name',
        },
        'optional': {
            'country': 'country',
        },
    }

    def prepare_authentication_request(self):
        redirect_to = webapp2.uri_for('openid_auth_complete', _full=True)
        openid_server_url = 'http://www.udacity.com/openid/server'

        oid_consumer = consumer.Consumer(gaesessions.get_current_session(), gaecache.MemcacheStore())
        try:
            auth_request = oid_consumer.begin(openid_server_url)
        except discover.DiscoveryFailure:
            raise InvalidAuthentication(_('Sorry, but your input is not a valid OpenId'))

        s = sreg.SRegRequest()
        for k, attr_dic in self.sreg_attributes.iteritems():
            is_required = k == 'required'
            for attr_name in attr_dic.keys():
                s.requestField(field_name=attr_name, required=is_required)
        auth_request.addExtension(s)

        axr = ax.FetchRequest()
        for data_type, schema in self.dataype2ax_schema.iteritems():
            if isinstance(schema, tuple):
                axr.add(ax.AttrInfo(schema[0], required=True, alias=schema[1]))
            else:
                axr.add(ax.AttrInfo(schema, required=True, alias=data_type))
        auth_request.addExtension(axr)

        trust_root = webapp2.uri_for('home', _full=True)
        return auth_request.redirectURL(trust_root, redirect_to)

    def process_authentication_request(self, request):
        oid_consumer = consumer.Consumer(
            gaesessions.get_current_session(), gaecache.MemcacheStore())
        query_dict = dict([(k, v) for k, v in request.GET.iteritems()])
        openid_response = oid_consumer.complete(query_dict, request.uri)

        if openid_response.status == consumer.SUCCESS:
            consumer_data = {}
            sreg_response = sreg.SRegResponse.fromSuccessResponse(openid_response)
            if sreg_response:
                all_attrs = {}
                [all_attrs.update(d)
                    for k, d in self.sreg_attributes.iteritems() if k != 'policy_url']
                for attr_name, local_name in all_attrs.items():
                    if attr_name in sreg_response:
                        consumer_data[local_name] = sreg_response[attr_name]

            ax = ax.FetchResponse.fromSuccessResponse(openid_response, False)
            if ax:
                axargs = ax.getExtensionArgs()
                ax_schema2data_type = dict([(s, t) for t, s in ax_schema.items()])
                available_types = dict([
                    (ax_schema2data_type[s], re.sub('^type\.', '', n))
                    for n, s in axargs.items() if s in ax_schema2data_type
                ])
                for t, s in available_types.items():
                    if not t in consumer_data:
                        if axargs.get('value.%s.1' % s, None):
                            consumer_data[t] = axargs['value.%s.1' % s]

            gaesessions.get_current_session().set_quick('auth_consumer_data', consumer_data)
            return request.GET['openid.identity']
        elif openid_response.status == consumer.CANCEL:
            raise InvalidAuthentication(_('The OpenId authentication request was canceled'))
        elif openid_response.status == consumer.FAILURE:
            raise InvalidAuthentication(_('The OpenId authentication failed: ') + openid_response.message)
        elif openid_response.status == consumer.SETUP_NEEDED:
            raise InvalidAuthentication(_('Setup needed'))
        else:
            raise InvalidAuthentication(_('The OpenId authentication failed with an unknown status: ') + openid_response.status)

    def get(self):
        self.process_authentication_request(self.request)
