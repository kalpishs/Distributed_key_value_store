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
                return  "failed to inset key = % with value : %".format(key,value)
        print(self.storage)
        return "stored"
