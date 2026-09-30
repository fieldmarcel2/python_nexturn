from assignment import DataStructure



class Queue(DataStructure):
        def __init__(self):
         super().__init__()

        def push( self,item):
            return self._items.append(item)
        
        def pop(self):
            return items.pop(0)
        def display(self):
            return items.display()

        def clear(self):
            return items.clear()


class Stack(DataStructure):
        def __init__(self, items):
         super().__init__(items)

        def push( self,item):
            self.item= item
            return item.append(item)
        
        def pop(self):
            return items.pop()
        def display(self):
            return items.display()

        def clear(self):
            return items.clear()        