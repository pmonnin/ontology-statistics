import multiprocessing
import sys
import urllib.error

__author__ = "Pierre Monnin"


def get_objects_number_for_class_multi_proc_wrapper(kwargs):
    return kwargs["object"].get_objects_number_for_class(kwargs["ontology_class"], kwargs["configuration_parameters"])


class ObjectsPerClassFactory:
    def __init__(self, server_manager):
        self._server_manager = server_manager

    def get_objects_number_for_class(self, ontology_class, configuration_parameters):
        ret_val = [ontology_class, '', '']
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

                ret_val = [
                                ontology_class,
                                asserted_objects_count_json["results"]["bindings"][0]["count"]["value"],
                                inferred_asserted_objects_json["results"]["bindings"][0]["count"]["value"]
                ]
                done = True

            except urllib.error.HTTPError as e:
                print("\rHTTP error " + str(e.getcode()) + " while querying objects of " + ontology_class)
                if e.getcode() == 404:
                    print("New try")
                else:
                    done = True

        return ret_val

    def get_objects_number_per_class(self, ontology, configuration_parameters):
        ret_val = []

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            parameters = [{"object": self, "ontology_class": c, "configuration_parameters": configuration_parameters}
                          for c in ontology.get_classes()]

            for i, result in enumerate(pool.imap_unordered(get_objects_number_for_class_multi_proc_wrapper,
                                       parameters)):
                sys.stdout.write("\rQuerying number of objects per ontology class %i %%\t\t"
                                 % (i * 100.0 / ontology.get_classes_number()))
                sys.stdout.flush()
                ret_val.append(result)

        print("\rQuerying number of objects per ontology class 100 %\t\t")

        return ret_val
