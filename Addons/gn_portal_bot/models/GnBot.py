from odoo import models, _
import requests

bot_server_url =  "http://localhost:5100"


class GnBot(models.AbstractModel):
    _inherit = 'mail.bot'

    
    def _set_headers(self):
        headers = {'Content-Type': 'application/json'}
        value = ' '.join(['Bearer', 'gnco_dev'])
        headers.update({'Authorization': value})
        self._headers = headers
        self._base_url = "http://localhost:5100"

    def _get_response(self, record,body,values):
        self._set_headers()
        url = '/'.join([self._base_url, 'odoobot'])
        jsonpayload = {
            'from':{
                'id':self.env.user.id,
                'name':self.env.user.name
            },
            'channel_id': record.id,
            'channel_name':record.name,
            'body': body,
            'server': self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        }
        botresponse = requests.post(url, headers=self._headers, json=jsonpayload)
        jsonresponse = botresponse.json()
        #print(jsonresponse['body'])
        res = jsonresponse['body']

        # # Start conversation and get us a conversationId to use
        # url = '/'.join([self._base_url, 'conversations'])
        # botresponse = requests.post(url, headers=self._headers)
        return res



    
    def _get_answer(self, record, body, values, command):
        #odoobot_state = self.env.user.odoobot_state
        if self._is_bot_in_private_channel(record):
            try:
                return self._get_response(record,body,values)
            except:
                return _("Something went wron try later....<br/><br/><b></b>")
        return super(GnBot, self)._get_answer(record, body, values, command)
