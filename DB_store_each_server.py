from singleton_cls_instance import Singleton

class Db_store(object):
    """
     This DB class is a singleton in memory key value storage class.
     only one Db_store obj at a time
    """
    __metaclass__ = Singleton
    def __init__(self,**kwargs):
        self.storage={}

    def set(self, **kwargs):
        data = kwargs.get('data')
        for key,value in data.items():
            try:
                self.storage[key] = value
            except:
                return  "failed to inset key = {0} with value : {1}".format(key,value)
        print("stored key value in Current servers are {}".format(self.storage))
        return "stored key:value is {}".format(value)

    def get(self,**kwargs):
        key=kwargs.get('data')
        if key in self.storage:
            return  "retrived key value is {}".format(self.storage[key])
        else:
            return "No such key on any server"

