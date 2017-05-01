# ontology-statistics

Python scripts to generate statistics on an ontology

## Execution

The script must be executed with the following command:

```bash
python main.py conf.json output
```

with:

* _conf.json_: being a configuration file -- see next paragraph
* _output_: being the prefix of all generated output files:
    * _output.json_: contains the main statistics
    * _output-cycles.json_: contains the cycles of the ontology
    * _output-objects-per-class.csv_: contains the number of objects per class (asserted and inferred) -- optional, 
    see next paragraph

## Configuration

TBC

## Dependencies

* Python 3

## Contributors

[Pierre Monnin](https://pmonnin.github.io/) (PhD student at [Loria](http://www.loria.fr/en/))

Under the supervision of [Amedeo Napoli](https://members.loria.fr/ANapoli/) and [Adrien Coulet](https://members.loria.fr/ACoulet/)