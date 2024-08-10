import os
from pathlib import Path
from pathlib import Path

from split_settings.tools import include, optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_PROJ_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENVVAR_SETTINGS_PREFIX = 'PROJVARBLOG_SETTINGS_'
LOCAL_SETTINGS_PATH = os.getenv(f'{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH')

if not LOCAL_SETTINGS_PATH:
	LOCAL_SETTINGS_PATH = 'local/settings.dev.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
	LOCAL_SETTINGS_PATH = str(BASE_PROJ_DIR / LOCAL_SETTINGS_PATH)

include(
	'base.py',
	'celery.py',
	optional(LOCAL_SETTINGS_PATH),
)
