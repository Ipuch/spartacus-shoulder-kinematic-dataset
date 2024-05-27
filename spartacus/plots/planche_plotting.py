import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from .constants import (
    BIOMECHANICAL_DOF_LEGEND,
    TRANSLATIONAL_BIOMECHANICAL_DOF_LEGEND,
    JOINT_ROW_COL_INDEX,
    AUTHORS_COLORS,
)
from .dataframe_interface import DataFrameInterface
from ..src.enums import JointType


def get_color(article):
    """
    Get the color of the article.
    If the article is not in the AUTHORS_COLORS dict, a random color is generated.
    """
    color = AUTHORS_COLORS.get(article)
    opacity = 0.5
    if color is None:
        random_ints = np.random.randint(0, 255, 3).tolist() + [opacity]
        #     turn it in to a tuple[int]
        random_ints = tuple(random_ints)
        color = f"rgba{random_ints}"
    else:
        color = f"rgba{tuple(list(color) + [opacity])}"

    return color


class DataPlanchePlotting:
    def __init__(self, dfi: DataFrameInterface, restrict_to_joints: list[str | JointType] = None):

        if dfi.has_translations_and_rotations:
            raise ValueError("The DataFrameInterface must contain only rotational data or translation data, not both.")

        self.rotations = dfi.has_rotational_data

        self.restrict_to_joints = restrict_to_joints

        self.fig = self.make_fig(rotation=self.rotations)

        self.dfi = dfi
        self.opacity = 0.5 if self.dfi.nb_articles > 1 else 1

        self.showlegend = True

    @property
    def nb_joints(self):
        return len(self.restrict_to_joints) if self.restrict_to_joints is not None else 4

    @property
    def joints(self):
        return self.restrict_to_joints if self.restrict_to_joints is not None else BIOMECHANICAL_DOF_LEGEND.keys()

    def joint_row_col_index(self, joint):
        count = 0
        for j in JOINT_ROW_COL_INDEX.keys():
            if j == joint:
                break
            if not j in joint:
                count -= 1

        return [(JOINT_ROW_COL_INDEX[joint][i][0] + count, JOINT_ROW_COL_INDEX[joint][i][1]) for i in range(3)]

    def make_fig(self, rotation: bool = True):
        return make_subplots(
            shared_xaxes=False,
            shared_yaxes=True,
            rows=self.nb_joints,
            cols=3,
            subplot_titles=self._rotation_titles if rotation else self._translation_titles,
        )

    @property
    def _rotation_titles(self) -> list[str]:
        suplot_titles = [list(BIOMECHANICAL_DOF_LEGEND[j]) for j in self.joints]
        return [item for sublist in suplot_titles for item in sublist]

    @property
    def _translation_titles(self) -> list[str]:
        suplot_titles = [list(TRANSLATIONAL_BIOMECHANICAL_DOF_LEGEND[j]) for j in self.joints]
        return [item for sublist in suplot_titles for item in sublist]

    def plot(self):
        for article in self.dfi.df["article"].unique():
            self.showlegend = True
            self.plot_article(name=article)

    def plot_article(self, name):
        sub_dfi = DataFrameInterface(self.dfi.select_article(article=name))
        color = get_color(name)
        for j, joint in enumerate(self.joints):
            sub_df_j = sub_dfi.select_joint(joint)

            if sub_df_j.empty:
                continue

            self.plot_dofs(article=name, joint=joint, color=color)

    def plot_dofs(self, article, joint, color):
        sub_dfi = DataFrameInterface(self.dfi.select_article(article=article))
        sub_df_j = sub_dfi.select_joint(joint)

        dofs = sub_df_j["degree_of_freedom"].unique()

        for i, dof in enumerate(dofs):
            self.plot_dof(article, joint, dof, color)

    def plot_dof(self, article, joint, dof, color):
        sub_dfi = DataFrameInterface(self.dfi.select_article(article=article))
        sub_df_j = sub_dfi.select_joint(joint)
        sub_df_ij = sub_df_j[sub_df_j["degree_of_freedom"] == dof]
        row, col = self.joint_row_col_index(joint)[dof - 1]
        subjects = sub_df_ij["shoulder_id"].unique()

        if len(subjects) > 1:
            for s in subjects:
                sub_df_ij_s = sub_df_ij[sub_df_ij["shoulder_id"] == s]
                self.plot_timeserie(sub_df_ij_s, article, row, col, color)
        else:
            self.plot_timeserie(sub_df_ij, article, row, col, color)

        row, col_left = self.joint_row_col_index(joint)[0]
        self.fig.update_yaxes(title_text=f"{joint[0].upper()}{joint[1:].lower()}", row=row + 1, col=col_left + 1)

    def plot_timeserie(self, df, article, row, col, color):
        self.fig.add_trace(
            go.Scatter(
                x=df["humerothoracic_angle"],
                y=df["value"],
                name=f"{article}",
                legendgroup=article,
                showlegend=self.showlegend,
                mode="lines+markers",
                opacity=self.opacity,
                marker=dict(
                    size=2,
                    color=color,
                ),
                line=dict(
                    width=0.5,
                    color=color,
                ),
            ),
            row=row + 1,
            col=col + 1,
        )

        # self.fig.update_xaxes(row=row + 1, col=col + 1, range=[-150, 180])
        grid_color = "rgba(0, 0, 0, 0.1)"
        n_ticks = 8  # It doesnt seem to exactly fit the number specified
        self.fig.update_xaxes(gridcolor=grid_color, row=row + 1, col=col + 1, showgrid=True, nticks=n_ticks)
        self.fig.update_yaxes(gridcolor=grid_color, row=row + 1, col=col + 1, showgrid=True, nticks=n_ticks)
        self.showlegend = False

    def update_style(self):
        self.fig.update_layout(
            # If we fix only the height the width will be adapted to the size of the screen
            # However not fixing the height AND the width make the graph not readable
            height=1000 * self.nb_joints / 4 if self.nb_joints >= 2 else 350,
            width=1000,
            paper_bgcolor="rgba(255,255,255,1)",
            plot_bgcolor="rgba(255,255,255,1)",
            legend=dict(
                title_font_family="Times New Roman",
                font=dict(family="Times New Roman", color="black", size=16),
                orientation="v" if self.nb_joints > 2 else "h",
                x=1 if self.nb_joints > 2 else 0.5,
                y=1.1 if self.nb_joints > 2 else -0.2,
                xanchor="left" if self.nb_joints > 2 else "center",
            ),
            font=dict(
                size=16,
                family="Times New Roman",
            ),
            yaxis=dict(color="black"),
            template="simple_white",
            boxgap=0.1,
            title="<b>Shoulder kinematics</b> <br>" + f"<i>{self.dfi.motions}</i>",
            title_x=0.5,
            title_yanchor="middle",
            title_y=0.965,
        )
        self.fig.update_xaxes(title_text="Humerothoracic angle (°)", row=4, col=1)
        self.fig.update_xaxes(title_text="Humerothoracic angle (°)", row=4, col=2)
        self.fig.update_xaxes(title_text="Humerothoracic angle (°)", row=4, col=3)

    def show(self):
        self.fig.show()
