import csv
import json
import xml.etree.ElementTree as ET

__author__ = "Pierre Monnin"


def load_configuration(configuration_file_path):
    with open(configuration_file_path, encoding='utf-8') as configuration_file:
        return json.loads(configuration_file.read())


def write_output(file_prefix, configuration_parameters, ontology, ontology_statistics, objs_per_class):
    print("\rWriting main JSON output file\t\t")
    with open(file_prefix + ".json", 'w', encoding='utf-8') as output:
        json.dump(ontology_statistics, output)

    if configuration_parameters["objects-per-class"]:
        print("\rWriting objects per class TSV output file\t\t")

        with open(file_prefix + "-objects-per-class.csv", 'w', encoding='utf-8') as output:
            csv_writer = csv.writer(output)
            csv_writer.writerow(['Class', 'Objects typed (asserted)', 'Objects typed (asserted + inferred)'])
            csv_writer.writerows(objs_per_class)

    if configuration_parameters["gexf-export"]:
        print("\rWriting GEXF output file\t\t")

        root = ET.Element("gexf")
        root.set("xmlns", "http://www.gexf.net/1.2draft")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd")
        root.set("version", "1.2")

        graph = ET.SubElement(root, "graph")
        graph.set("defaultedgetype", "directed")

        if configuration_parameters["objects-per-class"]:
            attributes = ET.SubElement(graph, "attributes")
            attributes.set("class", "node")
            number_asserted = ET.SubElement(attributes, "attribute")
            number_asserted.set("id", "0")
            number_asserted.set("title", "objs-asserted")
            number_asserted.set("type", "float")
            number_asserted_inferred = ET.SubElement(attributes, "attribute")
            number_asserted_inferred.set("id", "1")
            number_asserted_inferred.set("title", "objs-asserted-inferred")
            number_asserted_inferred.set("type", "float")

        # Writing nodes
        nodes = ET.SubElement(graph, "nodes")
        for i in range(0, len(ontology._index_to_class)):
            node = ET.SubElement(nodes, "node")
            node.set("id", str(i))
            node.set("label", ontology._index_to_class[i].replace('"', '\"'))

            if configuration_parameters["objects-per-class"]:
                objs_current_class = get_line_for_class(ontology._index_to_class[i], objs_per_class)

                attvalues = ET.SubElement(node, "attvalues")

                attvalue_asserted = ET.SubElement(attvalues, "attvalue")
                attvalue_asserted.set("for", "0")

                attvalue_asserted.set("value", str(objs_current_class[1]))

                attvalue_asserted_inferred = ET.SubElement(attvalues, "attvalue")
                attvalue_asserted_inferred.set("for", "1")
                attvalue_asserted_inferred.set("value", str(objs_current_class[2]))

        # Writing edges
        edges = ET.SubElement(graph, "edges")
        count_edge = 0
        for i in range(0, len(ontology._index_to_class)):
            for j in ontology._class_children[i]:
                edge = ET.SubElement(edges, "edge")
                edge.set("id", str(count_edge))
                edge.set("source", str(i))
                edge.set("target", str(j))
                count_edge += 1

        tree = ET.ElementTree(root)
        tree.write(file_prefix + ".gexf", encoding='utf-8')


def get_line_for_class(ontology_class, objects_per_class):
    for line in objects_per_class:
        if line[0] == ontology_class:
            return line

    return []
