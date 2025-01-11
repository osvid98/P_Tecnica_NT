from sqlalchemy import create_engine

class DatabaseHandler:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
        self._engine = None

    @property
    def engine(self):
        """Lazy loading de la DB"""
        if self._engine is None:
            self._engine = create_engine(self.connection_string)
        return self._engine

    def close(self):
        """Cerrar conexion"""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None