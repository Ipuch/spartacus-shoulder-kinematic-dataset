from .utils import TestUtils


def test_first_example():
    spartacus = TestUtils.spartacus_folder()
    module = TestUtils.load_module(spartacus + "/examples/first_example.py")
    confident_values = module.main()

    # verify the number of unique articles
    articles = list(confident_values["article"].unique())
    assert len(articles) == 9

    # Verify that the dataframe has the correct data
    Bourne2003 = confident_values[confident_values["article"] == "Bourne 2003"]
    assert Bourne2003.shape[0] == 2550
    humeral_motions = list(Bourne2003["humeral_motion"].unique())
    assert "frontal elevation" in humeral_motions
    assert "horizontal flexion" in humeral_motions

    joints = list(Bourne2003["joint"].unique())
    assert "scapulothoracic" in joints

    dofs = list(Bourne2003["degree_of_freedom"].unique())
    assert "1" in dofs
    assert "2" in dofs
    assert "3" in dofs

    # test three random values in the value columns and start and end
    assert Bourne2003["value"].iloc[0] == -16.3663
    assert Bourne2003["value"].iloc[1001] == 22.2405
    assert Bourne2003["value"].iloc[2000] == -38.2519
    assert Bourne2003["value"].iloc[-1] == 17.785

    Chu2012 = confident_values[confident_values["article"] == "Chu et al. 2012"]
    assert Chu2012.shape[0] == 96
    humeral_motions = list(Chu2012["humeral_motion"].unique())
    assert "frontal elevation" in humeral_motions
    assert "horizontal flexion" in humeral_motions
    assert "scapular elevation" in humeral_motions
    assert "internal rotation rotation 90 degree-abducted" in humeral_motions

    joints = list(Chu2012["joint"].unique())
    assert "scapulothoracic" in joints

    dofs = list(Chu2012["degree_of_freedom"].unique())
    assert "1" in dofs
    assert "2" in dofs
    assert "3" in dofs

    # test three random values in the value columns and start and end
    assert Chu2012["value"].iloc[0] == 20.8327
    assert Chu2012["value"].iloc[30] == -2.386
    assert Chu2012["value"].iloc[60] == -8.4559
    assert Chu2012["value"].iloc[-1] == -4.9707

    # Fung2001 = confident_values[confident_values["article"] == "Fung et al. 2001"]
    # todo

    Cereatti2017 = confident_values[confident_values["article"] == "Cereatti et al. 2017"]
    assert Cereatti2017.shape[0] == 3495
    humeral_motions = list(Cereatti2017["humeral_motion"].unique())

    assert "frontal elevation" in humeral_motions
    assert "sagittal elevation" in humeral_motions

    joints = list(Cereatti2017["joint"].unique())
    assert "glenohumeral" in joints

    dofs = list(Cereatti2017["degree_of_freedom"].unique())
    assert "1" in dofs
    assert "2" in dofs
    assert "3" in dofs

    # test three random values in the value columns and start and end
    assert Cereatti2017["value"].iloc[0] == 86.818
    assert Cereatti2017["value"].iloc[1001] == 58.179
    assert Cereatti2017["value"].iloc[2000] == -65.967
    assert Cereatti2017["value"].iloc[-1] == 63.876