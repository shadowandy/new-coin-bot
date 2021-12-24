import configparser
import os

__all__ = ('config', 'Config')


class Config:
    def __init__(self, file_name=os.path.join(os.path.dirname(__file__), os.pardir, 'configuration.cfg')):
        self._conf = self._load_config(file_name)

    @property
    def console_logs(self):
        return self._conf.getboolean('base', 'console_logs', fallback=False)

    @property
    def logs_file(self):
        return self._conf.get('base', 'logs_file', fallback=None)

    @property
    def delay(self):
        return self._conf.get('base', 'delay', fallback=0.5)

    @property
    def refresh_interval(self):
        return self._conf.get('base', 'refresh_interval_minutes', fallback=20) * 60

    @property
    def save_interval(self):
        return self._conf.get('base', 'save_interval_minutes', fallback=30) * 60

    @property
    def coins_list(self):
        return self._conf.get('base', 'coins_list', fallback=None)

    @property
    def coins_store(self):
        return self._conf.get('base', 'coins_store', fallback=None)

    @property
    def telegram_token(self):
        return self._conf.get('telegram', 'token', fallback=None)

    @property
    def telegram_chatid(self):
        return self._conf.get('telegram', 'chatid', fallback=None)

    @property
    def description_trim(self):
        return self._conf.get('telegram', 'description_trim', fallback=None)

    @staticmethod
    def _load_config(file_name):
        conf = configparser.ConfigParser()
        conf.read_file(open(file_name))
        return conf


# we want to import the config across the files
config = Config()
