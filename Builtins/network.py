from Modules.commands import Command, Parameter, EndlessParameter
from Modules.data_types import DataType

import Builtins.Executives._network as exe

Command("net", exe.net_info, [], "Show informations about network.")
Command("dlp", exe.dns_lookup, [Parameter("addr", DataType.Text, "Target's address.")], "Lookup target.")
Command("ilp", exe.ip_lookup, [Parameter("ip", DataType.Text, "Target's ip.")], "Lookup ip.")
Command("ipgeo", exe.ip_geo_info, [Parameter("target", DataType.Text, "Target's ip.")], "Get geographical information about ip.")
