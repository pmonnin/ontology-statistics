import sys
import json
import csv

from ObjectsPerClassFactory import ObjectsPerClassFactory
from OntologyFactory import OntologyFactory
from ServerManager import ServerManager

__author__ = "Pierre Monnin"


def main():
    print("Ontology statistics")

    if len(sys.argv) != 3:
        print_usage()

    else:
        with open(sys.argv[1], encoding='utf-8') as configuration_file:
            configuration_parameters = json.loads(configuration_file.read())
            server_manager = ServerManager(configuration_parameters)

            ontology_factory = OntologyFactory(server_manager)
            ontology = ontology_factory.build_ontology(configuration_parameters)

            with open(sys.argv[2] + ".json", 'w', encoding='utf-8') as output:
                json.dump(ontology.get_statistics(), output)

            if configuration_parameters["objects-per-class"]:
                with open(sys.argv[2] + "-objects-per-class.csv", 'w', encoding='utf-8') as output:
                    csv_writer = csv.writer(output)
                    csv_writer.writerow(['Class', 'Objects typed (asserted)', 'Objects typed (asserted + inferred)'])
                    objects_per_class_factory = ObjectsPerClassFactory(server_manager)
                    csv_writer.writerows(objects_per_class_factory.get_objects_number_per_class(ontology,
                                                                                                configuration_parameters
                                                                                                ))


def print_usage():
    print("Usage: main.py conf.json output")
    print("\tconf.json\tJSON file containing the necessary configuration parameters")
    print("\toutput\tPrefix of generated output files")

if __name__ == '__main__':
    main()
