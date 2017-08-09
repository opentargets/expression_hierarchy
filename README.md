# Expression Hierarchy
This `python` script maps TSV files provided by Expression Atlas to JSON format. The files can be found [here](https://github.com/gxa/atlas-metadata/tree/master/out). The content of these files is the hierarchy of tissues for which expression data is given, classified either by anatomical system or organ. Both tissues and parent systems are identified by UBERON codes. The JSON format files are intended for prototyping the RNA expression facets of the opentargets/webapp.

## Example Input
Here are a couple of example lines of input from the `anatomical_systems.txt` file.

|system id|system name|tissue id|tissue name|
|-|-|-|-|
|UBERON_0000949|endocrine system|UBERON_0000007|pituitary gland|
|UBERON_0000949|endocrine system|UBERON_0000016|endocrine pancreas|

## Example Output
```
{
  "anatomicalSystems": [
    {
      "key": "UBERON_0000949",
      "label": "endocrine system",
      "children": [
        "UBERON_0000007",
        "UBERON_0000016"
      ]
    }
  ],
  "tissues": {
    "UBERON_0000007": {
      "key": "UBERON_0000007",
      "label": "pituitary gland",
      "anatomical_systems": [
        "UBERON_0000949"
      ]
    },
    "UBERON_0000016": {
      "key": "UBERON_0000016",
      "label": "endocrine pancreas",
      "anatomical_systems": [
        "UBERON_0000949"
      ]
    }
  }
}
```
