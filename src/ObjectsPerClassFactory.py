import sys
import urllib.error

__author__ = "Pierre Monnin"


class ObjectsPerClassFactory:
    def __init__(self, server_manager):
        self._server_manager = server_manager

    def get_objects_number_per_class(self, ontology, configuration_parameters):
        ret_val = []

        for i, ontology_class in enumerate(ontology.get_classes()):
            sys.stdout.write("\rQuerying number of objects per ontology class %i %%\t\t"
                             % (i * 100.0 / ontology.get_classes_number()))
            sys.stdout.flush()

            done = False
            while not done:
                try:
                    # Number of objects typed (asserted)
                    asserted_objects_query = configuration_parameters["objects-per-class-prefix"] \
                                             + " select count(distinct ?object) as ?count where { " \
                                             + "?object " + configuration_parameters["type-predicate"] + " <" \
                                             + ontology_class + "> }"
                    asserted_objects_count_json = self._server_manager.query_server(asserted_objects_query)

                    # Number of objects typed (asserted or inferred from ontology class hierarchy)
                    inferred_asserted_objects_query = configuration_parameters["objects-per-class-prefix"] \
                        + " select count(distinct ?object) as ?count where { " \
                        + "?object " + configuration_parameters["type-predicate"] + "/" \
                        + configuration_parameters["parents-relationship"] + "* <" \
                        + ontology_class + "> }"
                    inferred_asserted_objects_json = self._server_manager.query_server(inferred_asserted_objects_query)

                    ret_val.append([ontology_class,
                                    asserted_objects_count_json["results"]["bindings"][0]["count"]["value"],
                                    inferred_asserted_objects_json["results"]["bindings"][0]["count"]["value"]])
                    done = True

                except urllib.error.HTTPError as e:
                    print("\rHTTP error " + str(e.getcode()) + " while querying objects of " + ontology_class)
                    if e.getcode() == 404:
                        print("New try")
                    else:
                        ret_val.append([ontology_class, '', ''])
                        done = True

            i += 1

        print("\rQuerying number of objects per ontology class 100 %\t\t")

        return ret_val
