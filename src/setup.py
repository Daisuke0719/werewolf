import re
from typing_extensions import TypeAlias
from enum import Enum
from player import Player, Players, PlayerName, PlayerNames
from role import Roles, AVAILABLE_ROLES, BASE_ROLES, WEREWOLF_SIDE_ROLES, VILLAGER_SIDE_ROLES



RoleAllocation: TypeAlias = dict[Roles,int]


class GameInitializer:
    """
    ゲーム開始に必要な情報を取得する
    取得する情報
    - 使用する役職
    - 役職別の人数
    - Playerの名前
    """

    def __init__(self, logger = None):
        self.logger = logger
    
    def initialize(self)->tuple[RoleAllocation,PlayerNames]:
        
        self.__use_roles = self._select_using_roles()
        self.role_allocation:RoleAllocation = self._allocate_role_numbers()
        
        self.__player_num = self._get_player_num()
        self.players: Players =  self._make_players()
        
        return self.role_allocation, self.players

    def _select_using_roles(self)-> list[Roles]:
        """
        ユーザーに使用する配役を入力してもらう
        AVAILABLE_ROLESに含まれていない役職は受け付けない
        TODO
        - 利用可能なすべての役職が追加されたらループを抜ける
        - 現在の役職を表示
        """
        print("追加したい役職があればその役職名を入力してください.なければDoneと入力してください\n"\
              "使用可能な役職:")
        for i, role in enumerate(AVAILABLE_ROLES):
            print(f"- {role}")

        keep_input = True

        use_roles = BASE_ROLES.copy()
        while keep_input:
            inputted = input()

            if inputted in use_roles:
                print("既に追加済みの役職です.その他の新たに追加したい役職を選択してください．なければDoneを入力してください")
                continue

            if inputted in AVAILABLE_ROLES:
                use_roles.append(inputted)
                print(f"使用する役職に{inputted}を追加しました．")
                print(f"その他に追加したい役職があれば役職名を入力してください.なければDoneを入力してください")

            elif inputted == "Done":
                keep_input = False

            else:
                print("無効な入力です．追加したい役職を入力するか，Doneを入力してください")    
        self._log_debug(f"使用する配役:{use_roles}")
        return use_roles

    
    def _allocate_role_numbers(self)-> dict[Roles, int]:
        """
        村人陣営の人数が人狼陣営の人数より多くなるように配役を入力させる
        """

        unbalance = True 
        
        #妥当なバランスになるまで入力を繰り返させる
        while unbalance:
            
            #配役別の人数を入力
            role_allocation = self.__allocate_role_numbers()
            self._log_debug(f"役職別の人数:{role_allocation}")

            if self._is_valid_player_balance(role_allocation):
                unbalance = False
                
            else:
                print("人狼陣営の方が人数が多いです.")
                print("村人陣営の人数が人狼陣営の人数より多くなるように配役の人数を設定してください.")
        return role_allocation
            
    
    def __allocate_role_numbers(self)->dict[Roles,int]:
        """
        役職毎の人数を入力させる,数値以外の入力は無効とする
        """
        
        role_allocation = dict()

        for role in self.__use_roles:
            print(f"役職：{role}の人数を入力してください")
            print(f"例:2人->[入力]:2")
            isnotint = True
            while isnotint:
                num = input()
                # TODO: 入力の妥当性検証
                if self._isInteger(num):
                    role_allocation[role] = int(num)
                    isnotint = False
                else:
                    print("無効な入力です,数値で入力してください.")
        
        return  role_allocation

    
    def _get_player_num(self):
        """playerの総数"""
        return sum([value for value in self.role_allocation.values()])
    
    
    def _make_players(self):
        players = list()
        
        for i in range(self.__player_num):
            player = Player(id_num = i)
            players.append(player)
        return players
        
    
    def _is_valid_player_balance(self, role_numbers:dict[Roles,int])->bool:
        """
        村人陣営<=人狼陣営の人数の場合,スタート直後から人狼陣営の勝利が確定しまうためチェックする必要あり
        """
        villagers_num = 0
        werewolfs_num = 0
        
        for role, num in role_numbers.items():
            self._log_debug(f"role:{role}, num:{num}")
            if role in VILLAGER_SIDE_ROLES:
                villagers_num += num

            if role in WEREWOLF_SIDE_ROLES:
                werewolfs_num += num
        self._log_debug(f"村人陣営の数:{villagers_num}")
        self._log_debug(f"人狼陣営の数:{werewolfs_num}")
        return villagers_num > werewolfs_num
        
    
    def _isInteger(self, value):
        """
        整数チェック
        :param value: チェック対象の文字列
        :rtype: チェック対象文字列が、全て数値の場合 True
        """
        return re.match(r"^\d+$", value) is not None
    
    def reset_isalive(self):
        for player in self.players:
            player.reborn()
            
    def _log_debug(self,text):
        if self.logger is not None:
            self.logger.debug(text)