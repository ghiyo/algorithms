"""
filename: rbtree.py
"""

from copy import deepcopy
from enum import Enum


class Color(Enum):
    """Color enum"""
    Black = 1
    Red = 2
    DoubleBlack = 3


class RBNode:
    """A Binary Search Tree node"""

    def __init__(self, value):
        self.value = deepcopy(value)
        self.right = None       # right child
        self.left = None        # left child
        self.height = 1         # omit (deletion gives wrong value)
        self.left_size = 0      # omit (deletion gives wrong value)
        self.right_size = 0     # omit (deletion gives wrong value)
        self.count = 1          # omit (deletion gives wrong value)
        self.size = 0           # omit (deletion gives wrong value)
        self.color = Color.Red
        self.parent = None

    def __str__(self):
        return f'value: {self.value} ({self.count}) | height: {self.height} | Color: {self.color.name}'

    def has_red_child(self):
        """Returns a boolean if node has red children"""
        return (self.left and self.left.color is Color.Red) or (self.right and self.right.color is Color.Red)

    def is_on_left(self):
        """returns boolean if node is a left child"""
        return self == self.parent.left

    def sibling(self):
        """returns the sibling of the node"""
        if self.parent is None:
            return None
        if self.parent.left == self:
            return self.parent.right
        return self.parent.left

    def recolor(self):
        """switched the color between black and red"""
        if self.color is Color.Black:
            self.color = Color.Red
        elif self.color is Color.Red:
            self.color = Color.Black

    def update_height(self):
        """updates the height of the node after insertion or deletion"""
        left_height = right_height = 0
        if self.left is not None:
            left_height = self.left.height
        if self.right is not None:
            right_height = self.right.height
        self.height = max(right_height, left_height) + 1

    def update_size(self):
        """updates the number of children a node has"""
        left_size = right_size = 0
        if self.left is not None:
            left_size = self.left.size
        if self.right is not None:
            right_size = self.right.size
        self.left_size = left_size
        self.right_size = right_size

    def move_down(self, new_parent):
        """moves self down and gives the new node its place"""
        if self.parent is not None:
            if self.is_on_left():
                self.parent.left = new_parent
            else:
                self.parent.right = new_parent
        new_parent.parent = self.parent
        self.parent = new_parent


class RBT:
    "Binary Search Tree"

    def __init__(self):
        self.root = None
        self.length = 0

        # Auxiliary attributes for temporarily global use within the class
        self._pred = None
        self._succ = None

        # Helper flags for rotations
        self._ll = False
        self._lr = False
        self._rr = False
        self._rl = False

    def __len__(self):
        return self.length

    def _left_rotate(self, node):
        """Does a left rotation on a node and its parent"""
        x = node.right
        y = x.left
        x.left = node
        node.right = y
        node.parent = x
        if y is not None:
            y.parent = node
        return x

    def _right_rotate(self, node):
        """Does a right rotation on a node and its parent"""
        x = node.left
        y = x.right
        x.right = node
        node.left = y
        node.parent = x
        if y is not None:
            y.parent = node
        return x

    def _balance(self, node):
        if self._ll:
            node = self._left_rotate(node)
            node.recolor()
            node.left.recolor()
            self._ll = False
        elif self._lr:
            node.left = self._left_rotate(node.left)
            node.left.parent = node
            node = self._right_rotate(node)
            node.recolor()
            node.right.recolor()
            self._lr = False
        elif self._rr:
            node = self._right_rotate(node)
            node.recolor()
            node.right.recolor()
            self._rr = False
        elif self._rl:
            node.right = self._right_rotate(node.right)
            node.right.parent = node
            node = self._left_rotate(node)
            node.recolor()
            node.left.recolor()
            self._rl = False

        if node.parent.right == node:
            if node.parent.left is None or node.parent.left.color is Color.Black:
                if node.left is not None and node.left.color is Color.Red:
                    self._rl = True
                elif node.right is not None and node.right.color is Color.Red:
                    self._ll = True
            else:
                node.parent.left.recolor()
                node.recolor()
                if node.parent != self.root:
                    node.parent.recolor()
        else:
            if node.parent.right is None or node.parent.right.color is Color.Black:
                if node.right is not None and node.right.color is Color.Red:
                    self._lr = True
                elif node.left is not None and node.left.color is Color.Red:
                    self._rr = True
            else:
                node.parent.right.recolor()
                node.recolor()
                if node.parent != self.root:
                    node.parent.recolor()
        return False

    def _insert_aux(self, node, key):
        """auxuliary function for insert"""
        rebalance = False
        if node is None:
            node = RBNode(key)
            self.length += 1
            inserted = True
        elif node.value < key:
            node.right, inserted = self._insert_aux(node.right, key)
            node.right.parent = node
            if node.color is Color.Red and node.right.color is Color.Red:
                rebalance = True
        elif node.value > key:
            node.left, inserted = self._insert_aux(node.left, key)
            node.left.parent = node
            if node.color is Color.Red and node.left.color is Color.Red:
                rebalance = True
        else:
            node.count += 1
            inserted = False

        if inserted:
            node.update_height()
            node.update_size()

        if rebalance:
            rebalance = self._balance(node)

        return node, inserted

    def insert(self, key):
        """Inserts a new key into the BST"""
        if self.root is None:
            self.root = RBNode(key)
            self.root.color = Color.Black
            inserted = True
            self.length += 1
            self.root.update_height()
            self.root.update_size()

        else:
            self.root, inserted = self._insert_aux(self.root, key)
        return inserted

    def _successor(self, node):
        """finds a successor of the node's parent"""
        temp = node
        while temp.left:
            temp = temp.left
        return temp

    def _v_replace(self, node):
        """finds the node to replace the deleted node"""
        if node.left is not None and node.right is not None:
            return self._successor(node.right)

        if node.left is None and node.right is None:
            return

        if node.left is not None:
            return node.left
        return node.right

    def _d_right_rotate(self, node):
        """right rotation for delete without returning a node pointer"""
        new_parent = node.left

        if node == self.root:
            self.root = new_parent

        node.move_down(new_parent)

        node.left = new_parent.right

        if new_parent.right is not None:
            new_parent.right.parent = node

        new_parent.right = node

    def _d_left_rotate(self, node):
        """left rotation for delete without returning a node pointer"""
        new_parent = node.right

        if node == self.root:
            self.root = new_parent

        node.move_down(new_parent)

        node.right = new_parent.left

        if new_parent.left is not None:
            new_parent.left.parent = node

        new_parent.left = node

    def _fix_double_black(self, x):
        if x == self.root:
            return
        sibling = x.sibling()
        parent = x.parent
        if sibling is None:  # no sibling, double black pushed up to parent
            self._fix_double_black(parent)
        else:
            if sibling.color is Color.Red:
                parent.color = Color.Red
                sibling.color = Color.Black
                if sibling.is_on_left():
                    self._d_right_rotate(parent)
                else:
                    self._d_left_rotate(parent)
                self._fix_double_black(x)
            else:
                if sibling.has_red_child():
                    if sibling.left and sibling.left.color is Color.Red:
                        if sibling.is_on_left():
                            sibling.left.color = sibling.color
                            sibling.color = parent.color
                            self._d_right_rotate(parent)
                        else:
                            sibling.left.color = parent.color
                            self._d_right_rotate(sibling)
                            self._d_left_rotate(parent)
                    else:
                        if sibling.is_on_left():
                            sibling.right.color = parent.color
                            self._d_left_rotate(sibling)
                            self._right_rotate(parent)
                        else:
                            sibling.right.color = sibling.color
                            sibling.color = parent.color
                            self._d_left_rotate(parent)
                    parent.color = Color.Black
                else:
                    sibling.color = Color.Red
                    if parent.color is Color.Black:
                        self._fix_double_black(parent)
                    else:
                        parent.color = Color.Black
        return

    def _swap_values(self, x, y):
        """swaps the values of two nodes"""
        temp = deepcopy(x.value)
        x.value = deepcopy(y.value)
        y.value = temp

    def _delete_aux(self, v):
        """Auxiliary function for delete"""
        u = self._v_replace(v)
        uvBlack = (u is None or u.color is Color.Black) and (
            v.color is Color.Black)

        if u is None:  # v is leaf
            if v == self.root:
                self.root = None
            else:
                if uvBlack:  # double black situation
                    self._fix_double_black(v)
                else:  # u or v are red
                    if v.sibling() is not None:
                        v.sibling().color = Color.Red
                if v.is_on_left():
                    v.parent.left = None
                else:
                    v.parent.right = None
            del v
            return

        if v.left is None or v.right is None:  # v has one child
            if v == self.root:
                v.value = deepcopy(u.value)
                v.left = None
                v.right = None
                del u
            else:
                if v.is_on_left():
                    v.parent.left = u
                else:
                    v.parent.right = u
                u.parent = v.parent
                del v
                if uvBlack:  # fix double black at u
                    self._fix_double_black(u)
                else:
                    u.color = Color.Black
            return
        self._swap_values(u, v)
        self._delete_aux(u)
        return

    def delete(self, key):
        """Deletes a key from the BST"""
        if self.root is None:
            return
        v = self.search_node(key)
        if v is None:
            return None
        self.length -= 1
        self._delete_aux(v)
        return v

    def _search_node_aux(self, node, key):
        """Auxiliary function for search"""
        if node is None:
            value = None
        elif key == node.value:
            value = node
        elif key < node.value:
            value = self._search_node_aux(node.left, key)
        elif key > node.value:
            value = self._search_node_aux(node.right, key)
        return value

    def search_node(self, key):
        """searches for and returns a copy of a key"""
        return self._search_node_aux(self.root, key)

    def _search_aux(self, node, key):
        """Auxiliary function for search"""
        if node is None:
            value = None
        elif key == node.value:
            value = deepcopy(node.value)
        elif key < node.value:
            value = self._search_aux(node.left, key)
        elif key > node.value:
            value = self._search_aux(node.right, key)
        return value

    def search(self, key):
        """searches for and returns a copy of a key"""
        return self._search_aux(self.root, key)

    def select(self, i):
        """finds the ith order statistics"""

    def _min_aux(self, node):
        """Auxiliary function to find min"""
        if node is None:
            value = None
        elif node.left is None:
            value = deepcopy(node.value)
        else:
            value = self._min_aux(node.left)
        return value

    def min(self):
        """finds and returns a copy of the minimum element"""
        return self._min_aux(self.root)

    def _max_aux(self, node):
        """Auxiliary function to find max"""
        if node is None:
            value = None
        elif node.right is None:
            value = deepcopy(node.value)
        else:
            value = self._max_aux(node.right)
        return value

    def max(self):
        """finds and returns a copy of the maximum element"""
        return self._max_aux(self.root)

    def _pred_succ_aux(self, node, key):
        """Auxiliary method for pred_succ"""
        if node is None:
            return

        if node.value == key:
            if node.left is not None:
                temp = node.left
                while temp.right:
                    temp = temp.right
                self._pred = temp
            if node.right is not None:
                temp = node.right
                while temp.left:
                    temp = temp.left
                self._succ = temp
            return

        if node.value > key:
            self._succ = node
            self._pred_succ_aux(node.left, key)
        else:
            self._pred = node
            self._pred_succ_aux(node.right, key)

    def pred_succ(self, key):
        """finds the predecessor and successor of a given key and returns a copy"""
        self._pred_succ_aux(self.root, key)
        pred = deepcopy(self._pred)
        succ = deepcopy(self._succ)
        self._pred = None
        self._succ = None
        return pred, succ

    def _rank_aux(self, node, key):
        """auxialary function for rank"""
        if node is None:
            rank = 0
        if key == node.value:
            rank = node.left_size
        if key < node.value:
            rank = self._rank_aux(node.left, key)
        elif key > node.value:
            rank = self._rank_aux(node.right, key) + node.left_size + 1
        return rank

    def rank(self, key):
        """finds the rank of a given node"""
        return self._rank_aux(self.root, key)

    def _order_aux(self, node, i):
        if node is None:
            return
        if node.left_size == i - 1:
            return deepcopy(node)
        elif node.left_size >= i:
            return self._order_aux(node.left, i)
        else:
            return self._order_aux(node.right, i - node.left_size - 1)

    def order(self, i):
        """ith order statistic of a i"""
        return self._order_aux(self.root, i)

    def _inorder_aux(self, node):
        """auxuliary function for inorder"""
        if node is not None:
            self._inorder_aux(node.left)
            print(f'{node}')
            print(f'{node.parent}\n---')
            self._inorder_aux(node.right)

    def inorder(self):
        """prints the tree inorder"""
        self._inorder_aux(self.root)

    def _preorder_aux(self, node):
        """auxuliary function for preorder"""
        if node is not None:
            print(f'{node}')
            self._preorder_aux(node.left)
            self._preorder_aux(node.right)

    def preorder(self):
        """prints the tree preorder"""
        self._preorder_aux(self.root)

    def _postorder_aux(self, node):
        """auxuliary function for postorder"""
        if node is not None:
            self._postorder_aux(node.left)
            self._postorder_aux(node.right)
            print(f'{node}', )

    def postorder(self):
        """prints the tree preorder"""
        self._postorder_aux(self.root)


def main():
    """main function"""
    test = [5, 2, 7, 1, 4, 3, 6, 9, 8]
    rbt = RBT()
    for i in test:
        print(f'{rbt.insert(i)}')

    print()
    rbt.inorder()
    print(rbt.length)
    for i in test:
        rbt.inorder()
        print('-'*40)
        rbt.delete(i)
    # for i in test:
    #     pred, succ = rbt.pred_succ(i)
    #     print(f'>> {i} >> {pred} {succ}')
    # for i in range(1, rbt.length+1):
    #     print(f'{i}: order: {rbt.order(i)}')
    # for i in test:
    #     print(f'value: {i} rank: {rbt.rank(i)}')
    # print(rbt.length)
    # print(rbt.search(5))
    # rbt.delete(5)
    # print(rbt.search(5))
    # rbt.preorder()
    # print(rbt.length)
    # print(rbt.min())
    # print(rbt.max())


if __name__ == "__main__":
    main()
