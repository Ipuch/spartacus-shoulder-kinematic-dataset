from spartacus import DataFolder, load_subdataset


def main():
    spartacus_dataset = load_subdataset(name=DataFolder.BEGON_2014)
    print(spartacus_dataset.confident_data_values)
    return spartacus_dataset.corrected_confident_data_values


if __name__ == "__main__":
    data = main()
    print(data)
