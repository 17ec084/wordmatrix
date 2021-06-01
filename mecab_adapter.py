# アダプタパターン(移譲版)の解説サイト https://www.techscore.com/tech/DesignPattern/Adapter/Adapter2.html/
# ※継承版アダプタパターンは「self」の扱いが難しく、断念。
"""
単語抽出器: アダプタパターンにおけるターゲット・インタフェース(解説サイトで言う、議長インタフェース)。
メカブアダプタ: 解説サイトで言う、花子。 太郎に当たるMeCab.Taggerを持つ(メカブアダプタ has-a Mecab.Tagger)。
"""
#!apt install aptitude
#!aptitude install mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file -y
#!pip install mecab-python3==0.7


import MeCab
from wordtype import 単語
from abc import ABC, ABCMeta, abstractmethod

class 単語抽出器(metaclass = ABCMeta):
    @abstractmethod
    def 解析する(self, 文):pass

    
class メカブアダプタ(単語抽出器):
    def __init__(self, モード=""):
        self.__m = MeCab.Tagger(モード)
    def 解析する(self, 文, モード=None):
        if 文[-1] != "。":
            raise Exception("文の最後は「。」である必要があります。")
        if "。" in 文[:-1]:
            raise Exception("文の途中に「。」が含まれていました。")
        if モード is not None:
            self.__m = MeCab.Tagger(モード)
        単語解析結果リスト = self.__m.parse(文).split("\n")[:-2]
        単語解析結果リスト = [単語解析結果.split("\t")[-1] for 単語解析結果 in 単語解析結果リスト]
        単語解析結果リスト = [単語解析結果.split(",") for 単語解析結果 in 単語解析結果リスト]
        単語リスト = [単語(_[0], _[1], _[2], _[3], _[4], _[6]) for _ in 単語解析結果リスト] 

        return 単語リスト
