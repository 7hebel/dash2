import pathlib
import os

import Modules.display as Display
import Modules.config as Config


class Session:

    def __init__(self):
        self.cwd = pathlib.Path("")
        self.raw_prompt = ""
        self.osprefix = ""
        self.version = None
        self.varsdump = None
        self.auto_update = None

        # Prepare cwd.
        cwd = Config.get_config()['defaultdir']

        if cwd == ".":
            cwd = os.getcwd()

        if not os.path.exists(cwd):
            Display.Message.warning(f"Default directory not found: {cwd}")
            Config.set_value("defaultdir", Config.__defaults__["defaultdir"])
            cwd = os.getcwd()

        cwd = pathlib.Path(cwd).absolute().resolve()
        self.cwd = cwd

        # Check varsdump.
        varsdump = Config.get_config()['varsdump']
        self.varsdump = varsdump
        if varsdump in (None, ""): self.varsdump = False
        if self.varsdump != False:
            if not os.path.exists(self.varsdump):
                Display.Message.warning("Invalid path for key: <varsdump>")
                Config.set_value("varsdump", Config.__defaults__["varsdump"])
                self.varsdump = False

        # Convert auto update to boolean value.
        autoupdate = Config.get_config()['autoupdate']
        if autoupdate == "1": self.auto_update = True
        elif autoupdate == "0": self.auto_update = False
        else:
            Display.Message.warning("Invalid value for key: <autoupdate>")
            Config.set_value("autoupdate", Config.__defaults__["autoupdate"])
            self.auto_update = False

    def refresh_config(self):
        _config = Config.get_config()
        raw_prompt = _config['prompt']
        osprefix = _config['osprefix']
        autoupdate = _config['autoupdate']
        varsdump = _config['varsdump']

        self._config = _config
        self.raw_prompt = raw_prompt
        self.osprefix = osprefix
        self.auto_update = autoupdate
        self.varsdump = varsdump
