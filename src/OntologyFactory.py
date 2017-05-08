import sys
import urllib.error

from Ontology import Ontology

__author__ = "Pierre Monnin"


class OntologyFactory:
    limit = 100000

    def __init__(self, server_manager):
        self._server_manager = server_manager

    def build_ontology(self, configuration_parameters):
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
        class_parents = []
        class_children = []
        for i in range(0, len(index_to_class)):
            class_parents.append([])
            class_children.append([])
        not_found = 0

        for i in range(0, len(index_to_class)):
            sys.stdout.write("\rQuerying relationships of the ontology %i %%\t\t" % (i * 100.0 / len(class_to_index)))
            sys.stdout.flush()

            parents_query = configuration_parameters["parents-prefix"] \
                            + " select distinct ?parent where { <" \
                            + index_to_class[i] + "> " + configuration_parameters["parents-relationship"] \
                            + " ?parent . FILTER(REGEX(STR(?parent), \"" \
                            + configuration_parameters["ontology-base-uri"] \
                            + "\", \"i\")) }"

            done = False
            while not done:
                try:
                    parents_json = self._server_manager.query_server(parents_query)

                    parents = []
                    for result in parents_json["results"]["bindings"]:
                        if result["parent"]["value"] in class_to_index:
                            parent_index = class_to_index[result["parent"]["value"]]

                            if parent_index not in parents:
                                parents.append(parent_index)

                            if i not in class_children[parent_index]:
                                class_children[parent_index].append(i)

                        else:
                            print("\rClass was found during relationships and not selected: "
                                  + result["parent"]["value"])
                            not_found += 1

                    class_parents[i] = parents
                    done = True

                except urllib.error.HTTPError as e:
                    print("\rHTTP error " + str(e.getcode()) + " while querying parents of " + index_to_class[i])
                    if e.getcode() == 404:
                        print("New try")
                    else:
                        done = True

        print("\rQuerying relationships of the ontology 100 %\t\t")
        print("\r" + str(not_found) + " classes were found during relationships queries but not selected")
        return Ontology(class_to_index, index_to_class, class_parents, class_children)
