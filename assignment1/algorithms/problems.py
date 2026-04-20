"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

 Each problem will be assessed on three sets of tests:

1. "It works":
       Basic inputs and outputs, including the ones peovided as examples, with generous time and memory restrictions.
       Large inputs will not be tested here.
       The most straightforward approach will likely fit into these restrictions.

2. "Exhaustive":
       Extensive testing on a wide range of inputs and outputs with tight time and memory restrictions.
       These tests won't accept brute force solutions, you'll have to apply some algorithms and optimisations.

 3. "Welcome to COMP3506":
       Extensive testing with the tightest possible time and memory restrictions
       leaving no room for redundant operations.
       Every possible corner case will be assessed here as well.

There will be hidden tests in each category that will be published only after the assignment deadline.

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
import math
from collections import deque, defaultdict

from structures.entry import Entry, Compound, Offer
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
from structures.bit_vector import BitVector
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable
import heapq


def maybe_maybe_maybe(database: list[str], query: list[str]) -> list[str]:
    """
    Task 3.1: Maybe Maybe Maybe

    @database@ is an array of k-mers in our database.
    @query@ is an array of k-mers we want to search for.

    Return a list of query k-mers that are *likely* to appear in the database.

    Limitations:
        "It works":
            @database@ contains up to 1000 elements;
            @query@ contains up to 1000 elements.

        "Exhaustive":
            @database@ contains up to 100'000 elements;
            @query@ contains up to 100'000 elements.

        "Welcome to COMP3506":
            @database@ contains up to 1'000'000 elements;
            @query@ contains up to 500'000 elements.

    Each test will run over three false positive rates. These rates are:
        fp_rate = 10%
        fp_rate = 5%
        fp_rate = 1%.

    You must pass each test in the given time limit and be under the given
    fp_rate to get the associated mark for that test.
    """
    answer = []

    bloomfilter = BloomFilter(len(database))
    for i in database:
        bloomfilter.insert(i)

    for i in query:
        if bloomfilter.contains(i):
            answer.append(i)

    return answer


class HuffmanNode:
    def __init__(self, symbol=None, frequency=0, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency


def get_symbol_frequencies(graph: Graph, origin: int) -> list[Entry]:
    queue = PriorityQueue()
    queue.insert_fifo(origin)
    visited = Map()
    visited.insert_kv(origin, 1)
    characters_present = [graph.get_node(origin).get_data()]
    characters_frequency = Map()
    characters_frequency[graph.get_node(origin).get_data()] = 1
    kp = []

    while not queue.is_empty():
        current_node = queue.remove_min()

        for neighbor in graph.get_neighbours(current_node):
            if visited.find(neighbor.get_id()) is None:
                visited[neighbor.get_id()] = 1
                if characters_frequency[neighbor.get_data()] is None:
                    characters_frequency[neighbor.get_data()] = 0
                    characters_present.append(neighbor.get_data())
                characters_frequency[neighbor.get_data()] += 1
                queue.insert_fifo(neighbor.get_id())
    for i in characters_present:
        kp.append(Entry(i, characters_frequency[i]))
    return kp


def build_huffman_tree(frequencies: list[Entry]):
    """
    Build the Huffman tree from the frequency dictionary.

    @param: frequencies
      A dictionary with symbols and their frequencies.

    @returns: HuffmanNode
      The root node of the Huffman tree.
    """
    heap = []

    for i in frequencies:
        heapq.heappush(heap, HuffmanNode(i.get_key(), i.get_value()))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = HuffmanNode(None, left.frequency + right.frequency, left, right)
        heapq.heappush(heap, merged)

    return heapq.heappop(heap)


def generate_huffman_codes(root):
    """
    Generate Huffman codes for all symbols by traversing the Huffman tree.

    @param: root
      The root node of the Huffman tree.

    @returns: dict
      A dictionary with symbols as keys and their corresponding Huffman codes as values.
    """
    codes = Map()

    def traverse(node, code):
        if node.symbol is not None:
            codes[node.symbol] = code
            return
        if node.left:
            traverse(node.left, code + '0')
        if node.right:
            traverse(node.right, code + '1')

    traverse(root, "")
    return codes


def dora(graph: Graph, start: int, symbol_sequence: str,
         ) -> tuple[BitVector, list[Entry]]:
    """
    Task 3.2: Dora and the Chin Bicken

    @graph@ is the input graph G; G might be disconnected; each node contains
    a single symbol in the node's data field.
    @start@ is the integer identifier of the start vertex.
    @symbol_sequence@ is the input sequence of symbols, L, with length n.
    All symbols are guaranteed to be found in G. 

    Return a BitVector encoding symbol_sequence via a minimum redundancy code.
    The BitVector should be read from index 0 upwards (so, the first symbol is
    encoded from index 0). You also need to return your codebook as a
    Python list of unique Entries. The Entry key should correspond to the
    symbol, and the value should be a string. More information below.

    Limitations:
        "It works":
            @graph@ has up to 1000 vertices and up to 1000 edges.
            the alphabet consists of up to 26 characters.
            @symbol_sequence@ has up to 1000 characters.

        "Exhaustive":
            @graph@ has up to 100'000 vertices and up to 100'000 edges.
            the alphabet consists of up to 1000 characters.
            @symbol_sequence@ has up to 100'000 characters.

        "Welcome to COMP3506":
            @graph@ has up to 1'000'000 vertices and up to 1'000'000 edges.
            the alphabet consists of up to 300'000 characters.
            @symbol_sequence@ has up to 1'000'000 characters.

    """
    coded_sequence = BitVector()

    """
    list of Entry objects, each entry has key=symbol, value=str. The str
    value is just an ASCII representation of the bits used to encode the
    given key. For example: x = Entry("c", "1101")
    """

    # DO THE THING
    frequencies = get_symbol_frequencies(graph, start)
    huffman_tree_root = build_huffman_tree(frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree_root)
    codebook = []
    for i in frequencies:
        codebook.append(Entry(i.get_key(), huffman_codes[i.get_key()]))
    for i in symbol_sequence:
        for bit in (huffman_codes[i]):
            coded_sequence.append(int(bit))

    return (coded_sequence, codebook)


def dfs(graph, node, visited):

    if len(graph[node]) == 0:
        return 1

    if node in visited:
        return 0

    visited.add(node)
    reachable_count = 1

    for neighbor in graph[node]:
        reachable_count += dfs(graph, neighbor, visited)

    visited.remove(node)

    return reachable_count


def check(coord1, coord2, r):
    return (((coord2[0] - coord1[0]) ** 2) + ((coord2[1] - coord1[1]) ** 2)) <= r ** 2


def chain_reaction(compounds: list[Compound]) -> int:
    """
    Task 3.3: Chain Reaction

    @compounds@ is a list of Compound types, see structures/entry.py for the
    definition of a Compound. In short, a Compound has an integer x and y
    coordinate, a floating point radius, and a unique integer representing
    the compound identifier.

    Return the compound identifier of the compound that will yield the
    maximal number of compounds in the chain reaction if set off. If there
    are ties, return the one with the smallest identifier.

    Limitations:
        "It works":
            @compounds@ has up to 100 elements

        "Exhaustive":
            @compounds@ has up to 1000 elements

        "Welcome to COMP3506":
            @compounds@ has up to 10'000 elements

    """
    maximal_node = -1
    maximum_reachable = 0
    graph = {}
    for i in range(len(compounds)):
        for j in range(i + 1, len(compounds)):
            if compounds[i].get_compound_id() not in graph:
                graph[compounds[i].get_compound_id()] = []
            if compounds[j].get_compound_id() not in graph:
                graph[compounds[j].get_compound_id()] = []
            if check(compounds[i].get_coordinates(), compounds[j].get_coordinates(), compounds[i].get_radius()):
                graph[compounds[i].get_compound_id()].append(compounds[j].get_compound_id())
            if check(compounds[i].get_coordinates(), compounds[j].get_coordinates(), compounds[j].get_radius()):
                graph[compounds[j].get_compound_id()].append(compounds[i].get_compound_id())
    for node in graph:
        temp = dfs(graph, node, set())
        if maximum_reachable < temp:
            maximum_reachable = temp
            maximal_node = node
        elif maximum_reachable == temp:
            maximal_node = min(maximal_node, node)

    # DO THE THING

    return maximal_node


def labyrinth(offers: list[Offer]) -> tuple[int, int]:
    """
    Task 3.4: Labyrinth

    @offers@ is a list of Offer types, see structures/entry.py for the
    definition of an Offer. In short, an Offer stores n (number of nodes),
    m (number of edges), and k (diameter) of the given Labyrinth. Each
    Offer also has an associated cost, and a unique offer identifier.
    
    Return the offer identifier and the associated cost for the cheapest
    labyrinth that can be constructed from the list of offers. If there
    are ties, return the one with the smallest identifier. 
    You are guaranteed that all offer ids are distinct.

    Limitations:
        "It works":
            @offers@ contains up to 1000 items.
            0 <= n <= 1000
            0 <= m <= 1000
            0 <= k <= 1000

        "Exhaustive":
            @offers@ contains up to 100'000 items.
            0 <= n <= 10^6
            0 <= m <= 10^6
            0 <= k <= 10^6

        "Welcome to COMP3506":
            @offers@ contains up to 5'000'000 items.
            0 <= n <= 10^42
            0 <= m <= 10^42
            0 <= k <= 10^42

    """
    best_offer_id = -1
    best_offer_cost = float('inf')

    for offer in offers:
        n = offer.get_num_nodes()
        m = offer.get_num_edges()
        k = offer.get_diameter()
        cost = offer.get_cost()

        if n <= 0:
            continue

        if m < n - 1 or m > (n * (n - 1)) // 2:
            continue

        if cost < best_offer_cost or (
                cost == best_offer_cost and offer.get_offer_id() < best_offer_id):
            best_offer_cost = cost
            best_offer_id = offer.get_offer_id()

    return (best_offer_id, best_offer_cost)
