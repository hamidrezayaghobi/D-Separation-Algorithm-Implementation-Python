import copy
import itertools
from collections import defaultdict


class Graph:

    def __init__(self, node_number):
        self.node_number = node_number
        self.graph = defaultdict(list)
        for i in range(1, node_number + 1):
            Node(i)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def topological_sort_util(self, node, visited, stack):
        visited[node] = True
        for node_number in self.graph[node + 1]:
            if visited[node_number - 1] == False:
                self.topological_sort_util(node_number - 1, visited, stack)
        stack.insert(0, node + 1)

    def topo_sort(self):
        visited = [False] * self.node_number
        stack = []

        for node in range(self.node_number):
            if visited[node] == False:
                self.topological_sort_util(node, visited, stack)
        return stack


    def printAllPathsUtil(self, u, d, visited, path, all_path):
        visited[u - 1] = True
        path.append(u)
        if u == d:
            all_path.append(copy.copy(path))
        else:

            for i in self.graph[u]:
                if visited[i - 1] == False:
                    self.printAllPathsUtil(i, d, visited, path, all_path)
        path.pop()
        visited[u - 1] = False

    def printAllPaths(self, s, d):
        global all_path
        visited = [False] * (self.node_number)
        path = []
        self.printAllPathsUtil(s, d, visited, path, all_path)


class Node:

    nodes_dict = {}

    def __init__(self, id):
        self.cpt = None
        self.id = id
        self.children = {}
        self.parents = {}
        Node.nodes_dict[id] = self

    def add_detail(self, cpt, parents_number):
        table = list(itertools.product(('True', 'False'), repeat=len(parents_number) + 1))
        converted_cpt = dict()
        for cpt_number in range(len(cpt)):
            converted_cpt[table[cpt_number * 2 + 1]] = 1 - cpt[cpt_number]
            converted_cpt[table[cpt_number * 2]] = cpt[cpt_number]
        self.cpt = Pandas(converted_cpt, parents_number + [self.id])
        for parent_number in parents_number:
            parent_node = Node.nodes_dict.get(parent_number)
            parent_node.children[self.id] = self
            self.parents[parent_number] = parent_node


def is_invalid_path(from_node, to_node, given):
    visited_nodes = copy.copy(given)
    observed_node = set()

    while visited_nodes:
        next_node = Node.nodes_dict[visited_nodes.pop()]
        for parent in next_node.parents:
            observed_node.add(parent)

    node_and_movement = [(from_node, "child to parent")]
    visited = []

    while node_and_movement:
        node_and_movement_poped = node_and_movement.pop()
        node = Node.nodes_dict[node_and_movement_poped[0]]

        node_name = node_and_movement_poped[0]
        direction = node_and_movement_poped[1]
        if node_and_movement_poped not in visited:
            visited.append((node_name, direction))

            if node_name not in given and node_name == to_node:
                return False

            if direction == "child to parent":
                if node_name not in given:
                    for parent in node.parents:
                        next_node_and_movement = (parent, "child to parent")
                        node_and_movement.append(next_node_and_movement)
                    for child in node.children:
                        next_node_and_movement = (child, "parent to chile")
                        node_and_movement.append(next_node_and_movement)
            else:
                if direction == "parent to chile":
                    if node_name not in given:
                        for child in node.children:
                            node_and_movement.append((child, "parent to chile"))
                    else:
                        if node_name in given:
                            for parent in node.parents:
                                node_and_movement.append((parent, "child to parent"))
                            continue
                    if node_name in observed_node:
                        for parent in node.parents:
                            node_and_movement.append((parent, "child to parent"))

    return True


def reduce_variable(cpt, number):
    if number in cpt.numbers:
        new_cpt = {}
        index = cpt.numbers.index(number)

        for key in cpt.probability_table.keys():
            first_part = key[:index]
            second_paer = key[index + 1:]
            redeced_key = first_part + second_paer
            if redeced_key in new_cpt:
                new_cpt[redeced_key] += cpt.probability_table[key]
            else:
                new_cpt[redeced_key] = 0 + cpt.probability_table[key]
        reduced_variable = copy.copy(cpt.numbers)
        reduced_variable.remove(number)
        return Pandas(new_cpt, reduced_variable)
    return cpt


def normalize_ctp(cpt):
    sum_ctp = 0
    for key in cpt.probability_table.keys():
        sum_ctp += cpt.probability_table[key]
    if not sum_ctp == 0:
        normalized_ctp = dict()
        for key in cpt.probability_table.keys():
            normalized_ctp[key] = cpt.probability_table[key] / sum_ctp
        return normalized_ctp
    return cpt.probability_table


def variable_elimination(variable, evidence, graph):
    sorted_node = []
    for node in graph.topo_sort():
        if node not in evidence and node not in variable:
            sorted_node.append(node)

    factors = [node.cpt for node in Node.nodes_dict.values()]

    for node_number in sorted_node:
        needed_cpt = []
        for collumn in factors:
            if node_number in collumn.numbers:
                needed_cpt.append(collumn)

        if len(needed_cpt) == 0:
            continue

        if len(needed_cpt) == 1:
            factors.append(reduce_variable(needed_cpt[0], node_number))
        else:
            factors.append(reduce_variable(Pandas.join(needed_cpt, node_number), node_number))

        for factor in needed_cpt:
            factors.remove(factor)
    final_table = normalize_ctp(Pandas.dot(factors, evidence, variable))
    return final_table


class Pandas:

    def __init__(self, probability_table, parent_number):
        self.probability_table = probability_table
        self.numbers = parent_number

    @staticmethod
    def join(cpts, node_number):
        first_cpt = cpts[0]
        for cpt_number in range(1, len(cpts)):
            table = dict()
            other_cpt = cpts[cpt_number]
            concatened_cpt = first_cpt.numbers + other_cpt.numbers
            concatened_cpt = set(concatened_cpt)
            concatened_cpt = list(concatened_cpt)
            for key in list(itertools.product(('True', 'False'), repeat=len(concatened_cpt))):
                first_key = []
                for i in first_cpt.numbers:
                    first_key.append(key[concatened_cpt.index(i)])
                first_key = tuple(first_key)
                second_key = []
                for i in other_cpt.numbers:
                    second_key.append(key[concatened_cpt.index(i)])
                second_key = tuple(second_key)
                if first_key in first_cpt.probability_table:
                    if second_key in other_cpt.probability_table:
                        if first_key[first_cpt.numbers.index(node_number)] == second_key[
                            other_cpt.numbers.index(node_number)]:
                            if key in table:
                                table[key] += first_cpt.probability_table[first_key] * other_cpt.probability_table[
                                    second_key]
                            else:
                                table[key] = 0 + first_cpt.probability_table[first_key] * other_cpt.probability_table[
                                    second_key]
            first_cpt = Pandas(table, concatened_cpt)
        return first_cpt

    @staticmethod
    def dot(cpts, evidence, variable):

        new_numbers = [id for cpt in cpts for id in cpt.numbers]
        return_value = Pandas({}, list(set(new_numbers)))

        for i in [True, False]:
            new_evidence = copy.copy(evidence)
            for id, val in variable.items():
                new_evidence[id] = i

            value = 1
            for cpt in cpts:
                key = []
                for x in cpt.numbers:
                    key.append(str(new_evidence[x]))
                value *= cpt.probability_table[tuple(key)]
            return_value.probability_table[tuple([new_evidence[i] for i in new_numbers])] = value
        return return_value


node_number = int(input())
undirected_graph = Graph(node_number)
for i in range(1, node_number + 1):
    parents = [int(x) for x in input().split()]
    cpt = [float(x) for x in input().split()]
    for p in parents:
        undirected_graph.addEdge(p, i)
    Node.nodes_dict[i].add_detail(cpt, parents)

evidence_list = input().split(",")
evidence = {}
for node_evidence in evidence_list:
    evidence[int(node_evidence[0])] = bool(int(node_evidence[-1]))

a, b = input().split()
a = int(a)
b = int(b)

if is_invalid_path(a, b, list(evidence.keys())):
    print("independent")
else:
    print("dependent")

for node_number in Node.nodes_dict.keys():
    node = Node.nodes_dict[node_number]
    for evidence_number in evidence.keys():
        value = evidence[evidence_number]
        if evidence_number in node.cpt.numbers:
            for node_number_1, probebility in node.cpt.probability_table.items():
                if node_number_1[node.cpt.numbers.index(evidence_number)] == str(value):
                    node.cpt.prob_tabl = {node_number_1: probebility}

print(round(list(variable_elimination({a: True}, evidence, undirected_graph).values())[0], 2))
print(round(list(variable_elimination({b: True}, evidence, undirected_graph).values())[0], 2))
