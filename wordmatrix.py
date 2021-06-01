from wordtype import 単語, EOS, BOS
import numpy as np

class Singleton:
    """
     Singleton パターン
    https://www.techscore.com/tech/DesignPattern/Singleton.html/
    """  
    _instance = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        kwargs.update({"__singleton":"__singleton"})
        mode = 2
        # 0: もっとも新しいインスタンスを生かす場合
        # 1: もっとも古いインスタンスを生かす場合
        # それ以外のintオブジェクト: 別のインスタンスが作られそうな時TypeError

        if mode:
            if mode != 1 and cls._instance is not None: 
                raise TypeError("singleton継承型のオブジェクトを複数生成することはできません")
            cls._instance = cls._instance or cls(*args, **kwargs)
        else:
            cls._instance = ("dummy" if cls._instance.__init__(*args, **kwargs) else cls._instance) or cls(*args, **kwargs)
        
        return cls._instance

    def __del__(self):
        type(self)._instance = None

    @classmethod
    def assert_initialize(cls, *args, **kwargs):
        if "__singleton" in kwargs.keys() and kwargs["__singleton"] == "__singleton":
            del kwargs["__singleton"]
            return (args, kwargs)
        else:
            raise type("AccessException", (Exception,), {})("private化されたコンストラクタにアクセスしないでください")   

class 単語行列エラー(Exception): pass
class 単語行列(Singleton):
    """
    必ず__del__特殊メソッドを継承し、super().__del__()を呼んでください。
    """
    エラー = 単語行列エラー
    def __init__(self, m, n, 学習率, default_eye=True, **kwargs):
        (args, kwargs) = type(self).assert_initialize(*(tuple()), **kwargs)
        self._m = int(m)
        self._n = int(n)
        self._学習率 = float(学習率)
        self._辞書 = {EOS:np.eye(self._m, self._n), BOS:np.array([[(self._m-1)**(-0.5)]*(self._m-1)])}
        self.__default_eye = default_eye

        # 基本的にm行m-1列
        # 「。」はm行n列
        # 「°」は1行m-1列

    def __setitem__(self, キー, 値):
        if type(キー) == 単語 and type(値) in (np.ndarray, str):
            if キー in (EOS, BOS):
                if キー == EOS and 値 == "eye":
                    self._辞書[キー] = np.eye(self._m, self._n)
                else:
                    raise 単語行列エラー("EOSやBOSは再代入不可能です。例外としてEOSは文字列\"eye\"のみ再代入可能です")
            if type(値) == str:
                if 値 == "eye":
                    self._辞書[キー] = np.eye(self._m, self._m-1)
                else:
                    raise 単語行列エラー("値は文字列\"eye\"またはnumpyによる適切な形状の行列である必要があります") 
            else:
                if 値.shape != (self._m,self._m-1) or 値.ndim != 2:
                    raise 単語行列エラー("値の形状が異常です")
                self._辞書[キー] = 値
        else: raise 単語行列エラー("適切な代入ではありません。キーが単語でない、あるいは値が行列(2次元数値ndarray)でも文字列\"eye\"でもないようです")

    def __getitem__(self, キー):
        try:
            return np.array(self._辞書[キー])
        except KeyError as e:
            if self.__default_eye and type(キー) == 単語:
                self[キー] = "eye"
                return self[キー]
            else:
                raise e

    def __len__(self):
        return len(self._辞書)

    def __delitem__(self, キー):
        del self._辞書[キー]
    
    def __str__(self):
        return str(self._辞書)

    def __repr__(self):
        return repr(self._辞書)

    def 更新する(self, キー, 差分, 学習率=None):
        学習率 = 学習率 or self._学習率
        if キー == BOS:
            raise 単語行列エラー("BOSは更新不能です")
        if type(差分) != np.ndarray:
            raise 単語行列エラー("差分の型が異常です")
        if 差分.shape != self._辞書[キー].shape:
            raise 単語行列エラー("差分の形状が異常です")
        try:
            self._辞書[キー] -= 学習率 * 差分
        except KeyError:
            self._辞書[キー] = np.eye(m, m-1) - 学習率 * 差分

    

    
                  
