from spartacus import import_data, DataFrameInterface, DataPlanchePlotting
from pandas import DataFrame
import os


def plot_mvt(df: DataFrame, dataset: str = ".", suffix: str = ""):

    humeral_motions = df["humeral_motion"].unique()

    for mvt in humeral_motions:
        sub_df = df[df["humeral_motion"] == mvt]
        dfi = DataFrameInterface(sub_df)
        plt = DataPlanchePlotting(dfi)
        plt.plot()
        plt.update_style()
        plt.show()

        plt.fig.write_image(f"{dataset+"/"}{mvt}{suffix}.png")
        plt.fig.write_image(f"{dataset+"/"}{mvt}{suffix}.pdf")
        plt.fig.write_html(f"{dataset+"/"}{mvt}{suffix}.html", include_mathjax="cdn")


def main():
    df = import_data(correction=True)
    plot_mvt(df)


def before_after():
    df_before = import_data(correction=False)
    df_after = import_data(correction=True)

    datasets = df_after["article"].unique()
    for dataset in datasets:

        if not os.path.exists(dataset):
            os.mkdir(dataset)

        sub_df_before = df_before[df_before["article"] == dataset]
        sub_df_after = df_after[df_after["article"] == dataset]
        plot_mvt(sub_df_before, dataset, suffix="_before")
        plot_mvt(sub_df_after, dataset, suffix="_after")


if __name__ == "__main__":
    main()
    before_after()
