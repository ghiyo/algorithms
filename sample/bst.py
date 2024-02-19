"""
filename: bst.py
"""


from copy import deepcopy


class BSTNode:
    """A Binary Search Tree node"""

    def __init__(self, value):
        self.value = deepcopy(value)
        self.right = None       # right child
        self.left = None        # left child
        self.height = 1         # height of the node (depth)
        self.left_size = 0      # size of the left subtree
        self.right_size = 0     # size o the right subtree
        self.count = 1          # number of copies of the value
        self.size = 0

    def __str__(self):
        return f'value: {self.value} ({self.count}) | height: {self.height}'

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


class BST:
    "Binary Search Tree"

    def __init__(self):
        self.root = None
        self.length = 0

        # Auxiliary attributes for temporarily global use within the class
        self._pred = None
        self._succ = None

    def __len__(self):
        return self.length

    def _insert_aux(self, node, key):
        """auxuliary function for insert"""
        if node is None:
            node = BSTNode(key)
            self.length += 1
            inserted = True
        elif node.value < key:
            node.right, inserted = self._insert_aux(node.right, key)
        elif node.value > key:
            node.left, inserted = self._insert_aux(node.left, key)
        else:
            node.count += 1
            inserted = False

        if inserted:
            node.update_height()
            node.update_size()

        return node, inserted

    def insert(self, key):
        """Inserts a new key into the BST"""
        self.root, inserted = self._insert_aux(self.root, key)
        return inserted

    def _delete_node_aux(self, parent, node):
        """Finds the successor of a node to be deleted and moves the node and keeping the BST intact"""
        if node.right is None:
            if parent.left == node:
                parent.left = node.left
            elif parent.right == node:
                parent.right = node.left
        else:
            node = self._delete_node_aux(node, node.right)
        parent.update_height()
        parent.update_size()
        return node

    def _delete_node(self, node):
        if node.left is None and node.right is None:
            node = None
        elif node.left is None or node.right is None:
            if node.left is None:
                node = node.right
            else:
                node = node.left
        else:
            temp = node
            node = self._delete_node_aux(node, node.left)
            node.left = temp.left
            node.right = temp.right
        return node

    def _delete_aux(self, node, key):
        """Auxiliary function for delete"""
        if node is None:
            value = None
        if key < node.value:
            node.left, value = self._delete_aux(node.left, key)
        elif key > node.value:
            node.right, value = self._delete_aux(node.right, key)
        else:
            value = node.value
            node = self._delete_node(node)
            self.length -= 1

        if node is not None and value is not None:
            node.update_height()
            node.update_size()

        return node, value

    def delete(self, key):
        """Deletes a key from the BST"""
        self.root, value = self._delete_aux(self.root, key)
        return value

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
    # test = [5, 5, 2, 2, 2, 7, 1, 4, 3, 6, 9, 8]
    # bst = BST()
    # for i in test:
    #     print(f'{bst.insert(i)} ', end="")
    # print()
    # bst.inorder()
    # for i in test:
    #     pred, succ = bst.pred_succ(i)
    #     print(f'>> {i} >> {pred} {succ}')
    # for i in range(1, bst.length+1):
    #     print(f'{i}: order: {bst.order(i)}')
    # for i in test:
    #     print(f'value: {i} rank: {bst.rank(i)}')
    # print(bst.length)
    # print(bst.search(5))
    # bst.delete(5)
    # print(bst.search(5))
    # bst.preorder()
    # print(bst.length)
    # print(bst.min())
    # print(bst.max())
    test = [7, 5, 9, 6, 4, 8, 10]
    bst = BST()
    for i in test:
        bst.insert(i)
    bst.inorder()
    bst.preorder()
    bst.postorder()


if __name__ == "__main__":
    main()
