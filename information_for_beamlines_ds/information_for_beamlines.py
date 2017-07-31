"""This is the InformationForBeamlines device based on the facadedevice library. It stores communication between Control Room and beamlines."""

from facadedevice import Facade, proxy_attribute, logical_attribute
from tango import AttrWriteType, DevState, DispLevel
from tango.server import attribute

class InformationForBeamlines(Facade):

    filling_pattern = ''
    general_info = ''

    def safe_init_device(self):
        """
        Docstring for 'safe_init_device' - it is just safe initialization of the DS.
        :return:
        """
        super(InformationForBeamlines, self).safe_init_device()
        self.set_state(DevState.ON)
        self.set_status("Device is running")
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
    # device ?
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

    BeamCurrent = proxy_attribute(
        dtype='float',
        property_name='BeamCurrentAttr',
        unit='A',
        format='%8.6f',
        access=AttrWriteType.READ,
        display_level=DispLevel.EXPERT,
        doc="Forwarded beam current from BIM."
    )

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

    @logical_attribute(
        dtype=float,
        unit='mA',
        bind=["BeamCurrent"],
        format='%4.3f',
        label='Beam Current (mA)',
        doc='Beam current in miliamperes.',
        display_level=DispLevel.EXPERT)
    def BeamCurrent_mA(self, data):
        current_mA = data * 1000.0
        # :TODO: Clarify if it's possible to push AttrQuality here.
        # if abs(current_mA) >= 1e-6:
        #     return current_mA , time(), AttrQuality.ATTR_VALID
        # else:
        #     return current_mA , time(), AttrQuality.ATTR_INVALID
        return current_mA

    def always_executed_hook(self):
        pass

    def delete_device(self):
        pass

    def state_from_data(self, data):
        mps = data['MPSState']
        bim = data['BIMState']
        if mps == DevState.FAULT:
            self.set_status('MPS PLC device is in FAULT.')
            return DevState.FAULT
        elif mps != DevState.ON and mps != DevState.RUNNING:
            self.set_status('MPS PLC device is in an unexpected state: %s' % str(mps))
            return DevState.ALARM
        if bim == DevState.FAULT:
            self.set_status('BIM device is in FAULT.')
            return DevState.FAULT
        elif bim != DevState.ON and bim != DevState.RUNNING:
            self.set_status('BIM device is in an unexpected state: %s' % str(bim))
            return DevState.ALARM

        self.set_state(DevState.ON)
        self.set_status('Everything is OK.')

        # ------------------
        # Attributes methods
        # ------------------

    def read_GeneralInfo(self):
        return self.general_info

    def write_GeneralInfo(self, value):
        self.general_info = value
        # self.push_change_event('GeneralInfo')
        # self.push_data_ready_event('GeneralInfo')

    def read_FillingPattern(self):
        return self.filling_pattern

    def write_FillingPattern(self, value):
        self.filling_pattern = value
        # self.push_change_event('FillingPattern')
        # self.push_data_ready_event('FillingPattern')

# ----------
# Run server
# ----------

run = InformationForBeamlines.run_server()

if __name__ == '__main__':
    run()
