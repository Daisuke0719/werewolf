from logging import getLogger, StreamHandler, DEBUG
import re
import os 
def set_logger(level = DEBUG):
    logger = getLogger(__name__)
    logger.setLevel(DEBUG)
    if not logger.hasHandlers():
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        logger.addHandler(handler)
    logger.propagate = False
    return logger

def log_debug(logger,text):
    if logger is not None:
        logger.debug(text)
        
        
def isInteger(value):
    """
    整数チェック
    :param value: チェック対象の文字列
    :rtype: チェック対象文字列が、全て数値の場合 True
    """
    return re.match(r"^\d+$", value) is not None

def clear_cli():
        os.system("clear")

def show_text_on_cli(text):
    print("=" * 30)
    print(text)
    print("=" * 30)
