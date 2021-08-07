#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent *** In this problem? The nodes are buildings
# What do the graph's edges represent? *** The edges are paths between buildings
# Where are the distances represented? *** The distances represented as weighted edges between buildings.
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    # print("Loading map from file...")
    with open(map_filename, 'r') as f:
        mit_map = Digraph()
        nodes = set([])
        edges = set([])
        # reading through the lines in the file
        for line in f.readlines():
            # strips each line from a new-line char and splits it to its components - source, dest, tot_dist, out_dist
            edge_info = line.strip('\n').split(' ')
            # creating Nodes of the source and destinations - more lines of code,
            # but when breaking down code is easier to follow each line
            s_node = Node(edge_info[0])
            d_node = Node(edge_info[1])
            if not mit_map.has_node(s_node):
                mit_map.add_node(s_node)
            if not mit_map.has_node(d_node):
                mit_map.add_node(d_node)
            # creating weighted Edge of from the source to the destinations and adds it to the graph
            e = WeightedEdge(s_node, d_node, edge_info[2], edge_info[3])
            mit_map.add_edge(e)
    return mit_map


# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

# g = load_map("test_load_map.txt")
# print(g)

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: The objective function is first and foremost minimizing the total distance walked.
# The constrain is a maximum distance desired to walk outside.
# If 2 total distances are equal the one with least amount of outside walk is better.
# However by assumption, if we can walk 0 distance outside but walk even 1 more step in total this option is inferior.
#

# Problem 3b: Implement get_best_path

# note that the function is 25-30 lines of code. about 10 of them
# are assignment of temp variables to avoid long unreadable lines
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist=None, best_path=None):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    start_node = Node(start)
    end_node = Node(end)
    # if the start and end nodes does not exist in the diagraph raise error
    if not (digraph.has_node(start_node) and digraph.has_node(end_node)):
        raise ValueError("The starting/ending nodes does not exist")

    # if we reached the end return the best path - either the current path, or the best in memory
    elif start == end:
        if path[1] < int(0 if best_dist is None else best_dist) or best_dist is None:
            return path[0], path[1]
        else:
            return best_path, best_dist

    else:
        if not path[0]:
            path[0].append(start)
        # iterating over each edge originated from the start node. edge between 2 nodes is unique
        edges = digraph.get_edges_for_node(start_node)
        for child in edges:
            # saving the outdoor distance traveled and calculating outdoors dist left
            curr_dist_out = int(child.get_outdoor_distance())
            new_max_dist = max_dist_outdoors - curr_dist_out
            # saving the total distance traveled and calculating new total dist traveled
            curr_dist_traveled = int(child.get_total_distance())
            new_tot_dist = path[1] + curr_dist_traveled
            new_start = child.get_destination().get_name()  # setting the new start for next recursive iteration
            # return None if the constrain is violated OR the total dist walked so far
            # is exceeding the best distance on record (assuming None=0 is the default best which isn't valid answer)
            # OR the next node has already been visited in the current path (to prevent cycles)
            if new_max_dist < 0 or (new_tot_dist > int(0 if best_dist is None else best_dist) and
                                    best_dist is not None) or new_start in path[0]:
                continue
            else:
                # initiating variable to make the code more readable -
                # fixing the path parameter - adding next node, total distance traveled and dist traveled outside so far
                path_list = path[0].copy()
                path_list.append(new_start)
                new_path = [path_list, new_tot_dist, path[2]+curr_dist_out]
                # calling the function for another iteration with the new parameters.
                best_path, best_dist = get_best_path(digraph, new_start, end, new_path, new_max_dist, best_dist, best_path)
        return best_path, best_dist


# g = load_map("test_load_map.txt")
# start = 'a'
# end = 'c'
# print(get_best_path(g, start, end, [[], 0, 0], 10))


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    best_path, best_dist = get_best_path(digraph, start, end, [[], 0, 0], max_dist_outdoors, max_total_dist)
    if (best_dist and best_path) is None:
        raise ValueError("No path found")
    return best_path


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()

