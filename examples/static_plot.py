import numpy as np

from pandas import DataFrame
from plotly import graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

from spartacus import import_data
from spartacus.plots.constants import AUTHORS_COLORS, JOINT_ROW_COL_INDEX, BIOMECHANICAL_DOF_LEGEND


class DataFrameInterface:
    def __init__(self, dataframe: DataFrame):
        self.df = dataframe if dataframe is not None else import_data()

    @property
    def nb_mvt(self) -> int:
        return self.df["movement"].nunique()

    @property
    def nb_joints(self) -> int:
        return self.df["joint"].nunique()

    @property
    def nb_articles(self) -> int:
        return self.df["article_author_year"].nunique()

    @property
    def nb_units(self) -> int:
        return self.df["unit"].nunique()

    @property
    def nb_biomechanical_dof(self) -> int:
        return self.df["biomechanical_dof"].nunique()

    @property
    def biomechanical_dof(self) -> list[str]:
        return self.df["biomechanical_dof"].unique()

    @property
    def nb_dof(self) -> int:
        return self.df["degree_of_freedom"].nunique()

    def select_motion(self, motion: str) -> DataFrame:
        return self.df[self.df["humeral_motion"] == motion]

    def select_article(self, article: str) -> DataFrame:
        return self.df[self.df["article"] == article]

    def select_joint(self, joint: str) -> DataFrame:
        return self.df[self.df["joint"] == joint]

    def plot_motion(self, motion: str):
        pass


class DataPlanchePlotting:
    def __init__(self, dfi: DataFrameInterface):
        self.dfi = dfi
        self.fig = make_subplots(
            shared_xaxes=False,
            shared_yaxes=False,
            rows=4,
            cols=3,
            subplot_titles=self._rotation_titles,
        )
        self.showlegend = True

    @property
    def _rotation_titles(self) -> list[str]:
        suplot_titles = [list(v) for _, v in BIOMECHANICAL_DOF_LEGEND.items()]
        return [item for sublist in suplot_titles for item in sublist]

    def plot(self):
        for article in self.dfi.df["article"].unique():
            self.showlegend = True
            self.plot_article(name=article)

    def plot_article(self, name):
        sub_dfi = DataFrameInterface(self.dfi.select_article(article=name))
        for j, joint in enumerate(BIOMECHANICAL_DOF_LEGEND.keys()):
            sub_df_j = sub_dfi.select_joint(joint)

            if sub_df_j.empty:
                continue

            self.plot_dofs(article=name, joint=joint)

    def plot_dofs(self, article, joint):
        sub_dfi = DataFrameInterface(self.dfi.select_article(article=article))
        sub_df_j = sub_dfi.select_joint(joint)

        dofs = sub_df_j["degree_of_freedom"].unique()

        for i, dof in enumerate(dofs):
            self.plot_dof(article, joint, dof)

    def plot_dof(self, article, joint, dof):
        sub_dfi = DataFrameInterface(self.dfi.select_article(article=article))
        sub_df_j = sub_dfi.select_joint(joint)
        sub_df_ij = sub_df_j[sub_df_j["degree_of_freedom"] == dof]
        row, col = JOINT_ROW_COL_INDEX[joint][dof - 1]
        subjects = sub_df_ij["shoulder_id"].unique()

        if len(subjects) > 1:
            for s in subjects:
                sub_df_ij_s = sub_df_ij[sub_df_ij["shoulder_id"] == s]
                self.plot_timeserie(sub_df_ij_s, article, row, col)
        else:
            self.plot_timeserie(sub_df_ij, article, row, col)

        row, col_left = JOINT_ROW_COL_INDEX[joint][0]
        self.fig.update_yaxes(title_text=f"{joint[0].upper()}{joint[1:].lower()}", row=row + 1, col=col_left + 1)

    def plot_timeserie(self, df, article, row, col):
        self.fig.add_trace(
            go.Scatter(
                x=df["humerothoracic_angle"],
                y=df["value"],
                name=article,
                legendgroup=article,
                showlegend=self.showlegend,
                # legend=article_0,
                mode="lines+markers",
                opacity=0.5,
                marker=dict(
                    size=2,
                    color=f"rgba{AUTHORS_COLORS[article]}",
                    # line=dict(width=0.5),
                ),
                line=dict(
                    width=0.5,
                    color=f"rgba{AUTHORS_COLORS[article]}",
                ),
            ),
            row=row + 1,
            col=col + 1,
        )
        self.showlegend = False

    def update_style(self):
        self.fig.update_layout(
            # If we fix only the height the width will be adapted to the size of the screen
            # However not fixing the height AND the width make the graph not readable
            height=1000,
            width=1000,
            paper_bgcolor="rgba(255,255,255,1)",
            plot_bgcolor="rgba(255,255,255,1)",
            legend=dict(
                title_font_family="Times New Roman",
                font=dict(family="Times New Roman", color="black", size=16),
                orientation="v",
                x=1,
                y=1,
            ),
            font=dict(
                size=16,
                family="Times New Roman",
            ),
            yaxis=dict(color="black"),
            template="simple_white",
            boxgap=0.1,
        )

    def show(self):
        self.fig.show()


def main():

    df = import_data(correction=False)
    # df = import_data(correction=True)

    humeral_motions = df["humeral_motion"].unique()

    for mvt in humeral_motions:
        sub_df = df[df["humeral_motion"] == mvt]
        dfi = DataFrameInterface(sub_df)
        plt = DataPlanchePlotting(dfi)
        plt.plot()
        # plt.plot_article(name="Bourne 2003")
        plt.update_style()
        plt.show()
        plt.fig.write_image(f"{mvt}.png")
        plt.fig.write_image(f"{mvt}.pdf")
        plt.fig.write_html(f"{mvt}.html", include_mathjax="cdn")  #


if __name__ == "__main__":
    main()
