# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 21:15:54 2022

@author: Temitayo
"""
#import beautiful soup to parse web pages
from bs4 import BeautifulSoup

#libary contains a set of requests exception
import requests.exceptions

#library to split URL string into its components 
from urllib.parse import urlsplit

#library to create a deque object initialized from left-to-right
from collections import deque

#csv for import and export format for spreadsheets
import csv

#import networkx to inspect & visualize the dynamic and structure of the social network
import networkx as nx

#import pandas for data analysis
import pandas as pd

#import matplotlib to create plots for the statisctics of the network
import matplotlib.pyplot as plt

#import pylab that uses matplotlib and numpy with a single namespace
from matplotlib import pylab as pl

#import nxcom for community detection
import networkx.algorithms.community as nxcom

# sorting and printing 10 top or least nodes
def nodes_sort(dictionary, order):

    #initialize the variable to zero
    count = 0

    #sort the dictionary in ascending/descending form based on arguments passed
    nodes_order = sorted(dictionary, key = dictionary.get, reverse=order)

    #looping through sorted dictionary
    for key in nodes_order:

        #print only first ten nodes
        if count < 10:

            #print name of url and centrality value
            print(str(key) +': '+ str(dictionary[key]))
        
        #increase the variable count by 1
        count += 1
        
#creating an excel file for further analysis and manual preprocessing

# create an excel file to contain and save edges 
excel_file = 'edges.csv'

#open the file to start writing values into it
e = csv.writer(open(excel_file, 'w', newline='', encoding='utf-8')) 

#write and set the header in the first row
e.writerow(['source', 'target'])  


# links already worked on
links_processed = set()

#a set to hold web links within the target site
links_local = set()

#a set to hold web links outside of target site
links_external = set()

#a set to hold bad web links
links_invalid = set()

#link to the webpage to be crawled
link = 'ontariotechu.ca'

# initialize a queue with web links
links_current = deque([link])  


#run loop continuously

#using current crawled link
while len(links_current):  
    
    #pop current url from queue and get the next url
    url = links_current.popleft() 
    
    #add new url to processed links
    links_processed.add(url)  

    # test to see the url can be reached with no error
    try:
        response = requests.get(url)  
        
        #if there is an error or exception, the link is invalid
    except(equests.exceptions.InvalidURL, requests.exceptions.ConnectionError requests.exceptions.MissingSchema): 
        
        # add it to the set of invalid 
        links_invalid.add(url)
        
        #continue working on crawling links
        continue
    
    
    # get the consistent base url 
    
    # strip the url and extract its components
    parts = urlsplit(url)  
    
    #get network location (domain and port number)
    base = "{0.netloc}".format(parts)
    
    #remove 'www' from the url
    strip_base = base.replace("www.", "")
    
    #get the addressing scheme and path of the url
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    
    
    # use beautiful soup to parse web page and extract data
    result = BeautifulSoup(response.text, 'lxml')

    #find all 'a'(a_link) tags in web page holding links
    for anchor in result.find_all('a'):  
        
        #if there's a href attribute in the a_link tag assign it to variable
        a_link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
        
        # create links meeting the conditionals
        if a_link.startswith('/'):
            #concatenate the stripped base url and anchor link gotten from web page
            local_link = base_url + a_link
            
            #add newly formed link to the set
            links_local.add(local_link)
            
            #if stripped link is found in any of the links found in the web page
        elif strip_base in a_link:
            #add link to the set
            links_local.add(a_link)
            
            #if the link on the web does not have the 'http' in its address
        elif not a_link.startswith('http'):
            
            #concatenate the stripped path from base url with the link
            local_link = path + a_link
            links_local.add(local_link)
            
        #otherwise it's a link external to target website    
        else:
            links_external.add(a_link)

       #loop through the local links
        for url in links_local:
            
            #if current url is not a current link and wasn't proccessed
            if not url in links_current and not url in links_processed:
                
                #append it to current links set
                links_current.append(i)
                
                try:
                     # write the source and target links to the excel file opened above
                    e.writerow([url, i])
                    
                    #for exceptions, print to the console
                except:
                    print("Write Error: ", [url, i])

    # get only 9500 links
    for i in range(9500):  
        
        #print to user what iteration the crawler is on
        print('Iteration ' + str(len(links_current)))
        
        break
    
    
    #------------visualizing the network-----------

#create the graph object
G = nx.Graph()

#format the data gotten from 'ontariotechu.ca & uoit.ca' to a grpah
G = nx.from_pandas_edgelist(excel_file)

#print out statistical information of the graph for readability to user
print("------------Length of G", len(G))
print("OntarioTech / UOIT Statistics")

#networkx function to determine if network is weighted, returns bool value
if nx.is_weighted(G):
    #the network is weighted
    print('Weighted: Yes')
else:
   #the network is not weighted
    print('Unweighted: Yes')

#networkx function to determine if network is directed
if nx.is_directed(G):
    #the network is directed
    print('Directed: Yes')
    
    #returns number of scc in the network
    scc = nx.number_strongly_connected_components(G)

    #returns a generator nodes in scc
    nodes_scc = nx.strongly_connected_components(G)
    
    #returns number of wcc in the network
    wcc = nx.number_weakly_connected_components(G)

    #returns a generator nodes in wcc
    nodes_wcc = nx.weakly_connected_components(G)
    
    #printing out the wcc and scc numbers and nodes
    print("Strongly Connected Components (SCC)")
    print("Components Number: ", scc)
    print("Nodes in SCC (SCC): ", nodes_scc)
    
    print("Weakly Connected Components (WCC)")
    print("Components Number: ", wcc)
    print("Nodes in WCC (WCC): ", nodes_wcc)
    
    
#the network is undirected
else:
    #initialize the variable to zero
    count = 0

    #converts the nodes in the generated connected components into a list
    cc = list(nx.connected_components(G) )

    #prints if the network is undirected
    print('Undirected: Yes')

    #prints numnber of connected component(cc) and some nodes in the cc
    print('Connected Components Number: ', len(cc))
    print('\nSome nodes')

    #starts a loop to iterate between items in cc generated above
    for key in cc:

      #only prints 5 nodes in cc of undirected graph
      if count < 5:
        print(str(key))

      #increase count by 1
      count += 1
    
#returns number of nodes in the graph
nodes = nx.number_of_nodes(G)

#returns number of edges in the graph
edges = nx.number_of_edges(G)

#returns the density of a graph.
edge_density = nx.density(G)

# computes the average clustering coefficient of the graph
clustering = nx.average_clustering(G)

#returns a generator converted to a dictionary containing the degrees of nodes in the graph
degree = dict(G.degree(G))

#calculates sum of all the node degrees
sum_deg = sum(degree.values())

#caluclates the average degree of the graph G by dividing sum of degrees by the total number of nodes
avg_degree = sum_deg/nodes

#returns the average shortest path length.
path_length = nx.average_shortest_path_length(G) 

#returns the diameter of the graph
diameter = nx.diameter(G)


#printing all the statistics computed and generated above
print('Number of nodes: ', nodes)
print('Number of edges: ', edges)
print('Average degree: ', avg_degree)
print('Edge density: ', edge_density)
print('Clustering Coefficient: ',clustering)
print('Average path length: ', path_length)
print('Network diameter: ', diameter)

#set a value to m give the spacing in the plot a range     
m = 3

#create a figure object
fig = plt.figure()

#returns a list of the frequency of each degree value
degree_freq = nx.degree_histogram(G)

#create a range from 0 to the length of degree frequency values
degrees = range(len(degree_freq))

#set the size of the figure object
plt.figure(figsize=(12, 8)) 

#plot the degree values on x-axis and the frequency on y-axis
plt.plot(degrees[m:], degree_freq[m:],'go-') 

#label the x-axis and y-axis
plt.xlabel('Frequency Count')
plt.ylabel('Degree Value')

#name the title of the plot
plt.title("Degree Distribution")

#display the plotted graph
plt.show()

#set a value to m give the spacing in the plot a range    
m= 10

#create a figure object
fig = plt.figure()

#returns a list of the frequency of each degree value
degree_freq = nx.degree_histogram(G)

#create a range from 0 to the length of degree frequency values
degrees = range(len(degree_freq))

#set the size of the figure object
plt.figure(figsize=(12, 8)) 

#plot the degree values on x-axis and the frequency on y-axis on a logarithmic scale
plt.loglog(degrees[m:], degree_freq[m:],'go-') 

#label the x-axis and y-axis
plt.xlabel('Frequency Count')
plt.ylabel('Degree Value')

#name the title of the plot
plt.title("Log-log Degree Distribution")

#display the plotted graph
plt.show()


print('\n-------------------')
print("\nNotions of Centrality")

#Degree Centrality
deg_centrality = nx.degree_centrality(G) #returns degree centrality values of all the nodes

print('\n-------------------')
print('\nDegree Centrality')
print('\nTop 10 nodes')
nodes_sort(deg_centrality, True) #prints degree centrality values in descending order (highest values)

print('\nLeast 10 nodes')
nodes_sort(deg_centrality, False) #prints degree centrality values in ascending order (lowest values)


# #Betweenness Centrality
betw_centrality = nx.betweenness_centrality(G) #returns betweenness centrality values of all the nodes

print('\n-------------------')
print('\nBetweenness Centrality')
print('\nTop 10 nodes')
nodes_sort(betw_centrality, True) #prints betweenness centrality values in descending order (highest values)

print('\nLeast 10 nodes')
nodes_sort(betw_centrality, False) #prints betweenness centrality values in ascending order (lowest values)

# # Closeness Centrality
close_centrality = nx.closeness_centrality(G) #returns closeness centrality values of all the nodes


print('\n-------------------')
print('\nCloseness Centrality')
print('\nTop 10 nodes')
nodes_sort(close_centrality, True) #prints closeness centrality values in descending order (highest values)
 
print('\nLeast 10 nodes')
nodes_sort(close_centrality, False) #prints closeness centrality values in ascending order (lowest values)


# PageRank Centrality
pagerank_cent = nx.pagerank(G) #returns pagerank centrality values of all the nodes

# print('\n-------------------')
# print('\nPageRank Centrality')
# print('\nTop 10 nodes')
# nodes_sort(pagerank_cent, True) #prints pagerank centrality values in descending order (highest values)

print('\nLeast 10 nodes')
nodes_sort(pagerank_cent, False) #prints pagerank centrality values in ascending order (lowest values)
    

#import community_louvain to run community algorithm on the graph
import community.community_louvain as community_louvain

#import colormaps from matplolib
import matplotlib.cm as cm

#update parameters of the figure object
plt.rcParams.update({'figure.figsize': (7, 5)})

#compute the best partition
partition = community_louvain.best_partition(G)

# draw the graph using Fruchterman-Reingold force-directeda algorithm
pos = nx.spring_layout(G)

#use color maps to change color of communities
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)

# draw and color the nodes within the communities
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=10,
                       cmap=cmap, node_color=list(partition.values()))

#draw and color network edges
nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color='black')

#display graph
plt.show()



# Find the communities
communities = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)

# Count the communities
print(f"The karate club has {len(communities)} communities.")


# draw the graph using Fruchterman-Reingold force-directed algorithm
pos = nx.spring_layout(G)

#visualize the entire network with all of its nodes and edges
nx.draw(G, node_size=20, node_color='blue', edge_color='lightblue')

#display the complete network using the spring layout declared above
plt.show()



#returns a random graph with a probability of 0.5  
G=nx.erdos_renyi_graph(n=5929,p=.05)

close_cent=nx.closeness_centrality(G)

#creates a graph with nodes only with closeness centrality values over 0.1
G2=nx.subgraph(G,[x for x in G.nodes() if close_cent[x] > 0.1])

#change size based on closeness centrality values
size = [v * 10000 for v in close_cent.values()] 

# draw the graph using Fruchterman-Reingold force-directed algorithm
pos = nx.spring_layout(G2)

#draw the subgraph with nodes and edges
nx.draw(G2, pos, with_labels=True, node_size=10, node_color='purple', font_color='white', font_size=2, edge_color='lightgrey')

#display the graph
pl.show()


#returns a random graph with a probability of 0.5  
G=nx.erdos_renyi_graph(n=5929,p=.05)

#creates a graph with nodes only with closeness centrality values over 0.1
G2=nx.subgraph(G,[x for x in G.nodes() for v in degree.values() if v > 50])

#change size based on closeness centrality values
size = [v * 10000 for v in degree.values()] 

# draw the graph using Fruchterman-Reingold force-directed algorithm
pos = nx.nx_pydot.graphviz_layout(G2)

#draw the subgraph with nodes and edges
nx.draw(G2, pos, with_labels=True, node_size=10, node_color='olive', font_color='white', font_size=2, edge_color='black')

#display the graph
pl.show()