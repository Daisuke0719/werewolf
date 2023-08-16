from enum import Enum
from typing import Final
from typing_extensions import TypeAlias
from abc import ABC, abstractmethod


class Roles(Enum):
    """
    役職の列挙
    今後新たな役職を追加する場合は必ずここに役職を追加する
    """
    VILLAGER = "村人"
    WEREWOLF = "人狼"
    SEER = "占い師"
    MEDIC = "騎士"
    MADMAN = "狂人"    

BASE_ROLES: Final[list[Roles]] = [
    "村人",
    "人狼"]

AVAILABLE_ROLES: Final[list[Roles]] = [
    "占い師",
    "騎士",
    "狂人"]

VILLAGER_SIDE_ROLES: Final[list[Roles]] = [
    "村人",
    "騎士",
    "占い師"]

WEREWOLF_SIDE_ROLES: Final[list[Roles]] = [
    "人狼",
    "狂人"]


class BaseRole(ABC):
    """
    役職クラスに必要なメソッドは
    昼の行動
    夜の行動
    """
    
    @abstractmethod
    def dayaction(self):
        pass
    
    @abstractmethod
    def nightaction(self):
        pass
    
    def show_role_name(self):
        print(f"あなたの役職は{self._role_name}です")
        

RoleAllocation: TypeAlias = dict[Roles,int]

class Villager(BaseRole):
    """
    村人の行動
    """
    def __init__(self):
        super().__init__()
        self._role_name = "村人"
    def dayaction(self):
        pass
        
    def nightaction(self):
        pass    
    
    
class Werewolf(BaseRole):
    """
    人狼の行動
    """
    def __init__(self,logger = None):
        super().__init__()
        self.__logger = logger
        
        self._role_name = "人狼"
        
        self._target_name = None
        
    def dayaction(self):
        pass
    
    def nightaction(self):
        self.reset_target_for_kill()
        self.choose_target_for_kill()
        
    def reset_target_for_kill(self):
        self._target_name = None
    
    def choose_target_for_kill(self):
        print("殺害する人の名前を選択していください")
        name = input()
        #TODO 妥当性検証
        self._target_name = name    