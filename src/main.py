import argparse

from ObjectsPerClassFactory import ObjectsPerClassFactory
from OntologyFactory import OntologyFactory
from iofunctions import write_output, load_configuration
from ServerManager import ServerManager

__author__ = "Pierre Monnin"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("conf", help="JSON file containing the necessary configuration parameters")
    parser.add_argument("output", help="Prefix of generated output files (see full documentation)")
    args = parser.parse_args()

    print("Ontology statistics")

    configuration_parameters = load_configuration(args.conf)
    server_manager = ServerManager(configuration_parameters)

    ontology_factory = OntologyFactory(server_manager)
    ontology = ontology_factory.build_ontology(configuration_parameters)
    statistics = ontology.get_statistics(configuration_parameters["cycles-computation"])

    objs_per_class = []
    if configuration_parameters["objects-per-class"]:
        objs_per_class_factory = ObjectsPerClassFactory(server_manager)
        objs_per_class = objs_per_class_factory.get_objects_number_per_class(ontology, configuration_parameters)

    write_output(args.output, configuration_parameters, ontology, statistics, objs_per_class)


if __name__ == '__main__':
    main()
