class Deviation:

    @staticmethod
    def confidence_euler_sequence(row_data) -> float:
        """
        Quantify the confidence of the joint euler sequence associated with the row_data.
        """
        if row_data.is_joint_euler_angle_ISB_with_adaptation_from_segment():
            risk = 1.0
        else:
            risk = 0.5
        return risk

    @staticmethod
    def confidence_segment_proximal(row_data, type_risk: str) -> float:
        """
        Quantify the confidence associated to proximal segment with the row_data and the type of risk.

        Parameters
        ----------
        row_data: RowData
        type_risk: str
            "rotation" or "translation"
        """
        risk = row_data.parent_biomech_sys.get_segment_risk_quantification("proximal", type_risk)
        return risk

    @staticmethod
    def confidence_segment_distal(row_data, type_risk: str) -> float:
        """
        Quantify the confidence associated to distal segment with the row_data and the type of risk.

        Parameters
        ----------
        row_data: RowData
        type_risk: str
            "rotation" or "translation"
        """
        risk = row_data.child_biomech_sys.get_segment_risk_quantification("distal", type_risk)
        return risk

    @staticmethod
    def confidence_segment(row_data, type_risk: str) -> float:
        """
        Quantify the confidence associated to both proximal and distal segment with the row_data and the type of risk.

        Parameters
        ----------
        row_data: RowData
        type_risk: str
            "rotation" or "translation"
        """
        risk_parent = Deviation.confidence_segment_proximal(row_data, type_risk)
        risk_child = Deviation.confidence_segment_distal(row_data, type_risk)

        return risk_child * risk_parent

    @staticmethod
    def confidence_total(row_data, type_risk: str) -> float:
        """
        Quantify the total confidence associated with the row_data and the type of risk.

        Parameters
        ----------
        row_data: RowData
        type_risk: str
            "rotation" or "translation"
        """
        euler = Deviation.confidence_euler_sequence(row_data)
        segment = Deviation.confidence_segment(row_data, type_risk)

        return euler * segment
