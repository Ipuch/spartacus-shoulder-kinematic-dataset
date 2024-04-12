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

JOINT_ROW_COL_INDEX = {
    "glenohumeral": ((0, 0), (0, 1), (0, 2)),
    "scapulothoracic": ((1, 0), (1, 1), (1, 2)),
    "acromioclavicular": ((2, 0), (2, 1), (2, 2)),
    "sternoclavicular": ((3, 0), (3, 1), (3, 2)),
}


def author_colors_constant():
    palette = sns.color_palette(cc.glasbey, n_colors=24)

    return {
        "Bourne 2003": palette[0],
        "Cereatti et al. 2017": palette[1],
        "Charbonnier et al 2014": palette[2],
        "Chu et al. 2012": palette[3],
        "Dal Maso et al. 2014": palette[4],
        "Fung et al. 2001": palette[5],
        "Gutierrez Delgado et al 2017": palette[6],
        "Kijima et al. 2015": palette[7],
        "Kim et al. 2017": palette[8],
        "Kolz et al. 2020": palette[9],
        "Kozono et al. 2017": palette[10],
        "Lawrence et al. 2014": palette[11],
        "Matsuki et al. 2011": palette[12],
        "Matsuki et al. 2012": palette[13],
        "Matsuki et al. 2014": palette[14],
        "Matsumura et al. 2013": palette[15],
        "McClure et al. 2001": palette[16],
        "Nishinaka et al. 2008": palette[17],
        "Oki et al. 2012": palette[18],
        "Sahara et al. 2006": palette[19],
        "Sahara et al. 2007": palette[20],
        "Sugi et al. 2021": palette[21],
        "Teece et al. 2008": palette[22],
        "Yoshida et al. 2023": palette[23],
    }


AUTHORS_COLORS = author_colors_constant()
