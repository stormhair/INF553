#Assignment 1 problem 2
import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
   key = record[0]
   value = record[1]
   mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    friend = []
    list_of_values.sort()
    pre = ""
    for i in range(0, len(list_of_values)):
    	if list_of_values[i]!=pre:
    		friend.append(list_of_values[i])
    	pre = list_of_values[i]
    mr.emit((key, friend))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
