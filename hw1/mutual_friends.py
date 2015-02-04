#mutual friends
import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
	key = record[0]
	value = record[1]
	for elem in value:
		rel = [key, elem]
		rel.sort()
		mr.emit_intermediate(('').join(rel), value);

def reducer(key, list_of_values):
	if len(list_of_values) == 2:
		common_friends= []
		for elem in list_of_values[0]:
			if elem in list_of_values[1]:
				common_friends.append(elem)
		if len(common_friends)>0:
			mr.emit((key, common_friends))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
