class BTreeNode:
    def __init__(self, is_leaf=True):
        self.is_leaf = is_leaf  # To check if the node is a leaf
        self.keys = []  # List of keys in the node
        self.children = []  # List of child nodes (used if node is not a leaf)

class BTree:
    def __init__(self, t=3):
        self.root = BTreeNode(is_leaf=True)
        self.t = t  # Minimum degree (defines the range of children for each node)

    def search(self, file_name):
        """Search for a file by name in the B-tree."""
        return self._search(self.root, file_name)

    def _search(self, node, file_name):
        # Find the first key greater than or equal to file_name
        i = 0
        while i < len(node.keys) and file_name > node.keys[i][0]:
            i += 1

        # If the file is found
        if i < len(node.keys) and node.keys[i][0] == file_name:
            return node.keys[i][1]  # Return the location of the file

        # If the node is a leaf, then the file does not exist in the tree
        if node.is_leaf:
            return None

        # Move to the appropriate child
        return self._search(node.children[i], file_name)

    def insert(self, file_name, location):
        """Insert a file name and location into the B-tree."""
        root = self.root
        # If the root is full, grow the tree in height
        if len(root.keys) == 2 * self.t - 1:
            new_node = BTreeNode(is_leaf=False)
            new_node.children.append(self.root)
            self.root = new_node
            self._split_child(new_node, 0)
            self._insert_non_full(new_node, file_name, location)
        else:
            self._insert_non_full(root, file_name, location)

    def _insert_non_full(self, node, file_name, location):
        # If node is a leaf, insert the file directly
        if node.is_leaf:
            node.keys.append((file_name, location))
            node.keys.sort(key=lambda x: x[0])  # Keep keys ordered
        else:
            # Find the child where the key should be inserted
            i = len(node.keys) - 1
            while i >= 0 and file_name < node.keys[i][0]:
                i -= 1
            i += 1

            # If the child is full, split it
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if file_name > node.keys[i][0]:
                    i += 1

            # Recur to insert in the non-full child
            self._insert_non_full(node.children[i], file_name, location)

    def _split_child(self, parent, index):
        """Split the full child of a node."""
        t = self.t
        full_child = parent.children[index]
        new_child = BTreeNode(is_leaf=full_child.is_leaf)

        # Split the keys and children between the nodes
        parent.keys.insert(index, full_child.keys[t - 1])
        parent.children.insert(index + 1, new_child)

        # New child gets half of the keys and children from full_child
        new_child.keys = full_child.keys[t:(2 * t - 1)]
        full_child.keys = full_child.keys[0:(t - 1)]

        # If the child is not a leaf, split its children as well
        if not full_child.is_leaf:
            new_child.children = full_child.children[t:(2 * t)]
            full_child.children = full_child.children[0:t]

# Example usage:
btree = BTree(t=3)
btree.insert("file1.txt", "/path/to/file1.txt")
btree.insert("file2.txt", "/path/to/file2.txt")
btree.insert("file3.txt", "/path/to/file3.txt")

# Search for a file
location = btree.search("file2.txt")
print("Location of file2.txt:", location)  # Output should be /path/to/file2.txt
