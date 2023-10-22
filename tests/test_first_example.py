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
        79.81940280567984,
        [(0, -1.7635787620698762), (1001, -0.15667834031565844), (2000, -0.20737280944999392), (-1, np.nan)],
    ),
    "Chu et al. 2012": (
        96,
        ["frontal elevation", "scapular elevation", "internal-external rotation 90 degree-abducted"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        -553.7318,
        [(0, 20.8327), (30, -2.386), (60, -8.4559), (-1, -4.9707)],
    ),
    # TODO: "Fung et al. 2001": (0, [], [], [], 0, []),
    "Cereatti et al. 2017": (
        3495,
        ["frontal elevation", "sagittal elevation"],
        ["glenohumeral"],
        ["1", "2", "3"],
        90447.72414830001,
        [(0, 86.818), (1001, 58.179), (2000, -65.967), (-1, 63.876)],
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
        1788111.3421318345,
        [(0, 16.7114492478597), (1001, 89.1886474934728), (40001, 2.1350129808377), (-1, 5.87426453808623)],
    ),
    "Kozono et al. 2017": (
        30,
        ["internal-external rotation 0 degree-abducted"],
        ["glenohumeral"],
        ["1", "2", "3"],
        0,
        [(0, np.nan), (1, np.nan), (2, np.nan), (-1, np.nan)],
    ),
    "Matsumura et al. 2013": (
        99,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        -558.322,
        [(0, -23.068), (20, 32.64), (60, -0.921), (-1, 11.971)],
    ),
    "Oki et al. 2012": (
        354,
        ["frontal elevation", "sagittal elevation", "horizontal flexion"],
        ["scapulothoracic", "sternoclavicular"],
        ["1", "2", "3"],
        2341.1053,
        [(0, -23.5715), (100, 23.6982), (200, 15.4229), (-1, 31.7351)],
    ),
    "Teece et al. 2008": (
        39,
        ["scapular elevation"],
        ["acromioclavicular"],
        ["1", "2", "3"],
        # 14.200462694343685,
        # [(0, 1.467054274614342), (10, -0.021138378975446268), (22, -0.11738530717958653), (-1, -2.3379632679489672)],
        -14.321849530406698,
        # [(0, -2.0737591719978203), (10, -2.672464827053776), (22, 34.51266), (-1, 19.2415854)],
        [(0, -2.0737591719978203), (10, -2.672464827053776), (22, -0.21841936528834072), (-1, -0.20111009003612457)],
    ),
    "Yoshida et al. 2023": (
        84,
        ["sagittal elevation"],
        ["glenohumeral", "scapulothoracic"],
        ["1", "2", "3"],
        912.7213939526243,
        [(0, -2.2092814772601055), (40, 2.8373811388792496), (65, 34.51266), (-1, 19.2415854)],
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
    assert len(articles) == 12


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
