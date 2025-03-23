class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        
def sorting(oo):
            n = 0
            while n == 0:
                n += 1
                for i in range(0,len(oo)-1):
                    if oo[i+1] < oo[i]:
                        oo[i+1],oo[i] = oo[i],oo[i+1]
                        n *= 0
            return oo
        
def func(lis):
            oo = []
            current = lis.head
            
            while current:
                oo.append(current.value)
                current = current.next
            oo = sorting(oo)
            return oo
    
# common iterator:
# class Iterator():
#     def __init__(self,value):
#         self.value = value
#         self.index = 0
        
#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         if self.index == len(self.value):
#             raise StopIteration
#         else:
#             # print(self.index)
#             self.index = self.index + 1
#             return self.value[self.index-1]
        
class Iterator():
    def __init__(self,listik):
        self.listik = listik
        self.current = listik.head
        self.for_return = listik.head
        
    def __iter__(self):
        return self
    
    def __next__(self):
        self.for_return = self.current
        if self.for_return == None:
            raise StopIteration
        else:
            self.current = self.current.next
            return self.for_return.value

        
class LinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def print_linkedlist(self):
        current = self.head
        while current:
            print(current.value)
            current = current.next

    def add_first(self, value):
        new_node = Node(value)
        if(self.length == 0):
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1

    def add_last(self, value):
        new_node = Node(value)
        if(self.length == 0):
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def insert(self, index, value):
        if(index == 0):
            self.add_first(value)
            return
        if(index >= self.length):
            self.add_last(value)
            return
        
        new_node = Node(value)
        current = self.head
        for i in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node

        self.length += 1


    def remove_first(self):
        if(self.length > 1):
            self.head = self.head.next
        if(self.length == 1):
            self.head = None
            self.tail = None
        if(self.length != 0):
            self.length -= 1

    def remove_last(self):
        if(self.length > 1):
            current = self.head
            for i in range(self.length - 2):
                current = current.next
            self.tail = current
            self.tail.next = None
        if(self.length == 1):
            self.head = None
            self.tail = None
        if(self.length != 0):
            self.length -= 1

    def remove(self, index):
        if(index == 0):
            self.remove_first()
            return
        if(index >= self.length):
            self.remove_last()
            return

        current = self.head
        for i in range(index - 1):
            current = current.next
        
        current.next = current.next.next
        self.length -= 1

    def remove_value(self,value):
        current = self.head
        while current.next:
            if current == self.head:
                if current.value == value:
                    self.head = current.next
    
            if current.next.next:
                if current.next.value == value:
                    current.next = current.next.next
                
            else:
                
                if current.next.value == value:
                    print("heheh")
                    current.next = None
            if current.next:
                current = current.next
                
                    
    def remove_dublicate(self):
        current = self.head
        dubl = [current.value]
        while current.next:
            if current.next.value not in dubl:
                dubl.append(current.next.value)
                if current.next:
                    current = current.next
                    
            else:
                current.next = current.next.next
            
            
        
        return self
                

    # итератор для циклического прохода
    def __iter__(self):
        iterator = Iterator(self)
        return iterator

    # слияние отсортированных связных списков
    # возрат нового списка 
    # (нельзя использовать встроенную сортировку)
    @staticmethod
    def merge(linked1, linked2):
        
        list1 = func(linked1)
        list2 = func(linked2)
        listik = list1 + list2
        listik = sorting(listik)
        
        new_list = LinkedList()
        for x in listik:
            new_list.add_last(x)
            
        return new_list
    
    @staticmethod
    def compression(linked_list):
        listik = func(linked_list)
        new_list = LinkedList()
        for x in listik:
            new_list.add_last(x)
            
        return new_list.remove_dublicate()
        
        
            
        
        
        
    
    

linked_list = LinkedList()
linked_list.add_first(5)
linked_list.add_last(4)
linked_list.add_last(5)
linked_list.add_last(4)
linked_list.add_last(6)
linked_list.add_last(2)
linked_list.add_last(6)
linked_list.add_last(5)

linked_list2 = LinkedList()
linked_list2.add_first(1)
linked_list2.add_last(8)
linked_list2.add_last(5)
linked_list2.add_last(4)
linked_list2.add_last(0)

# iterator = Iterator(linked_list)
iterator = iter(linked_list)
for x in iterator:
    print(x)
# lisk = linked_list.merge(linked_list2,linked_list)
# listik = linked_list.compression(linked_list)
# linked_list = linked_list.remove_dublicate()
# linked_list.remove_value(5)
# linked_list.remove(0)
# linked_list.print_linkedlist()