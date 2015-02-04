#Assignment 1 problem 1 problematic???
import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
	key = record[0]
	value = record[1]
	words = value.split()
	count = [0, 0, 0, 0]
	for w in words:
		wl = len(w)
		if wl < 2:
			count[0] += 1
		elif wl>=2 and wl<5:
			count[1] += 1
		elif wl>=5 and wl<10:
			count[2] += 1
		else:
			count[3] += 1
	mr.emit_intermediate(key, count)

def reducer(key, list_of_values):
	total_count = [["tiny", 0], ["small", 0], ["medium", 0], ["large", 0]]
	for vec in list_of_values:
		for i in range(0, len(vec)):
			total_count[i][1]+=vec[i]
	mr.emit((key, total_count))

if __name__ == '__main__':
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)