"""This is the InformationForBeamlines device
based on the facadedevice library. It stores communication
between Control Room and beamlines."""

from facadedevice import Facade, proxy_attribute, \
    logical_attribute, state_attribute
from tango import AttrWriteType, DevState, DispLevel
from tango.server import attribute

class InformationForBeamlines(Facade):
    """
    This class specifies InformationForBeamlines facade.
    It is based on facadedevice library.
    It contains:

    - two attributes GeneralInfo and FillingPattern which provide string
      messages
    - two bool proxy attributes: InjectionStatus (true during injection process)
      ExperimentEnable (true when experiments can be performed)
    - two DevState proxy attributes: BIMState and MPSState which show states of those
    - logical attribute which indicates three possible statuses: Injection
      (InjectionStatus:true), ExperimentEnable (ExperimentEnable:true and current
      is higher than 1mA), MDT (in other cases)
    - state attribute that recognises states of MPS and BIM

    """

    filling_pattern = ''
    general_info = ''

    def safe_init_device(self):
        """
        Docstring for 'safe_init_device' - it is just safe
        initialization of the DS.
        :return:
        """
        super(InformationForBeamlines, self).safe_init_device()
        self.set_state(DevState.ON)
        self.set_status("Device is running")
        self.set_change_event("GeneralInfo", True, False)
        self.set_change_event("Fillingpattern", True, False)
        self.general_info = 'No information.'
        self.filling_pattern = 'No filling pattern.'

    # ----------
    # Attributes
    # ----------

    GeneralInfo = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        label="General info",
        doc="General message from CR to all beamlines.",
    )

    FillingPattern = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        label="Filling Pattern",
        doc="The filling pattern currently used in the storage ring.",
    )

    # ----------
    # Proxy attributes
    # ----------

    InjectionStatus = proxy_attribute(
        dtype='bool',
        property_name="InjectionStatusTag",
        display_level=DispLevel.EXPERT,
        access=AttrWriteType.READ,
        doc="Forwarded injection status tag from MPS PLC."
    )

    ExperimentEnable = proxy_attribute(
        dtype='bool',
        property_name='ExperimentEnableTag',
        display_level=DispLevel.EXPERT,
        access=AttrWriteType.READ,
        doc='Forwarded experiment enable status tag from MPS PLC.'
    )

    @proxy_attribute(
        dtype='float',
        property_name='BeamCurrentAttr',
        unit='mA',
        label="Beam Current in mA",
        access=AttrWriteType.READ,
        display_level=DispLevel.EXPERT,
        doc="Forwarded beam current from BIM. It is displayed in mA."
    )
    def BeamCurrent(self,data):
        return data*1000

    BIMState = proxy_attribute(
        dtype="DevState",
        property_name="BIMStateTag",
        access=AttrWriteType.READ,
        display_level=DispLevel.EXPERT,
        doc="State of the beam intensity monitor."
    )

    MPSState = proxy_attribute(
        dtype="DevState",
        property_name="MPSStateTag",
        access=AttrWriteType.READ,
        display_level=DispLevel.EXPERT,
        doc="State of the MPS PLC device."
    )

    # ----------
    # Logical attributes
    # ----------

    @logical_attribute(
        dtype='str',
        label="Operation Status",
        bind=["BeamCurrent","ExperimentEnable","InjectionStatus"],
        doc="One of: Injection, MDT (Machine Dedicated Time), Experiment Enable.",)
    def OperationStatus(self, beam_c,exp_en,inj_stat):
        if inj_stat:
            return 'Injection'
        elif beam_c > 1 and exp_en:
            return 'Experiment Enable'
        else:
            return 'MDT'

    @state_attribute(
        bind=["MPSState","BIMState"])
    def state_from_data(self, mps, bim):
        if mps == DevState.FAULT:
            return DevState.FAULT, "MPS PLC device is in FAULT."
        elif mps != DevState.ON and mps != DevState.RUNNING:
            return DevState.ALARM, "MPS PLC device is in an unexpected state: %s" % str(mps)
        if bim == DevState.FAULT:
            return DevState.FAULT, "BIM device is in FAULT."
        elif bim != DevState.ON and bim != DevState.RUNNING:
            return DevState.ALARM, "BIM device is in an unexpected state: %s" % str(bim)
        else:
            return DevState.ON, "Everything is OK."

    # ------------------
    # Attributes methods
    # ------------------

    def read_GeneralInfo(self):
        return self.general_info

    def write_GeneralInfo(self, value):
        self.general_info = value
        self.push_change_event('GeneralInfo', value)
        self.push_data_ready_event('GeneralInfo', 0)

    def read_FillingPattern(self):
        return self.filling_pattern

    def write_FillingPattern(self, value):
        self.filling_pattern = value
        self.push_change_event('FillingPattern', value)
        self.push_data_ready_event('FillingPattern', 0)

# ----------
# Run server
# ----------

#run = InformationForBeamlines.run_server()

if __name__ == '__main__':
    #run()
    InformationForBeamlines.run_server()
