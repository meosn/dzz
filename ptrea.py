class Node:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None
    
    def insert(self, value, priority):
        self.root = self._insert(self.root, value, priority)
    
    def _insert(self, node, value, priority):
        if node is None:
            return Node(value, priority)
        
        if value < node.value:
            node.left = self._insert(node.left, value, priority)
            if node.left and node.left.priority < node.priority:
                node = self.right_rotate(node)
        else:
            node.right = self._insert(node.right, value, priority)
            if node.right and node.right.priority < node.priority:
                node = self.left_rotate(node)
        
        return node
    
    def delete(self, value):
        self.root = self._delete(self.root, value)
    
    def _delete(self, node, value):
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                if node.left.priority < node.right.priority:
                    node = self.right_rotate(node)
                    node.right = self._delete(node.right, value)
                else:
                    node = self.left_rotate(node)
                    node.left = self._delete(node.left, value)
        
        return node
    
    def right_rotate(self, y):
        x = y.left
        a = x.right
        
        x.right = y
        y.left = a
        
        return x

    def left_rotate(self, x):
        y = x.right
        a = y.left
        
        y.left = x
        x.right = a
        
        return y
    
    def printTree(self, root=None, level=0):
        if root is None:
            return
        
        self.printTree(root.right, level + 1)
        print("    " * level, "->", f"{root.value}({root.priority})")
        self.printTree(root.left, level + 1)

treap = Treap()


print("\033c")   

treap.insert(30,2)
treap.insert(60,0)
treap.insert(20,2)
treap.insert(15,1)
treap.insert(76,3)
treap.insert(49,0)
treap.insert(78,0)
treap.printTree(treap.root)
print("\n\n")
treap.delete(15)
treap.printTree(treap.root)