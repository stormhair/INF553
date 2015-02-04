#relational_join
#mutual friends
import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
	key = record[0]
	if key == 'MovieNames':
		mr.emit_intermediate(record[2], record)
	elif key == 'MovieRatings':
		mr.emit_intermediate(record[1], record)

def reducer(key, list_of_values):
	t1=[]
	t2=[]
	for v in list_of_values:
		if v[0] == 'MovieNames':
			t1.append(v)
		elif v[0] == 'MovieRatings':
			t2.append(v)
	if len(t1)>0 and len(t2)>0:
		total_score = 0
		for elem1 in t1:
			for elem2 in t2:
				ret = []
				for i in range(1, len(elem1)):
					ret.append(elem1[i])
				for i in range(1, len(elem2)):
					ret.append(elem2[i])
				mr.emit(ret)
				total_score += elem2[3]
		mr.emit((t1[0][1], total_score/len(t2)))

if __name__ == '__main__':
	inputdata = open(sys.argv[1])
	mr.execute(inputdata, mapper, reducer)
