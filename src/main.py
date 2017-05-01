import sys
import json

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

            output = open(sys.argv[2], 'w', encoding='utf-8')
            json.dump(ontology.get_statistics(), output)

            if configuration_parameters["objects-per-class"]:
                pass


def print_usage():
    print("Usage: main.py conf.json output.json")
    print("\tconf.json\tJSON file containing the necessary configuration parameters")
    print("\toutput\tPrefix of generated output files")

if __name__ == '__main__':
    main()
