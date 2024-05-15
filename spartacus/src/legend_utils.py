from .joint import JointType


def isb_rotation_biomechanical_dof(joint_type: JointType):
    joint_mapping = {
        JointType.GLENO_HUMERAL: ("plane of elevation", "elevation", "internal(+)-external(-) rotation"),
        JointType.SCAPULO_THORACIC: (
            "protraction(+)-retraction(-)",
            "medial(+)-lateral(-) rotation",
            "posterior(+)-anterior(-) tilt",
        ),
        JointType.ACROMIO_CLAVICULAR: (
            "protraction(+)/retraction(-)",
            "medial(+)/lateral(-) rotation",
            "posterior(+)/anterior(-) tilt",
        ),
        JointType.STERNO_CLAVICULAR: (
            "protraction(+)/retraction(-)",
            "depression(+)/elevation(-)",
            "backwards(+)/forward(-) rotation",
        ),
        JointType.THORACO_HUMERAL: ("plane of elevation", "elevation", "internal(+)/external(-) rotation"),
    }
    return joint_mapping.get(joint_type)
