# ontology-statistics

Python scripts to generate statistics on the class hierarchy of an ontology

## Execution

The script must be executed with the following command:

```bash
python main.py conf.json output
```

with:

* _conf.json_: being a configuration file -- see next paragraph
* _output_: being the prefix of all generated output files:
    * _output.json_: contains the main statistics
    * _output-objects-per-class.csv_: contains the number of objects per class (asserted and inferred) -- optional, 
    see next paragraphs
    * _output.gexf_: graph output to be opened with [Gephi](https://gephi.org/) -- optional, see next paragraphs

## Configuration

An example of a configuration file is available below:

```json
{
  "server-address": "http://127.0.0.1/sparql",
  "url-json-conf-attribute": "format",
  "url-json-conf-value": "application/sparql-results+json",
  "url-default-graph-attribute": "default-graph-uri",
  "url-default-graph-value": "http://dbpedia.org",
  "url-query-attribute": "query",
  "ontology-base-uri": "http://dbpedia.org/ontology/",
  "classes-selection-prefix": "",
  "classes-selection-where": "?class a owl:Class . FILTER(REGEX(STR(?class), \"http://dbpedia.org/ontology/\", \"i\")) .",
  "parents-prefix": "",
  "parents-relationship": "rdfs:subClassOf",
  "objects-per-class": true,
  "objects-per-class-prefix": "",
  "type-predicate": "rdf:type",
  "gexf-export": true,
  "timeout": 20000
}
```

with:

* _server-address_: address of the SPARQL endpoint to query
* _url-json-conf-attribute_: URL attribute to use to get JSON results
* _url-json-conf-value_: value of the _url-json-conf-attribute_ to get JSON results
* _url-default-graph-attribute_: URL attribute to use to define the default graph
* _url-default-graph-value_: value of _url-default-graph-attribute_ to define the default graph
* _url-query-attribute_: URL attribute to use to define the query
* _ontology-base-uri_: base URI of the ontology
* _classes-selection-prefix_: prefixes used in the query to select classes -- see next paragraphs
* _classes-selection-where_: where clauses used in the query to select classes -- see next paragraphs
* _parents-prefix_: prefixes used in the query to select relationships between classes -- see next paragraphs
* _parents-relationship_: predicate used to express _subClassOf_ relationships in the ontology
* _objects-per-class_: boolean value to indicate the need to generate the _output-objects-per-class.csv_ file
* _objects-per-class-prefix_: prefixes used in the objects per class query -- see next paragraphs
* _type-predicate_: predicate used to type an object with a class from the ontology
* _gexf-export_: boolean value to indicate the need to generate the _output.gexf_ file
* _timeout_: timeout value for HTTP requests

## Output

### _output.json_

Main output file containing:

* _classes-number_: number of classes of the ontology
* _top-level-classes_: number of top level classes of the ontology, _i.e., number of classes having 0 parents from the 
ontology
* _asserted-subsumptions-number_: number of asserted subsumptions in the ontology
* _inferred-subsumptions-number_: number of subsumptions that can be inferred from the asserted subsumptions
* _cycles_: detected cycles in the ontology
* _cycles-number_: number of cycles in the ontology
* _depth_: max depth of the ontology (top level classes are considered with a depth of 0)


### _output-objects-per-class.csv_

If the parameter _objects-per-class_ is set to true, this file will be generated with three columns:
 
* _Class_: class URI
* _Objects typed (asserted)_: number of objects typed by the class (directly asserted with the _type-predicate_)
* _Objects typed (asserted + inferred)_: number of objects typed by the class (asserted with the _type-predicate_ and 
inferred from the class hierarchy, _i.e._, typed with a subclass of the considered class)

### _output.gexf_

If the parameter _gexf-export_ is set to true, this file will be generated.
If the parameter _objects-per-class_ is set to true, the numbers of objects (asserted and asserted+inferred) per class 
will be added to each class node so they can be used in Gephi.

## SPARQL queries

Below are the SPARQL queries used in the Python scripts. The use of configuration parameters is highlighted 
with ``("parameter_used")``.

### Selection of classes

```sparql
("classes-selection-prefix")

select distinct ?class {
    ("classes-selection-where")
}
```

(A ``LIMIT`` and an ``OFFSET`` are also used in this query but not presented here)

### Relationships between classes

For each class_uri in the ontology

```sparql
("parents-prefix")

select distinct ?parent where {
    <class_uri> ("parents-relationship") ?parent . 
    FILTER(REGEX(STR(?parent), "(ontology-base-uri)", "i"))
}
```

### Objects per class

For each class_uri in the ontology

#### Asserted

```sparql
("objects-per-class-prefix")

select count(distinct ?object) as ?count where {
    ?object ("type-predicate") <class_uri>
}
```

#### Asserted and inferred

```sparql
("objects-per-class-prefix")

select count(distinct ?object) as ?count where {
    ?object ("type-predicate")/("parents-relationship")* <class_uri> 
}
```

## Dependencies

* Python 3.6

## License

[![Creative Commons BY NC SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)


## Contributors

[Pierre Monnin](https://pmonnin.github.io/)
