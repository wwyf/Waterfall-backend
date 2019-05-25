class Mocker(object):
    def __init__(self, **kwargs):
        for name, attr in kwargs.items():
            self.__setattr__(name, attr)