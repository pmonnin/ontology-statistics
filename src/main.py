import sys

from ObjectsPerClassFactory import ObjectsPerClassFactory
from OntologyFactory import OntologyFactory
from iofunctions import write_output, load_configuration
from ServerManager import ServerManager

__author__ = "Pierre Monnin"


def main():
    print("Ontology statistics")

    if len(sys.argv) != 3:
        print_usage()

    else:
        configuration_parameters = load_configuration(sys.argv[1])
        server_manager = ServerManager(configuration_parameters)

        ontology_factory = OntologyFactory(server_manager)
        ontology = ontology_factory.build_ontology(configuration_parameters)
        statistics = ontology.get_statistics()

        objs_per_class = []
        if configuration_parameters["objects-per-class"]:
            objs_per_class_factory = ObjectsPerClassFactory(server_manager)
            objs_per_class = objs_per_class_factory.get_objects_number_per_class(ontology, configuration_parameters)

        write_output(sys.argv[2], configuration_parameters, ontology, statistics, objs_per_class)


def print_usage():
    print("Usage: main.py conf.json output")
    print("\tconf.json\tJSON file containing the necessary configuration parameters")
    print("\toutput\tPrefix of generated output files")

if __name__ == '__main__':
    main()
