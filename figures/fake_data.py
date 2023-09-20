import numpy as np
import pandas as pd


def create_random_data(
    name_article: str,
    name_joint: str,
    name_dof: str,
    angle_or_translation,
    name_movement: str,
    nb_frame: int,
    initialize: bool = False,
) -> pd.DataFrame:
    # Base structure for DataFrame
    data = {
        "article": [],
        "joint": [],
        "angle_translation": [],
        "degree_of_freedom": [],
        "movement": [],
        "humerothoracic_angle": [],
        "value": [],
    }

    if initialize:
        df = pd.DataFrame(data)
    else:
        if nb_frame is None:
            raise ValueError("nb_frame must be provided if not initializing with empty values.")

        random_x = np.linspace(0, 120, nb_frame)
        random_y0 = np.random.randn(nb_frame) + 5

        for key in ["article", "joint", "angle_translation", "degree_of_freedom", "movement"]:
            data[key] = [locals()[f"name_{key}"]] * nb_frame

        data["humerothoracic_angle"] = random_x
        data["value"] = random_y0
        df = pd.DataFrame(data)

    return df
