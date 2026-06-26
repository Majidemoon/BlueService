from BlueService.models import Settings, ForcedJoinUsers, ForcedJoinChannels, Admins, Users
from BlueService.database import SessionLocal
from BlueService.logger import logger
import traceback
from datetime import datetime
from sqlalchemy.sql import func

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
            try:
                if self._cache:
                    return self._cache
            except Exception:
                pass
            with self.get_connection() as conn:
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
        
class ForcedJoinChannelsHelper(Connected):

    def get_forced_join_channels_count(self) -> int:
        try:
            with self.get_connection() as conn:
                count = conn.query(ForcedJoinChannels).count()
                return count
        except Exception:
            logger.error(f"Error getting forced join channels count")
            traceback.print_exc()
            return 0
        
    def get_forced_join_channels(self) -> list[ForcedJoinChannels]:
        try:
            with self.get_connection() as conn:
                forced_join_channels = conn.query(ForcedJoinChannels).all()
                return forced_join_channels
        except Exception:
            logger.error(f"Error getting forced join channels")
            traceback.print_exc()
            return []
        
    def insert_forced_join_channel(self, channel_id : int, channel_name : str, channel_link : str) -> None:
        try:
            with self.get_connection() as conn:
                forced_join_channel = ForcedJoinChannels(channel_id=channel_id, channel_name=channel_name, channel_link=channel_link)
                conn.add(forced_join_channel)
                conn.commit()
        except Exception:
            logger.error(f"Error inserting forced join channel")
            traceback.print_exc()

    def get_forced_join_channel(self, id : int) -> ForcedJoinChannels:
        try:
            with self.get_connection() as conn:
                forced_join_channel = conn.query(ForcedJoinChannels).filter_by(id=id).first()
                return forced_join_channel
        except Exception:
            logger.error(f"Error getting forced join channel")
            traceback.print_exc()
            return
        
    def get_forced_join_channel_by_channel_id(self, channel_id : int) -> ForcedJoinChannels:
        try:
            with self.get_connection() as conn:
                forced_join_channel = conn.query(ForcedJoinChannels).filter_by(channel_id=channel_id).first()
                return forced_join_channel
        except Exception:
            logger.error(f"Error getting forced join channel")
            traceback.print_exc()
            return
        
    def delete_forced_join_channel(self, id : int) -> None:
        try:
            with self.get_connection() as conn:
                forced_join_channel = conn.query(ForcedJoinChannels).filter_by(id=id).first()
                conn.delete(forced_join_channel)
                conn.commit()
        except Exception:
            logger.error(f"Error deleting forced join channel")
            traceback.print_exc()

    def update_forced_join_channel(self, id : int, **kwargs) -> None:
        try:
            with self.get_connection() as conn:
                forced_join_channel = conn.query(ForcedJoinChannels).filter_by(id=id).first()
                for key, value in kwargs.items():
                    setattr(forced_join_channel, key, value)
                conn.commit()
        except Exception:
            logger.error(f"Error updating forced join channel")
            traceback.print_exc()

class ForcedJoinUsersHelper(Connected):

    def get_forced_join_user(self, user_id : int, channel_id : int) -> ForcedJoinUsers:
        try:
            with self.get_connection() as conn:
                forced_join_user = conn.query(ForcedJoinUsers).filter_by(user_id=user_id, channel_id=channel_id).first()
                return forced_join_user
        except Exception:
            logger.error(f"Error getting forced join user")
            traceback.print_exc()
            return
        
    def insert_forced_join_user(self, user_id : int, channel_id : int) -> None:
        try:
            with self.get_connection() as conn:
                forced_join_user = ForcedJoinUsers(user_id=user_id, channel_id=channel_id)
                conn.add(forced_join_user)
                conn.commit()
        except Exception:
            logger.error(f"Error inserting forced join user")
            traceback.print_exc()

    def delete_forced_join_user(self, user_id : int, channel_id : int) -> None:
        try:
            with self.get_connection() as conn:
                forced_join_user = conn.query(ForcedJoinUsers).filter_by(user_id=user_id, channel_id=channel_id).first()
                conn.delete(forced_join_user)
                conn.commit()
        except Exception:
            logger.error(f"Error deleting forced join user")
            traceback.print_exc()

class AdminsHelper(Connected):

    def get_admins(self) -> list[Admins]:
        try:
            with self.get_connection() as conn:
                admins = conn.query(Admins).all()
                return admins
        except Exception:
            logger.error(f"Error getting admins")
            traceback.print_exc()
            return
        
    def get_admin(self, id : int, ) -> Admins:
        try:
            with self.get_connection() as conn:
                admin = conn.query(Admins).filter_by(id=id).first()
                return admin
        except Exception:
            logger.error(f"Error getting admin")
            traceback.print_exc()
            return
        
    def insert_admin(self, user_id : int) -> None:
        try:
            with self.get_connection() as conn:
                admin = Admins(user_id=user_id)
                conn.add(admin)
                conn.commit()
        except Exception:
            conn.rollback()
            logger.error(f"Error inserting admin")
            traceback.print_exc()

    def delete_admin(self, id : int) -> None:
        try:
            with self.get_connection() as conn:
                admin = conn.query(Admins).filter_by(id=id).first()
                conn.delete(admin)
                conn.commit()
        except Exception:
            conn.rollback()
            logger.error(f"Error deleting admin")
            traceback.print_exc()

    def get_admin_by_user_id(self, user_id : int) -> Admins:
        try:
            with self.get_connection() as conn:
                admin = conn.query(Admins).filter_by(user_id=user_id).first()
                return admin
        except Exception:
            logger.error(f"Error getting admin")
            traceback.print_exc()
            return
        
class UsersHelper(Connected):

    def insert_user(self, user_id : int) -> None:
        try:
            with self.get_connection() as conn:
                user = Users(user_id=user_id, balance=0, join_date=datetime.now(), status=0, is_verified=0)
                conn.add(user)
                conn.commit()
        except Exception:
            logger.error(f"Error inserting user: {user_id}")
            traceback.print_exc()

        logger.info(f'✅ Successfully saved user {user_id} into the users table')

    def get_user(self, user_id : int) -> Users:
        try:
            with self.get_connection() as conn:
                user = conn.query(Users).filter_by(user_id=user_id).first()
                if user is None:
                    self.insert_user(user_id)
                user = conn.query(Users).filter_by(user_id=user_id).first()
            return user
        except Exception:
            logger.error(f"Error getting user: {user_id}")
            traceback.print_exc()
            return None
    
    def update_balance(self, user_id : int, balance : float) -> None:
        try:
            with self.get_connection() as conn:
                user = conn.query(Users).filter_by(user_id=user_id).first()
                user.balance = balance
                conn.commit()
        except Exception:
            logger.error(f"Error updating balance for user: {user_id}")
            traceback.print_exc()
            return None

        logger.info(f'✅ Successfully updated balance for user {user_id}')

    def get_all_users(self, offset : int = None, limit : int = None) -> list[Users]:
        try:
            with self.get_connection() as conn:
                if offset is not None and limit is not None:
                    users = conn.query(Users).offset(offset).limit(limit).all()
                else:
                    users = conn.query(Users).all()
                return users
        except Exception:
            logger.error(f"Error getting all users")
            traceback.print_exc()
            return None
    
    def user_count(self) -> int:
        try:
            with self.get_connection() as conn:
                user_count = conn.query(Users).count()
                return user_count
        except Exception:
            logger.error(f"Error getting user count")
            traceback.print_exc()
            return None
        
    def users_total_balance(self) -> float:
        try:
            with self.get_connection() as conn:
                users_total_balance = conn.query(func.sum(Users.balance)).scalar()
                return round(float(users_total_balance), 1)
        except Exception:
            logger.error(f"Error getting users total balance")
            traceback.print_exc()
            return None
        
    def verify_user(self, user_id : int, status : int) -> None:
        try:
            with self.get_connection() as conn:
                user = conn.query(Users).filter_by(user_id=user_id).first()
                user.is_verified = status
                conn.commit()
                return
                
        except Exception:
            conn.rollback()
            logger.error(f"Error transferring balance")
            traceback.print_exc()
            return 0
        
    def update_user_status(self, user_id : int, status : int) -> None:
        try:
            with self.get_connection() as conn:
                user = conn.query(Users).filter_by(user_id=user_id).first()
                user.status = status
                conn.commit()
                return
        except:
            conn.rollback()
            logger.error(f"Error changing user status")
            traceback.print_exc()
            return 0