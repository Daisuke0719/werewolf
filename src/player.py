from typing import Optional
from typing_extensions import TypeAlias
from role import BaseRole
import os

class Player():

    def __init__(self,id_num):
        self.id: int = id_num

        self.name: str = self.input_name() 
        self.role: Optional[BaseRole] = None
        self.is_Alive: bool = True
        # self.is_Guardable: bool = False
        # self.is_Divinationable: bool = True
    
    
    def input_name(self):
        print(f"player{self.id}の名前を入力してください")
        name = input()
        return name


    def dead(self):
        self.is_Alive = False

    
    def reborn(self):
        self.is_Alive = True

    
    def set_role(self,role: BaseRole):
        self.role = role
        

    def dayaction(self):        
        self.role.dayaction()
                
    
    def nightaction(self):        
        self.role.nightaction()
        os.system('clear')



Players: TypeAlias = list[Player]
PlayerName: TypeAlias = str
PlayerNames: TypeAlias = list[PlayerName]
