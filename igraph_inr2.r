library(igraph)


# csv_file should be in csv format where it has the entire edgelist.
# A data frame, wehre one of the columns has the "user_id" as the header, and "collegue_id" as another. 
# Example:
# user_id, colleague_id
# 1, 2
# 2, 3
# 4, 3


csv_to_table <- function(csv_file, directed) {
	csv_data <- read.csv(csv_file)
	#get unique user_id
	unique_user <-unique(csv_data["user_id"])
	unique_colleague <- unique(csv_data["colleague_id"])
	names(unique_user) <- "unique_num"
	names(unique_colleague) <- "unique_num"
	unique_id <-unique(rbind(unique_user, unique_colleague))
	#make the actual edge dataframe
	tofrom <-cbind(csv_data["user_id"], csv_data["colleague_id"])
	#let's make the (directed) graph
	g <- graph.data.frame(tofrom, directed, vertices=unique_id)
	g
}


#################################################
### Network realated calculations ###############
#################################################

#maximal.cliques finds all maximal cliques in the input graph. 
#A clique in maximal if it cannot be extended to a larger clique. 
#The largest cliques are always maximal, but a maximal clique is not neccessarily the largest.

# Community detection algorithms:
# if you would like to use other algo plz look at this link : http://stackoverflow.com/questions/9471906/what-are-the-differences-between-community-detection-algorithms-in-igraph
# g_fastgreedy_community <- fastgreedy.community(g, merges=TRUE, modularity=TRUE, membership=TRUE, weights= NULL)
# g_walktrap_community <- walktrap.community(g, steps = 4, merges =TRUE, modularity = TRUE, membership = TRUE, weights = NULL)


writetable <- function(data, directed, d = 0, in_d = 0, out_d = 0, between = 0, closeness = 0, eig = 0, fc = 0, wc = 0, clique =0) {
	g = csv_to_table(data, directed)
	u_g = as.undirected(g, mode=c("collapse"))
	new_matrix = matrix(ncol = 1, nrow = vcount(g))
	if (d == "degree") 
	{
		g_degree = degree(g, normalized=TRUE)
		new_matrix = cbind(new_matrix, g_degree) 
	}
	if (in_d == "indegree") {
		g_indegree = degree(g, normalized=TRUE, mode = c("in"))
		new_matrix = cbind(new_matrix, g_indegree)
	}
	if (out_d == "outdegree") {
		g_outdegree = degree(g, normalized=TRUE, mode = c("out"))
		new_matrix = cbind(new_matrix, g_outdegree)
	}
	if (between == "between") {
		g_between = betweenness(g, normalized=TRUE)
		new_matrix = cbind(new_matrix, g_between)
	}
	if (closeness == "closeness") {
		g_closeness = closeness(g, normalized=TRUE)
		new_matrix = cbind(new_matrix, g_closeness)
	}
	if (eig == "eigenvector") {
		g_eigv_centr= evcent(g)$vector
		new_matrix = cbind(new_matrix, g_eigv_centr)
	}
	if (fc == "fc") {
		g_fastgreedy_community <- fastgreedy.community(u_g, merges=TRUE, modularity=TRUE, membership=TRUE, weights= NULL)
		fastgreedy_membership <- membership(g_fastgreedy_community)
		fg_dataframe <- as.data.frame(fastgreedy_membership)
		write.csv(fg_dataframe, file = "fc.csv", row.names = TRUE)
	}
	if (wc == "wc") {
		g_walktrap_community <- walktrap.community(u_g, steps = 4, merges =TRUE, modularity = TRUE, membership = TRUE, weights = NULL)
		walktrap_membership <- membership(g_walktrap_community)
		wc_dataframe <- as.data.frame(walktrap_membership)
		write.csv(wc_dataframe, file = "wc.csv", row.names = TRUE)
	}
	if (clique == "clique") {
		g_cliques <- maximal.cliques(u_g, min=NULL, max=NULL, subset=NULL, file = "cliques.csv")
	}
	#getting rid of the first NA column
	new_matrix = new_matrix[,-1]
	write.csv(new_matrix, file = "igraph_table.csv", row.names = TRUE)

}


