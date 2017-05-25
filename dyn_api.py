# -*- coding: utf-8 -*-
import requests
import xmltodict


class DynApi(object):
    def __init__(self):
        self.domain = 'emailapi.dynect.net/rest/xml'
        self.api_key = '<<your API key here>>'
        self.headers = {'User-Agent': 'dnyapi.py 0.1'}

# needs contemplate the case where accounts > 25 (would need to query multiple times and merge it
    def get_accounts(self, startindex=0, accountname=None):
        accounts_url = "http://{domain}/accounts".format(domain=self.domain)
        params = dict(
            apikey=self.api_key,
            startindex=startindex,
            accountname=accountname)
        result = requests.get(accounts_url, params=params)
        d = xmltodict.parse(result.text)
        accounts_dict = d['response']['data']['accounts']['account']
        dict_accs = {}
        for a in accounts_dict:
            username = a['username']
            accountname = a['accountname']
            companyname = a['companyname']
            address = a['address']
            city = a['city']
            state = a['state']
            country = a['country']
            zipcode = a['zipcode']
            phone = a['phone']
            usertype = a['usertype']
            created = a['created']
            apikey = a['apikey']
            timezone = a['timezone']
            tracklinks = a['tracklinks']
            trackopens = a['trackopens']
            testmode = a['testmode']
            trackunsubscribes = a['trackunsubscribes']
            max_sample_count = a['max_sample_count']
            shard_id = a['shard_id']
            contactname = a['contactname']
            emailssent = a['emailssent']
            dict_accs[username] = {'accountname': accountname, 'companyname': companyname, 'address': address,
                                   'city': city, 'state': state, 'country': country, 'zipcode': zipcode,
                                   'phone': phone, 'usertype': usertype, 'created': created, 'apikey': apikey,
                                   'timezone': timezone, 'tracklinks': tracklinks, 'trackopens': trackopens,
                                   'testmode': testmode, 'trackunsubscribes': trackunsubscribes,
                                   'max_sample_count': max_sample_count, 'shard_id': shard_id,
                                   'contactname': contactname, 'emailssent': emailssent}
        return dict_accs

    def get_xheaders(self):
        xheaders_url = "http://{domain}/accounts/xheaders".format(domain=self.domain)
        params = dict(apikey=self.api_key)
        result = requests.get(xheaders_url, params=params)
        d = xmltodict.parse(result.text)
        xheaders_dict = d['response']['data']
        dict_xhead = {}
        for x in xheaders_dict:
            dict_xhead[x] = xheaders_dict[x]
        return dict_xhead

    def get_senders(self):
        senders_url = "http://{domain}/senders".format(domain=self.domain)
        params = dict(apikey=self.api_key)
        result = requests.get(senders_url, params=params)
        d = xmltodict.parse(result.text)
        senders_dict = d['response']['data']['senders']['sender']
        dict_senders = {}
        for s in senders_dict:
            dict_senders[s['emailaddress']] = s['email']
        return dict_senders

    def get_sender_details(self, emailaddress):
        sender_details_url = "http://{domain}/senders/details".format(domain=self.domain)
        params = dict(
            apikey=self.api_key,
            emailaddress=emailaddress)
        result = requests.get(sender_details_url, params=params)
        d = xmltodict.parse(result.text)
        sender_details_dict = d['response']['data']
        return sender_details_dict

    def get_sender_status(self, emailaddress):
        sender_status_url = "http://{domain}/senders/status".format(domain=self.domain)
        params = dict(
            apikey=self.api_key,
            emailaddress=emailaddress)
        result = requests.get(sender_status_url, params=params)
        d = xmltodict.parse(result.text)
        sender_status_dict = d['response']['data']['ready']
        return sender_status_dict

    def get_recipients(self, emailaddress):
        recipients_url = "http://{domain}/recipients/status".format(domain=self.domain)
        params = dict(
            apikey=self.api_key,
            emailaddress=emailaddress)
        result = requests.get(recipients_url, params=params)
        d = xmltodict.parse(result.text)
        recipients_dict = d['response']['data']['recipients']['recipient']
        dict_recipients = {}
        for r in recipients_dict:
            dict_recipients[r] = recipients_dict[r]
        return dict_recipients

    def post_recipients(self, emailaddress):
        recipients_post_url = "http://{domain}/recipients/activate".format(domain=self.domain)
        params = dict(
            apikey=self.api_key,
            emailaddress=emailaddress)
        result = requests.post(recipients_post_url, data=params)
        d = xmltodict.parse(result.text)
        recipients_post_response = d['response']['message']
        return recipients_post_response

    def send(self, ffrom, to, subject, bodyhtml, xheaders, replyto=None, cc=None, bcc=None, sender=None, messageid=None,
             inreplyto=None, references=None, comments=None, keywords=None, replyby=None, importance='normal',
             priority='normal', sensitivity='private', resent_date=None, resent_from=None, resent_sender=None,
             resent_replyto=None, resent_messageid=None):
        send_url = "http://{domain}/send".format(domain=self.domain)
        params = {'apikey': self.api_key,
                  'from': ffrom,
                  'to': to,
                  'subject': subject,
                  'replyto': replyto,
                  'cc': cc,
                  'bcc': bcc,
                  'sender': sender,
                  'messageid': messageid,
                  'inreplyto': inreplyto,
                  'references': references,
                  'comments': comments,
                  'keywords': keywords,
                  'replyby': replyby,
                  'importance': importance,
                  'priority': priority,
                  'sensitivity': sensitivity,
                  'resent-date': resent_date,
                  'resent-from': resent_from,
                  'resent-sender': resent_sender,
                  'resent-replyto': resent_replyto,
                  'resent-messageid': resent_messageid,
                  'bodyhtml': bodyhtml,
                  'xheaders': xheaders}
        result = requests.post(send_url, data=params)
        d = xmltodict.parse(result.text)
        return d['response']['data']
        # answer on success = '250 2.1.5 Ok'
        # answer on fail = '503 5.5.1 Error: need MAIL command'

    def get_supressions(self, startdate=None, enddate=None, startindex=None):
        supressions_url = "http://{domain}/supressions".format(domain=self.domain)
        params = dict(
            apikey=self.api_key,
            startdate=startdate,
            enddate=enddate,
            startindex=startindex)
        result = requests.get(supressions_url, params=params)
        d = xmltodict.parse(result.text)
        supressions_response = d
        return supressions_response
        # need finish formatting the response

    def get_supressions_count(self):
        supressions_count_url = "http://{domain}/supressions/count".format(domain=self.domain)
        params = dict(
            apikey=self.api_key,
            startdate=startdate,
            enddate=enddate)
        result = requests.get(supressions_url, params=params)
        d = xmltodict.parse(result.text)
        supressions_response = d
        return supressions_response

    def post_supressions(self, emailaddress):
        post_supressions_url = "http://{domain}/supressions"
        params = dict(
            apikey=self.api_key,
            emailaddress=emailaddress)
        result = requests.post(post_supressions_url, data=params)
    # def post_supressions_activate(self):

# missing methods
# POST /accounts
# POST /accounts/xheaders
# POST /accounts/delete
# POST 	/senders
# POST 	/senders/dkim
# POST / senders / delete