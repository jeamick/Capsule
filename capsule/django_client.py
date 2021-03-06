from syft.he.paillier.keys import KeyPair, PublicKey
import syft
import redis, os, requests, random

class LocalDjangoCapsuleClient():

    def __init__(self,host='127.0.0.1',port='9000'):
        self.host = host
        self.port = port

    def keygen(self,scheme='paillier'):
        id = str(random.randint(0,2**32))
        r = requests.get('http://'+self.host+':'+self.port+'/keygen/'+id+'/'+scheme+'/')

        pk = PublicKey.deserialize(r.content.decode())
        pk.id = id
        return pk

    def bootstrap(self,x,id=None):
        if(id is None):
            id = x.public_key.id
        r = requests.post('http://'+self.host+':'+self.port+"/bootstrap/"+str(id)+'/', data=x.serialize())
        return syft.tensor.TensorBase.deserialize(r.content.decode())

    def decrypt(self,x,id=None):

        if(id is None):
            id = x.public_key.id

        url = 'http://'+self.host+':'+self.port+"/decrypt/"+str(id)+'/'
        r = requests.post(url, data=x.serialize().decode('ISO-8859-1'))
        try:
            out = syft.tensor.TensorBase.deserialize(r.content)
        except Exception as e:
            print(e)
            out = float(r.content)
        return out
