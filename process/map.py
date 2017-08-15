import os.path
import csv
import json
import urllib


ANATOMICAL_SYSTEMS_URL = "https://raw.githubusercontent.com/gxa/atlas-metadata/master/out/anatomical_systems.txt"
ORGANS_URL = "https://raw.githubusercontent.com/gxa/atlas-metadata/master/out/organs.txt"
ANATOMICAL_SYSTEMS_FILE = "anatomical_systems.tsv"
ORGANS_FILE = "organs.tsv"
CURATION_FILE = "curation.tsv"
MERGED_TISSUES_FILE = "merged_rna_protein_tissues.txt"
HIERARCHY_JSON_FILE = "hierarchy.json"
MAP_JSON_FILE = "map.json"


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
        tissues[tissue_id] = {}
      
      # add parent (if not yet present)
      if parent_id not in parents.keys():
        parents[parent_id] = []

      # add parent to tissue (if not yet present)
      if not parent_type in tissues[tissue_id]:
        tissues[tissue_id][parent_type] = []
      
      # add the tissue to the parent (if not yet present)
      if (tissue_id not in parents[parent_id]):
        parents[parent_id].append(tissue_id)

      # add the parent to the tissue (if not yet present)
      if (parent_id not in tissues[tissue_id][parent_type]):
        tissues[tissue_id][parent_type].append(parent_id)


def parse_txt():
  # merged file contains tissue names from protein and rna
  with open(MERGED_TISSUES_FILE, 'r') as txt:
    tissues = [tissue.strip() for tissue in txt]
  
  # curations map some slightly variant names together
  curations = parse_curations()

  # apply curations
  curated_tissues = [curations[tissue] if tissue in curations else tissue
                     for tissue in tissues]

  return curated_tissues


def parse_curations():
  curations = {}

  with open(CURATION_FILE, 'r') as tsv:
    for line in csv.reader(tsv, delimiter="\t"):
      original, mapped = line
      curations[original] = mapped
  
  return curations


def write_json(filename, state):
  with open(filename, 'w') as json_file:
    json.dump(state, json_file, sort_keys=True, separators=(',', ': '), indent=2)


def filter_parents(parents, parent_type, minimal_tissues):
  # for each parent, filter its tissue list against the minimal list
  filtered_parents = {parent_name: [tissue_name 
                                    for tissue_name in tissue_list
                                    if tissue_name in minimal_tissues]
                      for (parent_name, tissue_list) in parents.iteritems()}

  # there may now be parents with empty tissue lists, so remove these
  filtered_parents = {parent_name: tissue_list
                      for (parent_name, tissue_list) in filtered_parents.iteritems()
                      if len(tissue_list) > 0}

  return filtered_parents

def tsv2json():
  # state
  tissues = {}
  anatomical_systems = {}
  organs = {}

  # input
  parse_tsv(ANATOMICAL_SYSTEMS_FILE, tissues, anatomical_systems, 'anatomical_systems')
  parse_tsv(ORGANS_FILE, tissues, organs, 'organs')
  minimal_tissues = parse_txt()
  
  # filter
  filtered_tissues = {tissue_name: info
                      for (tissue_name, info) in tissues.iteritems()
                      if tissue_name in minimal_tissues}
  filtered_organs = filter_parents(organs, 'organs', minimal_tissues)
  filtered_anatomical_systems = filter_parents(anatomical_systems, 'anatomical_systems', minimal_tissues)

  # checks
  assert all(tissue_name in filtered_tissues.keys() for tissue_name in minimal_tissues), \
         'Not all minimal tissues present in curated gxa mappings, specifically:\n%s' % \
         '\n'.join(tissue_name for tissue_name in minimal_tissues if tissue_name not in filtered_tissues.keys())
  assert all(len(info['anatomical_systems']) > 0 for (tissue_name, info) in filtered_tissues.iteritems()), \
         'Not all minimal tissues have at least one anatomical system'
  assert all(len(info['organs']) > 0 for (tissue_name, info) in filtered_tissues.iteritems()), \
         'Not all minimal tissues have at least one organ'

  # output
  write_json(HIERARCHY_JSON_FILE, {
    "anatomical_systems": filtered_anatomical_systems,
    "organs": filtered_organs,
  })
  write_json(MAP_JSON_FILE, {
    "tissues": filtered_tissues
  })


if __name__ == '__main__':
  if not os.path.isfile(ANATOMICAL_SYSTEMS_FILE) or not os.path.isfile(ORGANS_FILE):
    download_files()
  
  tsv2json()
