import sys, collections, csv
import copy
import numpy as np
import pandas as pd
import igraph as gp
from sklearn.metrics.pairwise import cosine_similarity

def cosineSimilarity(x, community_list, community_id, g, consine_data, no_of_clusters):
	count_for_new_cluster = 0.0
	count_for_old_cluster = 0.0
	new_community = community_list[community_list == community_id].index
	for i in new_community:
		count_for_new_cluster += consine_data[i, x]

	community_of_x = community_list[x]
	old_community = set(community_list[community_list == community_of_x].index)

	old_community = old_community - set([x])

	for i in old_community:
		count_for_old_cluster += consine_data[i, x]

	new_cardinalities = map(lambda x: g.vs[x]["c"], new_community)
	old_cardinalities = map(lambda x: g.vs[x]["c"], old_community)

	if(len(old_cardinalities) == 0):
		return float(count_for_new_cluster)/(sum(new_cardinalities)**2)
	else:
		return float(count_for_new_cluster)/(sum(new_cardinalities)**2) - float(count_for_old_cluster)/(sum(old_cardinalities)**2)

def cleaningUp(j, i, g, community_list, consine_data, old_modularity_newman):
	temp_membership = copy.deepcopy(community_list)
	community_of_j = community_list[j]
	temp_membership[i] = community_of_j

	if alpha_value == 1:
		delta_newman =  g.modularity(temp_membership, weights=g.es['weight']) - old_modularity_newman
		delta_sim = 0
	elif alpha_value == 0:
		delta_newman = 0
		delta_sim = cosineSimilarity(i, community_list, community_of_j, g, consine_data, no_of_clusters = 0)
	else:
		delta_newman =  g.modularity(temp_membership, weights=g.es['weight']) - old_modularity_newman
		delta_sim = cosineSimilarity(i, community_list, community_of_j, g, consine_data, no_of_clusters = 0)

	composite_delta = alpha_value * delta_newman + (1 - alpha_value) * delta_sim

	return composite_delta


def phase1(g, community_list, g_original):
	no_of_nodes = len(g.vs)

	consine_data = np.zeros((no_of_nodes, no_of_nodes))

	if alpha_value != 1:
		for i in range(no_of_nodes):
			for j in range(i, no_of_nodes):
				consine_data[i, j] = cosine_similarity(g.vs[i]["attr"].reshape(1, -1), g.vs[j]["attr"].reshape(1, -1))
				consine_data[j, i] = consine_data[i, j]

	for loop in range(15):
		copy_community = copy.deepcopy(community_list)
		for i in range(no_of_nodes):
			max_comp_mod = float('-inf')
			max_composite_j = 0
			old_modularity_newman = g.modularity(community_list, weights=g.es['weight'])
			no_of_clusters = community_list.nunique()

			for j in community_list.unique():
				composite_delta = cleaningUp(j, i, g, community_list, consine_data, old_modularity_newman)
				if composite_delta > max_comp_mod:
					max_comp_mod = composite_delta
					max_composite_j = j

			if max_comp_mod > 0:
				community_list[i] = community_list[max_composite_j]

		print "This is inside loop number: " + str(loop)
		if copy_community.equals(community_list):
			break
	return community_list


def attribute_mean(x):
	return sum(x)/len(x)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "No alpha value provided"
		sys.exit(1)

	alpha_value = float(sys.argv[1])

	g = gp.Graph.Read_Edgelist('data/fb_caltech_small_edgelist.txt', directed=False)
	attr = pd.read_csv("data/fb_caltech_small_attrlist.csv")
	headers = attr.columns.tolist()

	for i, item in attr.iterrows():
		g.vs[i]["attr"] = item

	g.es["weight"] = 1
	g.vs["c"] = 1

	g_original = g.copy()

	clusters_dict = dict()
	for item in range(len(g.vs)):
		clusters_dict[item] = [item]

	community_list = pd.Series(range(len(g.vs)))
	print "This is gonna take a long time. Grab a cup of drink..."

	for i in range(15):
		no_of_nodes = len(g.vs)
		if no_of_nodes == 1:
			break
		#Earlier code suffered because of not using deepcopy.
		#The new list was just binding not copying
		copy_community = copy.deepcopy(community_list)
		community_list = pd.Series(range(no_of_nodes))

		community_list = phase1(g, community_list, g_original)

		unique_clusters = community_list.unique()
		panda_unique = pd.Series(unique_clusters)

		community_map = community_list.map(lambda x: pd.Index(panda_unique).get_loc(x))

		next_clusters_dict = dict()

		for item in range(len(unique_clusters)):
			curr_cluster = list(community_map[community_map == item].index)
			next_cluster = list()
			for item_c in curr_cluster:
				next_cluster = next_cluster + clusters_dict[item_c]
			next_clusters_dict[item] = next_cluster

		clusters_dict = next_clusters_dict

		g.contract_vertices(community_map, combine_attrs=dict(c=sum, attr=attribute_mean))
		g.simplify(loops=False, combine_edges=sum)
		print "This is outside loop number: " + str(i)
		if copy_community.equals(community_list):
			break
	out_file = open("communities.txt",'w')
	line = "\n".join(",".join(str(x) for x in clusters_dict[item]) for item in clusters_dict.iterkeys())
	out_file.write(line)
	out_file.write('\n')
	out_file.close()
