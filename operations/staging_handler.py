import pandas as pd
from sqlalchemy import create_engine

from config import STAGING_DATABASE_URI


class StagingHandler:


    def __init__(self) -> None:
        self.STAGING_DATABASE_URI = STAGING_DATABASE_URI


    def extract(self, query:str) -> pd.DataFrame:
        """Extracts data from staging database."""
        df = None
        engine = create_engine(self.STAGING_DATABASE_URI, echo=False)
        with engine.begin() as connection:
            df = pd.read_sql(query, connection)
        return df


    def load(self, df:pd.DataFrame, table_name:str) -> None:
        """Loads data to staging database."""
        engine = create_engine(self.STAGING_DATABASE_URI, echo=False)
        with engine.begin() as connection:
            df.to_sql(table_name, con=connection, if_exists='replace', index=False, method='multi')
