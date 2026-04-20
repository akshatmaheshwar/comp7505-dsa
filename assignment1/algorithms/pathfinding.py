"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable


def bfs_traversal(
        graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.1: Breadth First Search

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()

    # ALGO GOES HERE
    if origin == goal:
        visited_order.append(origin)
        path.append(origin)
        return (path, visited_order)

    temp_path = []

    queue = PriorityQueue()
    queue.insert_fifo(origin)
    predecessors = Map()
    predecessors.insert_kv(origin, -1)
    visited_order.append(origin)

    while not queue.is_empty():
        current_node = queue.remove_min()

        for neighbor in graph.get_neighbours(current_node):
            if predecessors.find(neighbor.get_id()) is None:
                visited_order.append(neighbor.get_id())
                predecessors[neighbor.get_id()] = current_node
                queue.insert_fifo(neighbor.get_id())

                if neighbor.get_id() == goal:
                    path_node = goal
                    while path_node is not -1:
                        temp_path.insert(0, path_node)
                        path_node = predecessors[path_node]

                    path.build_from_list(temp_path)
                    return (path, visited_order)

    # Return the path and the visited nodes list
    return (path, visited_order)


def dijkstra_traversal(graph: Graph, origin: int) -> DynamicArray:
    """
    Task 2.2: Dijkstra Traversal

    @param: graph
      The *weighted* graph to process (POSW graphs)
    @param: origin
      The ID of the node from which to start traversal.

    @returns: DynamicArray containing Entry types.
      The Entry key is a node identifier, Entry value is the cost of the
      shortest path to this node from the origin.

    NOTE: Dijkstra does not work (by default) on LatticeGraph types.
    This is because there is no inherent weight on an edge of these
    graphs. It should of course work where edge weights are uniform.
    """
    valid_locations = DynamicArray()  # This holds your answers
    visited = Map()
    visited.insert_kv(origin,1)
    pq = PriorityQueue()
    # ALGO GOES HERE
    valid_locations.append(Entry(origin,0))
    for i in graph.get_neighbours(origin):
        pq.insert(i[1], i[0].get_id())
    while not pq.is_empty():
        while visited.find(pq.get_min_value()) is not None:
            pq.remove_min()
            if pq.is_empty():
                return valid_locations
        valid_locations.append(Entry(pq.get_min_value(), pq.get_min_priority()))
        visited.insert_kv(pq.get_min_value(),1)
        cur_dist_from_org = pq.get_min_priority()
        for i in graph.get_neighbours(pq.remove_min()):
            if visited.find(i[0].get_id()) is None:
                pq.insert(cur_dist_from_org + i[1], i[0].get_id())

    # Return the DynamicArray containing Entry types
    return valid_locations


def dfs_traversal(
        graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.3: Depth First Search **** COMP7505 ONLY ****
    COMP3506 students can do this for funsies.

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()

    # ALGO GOES HERE
    if origin == goal:
        visited_order.append(origin)
        path.append(origin)
        return (path, visited_order)

    temp_path = []

    stack = DynamicArray()
    stack.append(origin)
    predecessors = Map()
    predecessors.insert_kv(origin, -1)
    visited_order.append(origin)

    while not stack.is_empty():
        current_node = stack.remove_at(stack.get_size()-1)

        for neighbor in reversed(graph.get_neighbours(current_node)):
            if predecessors.find(neighbor.get_id()) is None:
                visited_order.append(neighbor.get_id())
                predecessors[neighbor.get_id()] = current_node
                stack.append(neighbor.get_id())

                if neighbor.get_id() == goal:
                    path_node = goal
                    while path_node is not -1:
                        temp_path.insert(0, path_node)
                        path_node = predecessors[path_node]

                    path.build_from_list(temp_path)
                    return (path, visited_order)

    # Return the path and the visited nodes list
    return (path, visited_order)
