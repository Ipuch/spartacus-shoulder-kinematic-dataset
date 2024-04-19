from spartacus import import_data

df_before = import_data(correction=False)
df_after = import_data(correction=True)


def test_bourne2003():
    dataset = "Bourne 2003"
    sub_df_before = df_before[df_before["article"] == dataset]
    sub_df_after = df_after[df_after["article"] == dataset]

    # test the length to be equal in both dataframes
    assert len(sub_df_before) == len(sub_df_after)
