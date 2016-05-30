# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#
import copy
import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Instantiate the graph.
# Then reading the file line by line 
# if the node doesn't exist yet, add it
# and add appropriate destination 
# (again add to the node list if doesn't exist) and weight
#
def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    # instantiate a graph
    g = WeightedDigraph()
    
    # open and read file line by line
    f = open(mapFilename)
    for line in f:
        
        data = line.split()
        
        n1 = Node(data[0])
        n2 = Node(data[1])
        if not g.hasNode(n1):
            g.addNode(n1)
        if not g.hasNode(n2):
            g.addNode(n2)
        
        g.addEdge(WeightedEdge(n1, n2, float(data[2]), float(data[3])))
        
    return g
    
#mitMap = load_map("/Users/makarymalinouski/Documents/Programming/MIT-CS.2/ProblemSet5/mit_map.txt")
##print isinstance(mitMap, Digraph)
##print isinstance(mitMap, WeightedDigraph)        
#nodes = mitMap.nodes
#print nodes


#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# Look for the shortest path using depth-first-search.
# Start at the src node, put its children on a stack,
# look at the first one and put its children, then look at the first one
# among the children, etc.
# Once all paths found, check which ones satisfy constraints.
# Then fine the shortest.
#
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """    
    ls = []
    allPaths = DFS(digraph, start, end, ls[:], ls[:])
    validPaths = []
    for p in allPaths:
       if validatePath(digraph, p[:], maxTotalDist, maxDistOutdoors):
           validPaths.append(p[:])
                
    if validPaths == []:
        raise ValueError('No paths that satisfy max distance')
    
    return findShortestPath(digraph, validPaths)    


def DFS(digraph, start, end, path, result):
    
    if start == None:
        return result
    if start not in path:
        path.append(start)
    if start == end:
        #print path
        return path
    #print "appending children of ", start      
    for child in digraph.childrenOf(Node(start)):
        #print "child ", child.getName()
        if child.getName() not in path:    
            #print "path ", path
            newPath = copy.deepcopy(DFS(digraph, child.getName(), end, path, result))
            
            if newPath != None:
                result.append(newPath)
           
            path.pop()
    if len(path) <= 1:
        #print "!!!!!!!!!!!!!!!!!ALL PATHS!!!!!!!!!!!!!!!\n" , result[0:5], "\n!!!!!!!!!!!!!!!!!ALL PATHS!!!!!!!!!!!!!!!\n"
        return result

def validatePath(digraph, path, maxTotalDist, maxDistOutdoors):
    dist = ((-1)*maxTotalDist, (-1)*maxDistOutdoors)
    prev_node = None
    for i, node in enumerate(path):
        if i > 0:
            for edge in digraph.edges[Node(prev_node)]:
                if edge[0] == Node(node):
                    dist = map(sum, zip(edge[:][1], dist))
                    if dist[0] > 0 or dist[1] > 0:
                        return False
        prev_node = node
    return True
    
def findShortestPath(digraph, paths):
    shortestDist = 1000000000000
    shortestPath = None
    prev_node = None
    for path in paths:
        dist = 0
        for i, node in enumerate(path):
            if i > 0:
                for edge in digraph.edges[Node(prev_node)]:
                    if edge[0] == Node(node):
                        dist += edge[1][0]
                        if dist >= shortestDist:
                            continue
            prev_node = node                
            
        if dist < shortestDist:    
            shortestDist = dist
            shortestPath = path
    
    return shortestPath

#mitMap = load_map("/Users/makarymalinouski/Documents/Programming/MIT-CS.2/ProblemSet5/mit_map.txt")            
#print mitMap.edges
#print DFS(mitMap, "32", "67")
#print bruteForceSearch(mitMap, "12", "3", 40, 40)                    
#print validatePath(mitMap, ['3', '4'], 50, 60)                        
  
               


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    path = []
    result = search(digraph, start, end, maxTotalDist, maxDistOutdoors, path[:])
    if result[0] == []:
        raise ValueError("No such path")
    return result[0]
    
    
def search(digraph, start, end, maxTotalDist, maxDistOutdoors, path = [], shortest = [[],(1000000,1000000)]):
    
    if start == None:
        return result

    # add the start node to the path
    path.append(start)

    # filter the path for max distance and for being shorter than shortest.
    # do anything only if it passes the test
    isPathDistOk = filterPath(digraph, path, maxTotalDist, maxDistOutdoors, shortest[1])
    if (isPathDistOk):
        if start == end:
            # returns the path alongside sum of all (totDist, outDist)
            shortest = [path, isPathDistOk]
            return shortest
              
        # fo through each child of the current node
        for child in digraph.childrenOf(Node(start)):
            if child.getName() not in path:    
                # search will return something only if the path is shorter 
                # than the shortest start == end, 
                # or if it traversed everything at the end, which won't reach here
                # newPath is the path and the shortest distance tuple
                newPath = search(digraph, child.getName(), end, maxTotalDist, maxDistOutdoors, path, shortest)
            
                # if doesn't have children search will return None
                if newPath[1][0] < shortest[1][0]:
                    shortest = copy.deepcopy(newPath)
                    
                # once it got out of deeper level of search, it will pop the top of path
                path.pop()
    return shortest


# filters the path so that it fits max distance requirements and checks if it is shortest
def filterPath(digraph, path, maxTotalDist, maxDistOutdoors, shortestDist):
    maxDistLeft = ((-1)*maxTotalDist, (-1)*maxDistOutdoors)
    totalDistSum = (0, 0)
    prev_node = None
    # check each node in the path
    for i, node in enumerate(path):
        if i > 0:
            # check each edge in the node: 
            # digraph.edges = [ nodeA: [[edge1, (totDist1, outDist1)], [edge2, (totDist2, outDist2), ...],
            #                   nodeB: [[edge, (totDist, outDist)], ... ], 
            #                    ...]
            for edge in digraph.edges[Node(prev_node)]:
                if edge[0] == Node(node):
                    # sum the minus totalDist with current dist
                    maxDistLeft = map(sum, zip(edge[1], maxDistLeft))
                    if maxDistLeft[0] > 0 or maxDistLeft[1] > 0:
                        return False
                    # sum the total distance
                    totalDistSum = map(sum, zip(edge[1], totalDistSum))
                    if totalDistSum[0] >= shortestDist[0]:
                        return False
        prev_node = node
    return totalDistSum
#mitMap = load_map("/Users/makarymalinouski/Documents/Programming/MIT-CS.2/ProblemSet5/mit_map.txt")    
#print directedDFS(mitMap, '32', '56', 100, 0)   

# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    #Test cases
    mitMap = load_map("/Users/makarymalinouski/Documents/Programming/MIT-CS.2/ProblemSet5/mit_map.txt")
    #print isinstance(mitMap, Digraph)
    #print isinstance(mitMap, WeightedDigraph)
    #print 'nodes', mitMap.nodes
    #print 'edges', mitMap.edges


    LARGE_DIST = 1000000

    
#    Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#   Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'

    try:
        directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'

    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'

    try:
        directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'

    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr
