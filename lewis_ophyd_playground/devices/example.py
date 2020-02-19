
from lewis.devices import Device

from lewis.adapters.epics import EpicsInterface, PV
from lewis.adapters.stream import StreamInterface, Var
from lewis.core.utils import check_limits


class VerySimpleDevice(Device):
    upper_limit = 100
    lower_limit = 0

    simple = 42
    ropi = 3.141
    param = 10
    _second = 2.0

    def get_param(self):
        """The parameter multiplied by 2."""
        return self.param * 2

    def set_param(self, new_param):
        self.param = int(new_param / 2)

    @property
    def second(self):
        """A second (floating point) parameter."""
        return self._second

    @second.setter
    @check_limits('lower_limit', 'upper_limit')
    def second(self, new_second):
        self._second = new_second


class VerySimpleInterface(EpicsInterface):
    """
    This is the EPICS interface to a quite simple device. It offers 5 PVs that expose
    different things that are part of the device, the interface or neither.
    """
    pvs = {
        'Simple': PV('simple', type='int', doc='Just an attribute exposed as on a PV'),
        'PI': PV('ropi', type='float', read_only=True, doc='Example of a read-only attribute'),
        'Param': PV(('get_param', 'set_param'), type='int', doc='Exposed via getter/setter'),
        'Second': PV('second', meta_data_property='param_raw_meta', doc='Meta-property to add limits'),
        'Second-Int': PV('second_int', type='int', doc='Conversion to int via helper function'),
        'Constant': PV(lambda: 4, doc='A constant number, returned from lambda function.')
    }

    @property
    def param_raw_meta(self):
        return {'lolo': self.device.lower_limit, 'hihi': self.device.upper_limit}

    @property
    def second_int(self):
        """The second parameter as an integer."""
        return int(self.device.second)


class VerySimpleStreamInterface(StreamInterface):
    """This is a TCP stream interface to the epics device, which only exposes param."""

    commands = {
        Var('param', read_pattern=r'P\?$', write_pattern=r'P=(\d+)', argument_mappings=(int,),
            doc='An integer parameter.')
    }

    in_terminator = '\r\n'
    out_terminator = '\r\n'


# Really don't like this
framework_version = '1.2.1'
