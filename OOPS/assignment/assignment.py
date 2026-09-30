# from abc import ABC , abstractmethod



# class Player(ABC):

#     def __init__(self, name, games_played):
#         self.name= name
#         self.games_played= games_played
#         pass

#     @abstractmethod
#     def calculate_score(self):
#         pass

#     @abstractmethod
#     def title(self):
#         pass

    
#     def show_details(self):
#          print("name:",self.name)
#          print("games played:",self.games_played)


from abc import ABC , abstractmethod


@abstractmethod
class DataStructure(ABC):
    def __init__(self):
        self._items=[]

    @abstractmethod
    def  push(self):
        pass
    @abstractmethod
    def  pop(self):
      pass 


    @abstractmethod
    def  display(self):
         pass

    @abstractmethod
    def  clear(self):
       pass
     
    def  isempty(self,*items):
        if( len(self._items)==0): return True

         