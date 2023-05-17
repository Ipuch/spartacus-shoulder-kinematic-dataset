from enum import Enum
from pathlib import Path


class DatasetCSV(Enum):
    """Enum for the dataset csv files, with dynamic path"""

    RAW = Path(__file__).parent.parent / "dataset" / "only_dataset_raw.csv"
    CLEAN = Path(__file__).parent.parent / "dataset" / "dataset_clean.csv"


class CartesianAxis(Enum):
    plusX = "x"
    plusY = "y"
    plusZ = "z"
    minusX = "-x"
    minusY = "-y"
    minusZ = "-z"


class BiomechDirection(Enum):
    """Enum for the biomechanical direction"""

    AnteroPosterior = "Antero-Posterior"
    InferoSuperior = "Infero-Superior"
    MedioLateral = "Medio-Lateral"


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


class JointType(Enum):
    """Enum for the joint"""

    GLENO_HUMERAL = "GH"
    SCAPULO_THORACIC = "ST"
    ACROMIO_CLAVICULAR = "AC"
    STERNO_CLAVICULAR = "SC"
    THORACO_HUMERAL = "TH"
