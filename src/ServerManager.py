import urllib.parse
import urllib.request
import json
import socket

__author__ = "Pierre Monnin"


class ServerManager:
    def __init__(self, configuration_parameters):
        self.server_address = configuration_parameters["server-address"]
        self.json_conf_attribute = configuration_parameters["url-json-conf-attribute"]
        self.json_conf_value = configuration_parameters["url-json-conf-value"]
        self.default_graph_attribute = configuration_parameters["url-default-graph-attribute"]
        self.default_graph_value = configuration_parameters["url-default-graph-value"]
        self.query_attribute = configuration_parameters["url-query-attribute"]
        socket.setdefaulttimeout(configuration_parameters["timeout"])

    def query_server(self, query):
        query_parameters = {
            self.json_conf_attribute: self.json_conf_value,
            self.default_graph_attribute: self.default_graph_value,
            self.query_attribute: query
        }

        content = urllib.request.urlopen(self.server_address + "?" + urllib.parse.urlencode(query_parameters))
        return json.loads(content.read())
