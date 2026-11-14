"""Project settings for Kedro."""

import sys

from kedro.config import OmegaConfigLoader

from project_template.profile_hook import ProfileHook

CONF_SOURCE = "conf"

CONFIG_LOADER_CLASS = OmegaConfigLoader

CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    "config_patterns": {
        "catalog": ["catalog*", "catalog*/**", "**/catalog*"],
        "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
        "credentials": ["credentials*", "credentials*/**", "**/credentials*"],
        "globals": ["globals.yml"],
    },
}

_is_dry_run = any("DryRunner" in arg for arg in sys.argv)

HOOKS: tuple[ProfileHook, ...] = () if _is_dry_run else (ProfileHook(save_file=True),)
