from spartacus import import_data, DataFrameInterface, DataPlanchePlotting


def main():
    export = True
    mvt = "frontal elevation"
    df = import_data(correction=True)
    sub_df = df[df["humeral_motion"] == mvt]
    dfi = DataFrameInterface(sub_df)
    plt = DataPlanchePlotting(dfi, restrict_to_joints=["scapulothoracic"])
    plt.plot()
    plt.update_style()
    plt.show()

    if export:
        plt.fig.write_image(f"../plots/{mvt}_scapulothoracic.png")
        plt.fig.write_image(f"../plots/{mvt}_scapulothoracic.pdf")
        plt.fig.write_html(f"../plots/{mvt}_scapulothoracic.html", include_mathjax="cdn")


if __name__ == "__main__":
    main()
