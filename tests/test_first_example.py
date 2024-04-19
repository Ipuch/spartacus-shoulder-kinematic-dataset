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
        30304.3459,
        [(0, -16.366300000000003), (1001, 22.2405), (2000, -38.251900000000006), (-1, np.nan)],
    ),
    "Chu et al. 2012": (
        96,
        ["frontal elevation", "scapular elevation", "internal-external rotation 90 degree-abducted"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        -553.7318,
        [(0, 20.832700000000003), (30, -2.386), (60, -8.4559), (-1, -4.9707)],
    ),
    "Fung et al. 2001": (
        621,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        3676.4321999999997,
        [(0, 36.84060000000001), (30, 29.6062), (60, 18.136000000000003), (-1, 9.294200000000002)],
    ),
    "Kijima et al. 2015": (
        48,
        ["scapular elevation"],
        ["glenohumeral", "scapulothoracic"],
        ["1", "2", "3"],
        306.44232769340545,
        [(0, np.nan), (1, np.nan), (2, np.nan), (-1, 7.412221776556216)],
    ),
    "Cereatti et al. 2017": (
        3495,
        ["frontal elevation", "sagittal elevation"],
        ["glenohumeral"],
        ["1", "2", "3"],
        90447.72414830001,
        [(0, 86.818), (1001, 58.178999999999995), (2000, -65.967), (-1, 63.87599999999999)],
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
        1856259.0365862055,
        [(0, -20.35748376107582), (1001, 80.21966852594535), (40001, -16.285172647839502), (-1, 15.158979447120556)],
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
        12601.038459374904,
        [(0, 137.332189001885), (1, 138.62633045180257), (2, 139.82856070895113), (-1, 25.0)],
    ),
    "Matsumura et al. 2013": (
        99,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        -558.3220000000001,
        [(0, -23.068), (20, 32.64), (60, -0.921), (-1, 11.971)],  # Repeating total value here as a placeholder
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
        2341.1053,
        [(0, -23.571499999999997), (100, 23.6982), (200, 15.422899999999998), (-1, 31.735099999999992)],
    ),
    "Teece et al. 2008": (
        39,
        ["scapular elevation"],
        ["acromioclavicular"],
        ["1", "2", "3"],
        1070.389125329676,  # Repeating total value here as a placeholder
        [(0, 53.20906080633492), (10, 55.354366143249585), (22, 12.68647863928707), (-1, 21.701799415162878)],
        # Random checks
    ),
    "Yoshida et al. 2023": (
        84,
        ["sagittal elevation"],
        ["glenohumeral", "scapulothoracic"],
        ["1", "2", "3"],
        1445.1089898448326,
        [(0, -44.304576869953905), (40, -16.641814272341282), (65, 34.51266), (-1, 19.2415854)],
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
        print(f"Data {idx}: {data['value'].iloc[idx]}")
        print(f"Check {idx}: {value}")
    print("")
