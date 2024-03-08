import biorbd
import numpy as np

from .enums import CartesianAxis, BiomechDirection, BiomechOrigin, Segment
from .utils import compute_rotation_matrix_from_axes


class BiomechCoordinateSystem:
    def __init__(
        self,
        segment: Segment,
        antero_posterior_axis: CartesianAxis,
        infero_superior_axis: CartesianAxis,
        medio_lateral_axis: CartesianAxis,
        origin=None,
    ):
        # verify isinstance
        if not isinstance(antero_posterior_axis, CartesianAxis):
            raise TypeError("antero_posterior_axis should be of type CartesianAxis")
        if not isinstance(infero_superior_axis, CartesianAxis):
            raise TypeError("infero_superior_axis should be of type CartesianAxis")
        if not isinstance(medio_lateral_axis, CartesianAxis):
            raise TypeError("medio_lateral_axis should be of type CartesianAxis")
        # verity they are all different
        if (
            antero_posterior_axis == infero_superior_axis
            or antero_posterior_axis == medio_lateral_axis
            or infero_superior_axis == medio_lateral_axis
        ):
            raise ValueError("antero_posterior_axis, infero_superior_axis, medio_lateral_axis should be different")

        self.anterior_posterior_axis = antero_posterior_axis
        self.infero_superior_axis = infero_superior_axis
        self.medio_lateral_axis = medio_lateral_axis

        self.origin = origin
        self.segment = segment

    @classmethod
    def from_biomech_directions(
        cls,
        x: BiomechDirection,
        y: BiomechDirection,
        z: BiomechDirection,
        origin: BiomechOrigin = None,
        segment: Segment = None,
    ):
        my_arg = dict()

        # verify each of the x, y, z is different
        if x == y or x == z or y == z:
            raise ValueError("x, y, z should be different")

        # verify is positive or negative
        actual_axes = [x, y, z]
        positive_enums_axis = [CartesianAxis.plusX, CartesianAxis.plusY, CartesianAxis.plusZ]
        negative_enums_axis = [CartesianAxis.minusX, CartesianAxis.minusY, CartesianAxis.minusZ]

        for axis, positive_enum, negative_enum in zip(actual_axes, positive_enums_axis, negative_enums_axis):
            if axis.sign == 1:
                if axis == BiomechDirection.PlusPosteroAnterior:
                    my_arg["antero_posterior_axis"] = positive_enum
                    continue
                elif axis == BiomechDirection.PlusMedioLateral:
                    my_arg["medio_lateral_axis"] = positive_enum
                    continue
                elif axis == BiomechDirection.PlusInferoSuperior:
                    my_arg["infero_superior_axis"] = positive_enum
                    continue
            elif axis.sign == -1:
                if axis == BiomechDirection.MinusPosteroAnterior:
                    my_arg["antero_posterior_axis"] = negative_enum
                    continue
                elif axis == BiomechDirection.MinusMedioLateral:
                    my_arg["medio_lateral_axis"] = negative_enum
                    continue
                elif axis == BiomechDirection.MinusInferoSuperior:
                    my_arg["infero_superior_axis"] = negative_enum
                    continue

        my_arg["origin"] = origin
        my_arg["segment"] = segment

        return cls(**my_arg)

    def is_isb_origin(self) -> bool:
        if self.segment == Segment.THORAX and self.origin == BiomechOrigin.Thorax.IJ:
            return True
        elif self.segment == Segment.CLAVICLE and self.origin == BiomechOrigin.Clavicle.STERNOCLAVICULAR_JOINT_CENTER:
            return True
        elif self.segment == Segment.SCAPULA and self.origin == BiomechOrigin.Scapula.ANGULAR_ACROMIALIS:
            return True
        elif self.segment == Segment.HUMERUS and self.origin == BiomechOrigin.Humerus.GLENOHUMERAL_HEAD:
            return True
        else:
            return False

    def is_origin_on_an_isb_axis(self) -> bool:
        """
        Return True if the origin is on an ISB axis, False otherwise

        NOTE
        ----
        The true definition would be, the origin is part of the process to build an ISB axis.

        """
        if self.is_isb_origin():
            return True

        ON_ISB_AXES = {
            Segment.THORAX: [BiomechOrigin.Thorax.C7, BiomechOrigin.Thorax.T8, BiomechOrigin.Thorax.PX],
            Segment.CLAVICLE: [
                BiomechOrigin.Clavicle.STERNOCLAVICULAR_JOINT_CENTER,
                BiomechOrigin.Clavicle.ACROMIOCLAVICULAR_JOINT_CENTER,
            ],
            Segment.SCAPULA: [BiomechOrigin.Scapula.TRIGNONUM_SPINAE, BiomechOrigin.Scapula.ANGULUS_INFERIOR],
            Segment.HUMERUS: [BiomechOrigin.Humerus.MIDPOINT_EPICONDYLES],
        }

        return self.origin in ON_ISB_AXES.get(self.segment, [])

    def is_isb(self) -> bool:
        return self.is_isb_oriented() and self.is_isb_origin()

    def is_isb_oriented(self) -> bool:
        condition_1 = self.anterior_posterior_axis is CartesianAxis.plusX
        condition_2 = self.infero_superior_axis is CartesianAxis.plusY
        condition_3 = self.medio_lateral_axis is CartesianAxis.plusZ
        return condition_1 and condition_2 and condition_3

    def is_direct(self) -> bool:
        """check if the frame is direct (True) or indirect (False)"""
        return np.linalg.det(self.get_rotation_matrix()) > 0

    def get_rotation_matrix(self):
        """
        write the rotation matrix from the cartesian axis

        such that a_in_isb = R_to_isb_from_local @ a_in_local

        """

        return compute_rotation_matrix_from_axes(
            anterior_posterior_axis=self.anterior_posterior_axis.value[1][:, np.newaxis],
            infero_superior_axis=self.infero_superior_axis.value[1][:, np.newaxis],
            medio_lateral_axis=self.medio_lateral_axis.value[1][:, np.newaxis],
        )
    def is_mislabeled(self):

        condition_1 = (self.anterior_posterior is CartesianAxis.plusX) or (self.anterior_posterior is CartesianAxis.minusX)
        condition_2 = (self.infero_superior is CartesianAxis.plusY) or (self.infero_superior is CartesianAxis.minusY)
        condition_3 = (self.medio_lateral is CartesianAxis.plusZ) or (self.medio_lateral is CartesianAxis.minusZ)

        return not (condition_1 and condition_2 and condition_3)


    def is_frame_wrong_sens(self):

        is_ant_post_wrong_sens = is_axis_wrong_sens(self.anterior_posterior)
        is_med_lat_wrong_sens = is_axis_wrong_sens(self.medio_lateral)
        is_inf_sup_wrong_sens = is_axis_wrong_sens(self.infero_superior)

        return is_ant_post_wrong_sens or is_med_lat_wrong_sens or is_inf_sup_wrong_sens

    def has_wrong_direction(self):
        pass
    def get_risk_quantification(self,type_segment,type_risk):
        """
        Return the risk quantification of the segment
        """
        dict_coeff = dict()
        dict_coeff["proximal"] = dict()
        dict_coeff["distal"] = dict()

        dict_coeff["proximal"]["Rotation"]["Label"] = 0.9
        dict_coeff["proximal"]["Rotation"]["Sens"] = 0.9
        dict_coeff["proximal"]["Rotation"]["Origin"] = 0.9
        dict_coeff["proximal"]["Rotation"]["Direction"] = 0.5

        dict_coeff["proximal"]["Displacement"]["Label"] = 0.9
        dict_coeff["proximal"]["Displacement"]["Sens"] = 0.9
        dict_coeff["proximal"]["Displacement"]["Origin"] = 0.5
        dict_coeff["proximal"]["Displacement"]["Direction"] = 0.5

        dict_coeff["proximal"]["Rotation"]["Label"] = 0.9
        dict_coeff["proximal"]["Rotation"]["Sens"] = 0.9
        dict_coeff["proximal"]["Rotation"]["Origin"] = 0.9
        dict_coeff["proximal"]["Rotation"]["Direction"] = 0.5

        dict_coeff["proximal"]["Displacement"]["Label"] = 0.9
        dict_coeff["proximal"]["Displacement"]["Sens"] = 0.9
        dict_coeff["proximal"]["Displacement"]["Origin"] = 0.5
        dict_coeff["proximal"]["Displacement"]["Direction"] = 0.9


        risk = 1
        if not self.is_mislabeled():
            risk = risk * dict_coeff[type_segment][type_risk]["Label"]

        if not self.is_origin_isb():
            risk = risk * dict_coeff[type_segment][type_risk]["Origin"]

        if self.is_wrong_sens():
            risk = risk * dict_coeff[type_segment][type_risk]["Sens"]

        return risk

    def __print__(self):
        print(f"Segment: {self.segment}")
        print(f"Origin: {self.origin}")
        print(f"Anterior Posterior Axis: {self.anterior_posterior_axis}")
        print(f"Medio Lateral Axis: {self.medio_lateral_axis}")
        print(f"Infero Superior Axis: {self.infero_superior_axis}")

def is_axis_wrong_sens(axis)->bool:
    condition_1 = axis is CartesianAxis.minusX
    condition_2 = axis is CartesianAxis.minusY
    condition_3 = axis is CartesianAxis.minusZ

    return condition_1 or condition_2 or condition_3