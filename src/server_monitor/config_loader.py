import tomllib
import os
import sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.toml")


def load_config():
    path_to_load = CONFIG_PATH

    if not os.path.exists(path_to_load):
        print(f"Config file not found at {path_to_load}")
        example_config_path = os.path.join(PROJECT_ROOT, "example_config.toml")
        if os.path.exists(example_config_path):
            print(
                f"Example config file found at {example_config_path}. Please copy it to {path_to_load} and edit it."
                f"Now using example config file."
            )

            path_to_load = example_config_path
        else:
            print(
                f"Can not find example config file at {example_config_path} or {path_to_load}. Please check your channel."
            )
            sys.exit(1)

    try:
        with open(path_to_load, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)


def get_config_value(config, section, key, default):
    return config.get(section, {}).get(key, default)
