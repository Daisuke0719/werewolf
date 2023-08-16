from setup import GameInitializer
from moderator import Moderator
from utils import set_logger, clear_cli, show_text_on_cli
import os


def main():
    clear_cli()
    logger = set_logger()
    #ゲームの設定
    
    show_text_on_cli("ゲームの設定")
    game = GameInitializer(logger=logger)
    role_allocation, players = game.initialize()
    clear_cli()
    
    #Game start

    show_text_on_cli("Game Start")
    moderator = Moderator(role_allocation,players,logger= logger)
    moderator.assign_role()
    moderator.check_own_role()

    day_counter = 1
    while True:
        # 朝の行動
        show_text_on_cli(f"{day_counter}日目の朝.")

        if moderator.get_last_naight_victim() is not None:
            print(f"昨晩の被害者:{moderator.get_last_naight_victim}")
        else:
            print("昨晩の被害者はいませんでした．")
            
        moderator.dayaction()        
        if moderator.gamestatus is not None:
            print(moderator.gamestatus)
            break
        clear_cli()
        
        show_text_on_cli(f"{day_counter}日目の夜.")

        moderator.nightaction()
        if moderator.gamestatus is not None:
            print(moderator.gamestatus)
            break
            
        day_counter +=1
        clear_cli()
        

if __name__ == "__main__":
    main()
    