print("\033c")
def create_Gen(history:"History"):
    # print("\033[32m{}".format("text"))
    current = history.head
    green = True
    while current:
        if green:
            yield "\033[32m{}".format(str(current))
        else:
            yield str(current)
        if current == history.current:
            green = False
        current = current.next
    
class Node():
    def __init__(self,timestamp,action_id,username,action_type):
        self.prev = None
        self.next = None
        self.action_id = action_id
        self.timestamp = timestamp
        self.username  = username
        self.action_type = action_type
        
    def __str__(self):
        return f"{self.action_id}, { self.timestamp}, {self.username}, {self.action_type}"
    
    
class History():
    def __init__(self,current:Node,actions_map:dict):
        self.head = None
        self.tail = None
        self.current = current
        self.actions_map = actions_map
        
    def add_action(self,timestamp,username,action_type):
        new_node = Node(timestamp,len(self.actions_map),username,action_type)
        self.actions_map[len(self.actions_map)] = new_node
        if self.tail:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        else:
            self.tail = new_node
            self.head = new_node
        
    def undo(self):
        if self.current != self.head and self.current.prev:
            self.current = self.current.prev
    
    def redo(self):
        if self.current != self.tail and self.current.next:
            self.current = self.current.next
        
    def find_action(self,action_id) -> Node:
        for k,val in self.actions_map.items():
            if k == action_id:
                return val
        return None
    
    def remove_action(self,action_id):
        node = self.find_action(action_id)
        if self.current == node:
            self.current = node.prev
        del self.actions_map[action_id]
        if node != self.head and node != self.tail:
            node.prev.next = node.next
            node.next.prev = node.prev
        elif node == self.head:
            if node == self.tail:
                self.tail = None
                self.head = None
            else:
                self.head = node.next
                node.next.prev = node.prev
        else:
            if node == self.tail:
                self.tail = node.prev
                node.prev.next = node.next
        id = 0
        for v in self.actions_map.values():
            v.action_id = id
            id += 1
            
    def filter_and_remove(self,action_type):
        delet = []
        cop = self.actions_map.copy()
        for k,v in cop.items():
            if v.action_type == action_type:
                delet.append(v)
                
                
        for x in delet:
            self.remove_action(x.action_id)
            for k,v in self.actions_map.items():
                if v == x:
                    del self.actions_map[k]
            
    def print(self):
        mygen = create_Gen(self)
        for i in mygen:
            print(i)
    
        
            
history = History(None,{})
history.add_action("03.05.2025 23:44:12","Petya","Brush")
history.add_action("05.05.2025 23:44:12","Petya","Paint")
history.add_action("03.05.2025 23:44:12","Petya","Layer")
# history.filter_and_remove("Layer")
# print(history.tail)
history.print()
