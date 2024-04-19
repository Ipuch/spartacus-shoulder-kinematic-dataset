from spartacus import import_data, DataFrameInterface, DataPlanchePlotting
from pandas import DataFrame


def plot_mvt(df: DataFrame):

    humeral_motions = df["humeral_motion"].unique()

    for mvt in humeral_motions:
        sub_df = df[df["humeral_motion"] == mvt]
        dfi = DataFrameInterface(sub_df)
        plt = DataPlanchePlotting(dfi)
        plt.plot()
        plt.update_style()
        plt.show()
        plt.fig.write_image(f"{mvt}.png")
        plt.fig.write_image(f"{mvt}.pdf")
        plt.fig.write_html(f"{mvt}.html", include_mathjax="cdn")


def main():
    df = import_data(correction=True)
    plot_mvt(df)


def before_after():
    df_before = import_data(correction=False)
    df_after = import_data(correction=True)

    datasets = df_after["article"].unique()
    for dataset in datasets:
        sub_df_before = df_before[df_before["article"] == dataset]
        sub_df_after = df_after[df_after["article"] == dataset]
        plot_mvt(sub_df_before)
        plot_mvt(sub_df_after)


if __name__ == "__main__":
    main()
    before_after()
