from .constants import BIOMECHANICAL_DOF_LEGEND


def isb_rotation_biomechanical_dof(joint_type: str):
    return BIOMECHANICAL_DOF_LEGEND.get(joint_type)
