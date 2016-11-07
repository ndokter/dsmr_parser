class DSMRObject(object):

    def __init__(self, values):
        self.values = values


class MBusObject(DSMRObject):

    @property
    def datetime(self):
        return self.values[0]['value']

    @property
    def value(self):
        return self.values[1]['value']

    @property
    def unit(self):
        return self.values[1]['unit']


class MBusObjectV2_2(DSMRObject):

    @property
    def datetime(self):
        return self.values[0]['value']

    @property
    def value(self):
        return self.values[5]['value']

    @property
    def unit(self):
        return self.values[4]['value']


class CosemObject(DSMRObject):

    @property
    def value(self):
        return self.values[0]['value']

    @property
    def unit(self):
        return self.values[0]['unit']


class ProfileGeneric(DSMRObject):
    pass
    # TODO implement
