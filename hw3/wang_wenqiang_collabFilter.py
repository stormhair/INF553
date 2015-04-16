'''
	item based collaborative filtering
	Usage
		python collabFilter.py TRAININGFILE USERID #NEIGHBOR LENGTHOFLIST
'''
import sys
from math import sqrt

def set_join(set1, set2):
	assert type(set1) == type(dict()) and type(set2) == type(dict())
	common_user = list()
	for key in set1:
		if key in set2:
			common_user.append(key)
	return common_user

def similarity(iid1, iid2, rating_matrix):
	'''
	@param
		iid1: type:integer description:item id
		iid2: type:integer description:item id
		rating_matrix type:list description:rating matrix
	@return
		Pearson similarity between the two items indicated by iid1 and iid2 respectively
	'''
	u_set = set_join(rating_matrix[iid1], rating_matrix[iid2])
	if len(u_set) <= 1:
		return 0
	avg1 = 0
	avg2 = 0
	
	for u in u_set:
		avg1+=rating_matrix[iid1][u]
		avg2+=rating_matrix[iid2][u]
	avg1/=len(u_set)
	avg2/=len(u_set)
	
	numerator = 0
	s1 = 0
	s2 = 0
	for u in u_set:
		numerator+=(rating_matrix[iid1][u]-avg1)*(rating_matrix[iid2][u]-avg2)
		s1 += (rating_matrix[iid1][u]-avg1)*(rating_matrix[iid1][u]-avg1)
		s2 += (rating_matrix[iid2][u]-avg2)*(rating_matrix[iid2][u]-avg2)
	if s1 == 0 or s2 == 0:
		return 0
	return numerator/(sqrt(s1)*sqrt(s2))

def itemCF_train(rating_matrix):
	'''
	@param
		user_map_table type:dictionary description:map user id to index
		item_map_table type:dictionary description:map item name to index
		rating_matrix type:list description:rating matrix
	@return
		similarity_matrix type:list description:similarity matrix between items
	'''
	similarity_matrix = list()
	for i in range(0, len(rating_matrix)):
		similarity_matrix.append(dict())
	for i in range(0, len(rating_matrix)-1):
		for j in range(i+1, len(rating_matrix)):
			sim = similarity(i, j, rating_matrix)
			similarity_matrix[i][j] = sim
			similarity_matrix[j][i] = sim
	return similarity_matrix

def itemCF_predict(uid, n, k, rating_matrix, similarity_matrix, item_reverse_map_table):
	'''
	@param
		uid: type:string description:user id
		n: type:integer description:the number of nearest neighbors for calculating scores
		k: type:integer description:the length of the recommender list
		rating_matrix: type:list description:rating matrix, where each element indicates the score of i rated by u
		similarity_matrix: type:list description:similarity matrix between items
	@return
		a list of length k which contains the recommended items for the user with user id indicated by uid
	'''
	score_pred = list()
	for iid in range(0, len(similarity_matrix)):
		if uid not in rating_matrix[iid]:
			pred = [iid, item_reverse_map_table[iid], 0]
			#if len(similarity_matrix[iid])>=n:
			wij = list()
			for key in similarity_matrix[iid]:
				wij.append([key, item_reverse_map_table[key], similarity_matrix[iid][key]])
			wij.sort(key = lambda x:x[1])
			wij.sort(reverse = True, key = lambda x:x[2])
			numerator = 0
			denominator = 0
			c = 0
			for i in range(0, len(wij)):
				if uid in rating_matrix[wij[i][0]]:
					numerator+=rating_matrix[wij[i][0]][uid]*wij[i][2]
					denominator+=abs(wij[i][2])
					c+=1
				if c == n:
					break
			if denominator!=0:
				pred[2] = numerator/denominator
			else:
				pred[2] = 0
			score_pred.append(pred)
	score_pred.sort(key = lambda x: x[1])
	score_pred.sort(reverse = True, key = lambda x: x[2])
	rec_list = list()
	for i in range(0, k):
		rec_list.append(score_pred[i])
	return rec_list

def load_train(path):
	'''
	@param
		path: type:string description:the file path containing training set
	@return
		user_map_table type:dictionary description:map user id to index
		item_map_table type:dictionary description:map item name to index
		item_reverse_map_table type:dictionary description:map index to item name
		rating_matrix type:list description:rating matrix
	'''
	handler = open(path)
	item_idx = 0
	user_idx = 0
	user_map_table = dict()
	item_map_table = dict()
	item_reverse_map_table = dict()
	rating_matrix = list()
	while True:
		text = handler.readline()
		if not text:
			break
		tokens = text.strip().split('\t')
		assert len(tokens) == 3
		uid = tokens[0]
		score = float(tokens[1])
		title = tokens[2]
		if uid not in user_map_table:
			user_map_table[uid] = user_idx
			user_idx+=1
		if title not in item_map_table:
			item_map_table[title] = item_idx
			item_reverse_map_table[item_idx] = title
			item_idx+=1
		iidx = item_map_table[title]
		uidx = user_map_table[uid]
		if iidx>=0 and iidx<len(rating_matrix):
			rating_matrix[iidx][uidx] = score
		else:
			rating_matrix.append(dict())
			rating_matrix[iidx][uidx] = score
	print('#User '+str(user_idx)+' #Item '+str(item_idx), file = sys.stderr)
	handler.close()
	return user_map_table, item_map_table, item_reverse_map_table, rating_matrix

def main():
	if len(sys.argv)!=5:
		print('python '+sys.argv[0]+' TRAININGFILE USERID #NEIGHBOR LENGTHOFLIST', file = sys.stderr)
		return
	training_file_path = sys.argv[1]
	target_uid = sys.argv[2]
	n_neighbor = int(sys.argv[3])
	len_list = int(sys.argv[4])

	#read data
	umt, imt, irmt, rm = load_train(training_file_path)

	if target_uid not in umt:
		print('Fatal error: no user information', file = sys.stderr)
		return

	#training: calculate similarity matrix
	sm = itemCF_train(rm)
	#make recommendation
	rl = itemCF_predict(umt[target_uid], n_neighbor, len_list, rm, sm, irmt)
	#output recommendation list
	print('Recommendation', file = sys.stderr)
	for i in range(0, len(rl)):
		print('%s\t%.5f' %(rl[i][1], rl[i][2]))

if __name__ == '__main__':
	main()
