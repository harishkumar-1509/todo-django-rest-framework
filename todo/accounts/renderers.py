from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data = None, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data.get('value',None),
                                   'success':False,
                                   'message':data['msg'],
                                   'token':data['token']
                                   })
        else:
            response = json.dumps({
                'success': True,
                'data': data['value'],
                'message':data['msg'],
                'token':data['token']
            })    
        return response