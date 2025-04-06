class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def list_to_linked(listik):
    new_list = LinkedList()
    for val in listik:
        new_list.add_last(val)
        
    return new_list
        
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
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.current == None:
            raise StopIteration
        else:
            
            result = self.current.value
            self.current = self.current.next
            return result

        
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
        if not current.next:
            if current.value == value:
                self.head = None
                self.tail = None
                
        while current.next:
            if current == self.head:
                if current.value == value:
                    self.head = current.next
    
            if current.next.next:
                if current.next.value == value:
                    current.next = current.next.next
                
            else:
                
                if current.next.value == value:
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
    def __len__(self):
        counter = 0
        current = self.head
        while current:
            counter += 1
            current = current.next
        return counter
            
    def __getitem__(self,ind):
        current = self.head
        index = 0
        while current:
            if index == ind:
                return current.value
            index += 1
            current = current.next
    @staticmethod
    def merge(linked1,linked2,i=0,j=0):
        if i == len(linked1):
            if j == len(linked2):
                return
            else:
                for_return = []
                for x in range(j,len(linked2)):
                    for_return.append(linked2[x])
                return for_return
        else:
            if j == len(linked2):
                for_return = []
                for x in range(i,len(linked1)):
                    for_return.append(linked1[x])
                return for_return
            else:
                if linked1[i] >= linked2[j]:
                    if linked1.merge(linked1,linked2,i,j+1):
                        return [linked2[j]]+linked1.merge(linked1,linked2,i,j+1)
                    return [linked2[j]]
                else:
                    if linked1.merge(linked1,linked2,i+1,j):
                        return [linked1[i]]+linked1.merge(linked1,linked2,i+1,j)
                    return [linked1[i]]
            
    @staticmethod
    def merge_for_return(linked1, linked2, i=0, j = 0):
        new_list = linked1.merge(linked1,linked2)
        return list_to_linked(new_list)
                    
                
                
            
        # list1 = func(linked1)
        # list2 = func(linked2)
        # listik = list1 + list2
        # listik = sorting(listik)
        
        # new_list = LinkedList()
        # for x in listik:
        #     new_list.add_last(x)
            
        return new_list
    
    
    @staticmethod
    def compression(linked_list):
        new_list = LinkedList()
        dubl = []
        current = linked_list.head
        while current:
            if current.value in dubl:
                pass
        return new_list.remove_dublicate()
        
        
            
        
        
        
    
    

linked_list = LinkedList()
linked_list.add_first(2)
linked_list.add_last(4)
linked_list.add_last(6)
# linked_list.add_last(4)
# linked_list.add_last(6)
# linked_list.add_last(2)
# linked_list.add_last(6)
# linked_list.add_last(5)

linked_list2 = LinkedList()
linked_list2.add_first(2)
linked_list2.add_last(3)
linked_list2.add_last(5)
linked_list2.add_last(6)
# linked_list2.add_last(0)

# iterator = Iterator(linked_list)
# iterator = iter(linked_list)
# for x in iterator:
#     print(x)
    
# print("\n")
# iterator2 = Iterator(linked_list2)
# iterator2 = iter(linked_list2)
# for x in iterator2:
#     print(x)

linked_list3 = (linked_list.merge_for_return(linked_list,linked_list2))
linked_list3.print_linkedlist()
print("\n")
linked_list3.remove_dublicate()
linked_list3.print_linkedlist()
# linked_list.remove_value(5)

# iterator = iter(linked_list)
# for x in iterator:
#     print(x)
# lisk = linked_list.merge(linked_list2,linked_list)
# listik = linked_list.compression(linked_list)
# linked_list = linked_list.remove_dublicate()
# linked_list.remove_value(5)
# linked_list.remove(0)
# linked_list.print_linkedlist()