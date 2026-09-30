from OOPS.assignment.assignment import Player

class proGamer(Player):

     def __init__(self, name,games_played, wins, kills):
         self.name= name
         self.games_played= games_played
         self.wins= wins
         self.kills= kills

     def calculate_score(self):
            return 100*self.wins + 20*self.kills
     def title(self):
                 return "Sweat Lord"      



class casualGamer(Player):    
     def __init__(self, name,games_played, wins, kills):
             self.name= name
             self.games_played= games_played
             self.wins= wins
             self.kills= kills

     def calculate_score(self):
            return 50*self.wins + 10*self.kills
     def title(self):
            return "Just Here for Fun"
     
class Streamer(Player):
        def __init__(self, name,games_played, wins, viewers):
                           self.name= name
                           self.games_played= games_played
                           self.wins= wins
                           self.viewers= viewers
                           
        def calculate_score(self):
            return 100*self.wins + self.viewers//100
        def title(self):
            return "Content Machine"


p1= proGamer("Rahul", 10, 10, 10)
# print(p1.games_played,p1.wins, p1.kills)
c1= casualGamer("Amit", 10, 5, 20)
# print(c1)

s1= Streamer("Priya", 8, 4, 50000)
# print(s1.games_played,s1.wins, s1.viewers)

list=[p1,c1,s1]


for i in list:
 ( i.show_details())
 print("score",i.calculate_score())
 print(i.title())