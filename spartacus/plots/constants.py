import colorcet as cc
import seaborn as sns


BIOMECHANICAL_DOF_LEGEND = {
    "glenohumeral": ("plane of elevation", "elevation", "internal(+)/external(-) rotation"),
    "scapulothoracic": (
        "protraction(+)/retraction(-)",
        "medial(+)/lateral(-) rotation",
        "posterior(+)/anterior(-) tilt",
    ),
    "acromioclavicular": (
        "protraction(+)/retraction(-)",
        "medial(+)/lateral(-) rotation",
        "posterior(+)/anterior(-) tilt",
    ),
    "sternoclavicular": (
        "protraction(+)/retraction(-)",
        "depression(+)/elevation(-)",
        "backwards(+)/forward(-) rotation",
    ),
    "thoracohumeral": ("plane of elevation", "elevation", "internal(+)/external(-) rotation"),
}

TRANSLATIONAL_BIOMECHANICAL_DOF_LEGEND = {
    "glenohumeral": ("postero(-)/anterior(+)", "infero(-)/superior(+)", "medio(-)/lateral(+)"),
    "scapulothoracic": ("postero(-)/anterior(+)", "infero(-)/superior(+)", "medio(-)/lateral(+)"),
    "acromioclavicular": ("postero(-)/anterior(+)", "infero(-)/superior(+)", "medio(-)/lateral(+)"),
    "sternoclavicular": ("postero(-)/anterior(+)", "infero(-)/superior(+)", "medio(-)/lateral(+)"),
    "thoracohumeral": ("postero(-)/anterior(+)", "infero(-)/superior(+)", "medio(-)/lateral(+)"),
}

JOINT_ROW_COL_INDEX = {
    "glenohumeral": ((0, 0), (0, 1), (0, 2)),
    "scapulothoracic": ((1, 0), (1, 1), (1, 2)),
    "acromioclavicular": ((2, 0), (2, 1), (2, 2)),
    "sternoclavicular": ((3, 0), (3, 1), (3, 2)),
}


def author_colors_constant():
    palette = sns.color_palette(cc.glasbey, n_colors=24)
    palette_c = sns.color_palette(cc.glasbey_cool, n_colors=24)

    return {
        "Bourne": palette[0],
        "Cereatti et al.": palette[1],
        "Charbonnier et al.": palette[2],
        "Chu et al.": palette[3],
        "Begon et al.": palette[4],
        "Fung et al.": palette[5],
        "Gutierrez Delgado et al.": palette[6],
        "Kijima et al.": palette[7],
        "Kim et al.": palette[8],
        "Kolz et al.": palette[9],
        "Kozono et al.": palette[10],
        "Lawrence et al.": palette[11],
        "Matsuki et al.": palette[12],
        "Matsumura et al.": palette[15],
        "McClure et al.": palette[16],
        "Nishinaka et al.": palette[17],
        "Oki et al.": palette[18],
        "Sahara et al.": palette[19],
        "Sugi et al.": palette[21],
        "Teece et al.": palette[22],
        "Yoshida et al.": palette[23],
        "Bourne_corrected": palette_c[0],
        "Cereatti et al._corrected": palette_c[1],
        "Charbonnier et al_corrected": palette_c[2],
        "Chu et al._corrected": palette_c[3],
        "Begon et al._corrected": palette_c[4],
        "Fung et al._corrected": palette_c[5],
        "Gutierrez Delgado et al_corrected": palette_c[6],
        "Kijima et al._corrected": palette_c[7],
        "Kim et al._corrected": palette_c[8],
        "Kolz et al._corrected": palette_c[9],
        "Kozono et al._corrected": palette_c[10],
        "Lawrence et al._corrected": palette_c[11],
        "Matsuki et al._corrected": palette_c[12],
        "Matsumura et al. 2013_corrected": palette_c[15],
        "McClure et al._corrected": palette_c[16],
        "Nishinaka et al. 2008_corrected": palette_c[17],
        "Oki et al._corrected": palette_c[18],
        "Sahara et al._corrected": palette_c[19],
        "Sugi et al._corrected": palette_c[21],
        "Teece et al._corrected": palette_c[22],
        "Yoshida et al._corrected": palette_c[23],
    }


AUTHORS_COLORS = author_colors_constant()
