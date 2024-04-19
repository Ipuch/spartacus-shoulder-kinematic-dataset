from pandas import DataFrame
from .quick_load import import_data


class DataFrameInterface:
    def __init__(self, dataframe: DataFrame):
        self.df = dataframe if dataframe is not None else import_data()

    @property
    def motions(self) -> list[str]:
        motions = self.df["humeral_motion"].unique()
        return motions if len(motions) > 1 else motions[0]

    @property
    def nb_mvt(self) -> int:
        return self.df["movement"].nunique()

    @property
    def nb_joints(self) -> int:
        return self.df["joint"].nunique()

    @property
    def nb_articles(self) -> int:
        return self.df["article_author_year"].nunique()

    @property
    def nb_units(self) -> int:
        return self.df["unit"].nunique()

    @property
    def nb_biomechanical_dof(self) -> int:
        return self.df["biomechanical_dof"].nunique()

    @property
    def biomechanical_dof(self) -> list[str]:
        return self.df["biomechanical_dof"].unique()

    @property
    def nb_dof(self) -> int:
        return self.df["degree_of_freedom"].nunique()

    def select_motion(self, motion: str) -> DataFrame:
        return self.df[self.df["humeral_motion"] == motion]

    def select_article(self, article: str) -> DataFrame:
        return self.df[self.df["article"] == article]

    def select_joint(self, joint: str) -> DataFrame:
        return self.df[self.df["joint"] == joint]
