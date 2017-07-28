"""This is the InformationForBeamlines device based on the facadedevice library. It stores communication between Control Room and beamlines."""

from facadedevice import Facade, proxy_attribute, proxy_command
from tango import AttrWriteType, DevState

class InformationForBeamlines(Facade):


    def safe_init_device(self):
        """
        Docstring for 'safe_init_device' - it is just safe initialization of the DS.
        :return:
        """
        super(InformationForBeamlines, self).safe_init_device()
        self.set_state(DevState.ON)
        self.set_status("Device is running")


run=InformationForBeamlines.run_server()

if __name__ == '__main__':
   run()
