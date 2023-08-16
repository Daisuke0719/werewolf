import random
from collections import Counter
import time
import os

from role import RoleAllocation, Roles, Villager, Werewolf, BaseRole
from player import Players, PlayerName, Player
from utils import isInteger, set_logger, clear_cli

class Moderator:
    
    def __init__(self,
                 role_allocation: RoleAllocation,
                 players:Players,
                 logger = None):
        self.role_allocation = role_allocation
        self.players = players
        self.aliveplayers = players
        self.deadplayers = None
        self.gamestatus = None
        self.logger = logger
        self.last_night_victim = None
        
    def assign_role(self):
        role_list = list()

        for role, num in self.role_allocation.items():
            for _ in range(num):
                role_list.append(self._set_role(Roles(role))) 
            
        if self.logger is not None:
            self.logger.debug(f"shuffle前:{[role._role_name for role in role_list]}")

        random.shuffle(role_list)
        
        if self.logger is not None:
            self.logger.debug(f"shuffle後:{[role._role_name for role in role_list]}")
            
        for player,role in zip(self.players,role_list):
            player.set_role(role)
        

    def _set_role(self,role: Roles)-> BaseRole:
        
        if role == Roles.VILLAGER:
            return Villager()
        
        if role == Roles.WEREWOLF:
            return Werewolf()
        
        
    def check_own_role(self):
        for player in self.players:  
            if self._is_yourself(player.name):
                player.role.show_role_name()
                self.finished_check_own_role()
                clear_cli()
    
    
    
    def _is_yourself(self,player_name):
        """
        Player_nameと同一人物か確認をとる.
        確認が取れるまで入力を促す
        """
        notmatch = True 
        print(f"あなたは{player_name}さんですか？正しければyesと入力して下さい")
        while notmatch:
            ans = input()
            if ans == "yes":
                return True
            else:
                print("無効な入力です.")
    
    def finished_check_own_role(self):
        print("役職の確認ができた場合はyesを入力してくだいさい")
        while True:
            check = input()
            if check == "yes":
                return None
            else:
                print("無効な入力です")
    
    def _get_discussion_time(self) -> int:
        
        print("議論する時間を入力してください")
        print("例：3分 -> 入力値: 3")
        invalid_input = True
        while invalid_input:
            minute = input()        
            if isInteger(minute):
                return int(minute)
            else:
                print("無効な入力です．整数値で入力してください.")
   
    
    def set_timer(self,minute):
        second = minute * 60
        time.sleep(second)
    
    
    def select_outcast(self)-> Player:
        """
        生存しているplayerに対して， 人狼と思われるplayerの名前を入力させる
        最多投票数が複数人いる場合は最多投票者からランダムに選択
        """
        result_list = list()
        
        aliveplayer_names = [player.name for player in self.aliveplayers]
        
        for name in aliveplayer_names:
            self._is_yourself(name)
            result_list.append(self._select_outcast(aliveplayer_names))
        
        counter = Counter(result_list)
        sorted_counter = counter.most_common()

        if self._is_vote_tied(sorted_counter):
            tied_players_name = self._get_tied_players(sorted_counter)
            outcast_name = random.choice(tied_players_name)
        else:
            outcast_name = sorted_counter[0][0]

        outcast_index = aliveplayer_names.index(outcast_name)
        
        return self.aliveplayers[outcast_index]
    
    
    def _select_outcast(self,aliveplayer_names):
        
        print("下記playerの中から,追放する人物名を入力して下さい")
        print(aliveplayer_names)

        while True:
            selected_player = input()
            if selected_player in aliveplayer_names:
                result = list
                os.system('clear')
                return selected_player
            
            else:
                print("向こうな入力で生存しているplayer名を入力して下さい")
    
                
    def _is_vote_tied(self,sorted_counter):
        if len(sorted_counter) == 1:
            return False
        
        top_vote_num = sorted_counter[0][1]
        next_vote_num = sorted_counter[1][1]
        
        if top_vote_num == next_vote_num:
            return True
        else:
            return False
        
        
    def _get_tied_players(self, sorted_counter)->list[PlayerName]:
        top_voted_num = sorted_counter[0][1]
        tied_players_name = list()
        for name, voted_num in sorted_counter:
            if voted_num == top_voted_num:
                tied_players_name.append(name)
            else:
                break
                
        return tied_players_name

    
    def update_alivalplayers(self):

        self.aliveplayers = [player for player in self.players if player.is_Alive]
        
    
    def judgment(self):
        aliveplayers_num = len(self.aliveplayers)
        werewolf_num = len([player for player in self.aliveplayers if player.role._role_name == "人狼"])
        other_roles_num = aliveplayers_num - werewolf_num
        
        if other_roles_num <= werewolf_num:
            self.gamestatus = "人狼陣営の勝利"
            
        if werewolf_num == 0:
            self.gamestatus = "村人陣営の勝利"
            
            
    def selcet_victim(self) -> Player:
        aliveplayer_names = [player.name for player in self.aliveplayers]
        target_list = list()        
        
        for player in self.aliveplayers:
            if player.role._role_name == "人狼":
                target_list.append(player.role._target_name)
                
        target_counter = Counter(target_list)
        sorted_counter = target_counter.most_common()
        
        if self._is_vote_tied(sorted_counter):
            tied_players_name = self._get_tied_players(sorted_counter)
            outcast_name = random.choice(tied_players_name)
        else:
            outcast_name = sorted_counter[0][0]

        target_index = aliveplayer_names.index(outcast_name)
        return self.aliveplayers[target_index]

            
    def dayaction(self):
        
        #昨晩の被害者の
        
        #議論の時間入力
        minute = self._get_discussion_time()
        #議論開始
        print("議論を開始してください.")
        self.set_timer(minute)
        
        #議論終了
        print("時間になりました議論を終了してください")
        
        self._log_player_status("select_outcast関数使用前")

        #投票
        outcast_player = self.select_outcast()
        #追放
        print(f"{outcast_player.name}が追放されます")
        
        self._log_player_status("dead関数使用前")
        
        outcast_player.dead()
        
        self._log_player_status("dead関数使用後")
                
        #勝利判定
        self.update_alivalplayers()
        
        self._log_player_status("update_alivalplayers使用後")

        self.judgment()
    
    
    def nightaction(self):
        
        #各Playerが夜の行動をとる
        for player in self.aliveplayers:
            if self._is_yourself(player.name):
                player.nightaction()
        
        #殺害する人物を決める
        victim = self.selcet_victim()
        victim.dead()
        self._log_player_status("dead使用後")
        self.last_night_victim = victim.name

        
        self.update_alivalplayers()
        self._log_player_status("update_alivalplayers使用後")

        self.judgment()
        
    def get_last_naight_victim(self):
        return self.last_night_victim
    
    
    def get_gamestatus(self):
        return self.gamestatus
    
    def _log_player_status(self,text = None):
        if self.logger is not None:
            self.logger.debug(text)
            for player in self.players:
                self.logger.debug(f"player:{player.name},status:{player.is_Alive}")