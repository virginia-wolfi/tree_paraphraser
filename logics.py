from itertools import permutations

import nltk


class PermutedSyntaxTree:
    """
    A class to generate permutations of a syntax tree based on specific tagged nodes and conjunctions.
    """

    CONJUNCTIONS = (",", "CC")
    TAG = "NP"

    def __init__(self, syntax_tree: str) -> None:
        """
        Initializes the PermutedSyntaxTree with a syntax tree string.
        """

        self.tree = nltk.Tree.fromstring(syntax_tree)
        self.tagged_trees = dict()
        self.tagged_trees_positions = dict()
        self.permutations = dict()
        self.find_permutations_and_positions()
        self.tagged_trees_keys = list(self.tagged_trees)

    def find_permutations_and_positions(self, conj_set=CONJUNCTIONS, tag=TAG) -> None:
        """
        Finds and stores the permutations and positions of tagged subtrees that can be permuted.
        """

        tree = nltk.ParentedTree.convert(self.tree)
        subtrees = tree.subtrees()

        for node in subtrees:
            if node.label() == tag:
                # Skip already included trees
                if not node.parent() or node in node.parent()[-2:]:
                    continue
                # The right sibling must be a conjunction
                conj = node.right_sibling()
                if conj and conj.label() in conj_set:
                    next_sibling = conj.right_sibling()
                    # Handle constructions like ', or/and'
                    if next_sibling and next_sibling.label() in conj_set:
                        next_sibling = next_sibling.right_sibling()
                    if next_sibling and next_sibling.label() == tag:
                        pos = node.treeposition()[:-1]
                        tagged_trees = self.tagged_trees.setdefault(pos, [])
                        tagged_tree_positions = self.tagged_trees_positions.setdefault(pos, [])
                        if node not in tagged_trees:
                            tagged_trees.extend([node, next_sibling])
                            tagged_tree_positions.extend([
                                node.treeposition(),
                                next_sibling.treeposition(),
                            ])
                        else:
                            tagged_trees.append(next_sibling)
                            tagged_tree_positions.append(next_sibling.treeposition())

        for tree_position, trees in self.tagged_trees.items():
            self.permutations[tree_position] = list(permutations(trees))

    def generate_permuted_trees(self, initial_tree: nltk.Tree, depth=0) -> list[nltk.Tree]:
        """
        Generates all permutations of the tagged subtrees at a specific depth.
        """

        new_trees = list()
        current_node_key = self.tagged_trees_keys[depth]
        insertion_positions = self.tagged_trees_positions[current_node_key]
        for permutation in self.permutations[current_node_key]:
            changing_tree = nltk.tree.Tree.convert(initial_tree)
            for i, pos in enumerate(insertion_positions):
                changing_tree[pos] = permutation[i]
            new_trees.append(changing_tree)
        return new_trees

    def get_all_tree_permutations(self) -> list[nltk.Tree]:
        """
        Recursively generates all possible permutations of the syntax tree.
        """

        all_permuted_trees = []

        def traverse_and_generate_permutations(tree: nltk.Tree, depth=0):
            if len(self.permutations) == depth:
                all_permuted_trees.append(tree)
            else:
                permuted_trees = self.generate_permuted_trees(tree, depth)
                for permuted_tree in permuted_trees:
                    traverse_and_generate_permutations(permuted_tree, depth + 1)

        traverse_and_generate_permutations(self.tree)
        return all_permuted_trees
