import numpy as np
import pytest

from .utils import TestUtils


# Data for each article test
articles_data = {
    ## "Article name": (
    # expected_shape i.e. number of rows
    # humeral_motions i.e. list of humeral motions
    # joints i.e. list of joints
    # dofs i.e. list of degrees of freedom
    # total_value i.e. sum of all values
    # random_checks i.e. list of tuples (index, value) to check
    # ),
    "Bourne 2003": (
        2550,
        ["frontal elevation", "horizontal flexion"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        # 31552.337999999996,
        # [(0, -16.3663), (1001, 22.2405), (2000, -38.2519), (-1, 17.785)],
        202.98869187659378,
        [(0, 2.4832559215387606), (1001, -0.24935142487144815), (2000, 2.588804496667313), (-1, np.nan)],
    ),
    "Chu et al. 2012": (
        96,
        ["frontal elevation", "scapular elevation", "internal-external rotation 90 degree-abducted"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        -10.212028626928308,
        [(0, 1.9831440784612397), (30, 0.7555926535897932), (60, 0.96887796076938), (-1, -1.8291073464102066)],
    ),
    "Fung et al. 2001": (
        621,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        61.749177553987906,
        [(0, 2.2830808105122764), (30, -1.8097265358979313), (60, 2.428036732051033), (-1, -0.1305779607693797)],
    ),
    "Kijima et al. 2015": (
        24,
        ["scapular elevation"],
        ["glenohumeral", "scapulothoracic"],
        ["1", "2", "3"],
        6.31180992544895,
        [(0, np.nan), (1, np.nan), (2, np.nan), (-1, 0.7169817831629339)],
    ),
    "Cereatti et al. 2017": (
        3495,
        ["frontal elevation", "sagittal elevation"],
        ["glenohumeral"],
        ["1", "2", "3"],
        1284.7791450076659,
        [(0, -1.146594300514213), (1001, 1.6303322353837237), (2000, -3.1351469282041338), (-1, 1.044146928204133)],
    ),
    "Kolz et al. 2020": (
        80862,
        [
            "frontal elevation",
            "scapular elevation",
            "sagittal elevation",
            "internal-external rotation 0 degree-abducted",
            "internal-external rotation 90 degree-abducted",
        ],
        ["glenohumeral", "scapulothoracic"],
        ["1", "2", "3"],
        20020.585716495105,
        [(0, -2.5685520015275887), (1001, 1.014615081297844), (40001, -1.3503417465344325), (-1, 2.2967864636674706)],
    ),
    "Kozono et al. 2017": (
        30,
        ["internal-external rotation 0 degree-abducted"],
        ["glenohumeral"],
        ["1", "2", "3"],
        0,
        [(0, np.nan), (1, np.nan), (2, np.nan), (-1, np.nan)],
    ),
    "Lawrence et al. 2014": (
        684,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["glenohumeral", "scapulothoracic", "acromioclavicular", "sternoclavicular"],
        ["1", "2", "3"],
        114.76964130026826,
        [(0, 1.9527515541902896), (1, 2.927958598494005), (2, -1.5148684762422286), (-1, 3.0088514248714473)],
    ),
    "Matsumura et al. 2013": (
        99,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        -10.935616210245463,  # Repeating total value here as a placeholder
        [(0, -1.0768514248714487), (20, 1.224073464102068), (60, -0.9209999999999999), (-1, -0.5953706143591729)],
    ),
    "Matsuki et al. 2012": (
        288,
        ["scapular elevation"],
        ["glenohumeral"],
        ["1", "2", "3"],
        0,
        [(0, np.nan), (1, np.nan), (2, np.nan), (-1, np.nan)],
    ),
    "Oki et al. 2012": (
        354,
        ["frontal elevation", "sagittal elevation", "horizontal flexion"],
        ["scapulothoracic", "sternoclavicular"],
        ["1", "2", "3"],
        2.847632105884358,
        [(0, 1.5612412287183455), (100, -1.4345412287183459), (200, 2.8565293856408274), (-1, -2.8224191894877264)],
    ),
    "Teece et al. 2008": (
        39,
        ["scapular elevation"],
        ["acromioclavicular"],
        ["1", "2", "3"],
        # 14.200462694343685,
        # [(0, 1.467054274614342), (10, -0.021138378975446268), (22, -0.11738530717958653), (-1, -2.3379632679489672)],
        # -14.321849530406698,
        # # [(0, -2.0737591719978203), (10, -2.672464827053776), (22, 34.51266), (-1, 19.2415854)],
        # [(0, -2.0737591719978203), (10, -2.672464827053776), (22, -0.21841936528834072), (-1, -0.20111009003612457)],
        -1.3330213407053026,  # Repeating total value here as a placeholder
        [(0, 1.1295762740086535), (10, -0.34625090695979804), (22, 0.03499430083367185), (-1, -2.3533873098833027)],
        # Random checks
    ),
    "Yoshida et al. 2023": (
        84,
        ["sagittal elevation"],
        ["glenohumeral", "scapulothoracic"],
        ["1", "2", "3"],
        21.200080110308463,
        [(0, -2.2092814772601055), (40, 2.8373811388792496), (65, 0.04485918948772884), (-1, -2.749563175128551)],
    ),
    # Add other articles here in the same format
}
transformed_data_article = [[name] + list(values) for name, values in articles_data.items()]


spartacus = TestUtils.spartacus_folder()
module = TestUtils.load_module(spartacus + "/examples/first_example.py")
confident_values = module.main()


# This line parameterizes the test function below
@pytest.mark.parametrize(
    "article_name,expected_shape,humeral_motions,joints,dofs,total_value,random_checks", transformed_data_article
)
def test_article_data(article_name, expected_shape, humeral_motions, joints, dofs, total_value, random_checks):
    data = confident_values[confident_values["article"] == article_name]
    print_data(data, random_checks)
    assert data.shape[0] == expected_shape

    for motion in humeral_motions:
        assert motion in data["humeral_motion"].unique()
    assert len(data["humeral_motion"].unique()) == len(humeral_motions)

    for joint in joints:
        assert joint in data["joint"].unique()
    assert len(data["joint"].unique()) == len(joints)

    for dof in dofs:
        assert dof in data["degree_of_freedom"].unique()
    assert len(data["degree_of_freedom"].unique()) == len(dofs)

    for idx, value in random_checks:
        np.testing.assert_almost_equal(data["value"].iloc[idx], value)

    np.testing.assert_almost_equal(data["value"].sum(), total_value, decimal=10)


def test_number_of_articles():
    # Check number of unique articles after processing all
    articles = list(confident_values["article"].unique())

    assert [
        "Bourne 2003",
        "Chu et al. 2012",
        "Cereatti et al. 2017",
        "Fung et al. 2001",
        "Kijima et al. 2015",
        "Kolz et al. 2020",
        "Kozono et al. 2017",
        "Lawrence et al. 2014",
        "Matsumura et al. 2013",
        "Matsuki et al. 2012",
        "Oki et al. 2012",
        "Teece et al. 2008",
        "Yoshida et al. 2023",
    ] == articles

    assert len(articles) == 13

    assert confident_values.shape[0] == 89250


def print_data(data, random_checks):
    print("\n")
    print("Shape:", data.shape)
    print("Humeral motions:", data["humeral_motion"].unique())
    print("Joints:", data["joint"].unique())
    print("Degrees of freedom:", data["degree_of_freedom"].unique())
    print("Total value:", data["value"].sum())
    print("Random checks:")
    for idx, value in random_checks:
        print(f"    {idx}: {data['value'].iloc[idx]}")
    print("")
