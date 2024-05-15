import numpy as np
import pytest

import spartacus as sp

spartacus_dataset = sp.load()
confident_values = spartacus_dataset.confident_data_values

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
    "Bourne et al.": (
        2550,
        ["frontal elevation", "horizontal flexion"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        32987.06725953286,
        [(0, -16.3663), (1001, 21.925651818083274), (2000, -38.92291527743668), (-1, 17.319848672019763)],
    ),
    "Chu et al.": (
        96,
        ["frontal elevation", "scapular elevation", "internal-external rotation 90 degree-abducted"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        -554.7492646716876,
        [(0, 20.8327), (30, -2.4029921148049445), (60, -8.436784721537704), (-1, -4.961429503563281)],
    ),
    "Fung et al.": (
        621,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        10808.1338,
        [(0, 36.8406), (30, 29.6062), (60, 18.136), (-1, 9.2942)],
    ),
    "Kijima et al.": (
        48,
        ["scapular elevation"],
        ["glenohumeral", "scapulothoracic"],
        ["1", "2", "3"],
        1149.815953912212,
        [(0, np.nan), (1, np.nan), (2, np.nan), (-1, 35.639)],
    ),
    "Cereatti et al. 2017": (
        3495,
        ["frontal elevation", "sagittal elevation"],
        ["glenohumeral"],
        ["1", "2", "3"],
        90447.72414830001,
        [(0, 86.818), (1001, 58.178999999999995), (2000, -65.967), (-1, 63.87599999999999)],
    ),
    "Kolz et al.": (
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
    "Kozono et al.": (
        30,
        ["internal-external rotation 0 degree-abducted"],
        ["glenohumeral"],
        ["1", "2", "3"],
        392.947,
        [(0, np.nan), (1, np.nan), (2, np.nan), (-1, 59.076)],
    ),
    "Ludewig et al.": (
        684,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["glenohumeral", "scapulothoracic", "acromioclavicular", "sternoclavicular"],
        ["1", "2", "3"],
        -3739.1000000000004,
        [(0, -8.6), (1, -12.0), (2, -15.5), (-1, 25.0)],
    ),
    "Matsumura et al.": (
        99,
        ["frontal elevation", "scapular elevation", "sagittal elevation"],
        ["scapulothoracic"],
        ["1", "2", "3"],
        -558.4569560038939,
        [(0, -23.068), (20, 32.595395315826835), (60, -0.8599417044686808), (-1, 11.971)],
    ),
    "Matsuki et al.": (
        288,
        ["scapular elevation"],
        ["glenohumeral"],
        ["1", "2", "3"],
        9303.5162527,
        [(0, np.nan), (1, np.nan), (2, np.nan), (-1, 79.56974273)],
    ),
    "Oki et al.": (
        354,
        ["frontal elevation", "sagittal elevation", "horizontal flexion"],
        ["scapulothoracic", "sternoclavicular"],
        ["1", "2", "3"],
        2343.222633228853,
        [(0, -23.5715), (100, 23.698003331400965), (200, 15.424283835508106), (-1, 31.7351)],
    ),
    "Teece et al.": (
        39,
        ["scapular elevation"],
        ["acromioclavicular"],
        ["1", "2", "3"],
        1061.3874465806718,
        [(0, 67.4405), (10, 69.0854773140717), (22, 6.135648345805435), (-1, 13.37)],
    ),
    "Yoshida et al.": (
        84,
        ["sagittal elevation"],
        ["glenohumeral", "scapulothoracic"],
        ["1", "2", "3"],
        2011.9508906100002,
        [(0, 2.8862207), (40, -20.767784), (65, 34.51266), (-1, 19.2415854)],
    ),
    # Add other articles here in the same format
}
transformed_data_article = [[name] + list(values) for name, values in articles_data.items()]


# This line parameterizes the test function below
@pytest.mark.parametrize(
    "article_name,expected_shape,humeral_motions,joints,dofs,total_value,random_checks", transformed_data_article
)
def test_article_data_no_correction(
    article_name, expected_shape, humeral_motions, joints, dofs, total_value, random_checks
):
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
