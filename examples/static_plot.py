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


def main():

    df = import_data(correction=False)
    # df = import_data(correction=True)

    sub_df = df[df["humeral_motion"] == "frontal elevation"]
    dfi = DataFrameInterface(sub_df)
    # BIOMECHANICAL_DOF_LEGEND, turn values of dict as list, breaking tuples
    suplot_titles = [list(v) for _, v in BIOMECHANICAL_DOF_LEGEND.items()]
    suplot_titles = [item for sublist in suplot_titles for item in sublist]

    fig = make_subplots(
        shared_xaxes=False,
        shared_yaxes=False,
        rows=dfi.nb_joints,
        cols=dfi.nb_dof,
        subplot_titles=suplot_titles,
    )

    article_0 = dfi.df["article"].unique()[0]
    sub_df = dfi.df[dfi.df["article"] == article_0]
    sub_dfi = DataFrameInterface(sub_df)
    legend_showed = True
    for i, joint in enumerate(BIOMECHANICAL_DOF_LEGEND.keys()):
        sub_df_i = sub_df[sub_df["joint"] == joint]

        if sub_df_i.empty:
            continue

        dofs = sub_df_i["degree_of_freedom"].unique()

        for j, dof in enumerate(dofs):
            sub_df_ij = sub_df_i[sub_df_i["degree_of_freedom"] == dof]
            row, col = JOINT_ROW_COL_INDEX[joint][dof - 1]

            subjects = sub_df_ij["shoulder_id"].unique()
            if subjects.size == 0:
                fig.add_trace(
                    go.Scatter(
                        x=sub_df_ij["humerothoracic_angle"],
                        y=sub_df_ij["value"],
                        name=article_0,
                        legendgroup=article_0,
                        showlegend=legend_showed,
                        # legend=article_0,
                        mode="lines+markers",
                        opacity=0.5,
                        marker=dict(
                            size=2,
                            color=f"rgba{AUTHORS_COLORS[article_0]}",
                            # line=dict(width=0.5),
                        ),
                        line=dict(
                            width=0.5,
                            color=f"rgba{AUTHORS_COLORS[article_0]}",
                        ),
                    ),
                    row=row + 1,
                    col=col + 1,
                )
                legend_showed = False
            else:
                for s in subjects[0]:
                    # for s in subjects:
                    sub_df_ij_s = sub_df_ij[sub_df_ij["shoulder_id"] == s]
                    fig.add_trace(
                        go.Scatter(
                            x=sub_df_ij_s["humerothoracic_angle"],
                            y=sub_df_ij_s["value"],
                            name=article_0,
                            legendgroup=article_0,
                            showlegend=legend_showed,
                            # legend=article_0,
                            mode="lines+markers",
                            opacity=0.5,
                            marker=dict(
                                size=2,
                                color=f"rgba{AUTHORS_COLORS[article_0]}",
                                # line=dict(width=0.5),
                            ),
                            line=dict(
                                width=0.5,
                                color=f"rgba{AUTHORS_COLORS[article_0]}",
                            ),
                        ),
                        row=row + 1,
                        col=col + 1,
                    )
                    legend_showed = False

        row, col_left = JOINT_ROW_COL_INDEX[joint][0]
        fig.update_yaxes(title_text=f"{joint[0].upper()}{joint[1:].lower()}", row=row + 1, col=col_left + 1)
        # fig.update_traces(
        #     #     markersize
        #     # marker=dict(size=1, opacity=0.3),
        #     # line=dict(width=1, opacity=0.3),
        # )

    fig.update_layout(
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

    fig.show()


if __name__ == "__main__":
    main()
