import numpy as np


# NORMALIZED_COUNTS_FILE = "1706_exp_summary_counts_all_genes.txt"
ARRAY_FILE = "array.txt"
# note: generate array.txt using the following (removes first row/column and reshapes 2d -> 1d)
# cut -f2- 1706_exp_summary_counts_all_genes.txt | tail -n +2 | tr '\t' '\n' > array.txt


if __name__ == '__main__':
  # load flat numeric array
  array = np.loadtxt(ARRAY_FILE)

  # required deciles
  deciles_as_percentiles = range(0, 101, 10)

  # filter
  array_above_zero = array[np.where(array > 0)]
  array_above_one = array[np.where(array > 1)]

  # calculate deciles (raw)
  deciles = np.percentile(array, deciles_as_percentiles)
  print 'Raw deciles:'
  print deciles
  print '\n'

  # calculate deciles (above zero)
  deciles = np.percentile(array_above_zero, deciles_as_percentiles)
  print '[x > 0] deciles:'
  print deciles
  print '\n'

  # calculate deciles (above one)
  deciles = np.percentile(array_above_one, deciles_as_percentiles)
  print '[x > 1] deciles:'
  print deciles
  print '\n'

  # # get max 20 values
  max_values = array[array.argsort()[-20:]]
  print 'largest 20 values:'
  print max_values
