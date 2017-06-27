import requests
from django.conf import settings

class MoocletEngineModel:

    @classmethod
    def create(self, **kwargs):
        r = requests.post("{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix), data=kwargs, headers={'Authorization': settings.MOOCLET_API_TOKEN})
        # print r.url
        return r.json()

    @classmethod
    def get(self, pk):
        r = requests.get("{}/{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix, pk), headers={'Authorization': settings.MOOCLET_API_TOKEN})
        # print r.url
        return r.json()
    
    @classmethod
    def list(self):
        r = requests.get("{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix), headers={'Authorization': settings.MOOCLET_API_TOKEN})
        # print r.url
        return r.json()
    
    @classmethod
    def update(self, pk, **kwargs):
        r = requests.put("{}/{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix, pk), data=kwargs, headers={'Authorization': settings.MOOCLET_API_TOKEN})
        # print r.url
        return r.json()
    
    @classmethod
    def delete(self, pk):
        r = requests.delete("{}/{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix, pk), headers={'Authorization': settings.MOOCLET_API_TOKEN})
        # print r.url
        return r.json()

class Mooclet(MoocletEngineModel):

    prefix = 'mooclet'

    # define additional api method for mooclet

    @classmethod
    def run(self, pk, **kwargs):
        '''
        use policy to get version for this mooclet
        arguments: 
        '''
        r = requests.get("{}/{}/{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix, pk, 'run'), headers={'Authorization': settings.MOOCLET_API_TOKEN})
        # print r.url
        return r.json()


class Version(MoocletEngineModel):
    prefix = 'version'

class Variable(MoocletEngineModel):
    prefix = 'variable'

class Value(MoocletEngineModel):
    prefix = 'value'
    
class Policy(MoocletEngineModel):
    prefix = 'policy'