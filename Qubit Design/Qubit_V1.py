from qiskit_metal import designs, draw
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket
from qiskit_metal.qlibrary.connectors.open_to_ground import OpenToGround
from qiskit_metal.qlibrary.lumped.r_chip_capacitor import RChipCapacitor
from qiskit_metal import MetalGUI, Dict
from qiskit_metal.analyses.quantization import EPRanalysis


design = designs.DesignPlanar()
gui = MetalGUI(design)

qubit_options = dict(
    connection_pads=dict(
        a=dict(loc_W=+1, loc_H=+1),
        b=dict(loc_W=-1, loc_H=+1),
        c=dict(loc_W=+1, loc_H=-1),
        d=dict(loc_W=-1, loc_H=-1)
    )
)

qubit = TransmonPocket(design, 'Q1', options=qubit_options)
gui.rebuild()

# Placeholder values for resonator's parameters
resonator_options = dict(
    pos_x='0um',
    pos_y='0um',
    orientation='0'
)

resonator = RChipCapacitor(design, 'R1', options=resonator_options)
gui.rebuild()

# Exporting the design to Ansys Q3D
from qiskit_metal.analyses.simulation import AnsysHfss, AnsysQ3d

hfss = AnsysHfss(design, 'hfss')
hfss.export_design()  # Adjust parameters as necessary for your Ansys environment

# Or for Q3D extraction
q3d = AnsysQ3d(design, 'q3d')
q3d.export_design()  # Adjust parameters