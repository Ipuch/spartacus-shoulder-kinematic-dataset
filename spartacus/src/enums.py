from enum import Enum
from pathlib import Path
import numpy as np


class DatasetCSV(Enum):
    """Enum for the dataset csv files, with dynamic path"""

    RAW = Path(__file__).parent.parent / "dataset" / "only_dataset_raw.csv"
    CLEAN = Path(__file__).parent.parent / "dataset" / "dataset_clean.csv"


class DataFolder(Enum):
    BOURNE_2003 = Path(__file__).parent.parent / "data" / "Bourne et al 2003"
    CEREATTI_2017 = Path(__file__).parent.parent / "data" / "Cereatti et al 2017" / "S2M"
    CHARBONNIER_2017 = Path(__file__).parent.parent / "data" / "Charbonnier et al 2017"
    CHU_2012 = Path(__file__).parent.parent / "data" / "Chu et al 2012"
    DAL_MASO_2014 = Path(__file__).parent.parent / "data" / "Dal Maso et al 2014"
    FUNG_2001 = Path(__file__).parent.parent / "data" / "Fung et al 2001"
    GRAICHEN_2000 = Path(__file__).parent.parent / "data" / "Graichen et al 2000"
    GUTIERREZ_DELGADO_2017 = Path(__file__).parent.parent / "data" / "Gutierrez Delgado et al 2017"
    HALLSTROM_2006 = Path(__file__).parent.parent / "data" / "Hallström et al 2006"
    KIJIMA_2015 = Path(__file__).parent.parent / "data" / "Kijima et al 2015"
    KIM_2017 = Path(__file__).parent.parent / "data" / "Kim et al 2017"
    KOLZ_2020 = Path(__file__).parent.parent / "data" / "Kolz et al 2020"
    KONOZO_2017 = Path(__file__).parent.parent / "data" / "Konozo et al 2017"
    LAWRENCE_2014 = Path(__file__).parent.parent / "data" / "Lawrence et al 2014"
    MATSUKI_2012 = Path(__file__).parent.parent / "data" / "Matsuki et al 2012"
    MATSUKI_2014 = Path(__file__).parent.parent / "data" / "Matsuki et al 2014"
    MATSUMURA_2013 = Path(__file__).parent.parent / "data" / "Matsumura et al 2013"
    MCCLURE_2001 = Path(__file__).parent.parent / "data" / "McClure et al 2001"
    NISHINAKA_2008 = Path(__file__).parent.parent / "data" / "Nishinaka et al 2008"
    OKI_2012 = Path(__file__).parent.parent / "data" / "Oki et al 2012"
    SAHARA_2006 = Path(__file__).parent.parent / "data" / "Sahara et al 2006"
    SAHARA_2007 = Path(__file__).parent.parent / "data" / "Sahara et al 2007"
    SUGI_2021 = Path(__file__).parent.parent / "data" / "Sugi et al 2021"
    TEECE_2008 = Path(__file__).parent.parent / "data" / "Teece et al 2008"
    YOSHIDA_2023 = Path(__file__).parent.parent / "data" / "Yoshida et al 2023"

    @classmethod
    def from_string(cls, data_folder: str):
        folder_name_to_enum = {
            "Bourne et al 2003": cls.BOURNE_2003,
            "Cereatti et al 2017/S2M": cls.CEREATTI_2017,
            "Charbonnier et al 2017": cls.CHARBONNIER_2017,
            "Chu et al 2012": cls.CHU_2012,
            "Dal Maso et al 2014": cls.DAL_MASO_2014,
            "Fung et al 2001": cls.FUNG_2001,
            "Graichen et al 2000": cls.GRAICHEN_2000,
            "Gutierrez Delgado et al 2017": cls.GUTIERREZ_DELGADO_2017,
            "Hallström et al 2006": cls.HALLSTROM_2006,
            "Kijima et al 2015": cls.KIJIMA_2015,
            "Kim et al 2017": cls.KIM_2017,
            "Kolz et al 2020": cls.KOLZ_2020,
            "Konozo et al 2017": cls.KONOZO_2017,
            "Lawrence et al 2014": cls.LAWRENCE_2014,
            "Matsuki et al 2012": cls.MATSUKI_2012,
            "Matsuki et al 2014": cls.MATSUKI_2014,
            "Matsumura et al 2013": cls.MATSUMURA_2013,
            "McClure et al 2001": cls.MCCLURE_2001,
            "Nishinaka et al 2008": cls.NISHINAKA_2008,
            "Oki et al 2012": cls.OKI_2012,
            "Sahara et al 2006": cls.SAHARA_2006,
            "Sahara et al 2007": cls.SAHARA_2007,
            "Sugi et al 2021": cls.SUGI_2021,
            "Teece et al 2008": cls.TEECE_2008,
            "Yoshida et al 2023": cls.YOSHIDA_2023,
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

    PlusAnteroPosterior = "PlusAntero-Posterior"
    PlusInferoSuperior = "PlusInfero-Superior"
    PlusMedioLateral = "PlusMedio-Lateral"
    MinusAnteroPosterior = "MinusAntero-Posterior"
    MinusInferoSuperior = "MinusInfero-Superior"
    MinusMedioLateral = "MinusMedio-Lateral"


class BiomechOrigin:
    """Enum for the biomechanical origins of the segment"""

    class Thorax(Enum):
        STERNAL_NOTCH = "SN"
        T7 = "T7"
        IJ = "IJ"
        T1_ANTERIOR_FACE = "T1 anterior face"
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


class JointType(Enum):
    """Enum for the joint"""

    GLENO_HUMERAL = "GH"
    SCAPULO_THORACIC = "ST"
    ACROMIO_CLAVICULAR = "AC"
    STERNO_CLAVICULAR = "SC"
    THORACO_HUMERAL = "TH"


class Segment(Enum):
    """Enum for the segment"""

    THORAX = "thorax"
    HUMERUS = "humerus"
    SCAPULA = "scapula"
    CLAVICLE = "clavicle"


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
