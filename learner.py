# https://www.techscore.com/tech/DesignPattern/TemplateMethod.html/
from abc import ABCMeta, abstractmethod
import numpy as np
from wordtype import 単語 as 単語型, EOS, BOS
from mecab_adapter import メカブアダプタ

def 交差エントロピー誤差を求める(y, t):
    return -np.sum(t * np.log(y + 1e-7))

class 学習器エラー(Exception): pass
class 学習器テンプレート(metaclass = ABCMeta):
    """
    デザインパターン「テンプレートメソッド」における抽象型である。
    具象クラスでは効率的に「学習器」を構成することができる。
    具象クラスでは、次のメソッドを定義してください。
    - _学習器テンプレート__順伝搬 
    - _学習器テンプレート__逆伝搬
    - get_n:  ラベルの場合の数nを返却するメソッドを定義してください。
    - n: こちらはメソッドではなくプロパティです。 n = property(get_n)として下さい。
    """
    エラー = 学習器エラー

    def 学習する(self, 文, 正解ラベル):
        t = type(self).__正解ラベル処理(正解ラベル, self.n)
        (誤差, y) = self.検証する(文, t)

        self._学習器テンプレート__逆伝搬(y,t)
        return (誤差, y)

    def 検証する(self, 文, 正解ラベル):
        正解ラベル = type(self).__正解ラベル処理(正解ラベル, self.n)
        意味ベクトル = self.予測する(文)
        return (type(self).損失関数(意味ベクトル, 正解ラベル), 意味ベクトル)
        
    def 予測する(self, 文):
        self.単語たち = メカブアダプタ().解析する(文)[:-1] # BOS/EOS/。を含まない
        return self._学習器テンプレート__順伝搬()


    @classmethod
    def 損失関数(cls, y, t):
        return 交差エントロピー誤差を求める(y, t)

    @classmethod
    def __正解ラベル処理(cls, 正解ラベル, n):
        if   (type(正解ラベル) in (int, float)) or \
             正解ラベル.ndim == 0:
            tmp = np.array([[0]*n])
            tmp[0, 正解ラベル] = 1
            正解ラベル = tmp
        elif 正解ラベル.ndim == 1: 正解ラベル = np.array([正解ラベル])
        elif 正解ラベル.ndim == 2: pass
        else: raise TypeError("正解ラベルの階数が異常です")
        return 正解ラベル        

    @abstractmethod
    def _学習器テンプレート__順伝搬(self): pass
    @abstractmethod
    def _学習器テンプレート__逆伝搬(self): pass

    @abstractmethod
    def get_n(self): pass
    # 具象クラスではラベルの個数(つまり出力ベクトルの長さ)を与えてください。
    # またget_nの実装後、n = property(get_n)を宣言して下さい。
    
    

class 学習器(学習器テンプレート):
    """
    「a1r丸t[x]」とはaddOneRight(x)の転置ベクトルのことである。
    addOneRightおよび「星」については次のページを参照のこと
    https://drive.google.com/file/d/1Pxfa75929rTupektcxNMV4KIHGle-tdy/view?usp=sharing
    """
    def __init__(self, m, n, 単語行列):
        self.__m = m
        self.__n = n
        self.単語行列 = 単語行列
    
    def _学習器テンプレート__順伝搬(self):
        全ての単語について計算した = IndexError # イテレータを使う場合はStopIteration
        単語行列 = self.単語行列
        単語たち = [None] + self.単語たち
        cls = type(self)
        (relu, add1right, softmax) = (cls.relu, cls.add1right, cls.softmax)
        self.__a1r丸t = [None]*(len(self.単語たち)+1)

        try:
            i = 0
            意味ベクトル = 単語行列[BOS]
            self.__a1r丸t[i] = add1right(意味ベクトル).T
            i += 1
            while True:
                意味ベクトル = relu(np.dot(add1right(意味ベクトル), 単語行列[単語たち[i]]))
                self.__a1r丸t[i] = add1right(意味ベクトル).T
                i += 1
        except 全ての単語について計算した:
            意味ベクトル = softmax(np.dot(add1right(意味ベクトル), 単語行列[EOS]))
            return 意味ベクトル

    def _学習器テンプレート__逆伝搬(self, y,t):
        単語行列 = self.単語行列
        全ての単語について計算した = type(単語行列).エラー # イテレータを使う場合はStopIteration
        単語たち = [BOS] + self.単語たち + [EOS]
        cls = type(self)
        (relu, add1right, softmax) = (cls.relu, cls.add1right, cls.softmax)

        星 = softmax(None, 逆伝搬=True, y=y, t=t)
        def 星の更新(星i_plus_1, i_plus_1):
            i = i_plus_1 - 1
            
            星i = \
            relu(
                add1right(
                    np.dot(
                        星i_plus_1, 単語行列[単語たち[i+1]].T
                    ), 
                    逆伝搬=True
                ), 
                逆伝搬=True
            )
            return 星i
       #end def

        try:
            i = len(self.単語たち)
            単語行列.更新する(単語たち[i+1], np.dot(self.__a1r丸t[i], 星))
            星 = 星の更新(星, i_plus_1=i+1)
            i -= 1
            while True:
                単語行列.更新する(単語たち[i+1], np.dot(self.__a1r丸t[i], 星))
                星 = 星の更新(星, i_plus_1=i+1)
                i -= 1
        except 全ての単語について計算した:
            return
            
    def get_n(self): return self.__n 
    n = property(get_n)

    @classmethod
    def add1right(cls, arr, 逆伝搬=False):
        return arr[0:,:-1] if 逆伝搬 else np.append(arr,[[1]], axis=1) 

    @classmethod
    def relu(cls, arr, 逆伝搬=False, leakiness=0):
        return np.where(arr > 0, 1, leakiness) if 逆伝搬 else np.where(arr > 0, arr, leakiness*arr)
        
    @classmethod
    def softmax(cls, 横ベクトル, 逆伝搬=False, **kwargs):
        return (kwargs["y"]-kwargs["t"]) if 逆伝搬 else np.exp(横ベクトル) / np.sum(np.exp(横ベクトル))
