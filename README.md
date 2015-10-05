# machine_learning

#How to use igraph_inr2.r:
PLEASE INSTALL IGRAPH BEFORE RUNNING THESE FILES
(if you don't have igraph installed, go to r and type "install.packages("igraph")")

1. Put both igraph_inr2.r and igraph_r_wrapper.r in the same folder where the output csv files are going to be created

2. In terminal, cd in to the folder where those two files are placed

3. In terminal type:
Rscript igraph_r_wrapper.r input.csv TRUE degree indegree outdegree between closeness eigenvector fc wc clique
1) TRUE means the graph is directed. If you want undirected graph, write FALSE instead.

2) replace input.csv with whatever your input input csv file.
csv_file should be in csv format where it has the entire edgelist.
A data frame, wehre one of the columns has the "user_id" as the header, and "collegue_id" as another. 
 Example:
user_id, colleague_id
1, 2
2, 3
4, 3

3) if you do not want any of the features replace it with 0

For example: 
Rscript igraph_r_wrapper.r input.csv TRUE degree indegree outdegree between closeness 0 fc wc 0
--> this command will not calculate eigenvector and clique

#How to use Search_Tweets
Before you use this script, please read the code to understand what each function is doing. Change the input/output file and write the function that you want to run. Ex. python search_tweets.py search_tweets_by_queries

#How to run NN_mse_cee
python -i hw6.py
In python, type kaggle() to get the csv file
Or you can run other functions to get accuracy
- mse_accuracy()
- cee_accuracy()
- 

