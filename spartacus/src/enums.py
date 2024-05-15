import numpy as np
from enum import Enum
from pathlib import Path


class DatasetCSV(Enum):
    """Enum for the dataset csv files, with dynamic path"""

    RAW = Path(__file__).parent.parent / "dataset" / "only_dataset_raw.csv"
    CLEAN = Path(__file__).parent.parent / "dataset" / "dataset_clean.csv"


class DataFolder(Enum):
    BOURNE_2003 = Path(__file__).parent.parent / "data" / "#2_Bourne_et_al"
    CHU_2012 = Path(__file__).parent.parent / "data" / "#3_Chu_et_al"
    FUNG_2001 = Path(__file__).parent.parent / "data" / "#4_Fung_et_al"
    GUTIERREZ_DELGADO_2017 = Path(__file__).parent.parent / "data" / "#5_Gutierrez_Delgado_et_al"
    KOLZ_2020 = Path(__file__).parent.parent / "data" / "Kolz et al 2020"
    MCCLURE_2001 = Path(__file__).parent.parent / "data" / "#7_Karduna_et_al"
    KIJIMA_2015 = Path(__file__).parent.parent / "data" / "#8_Kijima_et_al"
    KIM_2017 = Path(__file__).parent.parent / "data" / "#9_Kim_et_al"
    KONOZO_2017 = Path(__file__).parent.parent / "data" / "#10_Kozono_et_al"
    LAWRENCE_2014 = Path(__file__).parent.parent / "data" / "#11_Ludwig_et_al"
    MATSUKI_2011 = Path(__file__).parent.parent / "data" / "#12_Matsuki_et_al"
    # MATSUKI_2011 = Path(__file__).parent.parent / "data" / "Matsuki et al 2011"
    # MATSUKI_2012 = Path(__file__).parent.parent / "data" / "Matsuki et al 2012"
    # MATSUKI_2014 = Path(__file__).parent.parent / "data" / "Matsuki et al 2014"
    MATSUMURA_2013 = Path(__file__).parent.parent / "data" / "#13_Matsumara_et_al"
    MOISSENET = Path(__file__).parent.parent / "data" / "#14_Moissenet_et_al"
    NISHINAKA_2008 = Path(__file__).parent.parent / "data" / "#15_Nishinaka_et_al"
    OKI_2012 = Path(__file__).parent.parent / "data" / "#16_Oki_et_al"
    SAHARA_2006 = Path(__file__).parent.parent / "data" / "#17_Sahara_et_al"
    # SAHARA_2006 = Path(__file__).parent.parent / "data" / "Sahara et al 2006"
    # SAHARA_2007 = Path(__file__).parent.parent / "data" / "Sahara et al 2007"
    SUGI_2021 = Path(__file__).parent.parent / "data" / "#18_Sugi_et_al"
    TEECE_2008 = Path(__file__).parent.parent / "data" / "#19_Teece_et_al"
    YOSHIDA_2023 = Path(__file__).parent.parent / "data" / "#20_Yoshida_et_al"
    CEREATTI_2017 = Path(__file__).parent.parent / "data" / "Cereatti et al 2017" / "S2M"
    DAL_MASO_2014 = Path(__file__).parent.parent / "data" / "Dal Maso et al 2014"
    MALBERG = "TODO"

    @classmethod
    def from_string(cls, data_folder: str):
        folder_name_to_enum = {
            "Cereatti et al 2017/S2M": cls.CEREATTI_2017,
            "Dal Maso et al 2014": cls.DAL_MASO_2014,
            # "Bourne 2003": cls.BOURNE_2003,
            "#2_Bourne_et_al": cls.BOURNE_2003,
            "#3_Chu_et_al": cls.CHU_2012,  # "Chu et al 2012"
            "#4_Fung_et_al": cls.FUNG_2001,  # "Fung et al 2001"
            "#5_Gutierrez_Delgado_et_al": cls.GUTIERREZ_DELGADO_2017,  # "Gutierrez Delgado et al 2017"
            "Kolz et al 2020": cls.KOLZ_2020,  # "Kolz et al 2020
            "#7_Karduna_et_al": cls.MCCLURE_2001,
            "#8_Kijima_et_al": cls.KIJIMA_2015,  # "Kijima et al 2015"
            "#9_Kim_et_al": cls.KIM_2017,  # "Kim et al 2017"
            "#10_Kozono_et_al": cls.KONOZO_2017,  # "Kozono et al 2017"
            "#11_Ludwig_et_al": cls.LAWRENCE_2014,
            "#12_Matsuki_et_al": cls.MATSUKI_2011,  # "Matsuki et al 2011"
            # "Matsuki et al 2011": cls.MATSUKI_2011,
            # "Matsuki et al 2012": cls.MATSUKI_2012,
            # "Matsuki et al 2014": cls.MATSUKI_2014,
            "#13_Matsumara_et_al": cls.MATSUMURA_2013,  # "Matsumura et al 2013"
            "#14_Moissenet_et_al": cls.MOISSENET,  # "Moissenet et al"
            "#15_Nishinaka_et_al": cls.NISHINAKA_2008,  # "Nishinaka et al 2008"
            "#16_Oki_et_al": cls.OKI_2012,  # "Oki et al 2012"
            "#17_Sahara_et_al": cls.SAHARA_2006,  # "Sahara et al 2006"
            # "Sahara et al 2006": cls.SAHARA_2006,
            # "Sahara et al 2007": cls.SAHARA_2007,
            "#18_Sugi_et_al": cls.SUGI_2021,  # "Sugi et al 2021"
            "#19_Teece_et_al": cls.TEECE_2008,  # "Teece et al 2008"
            "#20_Yoshida_et_al": cls.YOSHIDA_2023,  # "Yoshida et al 2023"
            "#XX_Malberg": cls.MALBERG,
        }

        the_enum = folder_name_to_enum.get(data_folder)
        if the_enum is None:
            raise ValueError(f"Unknown data folder: {data_folder}")

        return the_enum


class CartesianAxis(Enum):
    plusX = ("x", np.array([1, 0, 0]))
    plusY = ("y", np.array([0, 1, 0]))
    plusZ = ("z", np.array([0, 0, 1]))
    minusX = ("-x", np.array([-1, 0, 0]))
    minusY = ("-y", np.array([0, -1, 0]))
    minusZ = ("-z", np.array([0, 0, -1]))


class BiomechDirection(Enum):
    """Enum for the biomechanical direction"""

    PlusPosteroAnterior = "PlusAntero-Posterior"
    PlusInferoSuperior = "PlusInfero-Superior"
    PlusMedioLateral = "PlusMedio-Lateral"
    MinusPosteroAnterior = "MinusAntero-Posterior"
    MinusInferoSuperior = "MinusInfero-Superior"
    MinusMedioLateral = "MinusMedio-Lateral"

    @classmethod
    def from_string(cls, biomech_direction: str):
        biomech_direction_to_enum = {
            "+mediolateral": cls.PlusMedioLateral,
            "+posteroanterior": cls.PlusPosteroAnterior,
            "+inferosuperior": cls.PlusInferoSuperior,
            "-mediolateral": cls.MinusMedioLateral,
            "-posteroanterior": cls.MinusPosteroAnterior,
            "-inferosuperior": cls.MinusInferoSuperior,
        }

        the_enum = biomech_direction_to_enum.get(biomech_direction)

        if the_enum is None:
            raise ValueError(
                f"{biomech_direction} is not a valid biomech_direction."
                "biomech_direction must be one of the following: "
                "+mediolateral, +anteroposterior, +inferosuperior, "
                "-mediolateral, -anteroposterior, -inferosuperior"
            )

        return the_enum

    @property
    def sign(self):
        sign = {
            self.PlusPosteroAnterior: 1,
            self.PlusMedioLateral: 1,
            self.PlusInferoSuperior: 1,
            self.MinusPosteroAnterior: -1,
            self.MinusMedioLateral: -1,
            self.MinusInferoSuperior: -1,
        }

        return sign[self]


class BiomechOrigin:
    """Enum for the biomechanical origins of the segment"""

    class Thorax(Enum):
        STERNAL_NOTCH = "SN"
        T7 = "T7"
        IJ = "IJ"
        T1_ANTERIOR_FACE = "T1 anterior face"
        T1s = "T1s"  # @todo: make sure to understand what is it
        C7 = "C7"
        T8 = "T8"
        PX = "PX"  # processus xiphoide

    class Clavicle(Enum):
        STERNOCLAVICULAR_JOINT_CENTER = "SCJC"
        MIDTHIRD = "MTC"
        CUSTOM = "CUSTOM"
        ACROMIOCLAVICULAR_JOINT_CENTER = "ACJC"

    class Scapula(Enum):
        ANGULAR_ACROMIALIS = "AA"
        GLENOID_CENTER = "GC"
        ACROMIOCLAVICULAR_JOINT_CENTER = "ACJC"
        TRIGNONUM_SPINAE = "TS"
        ANGULUS_INFERIOR = "AI"

    class Humerus(Enum):
        GLENOHUMERAL_HEAD = "GH"
        MIDPOINT_EPICONDYLES = "midpoint epicondyles"  # middle of Medial and Lateral epicondyles

    class Any(Enum):
        NAN = "nan"

    @classmethod
    def from_string(cls, biomech_origin: str):
        if biomech_origin is None:
            return None

        biomech_origin_to_enum = {
            "T7": cls.Thorax.T7,
            "IJ": cls.Thorax.IJ,
            "T1 anterior face": cls.Thorax.T1_ANTERIOR_FACE,  # old
            "T1s": cls.Thorax.T1_ANTERIOR_FACE,
            "GH": cls.Humerus.GLENOHUMERAL_HEAD,
            "midpoint EM EL": cls.Humerus.MIDPOINT_EPICONDYLES,  # old
            "(EM+EL)/2": cls.Humerus.MIDPOINT_EPICONDYLES,
            "SC": cls.Clavicle.STERNOCLAVICULAR_JOINT_CENTER,
            "CM": cls.Clavicle.MIDTHIRD,
            "point of intersection between the mesh model and the Zc axis": cls.Clavicle.CUSTOM,
            "AC": cls.Scapula.ACROMIOCLAVICULAR_JOINT_CENTER,
            "AA": cls.Scapula.ANGULAR_ACROMIALIS,
            "glenoid center": cls.Scapula.GLENOID_CENTER,  # old
            "GC": cls.Scapula.GLENOID_CENTER,
            "TS": cls.Scapula.TRIGNONUM_SPINAE,
            "clavicle origin": cls.Clavicle.CUSTOM,
        }

        the_enum = biomech_origin_to_enum.get(biomech_origin)
        if the_enum is None:
            raise ValueError(
                f"{biomech_origin} is not a valid biomech_origin."
                "biomech_origin must be one of the following: "
                "joint, parent, child"
            )

        return the_enum


class JointType(Enum):
    """Enum for the joint"""

    GLENO_HUMERAL = "GH"
    SCAPULO_THORACIC = "ST"
    ACROMIO_CLAVICULAR = "AC"
    STERNO_CLAVICULAR = "SC"
    THORACO_HUMERAL = "TH"

    @classmethod
    def from_string(cls, joint: str):
        dico = {
            "glenohumeral": cls.GLENO_HUMERAL,
            "scapulothoracic": cls.SCAPULO_THORACIC,
            "acromioclavicular": cls.ACROMIO_CLAVICULAR,
            "sternoclavicular": cls.STERNO_CLAVICULAR,
            "thoracohumeral": cls.THORACO_HUMERAL,
        }

        the_enum = dico.get(joint)
        if the_enum is None:
            raise ValueError(f"{joint} is not a valid joint.")

        return the_enum


class EulerSequence(Enum):
    XYX = "xyx"
    XZX = "xzx"
    XYZ = "xyz"
    XZY = "xzy"
    YXY = "yxy"
    YZX = "yzx"
    YXZ = "yxz"
    YZY = "yzy"
    ZXZ = "zxz"
    ZXY = "zxy"
    ZYZ = "zyz"
    ZYX = "zyx"

    @classmethod
    def isb_from_joint_type(cls, joint_type: JointType):
        joint_type_to_euler_sequence = {
            JointType.GLENO_HUMERAL: cls.YXY,
            JointType.SCAPULO_THORACIC: cls.YXZ,
            JointType.ACROMIO_CLAVICULAR: cls.YXZ,
            JointType.STERNO_CLAVICULAR: cls.YXZ,
            JointType.THORACO_HUMERAL: cls.YXY,
        }

        the_enum = joint_type_to_euler_sequence.get(joint_type)
        if the_enum is None:
            raise ValueError("JointType not recognized")

        return the_enum

    @classmethod
    def from_string(cls, sequence: str):
        if sequence is None:
            return None

        sequence_name_to_enum = {
            "xyx": cls.XYX,
            "xzx": cls.XZX,
            "xyz": cls.XYZ,
            "xzy": cls.XZY,
            "yxy": cls.YXY,
            "yzx": cls.YZX,
            "yxz": cls.YXZ,
            "yzy": cls.YZY,
            "zxz": cls.ZXZ,
            "zxy": cls.ZXY,
            "zyz": cls.ZYZ,
            "zyx": cls.ZYX,
        }

        the_enum = sequence_name_to_enum.get(sequence)
        if the_enum is None:
            raise ValueError(f"{sequence} is not a valid euler sequence.")

        return the_enum


class Frame:
    class Local(Enum):
        """Enum for the local frame"""

        THORAX = "thorax"
        HUMERUS = "humerus"
        SCAPULA = "scapula"
        CLAVICLE = "clavicle"

    class NonOrthogonal(Enum):
        """Enum for the non-orthogonal frame"""

        JOINT_STERNOCLAVICULAR = "SC"
        JOINT_ACROMIOCLAVICULAR = "AC"
        JOINT_GLENOHUMERAL = "GH"
        JOINT_SCAPULOTHORACIC = "ST"

    @classmethod
    def from_string(cls, frame: str, joint: str):
        segment_name_to_enum = {
            "thorax": cls.Local.THORAX,
            "humerus": cls.Local.HUMERUS,
            "scapula": cls.Local.SCAPULA,
            "clavicle": cls.Local.CLAVICLE,
        }

        frame_to_enum = {
            ("jcs", "glenohumeral"): cls.NonOrthogonal.JOINT_GLENOHUMERAL,
            ("jcs", "scapulothoracic"): cls.NonOrthogonal.JOINT_SCAPULOTHORACIC,
            ("jcs", "acromioclavicular"): cls.NonOrthogonal.JOINT_ACROMIOCLAVICULAR,
            ("jcs", "sternoclavicular"): cls.NonOrthogonal.JOINT_STERNOCLAVICULAR,
        }

        the_enum = segment_name_to_enum.get(frame)

        if the_enum is None:
            the_enum = frame_to_enum.get((frame, joint))

        if the_enum is None:
            raise ValueError(f"{frame} is not a valid frame.")

        return the_enum


class Segment(Enum):
    """Enum for the segment"""

    THORAX = "thorax"
    HUMERUS = "humerus"
    SCAPULA = "scapula"
    CLAVICLE = "clavicle"

    @classmethod
    def from_string(cls, segment: str):
        segment_name_to_enum = {
            "thorax": cls.THORAX,
            "humerus": cls.HUMERUS,
            "scapula": cls.SCAPULA,
            "clavicle": cls.CLAVICLE,
        }

        the_enum = segment_name_to_enum.get(segment)
        if the_enum is None:
            raise ValueError(f"{segment} is not a valid segment.")

        return the_enum


class Correction(Enum):
    """Enum for the segment coordinate system corrections"""

    # orientation of axis are not orientated as ISB X: anterior, Y: superior, Z: lateral
    TO_ISB_ROTATION = "to_isb"
    TO_ISB_LIKE_ROTATION = "to_isb_like"  # But despite this reorientation, the axis won't be exactly the same as ISB

    SCAPULA_KOLZ_AC_TO_PA_ROTATION = "kolz_AC_to_PA"  # from acromion center of rotation to acromion posterior aspect
    SCAPULA_KOLZ_GLENOID_TO_PA_ROTATION = (
        "glenoid_to_isb_cs"  # from glenoid center of rotation to acromion posterior aspect
    )
    HUMERUS_SULKAR_ROTATION = "Sulkar et al. 2021"  # todo: idk what it is
    SCAPULA_LAGACE_DISPLACEMENT = "Lagace 2012"  # todo: idk what it is

    @classmethod
    def from_string(cls, correction: str):
        correction_name_to_enum = {
            "to_isb": cls.TO_ISB_ROTATION,
            "to_isb_like": cls.TO_ISB_LIKE_ROTATION,
            "kolz_AC_to_PA": cls.SCAPULA_KOLZ_AC_TO_PA_ROTATION,
            "kolz_GC_to_PA": cls.SCAPULA_KOLZ_GLENOID_TO_PA_ROTATION,
            "glenoid_to_isb_cs": cls.SCAPULA_KOLZ_GLENOID_TO_PA_ROTATION,
            "Sulkar et al. 2021": cls.HUMERUS_SULKAR_ROTATION,
            "Lagace 2012": cls.SCAPULA_LAGACE_DISPLACEMENT,
        }

        the_enum = correction_name_to_enum.get(correction)
        if the_enum is None:
            raise ValueError(f"{correction} is not a valid correction method.")

        return the_enum
