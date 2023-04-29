import nltk
from itertools import permutations


def tree_parser(tree, conj_set=[",", "CC"], tag="NP"):
    """Calculates treepositions containing desired nested tag
    and permutations of these trees grouped by nesting depth

    Args:
        tree (str) -- the bracketed tree string
        conj_set (list) -- list of conjunction tags (default [",", "CC"])
        tag (str) -- desired tag

    Returns:
        tree_pos, permuted (dict, dict)
    """
    to_permute = {}
    tree_pos = {}
    permuted = {}
    subtrees = tree.subtrees()

    for tr in subtrees:
        if tr.label() == tag and tr.parent().label() == tag:
            if tr in [tr.parent()[-1], tr.parent()[-2]]:
                continue
            conj = tr.right_sibling()
            desired_tag = conj.right_sibling()
            if conj.label() and desired_tag.label() in conj_set:
                desired_tag = desired_tag.right_sibling()
            if conj.label() in conj_set and desired_tag.label() == tag:
                to_permute[tr.treeposition()[:-1]] = to_permute.get(
                    tr.treeposition()[:-1], []
                )
                tree_pos[tr.treeposition()[:-1]] = tree_pos.get(
                    tr.treeposition()[:-1], []
                )
                if tr not in to_permute[tr.treeposition()[:-1]]:
                    to_permute[tr.treeposition()[:-1]] += (tr, desired_tag)
                    tree_pos[tr.treeposition()[:-1]] += [
                        tr.treeposition(),
                        desired_tag.treeposition(),
                    ]
                else:
                    to_permute[tr.treeposition()[:-1]].append(desired_tag)
                    tree_pos[tr.treeposition()[:-1]].append(desired_tag.treeposition())

    for n in to_permute:
        permuted[n] = list(permutations(to_permute[n]))
    return tree_pos, permuted


def replace(tree_pos, permuted, tree, depth=0):
    """
    Creates a list of trees with all possible permutations at the given depth
    Args:
        tree_pos (dict) -- treeposition of trees with desired tags
        permuted (dict) -- combinations of these trees permutations
        tree (nltk.ParentedTree) -- tree to handle
        depth (int) -- nesting depth
    Returns
        new_trees (list) -- trees after permutation
    """
    keys = list(permuted.keys())
    new_trees = []
    for p in permuted[keys[depth]]:
        tree2 = nltk.Tree.convert(tree)
        for i in range(len(tree_pos[keys[depth]])):
            tree2[tree_pos[keys[depth]][i]] = nltk.Tree.convert(p[i])
        new_trees.append(tree2)
    return new_trees


def pull_list(tree):
    """
    Calls recursive function that returns list of trees with all possible permutations of nested tag

    Args:
        tree (nltk.Tree) -- tree to handle
    Returns:

    """
    tree_list = []

    def func(tree, tree_list, depth=0):
        tree = nltk.ParentedTree.convert(tree)
        tree_pos, permuted = tree_parser(tree)
        if len(permuted) == depth:
            tree_list += [tree]
            return
        else:
            new_trees = replace(tree_pos, permuted, tree, depth)
            for tr in new_trees:
                func(tr, tree_list, depth + 1)

    func(tree, tree_list)
    return tree_list
