from BlueService.models import Settings
from BlueService.database import SessionLocal
from BlueService.logger import logger
import traceback

class Connected:
    def __init__(self, session=SessionLocal()):
        self.session = session

    def get_connection(self):
        return SessionLocal()

class SettingsHelper(Connected):

    def __init__(self):
        self._cache = None
        super().__init__()

    def get_settings(self) -> Settings:
        try:
            with self.get_connection() as conn:
                if self._cache:
                    return self._cache
                settings = conn.query(Settings).first()
                self._cache = settings
                return settings
        except Exception:
            logger.error(f"Error getting settings")
            traceback.print_exc()
            return None
        
    def create_settings(self) -> None:
        try:
            with self.get_connection() as conn:
                settings = Settings()
                conn.add(settings)
                conn.commit()
        except Exception:
            logger.error(f"Error creating settings")
            traceback.print_exc()
            return
        
    def update_settings(self, **kwargs) -> None:
        try:
            with self.get_connection() as conn:
                settings = conn.query(Settings).first()
                for key, value in kwargs.items():
                    setattr(settings, key, value)
                conn.commit()
                self._cache = conn.query(Settings).first()
        except Exception:
            logger.error(f"Error updating settings")
            traceback.print_exc()
            return