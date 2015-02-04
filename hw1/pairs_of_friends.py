#Assignment 1 problem 3
import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line
def mapper(record):
	key = record[0]
	value = record[1]
	for elem in value:
		rel = [key, elem]
		rel.sort()
		mr.emit_intermediate(('').join(rel), rel);


def reducer(key, list_of_values):
	if len(list_of_values)>1:
		mr.emit((list_of_values[0][0], list_of_values[0][1]))


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
