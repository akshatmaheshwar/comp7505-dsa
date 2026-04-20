"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

All of the graph types are implemented here.

Note: You should NOT need to edit the functions provided in this file.
If you want to edit the functionality we have provided you may have
misunderstood what the specification required. Please let us know on Ed if
you think you have a good reason to edit the provided functions.

You may ADD YOUR OWN functions if necessary. The warning above is about
changing the code we already provide.
"""

from __future__ import annotations

import random
import re
from pathlib import Path
from typing import Any
from string import ascii_uppercase


class Node:
    """
    A graph node type. Stores an integer ID which maps the Node to its index
    in the adjacency list. Also can store abitrary data (labels).
    """

    def __init__(self, nid: int, data: Any = None) -> None:
        self._id = nid
        self._data = data

    def get_id(self) -> int:
        return self._id

    def get_data(self) -> Any:
        return self._data


class LatticeNode(Node):
    """
    A special lattice type; has four possible neighbors, as well as x and y
    coordinates.
    """

    def __init__(
        self,
        row: int,
        col: int,
        nid: int,
        data: Any = None,
        north: LatticeNode = None,
        east: LatticeNode = None,
        south: LatticeNode = None,
        west: LatticeNode = None,
    ) -> None:
        super().__init__(nid, data)
        self._row = row
        self._col = col
        self._north = north
        self._east = east
        self._south = south
        self._west = west

    def get_coordinates(self) -> tuple[int, int]:
        """
        Returns the (x, y) coordinates of the node
        """
        return self._row, self._col

    # Following functions return the specific {N,E,S,W} neighbors
    def get_north(self) -> LatticeNode | None:
        return self._north

    def get_east(self) -> LatticeNode | None:
        return self._east

    def get_south(self) -> LatticeNode | None:
        return self._south

    def get_west(self) -> LatticeNode | None:
        return self._west

    def get_adjacent(self) -> list[LatticeNode]:
        """
        Return a list of adjacent nodes to self
        """
        adjacent = []
        if self.get_north() is not None:
            adjacent.append(self.get_north())

        if self.get_east() is not None:
            adjacent.append(self.get_east())

        if self.get_south() is not None:
            adjacent.append(self.get_south())

        if self.get_west() is not None:
            adjacent.append(self.get_west())

        return adjacent

    def id_from_coordinates(self, rows: int) -> int:
        return self._col * rows + self._row

    def disconnect(self) -> None:
        if self._north is not None:
            self._north._south = None
            self._north = None

        if self._south is not None:
            self._south._north = None
            self._south = None

        if self._east is not None:
            self._east._west = None
            self._east = None

        if self._west is not None:
            self._west._east = None
            self._west = None


class Graph:
    def __init__(
        self,
        nodes: list[Node] | None = None,
        edges: list[list[int]] | list[list[tuple[int, int]]] | None = None,
        weighted: bool = True,
    ):
        self._nodes = nodes if nodes is not None else []
        self._edges = edges if edges is not None else []
        self._weighted = weighted
        if not self._weighted:
            for i in range(len(self._edges)):
                self._edges[i] = [((e, 1) if type(e) == int else e) for e in self._edges[i]]
        self.__check_graph()

    def __check_graph(self) -> None:
        for node_neighbours in self._edges:
            for neighbour, _ in node_neighbours:
                if neighbour < 0 or neighbour >= len(self._nodes):
                    raise ValueError(f"No node has ID {neighbour} but adjacency list refers to it.")

    def get_node(self, index: int) -> Node | None:
        try:
            return self._nodes[index]
        except IndexError:
            return None

    def get_neighbours(self, index: int) -> list[Node] | list[tuple[Node, int]]:
        if self._weighted:
            return [(self._nodes[neighbour], weight) for neighbour, weight in self._edges[index]]
        else:
            return [self._nodes[neighbour] for neighbour, _ in self._edges[index]]

    def generate_random_node_id(self) -> int | None:
        """
        Return a random node identifier from the graph or None if empty.
        """
        if len(self._nodes) > 0:
            return random.randint(0, len(self._nodes) - 1)
        return None

    def generate_labels(self) -> None:
        """
        Generates a random label for each vertex in self.
        Labels are ASCII capitals
        """
        for node in self._nodes:
            node._data = random.choice(ascii_uppercase)

    def from_file(self, path: Path) -> None:
        if type(path) == str:
            path = Path(path)
        with path.open("r") as ifile:
            contents = ifile.readlines()
        adjacency = [[] for _ in range(len(contents))]
        weighted = False
        weighted_set = False
        for line in contents:
            chunks = line.strip().split(":")
            if len(chunks) == 1:
                continue
            if len(chunks) > 2:
                raise ValueError(f"Can not interpret line {contents} in file {path}")
            [node, neighbours] = chunks
            node = int(node.strip())
            neighbours = neighbours.strip().split()
            if len(neighbours) == 0:
                continue
            if len(neighbours[0].split(",")) == 2 and not weighted_set:
                weighted = True
                weighted_set = True

            if weighted:
                neighbours = [(int(item.split(",")[0].strip()), int(item.split(",")[1].strip())) for item in neighbours]
            else:
                neighbours = [(int(item.strip()), 1) for item in neighbours]
            adjacency[node] = neighbours
        self._nodes = [Node(i) for i in range(len(contents))]
        self._edges = adjacency
        self._weighted = weighted
        self.__check_graph()

    def to_file(self, path: Path) -> None:
        if type(path) == str:
            path = Path(path)

        lines = [
            f"{ix}: " + " ".join([(f"{e},{w}" if self._weighted else f"{e}") for e, w in adj])
            for ix, adj in enumerate(self._edges)
        ]
        with path.open("w") as ofile:
            ofile.write("\n".join(lines))


class LatticeGraph(Graph):
    def __init__(self, nodes: list[LatticeNode] = None) -> None:
        self._rows = 0
        self._cols = 0
        edges = None

        if nodes is not None:
            nodes.sort(key=lambda x: x.get_id())
            self._rows = max([node.get_coordinates()[0] + 1 for node in nodes])
            self._cols = max([node.get_coordinates()[1] + 1 for node in nodes])
            edges = [[adj.get_id() for adj in node.get_adjacent()] for node in nodes]

        super().__init__(nodes, edges, weighted=False)

    def get_dimensions(self) -> tuple[int, int]:
        return self._rows, self._cols

    # LatticeNode specific version of get_neighbours
    def get_neighbours(self, index: int) -> list[LatticeNode]:
        return self._nodes[index].get_adjacent()

    def from_file(self, path: str) -> None:
        """
        Load the ASCII lattice graph format.
        """
        lines = None
        with open(path) as f:
            lines = f.readlines()
        # Just check that we actually think we have an ASCII LatticeGraph
        wc = 0
        for line in lines:
            wc += line.count("%")
        if wc == 0:
            raise ValueError(f"Can not interpret LatticeGraph in {path} - is your format correct?")
        lines = list(filter(lambda x: not re.match(r"^\s*$", x), lines))
        lines = [list(line.strip("\n")) for line in lines]
        rowcount = len(lines)
        colcount = len(lines[0])
        next_id = 0
        node_dict = dict()

        # First pass: Create all of the nodes and put them in a dictionary
        for row in range(rowcount):
            for col in range(colcount):
                elem = lines[row][col]
                # If it's not a wall, check neighbors
                if elem != "%":
                    line = LatticeNode(row, col, next_id)
                    # Put the node into a dictionary, with the key as its
                    # current x/y coordinate as a string: x_y
                    node_dict[str(row) + "_" + str(col)] = line
                    next_id += 1

        # Second pass: Link the nodes together
        for value in node_dict.values():
            x, y = value.get_coordinates()
            # See, maps are very useful...
            north_key = str(x) + "_" + str(y + 1)
            east_key = str(x + 1) + "_" + str(y)
            south_key = str(x) + "_" + str(y - 1)
            west_key = str(x - 1) + "_" + str(y)
            # Terrible, but it works eh?
            try:
                value._north = node_dict[north_key]
            except KeyError:
                pass
            try:
                value._east = node_dict[east_key]
            except KeyError:
                pass
            try:
                value._south = node_dict[south_key]
            except KeyError:
                pass
            try:
                value._west = node_dict[west_key]
            except KeyError:
                pass

        # Now finish setting up the data
        self._rows = rowcount
        self._cols = colcount
        self._nodes = sorted(list(node_dict.values()), key=lambda x: x.get_id())
        self._edges = [[x for adj in node.get_adjacent()] for node in self._nodes]

    def to_file(self, path: Path) -> None:
        if type(path) == str:
            path = Path(path)
        lattice = [["%" for _ in range(self._cols + 2)] for _ in range(self._rows + 2)]
        for n in self._nodes:
            r, c = n.get_coordinates()
            lattice[r + 1][c + 1] = " "
        for i in range(len(lattice)):
            lattice[i] = "".join(lattice[i])
        with path.open("w") as ofile:
            ofile.write("\n".join(lattice))
