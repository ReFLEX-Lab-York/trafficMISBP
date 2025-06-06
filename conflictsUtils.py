import networkx as nx
import networkx as nx
import numpy as np

def createMatrix(routes, laneNum):
  """Creates a matrix the same size as the numebr of lanes at the junction.
     The routes are then used to fill the matrix with ones where the conflicts
     are.
     Args:
         routes (list): List of routes. Each route is a tuple of two lanes.
         laneNum (int): Number of lanes in the intersection.
     Returns:
         (list): Square matrix of size laneNum x laneNum with conflicts marked as 1.
  """
  matrix = [[0] * laneNum for _ in range(laneNum)]
  
  for r in routes:
    ent= r[0]
    ext = r[1]

    if 0 <= ent < len(matrix) and 0 <= ext < len(matrix[0]):
      matrix[ent][ext] = 1
    else:
      print(f"Invalid indices: ent={ent}, ext={ext}, laneNum={laneNum}")
  return matrix 

def entranceLanes(route, lanes):
    """"Gets the potential conflict entrance lanes for that lanes routes in closewise order.

        Args:
            route (tuple): Tuple of a route.
            lanes (int): Number of lanes in the intersection.
        Returns:
            (list): List of entrance lanes for the route.
        """
    ent, ext = route
    entrances = [ent]
    currentLane = ent
    while currentLane != ext:
        currentLane = (currentLane + 1) % lanes
        entrances.append(currentLane)
    return entrances

def exitLanes(route, lanes):
    """Gets the potential conflict exit lanes for that lanes routes in clockwise order.
        Args: 
            route (tuple): Tuple of a route.
            lanes (int): Number of lanes in the intersection.
        Returns:
            (list): List of exit lanes for the route.
        """
    ent, ext = route
    exits = [ext]
    currentLane = ext
    while currentLane != ent:
        currentLane = (currentLane + 1) % lanes
        exits.append(currentLane)
    return exits

def FindMatrixConflicts(matrix, entrances, exits, routes):
  """Find route conflicts in the matrix based on the entrance and exit lanes combinations.
     Args:
        matrix (list): Square matrix of size laneNum x laneNum with conflicts marked as 1.
        entrances (list): List of conflict entrance lanes for the route.
        exits (list): List of conflcit exit lanes for the route.
      Returns:
        (list): List of tuples representing the conflicts routes of a particulare entrance lane.  
      """
  conflicts = []
  for e in entrances:
    for ex in exits:

      if matrix[e][ex] == 1:
        conflicts.append((e,ex))

  return conflicts

def getMatrixConflictList(matrix, routes, laneNum):
  """Get the list of conflicts for each route in the matrix.
     Args:
         matrix (list): Square matrix of size laneNum x laneNum with conflicts marked as 1.
         routes (list): List of routes. Each route is a tuple of two lanes.
         laneNum (int): Number of lanes in the intersection.
     Returns:
         (list): Conflict lanes for each lane in the routes.  
  """
  conflictList = []
  for i in range(len(routes)):
      forwardEntrance = entranceLanes(routes[i], laneNum)
      forwardExit = exitLanes(routes[i], laneNum)
      backwardEntrance = entranceLanes(routes[i][::-1], laneNum)
      backwardExit = exitLanes(routes[i][::-1], laneNum)
      matrix1 = FindMatrixConflicts(matrix, forwardEntrance, forwardExit, routes)
      matrix2 = FindMatrixConflicts(matrix, backwardEntrance, backwardExit, routes)
      matrix1.extend(matrix2)
      matrix1 = list(set(matrix1))
      conflictList.append((routes[i], matrix1))
  return conflictList

def getGraphNodes(conflictList):
  dictLane = {}
  for startLane, conflictLanes in conflictList:
    laneList = []
    for conflicts in conflictLanes:
      if conflicts[0] != startLane[0]:
        laneList.append(conflicts[0])
    dictLane[startLane[0]] = laneList
  return dictLane


def getConflicts(routes, laneNum):
  squarematrix = createMatrix(routes, laneNum)
  conflicts = getMatrixConflictList(squarematrix, routes, laneNum)
  graph = getGraphNodes(conflicts)
  return  graph

def getMIS(graph):
  return nx.approximation.maximum_independent_set(graph)


def getMISList(graphData):
  graph = nx.Graph()

  for start in graphData:
      graph.add_node(start)
      for end in graphData[start]:
          graph.add_edge(start, end)
  
  misList = []
  for node in graph.nodes():
     
    subgraphNodes = set(graph.nodes()) - set(graph.neighbors(node)) - {node}
    subgraph = graph.subgraph(subgraphNodes)
    if  len(list(getMIS(subgraph))) == 0:
      misList.append([node, [node]])
    else:
      misList.append([node, list(getMIS(subgraph))])
 
  return misList
