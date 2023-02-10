import pathlib
import os

import Modules.registry as Registry
import Modules.display as Display
import Modules.config as Config


class Session:

    def __init__(self):
        self.cwd = pathlib.Path("")
        self.raw_prompt = ""
        self.osprefix = ""
        self.version = None

        # Prepare cwd.
        cwd = Config.get_config()['defaultdir']

        if cwd == ".":
            cwd = os.getcwd()

        if not os.path.exists(cwd):
            Display.Message.warning(f"Default directory not found: {cwd}")
            Registry.set_value("defaultdir", ".")
            cwd = os.getcwd()

        cwd = pathlib.Path(cwd).absolute().resolve()
        self.cwd = cwd

    def refresh_config(self):
        _config = Config.get_config()
        raw_prompt = _config['prompt']
        osprefix = _config['osprefix']

        self.raw_prompt = raw_prompt
        self.osprefix = osprefix
