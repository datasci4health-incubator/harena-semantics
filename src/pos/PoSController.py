# from .clustring import Ner
# from .dist_v2 import BertEmbeds
# from .biobert_pytorch import Ner

# from src.ner.bert.Bert import Ner

import os, requests

class SingletonPoSController(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
        

class PoSController(metaclass=SingletonPoSController):
    def tags(self, text):
        POS_SERVICE_URL = "http://127.0.0.1:8028/"
        response = requests.get(url=POS_SERVICE_URL + text)

        rows = str(response.text).split('\n')

        pos_dict = []

        for row in rows:
            columns = row.split('\t')

            if len(columns) == 5:
                pos_dict.append({ 'term': columns[1], 'pos': columns[2],  'masked': False})
                # pos_dict[int(columns[0])] =

        return pos_dict
