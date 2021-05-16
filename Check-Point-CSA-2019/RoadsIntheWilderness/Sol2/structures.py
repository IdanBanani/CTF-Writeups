
# Stack Implementation

class stack:
    def __init__(self):
        self.size = 0
        self.top = 0
    def push(self,data):
        n = stack_node(data)
        n.next = self.top
        self.top = n
        self.size += 1
        return 0
    def pop(self):
        if self.top == 0:
            return -1
        else:
            self.top = self.top.next
            self.size = self.size -1
            return 0
    def peek(self):
        if self.top == 0:
            return -1
        else:
            return self.top.data
    def getSize(self):
        return self.size

class stack_node:
    def __init__(self, data):
        self.data = data
        self.next = 0
    

# Queue Implementation

class queue:
    def __init__(self):
        self.fisrt = 0
        self.last = 0
        self.size = 0

    def add(self, data):
        n = queue_node(data)
        if self.size == 0:
            self.first = n
        else:
            self.last.next = n
        self.last = n
        self.size += 1
        return 0

    def remove(self):
        if self.size == 0:
            return -1
        elif self.size == 1:
            last = 0
        self.first = self.first.next
        self.size -= 1

    def peek(self):
        if self.size == 0:
            return -1
        return self.first.data

    def getSize(self):
        return self.size

class queue_node:
    def __init__(self, data):
        self.data = data
        self.next = 0

# Linked List
class LinkedList:
    def __init__(self):
        self.top = 0
        self.size = 0
    
    def AddToTail(self, data):
        end = LinkedNode(data)
        if self.top == 0:
            self.top = end
        else:
            node = self.top
            if node.data == data:
                return -1
            while node.next != 0:
                if node.data == data:
                    return -1
                node = node.next
            node.next = end
        self.size += 1
        return 0

    def DeleteNode(self, data):
        node = self.top
        if node.data == data:
            self.top = self.top.next
            self.size -= 1
            return 0
        while node.next != 0:
            if node.next.data == data:
                node.next = node.next.next
                self.size -= 1
                return 0
            node = node.next
        return -1

    def Find(self,data):
        node = self.top
        if node.data == data:
            return node
        while node.next != 0:
            if node.next.data == data:
                return node.next
            node = node.next
        return -1

    def getSize(self):
        return self.size

class LinkedNode:
    def __init__(self, data):
        self.data = data
        self.next = 0

# Hash Table w/ Linked List

class HashTable:
    
    def __init__(self, mod_size):
        self.ListsList = [LinkedList() for i in range(mod_size)]

    def SearchAux(self, value):
        index = hash(value) % len(self.ListsList)
        indexed_list = self.ListsList[index]
        if indexed_list != 0:
            return indexed_list
        else:
            return -1

    def Search(self, val):
        list_ref = self.SearchAux(val)
        if list_ref == -1:
            return -1
        else:
            return list_ref.Find(val)
    
    def AddToTable(self, val):
        list_ref = self.SearchAux(val)
        if list_ref == -1:
            return -1
        else:
            return list_ref.AddToTail(val)
    
    def DeleteFromTable(self, val):
        list_ref = self.SearchAux(val)
        if list_ref == -1:
            return -1
        else:
            return list_ref.DeleteNode(val)

    def __str__(self):
        out = ''
        for (ind, item) in enumerate(self.ListsList):
            out += (str(ind)+": ")
            node = item.top
            if node != 0:
                out += (str(node.data))
                node = node.next
            while (node != 0):
                out += (" -> " + str(node.data))
                print(node.next)
                node = node.next
            out += ("\n")
        return out
'''
myHash = HashTable(10)
myHash.AddToTable(5)
print("Added 5")
print(myHash)
myHash.AddToTable(7)
print("Added 7")
print(myHash)
myHash.AddToTable(9)
print("Added 9")
print(myHash)
myHash.AddToTable(11)
print("Added 11")
print(myHash)
myHash.AddToTable(13)
print("Added 13")
print(myHash)
myHash.AddToTable(13)
print("Added 13")
print(myHash)
myHash.AddToTable(15)
print("Added 15")
print(myHash)
myHash.DeleteFromTable(1)
print("Removed 1")
print(myHash)
myHash.DeleteFromTable(5)
print("Removed 5")
print(myHash)
myHash.DeleteFromTable(15)
print("Removed 15")
print(myHash)
myHash.AddToTable(15)
print("Added 15")
print(myHash)
myHash.AddToTable(5)
print("Added 5")
print(myHash)
myHash.AddToTable(15)
print("Added 15")
print(myHash)
'''
# Tree

class TreeNode:
    def __init__(self, val = 0):
        self.parent = 0
        self.val = val
        self.left = 0
        self.right = 0

    def AddSon(self, val, side):
        node = TreeNode(val)
        if side == 'l':
            self.left = node
        elif side == 'r':
            self.right = node
        else:
            return -1 
        node.parent = self
        return node

    def RemoveSon(self, side):
        if side == 'l':
            self.left = 0
        elif side == 'r':
            self.right = 0
        else:
            return -1 
        return 0

class TreeNodeNonBinary:
    def __init__(self, val = 0):
        self.parent = 0
        self.val = val
        self.children = []

    def AddSon(self, val):
        node = TreeNodeNonBinary(val)
        self.children.append(node)
        node.parent = self
        return node

    def RemoveSon(self, son_val):
        if son_val in self.children:
            self.children.remove(son_val)
        else:
            return -1 
        return 0