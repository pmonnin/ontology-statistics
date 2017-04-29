import sys

__author__ = "Pierre Monnin"


class OntologyFactory:
    limit = 100000

    def __init__(self, server_manager):
        self._server_manager = server_manager

    def build_ontolgy(self, configuration_parameters):
        # Query number of classes in the ontology
        classes_number_query = configuration_parameters["classes-selection-prefix"] \
                               + " select count(distinct ?class) as ?count where { " \
                               + configuration_parameters["classes-selection-where"] \
                               + " }"
        classes_number_json = self._server_manager.query_server(classes_number_query)
        classes_number = int(classes_number_json["results"]["bindings"][0]["count"]["value"])

        # Query classes of the ontology
        class_to_index = {}
        index_to_class = []

        offset = 0
        while offset <= classes_number:
            sys.stdout.write("\rQuerying classes of the ontology %i %%\t\t" % (offset * 100.0 / classes_number))
            sys.stdout.flush()

            classes_query = configuration_parameters["classes-selection-prefix"] + " select distinct ?class { " \
                            + configuration_parameters["classes-selection-where"] \
                            + " } LIMIT " + str(OntologyFactory.limit) + " OFFSET " + str(offset)

            classes_json = self._server_manager.query_server(classes_query)

            for result in classes_json["results"]["bindings"]:
                if result["class"]["value"] not in class_to_index:
                    class_to_index[result["class"]["value"]] = len(index_to_class)
                    index_to_class.append(result["class"]["value"])

            offset += OntologyFactory.limit

        print("\rQuerying classes of the ontology 100 %\t\t")

        # Query relationships
        classes_parents = {}
        i = 0
        for ontology_class in class_to_index:
            sys.stdout.write("\rQuerying relationships of the ontology %i %%\t\t" % (i * 100.0 / len(class_to_index)))
            sys.stdout.flush()

            parents_query = configuration_parameters["parents-prefix"] \
                            + " select distinct ?parent where { <" \
                            + ontology_class + "> " + configuration_parameters["parents-relationship"] \
                            + " ?parent . FILTER(REGEX(STR(?parent), \"" \
                            + configuration_parameters["ontology-base-uri"] \
                            + "\", \"i\")) }"

            parents_json = self._server_manager.query_server(parents_query)

            parents = []
            for result in parents_json["results"]["bindings"]:
                parent_index = class_to_index[result["parent"]["value"]]
                if parent_index not in parents:
                    parents.append(parent_index)

            classes_parents[class_to_index[ontology_class]] = parents

            i += 1

        print("\rQuerying relationships of the ontology 100 %\t\t")
