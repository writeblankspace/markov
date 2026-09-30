import os

from dotenv import load_dotenv


class Config:
    _censor_path: str
    _db_path: str

    def __init__(self):
        load_dotenv()
        censor_path: str | None = os.getenv("CENSOR_PATH")
        db_path: str | None = os.getenv("DB_PATH")

        if censor_path:
            self._censor_path = censor_path
        else:
            self._censor_path = "./censor.txt"

        if db_path:
            self._db_path = db_path
        else:
            self._db_path = "./markov.db"

    def get_censor_path(self) -> str:
        return self._censor_path

    def get_db_path(self) -> str:
        return self._db_path

config = Config()
