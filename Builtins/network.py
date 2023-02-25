from Modules.commands import Command, Parameter, EndlessParameter
from Modules.data_types import DataType

import Builtins.Executives._network as exe

Command("net", exe.net_info, [], "Show informations about network.")
Command("dlp", exe.dns_lookup, [Parameter("addr", DataType.Text, "Target's address.")], "Lookup target.")
Command("ilp", exe.ip_lookup, [Parameter("ip", DataType.Text, "Target's ip.")], "Lookup ip.")
Command("ipgeo", exe.ip_geo_info, [Parameter("target", DataType.Text, "Target's ip.")], "Get geographical information about ip.")
Command("req", exe.make_request, [Parameter("url", DataType.Text, "Target url where request will be sent."), Parameter("type", DataType.Text, "Request type (get, set, post, put, patch, head, delete)", required=False, default="get"), Parameter("to_file", DataType.Boolean, "Decides if response will be saved into file.", required=False, default=False)], "Send request to given url.")
