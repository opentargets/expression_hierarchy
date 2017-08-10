import os.path
import csv
import json
import urllib


ANATOMICAL_SYSTEMS_URL = "https://raw.githubusercontent.com/gxa/atlas-metadata/master/out/anatomical_systems.txt"
ANATOMICAL_SYSTEMS_FILE = "anatomical_systems.tsv"
ORGANS_URL = "https://raw.githubusercontent.com/gxa/atlas-metadata/master/out/organs.txt"
ORGANS_FILE = "organs.tsv"
JSON_FILE = "hierarchy.json"


def download_files():
  print "downloading files"
  urllib.urlretrieve(ANATOMICAL_SYSTEMS_URL, ANATOMICAL_SYSTEMS_FILE)
  urllib.urlretrieve(ORGANS_URL, ORGANS_FILE)


def parse_tsv(structure_file, tissues, parents, parent_type):
  with open(structure_file, 'r') as tsv:
    is_first_line = True
    for line in csv.reader(tsv, delimiter="\t"):
      # skip the first line (headers)
      if is_first_line:
        is_first_line = False
        continue

      # parse line
      parent_efo, parent_id, tissue_efo, tissue_id = line

      # add tissue (if not yet present)
      if tissue_id not in tissues.keys():
        tissues[tissue_id] = {
          "label": tissue_id,
        }
      
      # add parent (if not yet present)
      if parent_id not in parents.keys():
        parents[parent_id] = {
          "label": parent_id,
          "children": []
        }

      # add parent to tissue (if not yet present)
      if not parent_type in tissues[tissue_id]:
        tissues[tissue_id][parent_type] = []
      
      # add the tissue to the parent (if not yet present)
      if (tissue_id not in parents[parent_id]["children"]):
        parents[parent_id]["children"].append(tissue_id)

      # add the parent to the tissue (if not yet present)
      if (parent_id not in tissues[tissue_id][parent_type]):
        tissues[tissue_id][parent_type].append(parent_id)


def write_json(state):
  with open(JSON_FILE, 'w') as json_file:
    json.dump(state, json_file, sort_keys=True, separators=(',', ': '), indent=2)


def tsv2json():
  # state
  tissues = {}
  anatomical_systems = {}
  organs = {}

  # input
  parse_tsv(ANATOMICAL_SYSTEMS_FILE, tissues, anatomical_systems, 'anatomical_systems')
  parse_tsv(ORGANS_FILE, tissues, organs, 'organs')
  
  # output
  write_json({
    "tissues": tissues,
    "anatomical_systems": anatomical_systems,
    "organs": organs,
  })


if __name__ == '__main__':
  if not os.path.isfile(ANATOMICAL_SYSTEMS_FILE) or not os.path.isfile(ORGANS_FILE):
    download_files()

  tsv2json()
