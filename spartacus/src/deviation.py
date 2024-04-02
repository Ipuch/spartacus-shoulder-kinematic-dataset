class Deviation:

    @staticmethod
    def risk_euler_sequence(row_data) -> float:
        """
        Quantify the risk of the joint euler sequence.
        """
        if row_data.is_joint_euler_angle_ISB_with_adaptation_from_segment():
            risk = 1.0
        else:
            risk = 0.5
        return risk

    @staticmethod
    def risk_segment_proximal(row_data, type_risk) -> float:
        """
        Quantify the risk of the joint.
        """
        risk = row_data.parent_biomech_sys.get_segment_risk_quantification("proximal", type_risk)
        return risk

    @staticmethod
    def risk_segment_distal(row_data, type_risk) -> float:
        """
        Quantify the risk of the joint.
        """
        risk = row_data.child_biomech_sys.get_segment_risk_quantification("distal", type_risk)
        return risk

    @staticmethod
    def risk_segment(self, row_data, type_risk) -> float:
        """
        Quantify the risk of the joint.
        """
        risk_parent = self.risk_segment_proximal(row_data, type_risk)
        risk_child = self.risk_segment_distal(row_data, type_risk)

        return risk_child * risk_parent

    @staticmethod
    def total_risk(self, row_data, type_risk) -> float:
        """
        Quantify the risk of the joint.
        """
        euler = self.risk_euler_sequence(row_data)
        segment = self.risk_segment(row_data, type_risk)

        return euler * segment
