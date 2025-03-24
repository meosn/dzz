print("\033c")
class Iterator():
    def __init__(self,listik):
        self.listik = listik
        self.current = listik.head
        self.started = False
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current == self.listik.head.next:
            self.started = True
            
        if self.current == None or self.current == self.listik.head and self.started:
            raise StopIteration
        else:
            self.current = self.current.next
            return self.current.previous.value
        
        
class Node():
    def __init__(self,value) -> None:
        self.next = None
        self.previous = None
        self.value = value

class DoubleLinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.length = 0
        self.cycle = False
    
    def add_left(self,value):
        self.length += 1
        newNode = Node(value)
        if self.head:
            if self.head.previous:
                self.head.previous.next = newNode
                
            newNode.next = self.head
            newNode.previous = self.head.previous
            self.head.previous = newNode
            self.head = newNode
        else:
            self.head = newNode
            self.tail = newNode
    
    def add_right(self,value):
        self.length += 1
        newNode = Node(value)
        if self.tail:
            if self.tail.next:
                self.tail.next.previous = newNode
                
            newNode.next = self.tail.next
            newNode.previous = self.tail
            self.tail.next = newNode
            self.tail = newNode
        else:
            self.head = newNode
            self.tail = newNode

    def add_index(self,value,index):
        i = 0
        
        newNode = Node(value)
        current = self.head
        while current:
            if i == index:
                if current.previous:
                    current.previous.next = newNode
                else:
                    self.head = newNode
                newNode.next = current
                newNode.previous = current.previous
                current.previous = newNode
            i += 1
            if current.next != self.head:
                current = current.next
            else:
                break

        if index == self.length-1:
            # if self.tail.next:
            #     self.tail.next.previous = newNode
            self.add_right(value)
        else:
            self.length += 1
            
    def delete_left(self):
        if self.head:
            if self.head.previous:
                self.head.previous.next = self.head.next
            self.head.next.previous = self.head.previous
            self.head = self.head.next
            self.length -= 1
    
    def delete_right(self):
        if self.tail:
            if self.tail.next:
                self.tail.next.previous = self.tail.previous
            self.tail.previous.next = self.tail.next
            self.tail = self.tail.previous
            self.length -= 1
    
    def delete_index(self,index):
        i = 0
        current = self.head
        while current:
            if i == index:
                if current.previous and current.next:
                    current.previous.next = current.next
                    current.next.previous = current.previous
                    
                elif current.previous:
                    self.delete_right()
                elif current.next:
                    self.delete_left()
                self.length = self.length-1
            i += 1
            if current.next != self.head:
                current = current.next
            else:
                break
            
    def delete_all_value(self,value):
        i = 0
        current = self.head
        while current:
            if current.value == value:
                self.delete_index(i)
                i -= 1
                self.length = self.length - 1
            i += 1
            if current.next != self.head:
                current = current.next
            
    def swichType(self):
        if self.cycle:
            self.cycle = False
            self.head.previous = None
            self.tail.next = None
        else:
            self.cycle = True
            self.head.previous = self.tail
            self.tail.next = self.head


    def __str__(self) -> str:
        output = []
        current = self.head
        while current:
            output.append(current.value)
            if current.next != self.head:
                current = current.next
            else:
                break

        output = " <-> ".join(list(map(str,output)))
        return output
    
    def __iter__(self):
        iterator = Iterator(self)
        return iterator
    
    def __getitem__(self, i):
        current = self.head
        ind = 0
        while current:
            if ind == i:
                return current.value
            ind += 1 
            if current.next != self.head:
                current = current.next
            else:
                break
            
    def __len__(self):
        return self.length
    
    def reverse(self):
        new_list = DoubleLinkedList()
        for i in range(self.length):
            new_list.add_left(self[i])
        return new_list
            
    

linked_list = DoubleLinkedList()
linked_list.add_right(2)
linked_list.add_right(10)
linked_list.add_left(6)
linked_list.add_index(5,1)
# print(linked_list.length)
linked_list.add_index(5,4)
# linked_list.delete_left()
# linked_list.delete_right()
# linked_list.delete_index(2)
linked_list.delete_all_value(5)
linked_list.swichType()

# iterator = iter(linked_list)
# for item in iterator:
#     print(item)
# for i in range(len(linked_list)):
#     print(linked_list[i])
reversed_list = linked_list.reverse()
print(reversed_list)
# print(len(linked_list))
# print(linked_list[2])
# print(linked_list)