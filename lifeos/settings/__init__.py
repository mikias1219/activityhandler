"""
LifeOS settings entry point.
Set LIFEOS_ENV=development|docker|production (default: development).
"""

import os

_env = os.environ.get("LIFEOS_ENV", "development")
if _env == "docker":
    from lifeos.settings.docker import *  # noqa: F401, F403
elif _env == "production":
    from lifeos.settings.production import *  # noqa: F401, F403
else:
    from lifeos.settings.development import *  # noqa: F401, F403
