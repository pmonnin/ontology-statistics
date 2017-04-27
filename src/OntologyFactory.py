__author__ = "Pierre Monnin"


class OntologyFactory:
    patterns = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "[^a-z0-9]"]

    def __init__(self, server_manager):
        self._server_manager = server_manager

    def build_ontolgy(self, configuration_parameters):
        # Query classes of the ontology
        classes_to_index = {}
        index_to_classes = []
        for suffix in OntologyFactory.patterns:
            classes_query = configuration_parameters["classes-selection-prefix"] + " select distinct ?class { " \
                            + configuration_parameters["classes-selection-where"] \
                            + " FILTER(REGEX(STR(?class), \"" + configuration_parameters["ontology-base-uri"] + suffix \
                            + "\", \"i\"))}"

            classes_json = self._server_manager.query_server(classes_query)

            for result in classes_json["results"]["bindings"]:
                if not result["class"]["value"] in classes_to_index:
                    classes_to_index[result["class"]["value"]] = len(index_to_classes)
                    index_to_classes.append(result["class"]["value"])
