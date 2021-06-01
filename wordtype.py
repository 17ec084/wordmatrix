class 単語:
    def __init__(self, 品詞, 品詞細分類1, 品詞細分類2, 品詞細分類3, 活用型, 原形):
        self.__品詞 = 品詞
        self.__品詞細分類1 = 品詞細分類1
        self.__品詞細分類2 = 品詞細分類2
        self.__品詞細分類3 = 品詞細分類3
        self.__活用型 = 活用型
        self.__原形 = 原形

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __hash__(self):
        return sum([hash(v) for v in self.__dict__.values()])

    def __str__(self):
        EOS = 単語("EOS", None, None, None, None, None)
        BOS = 単語("BOS", None, None, None, None, None)
        if self not in (EOS, BOS):
            return 'wordtype.単語(品詞="' + self.__品詞        + '", ' + \
                          '品詞細分類1="' + self.__品詞細分類1 + '", ' + \
                          '品詞細分類2="' + self.__品詞細分類2 + '", ' + \
                          '品詞細分類3="' + self.__品詞細分類3 + '", ' + \
                               '活用型="' + self.__活用型      + '", ' + \
                                 '原形="' + self.__原形        + '")' 
        else:
            return "wordtype.EOS" if self == EOS else "wordtype.BOS" 
    
    def __repr__(self):
        return str(self)

    品詞 = property(fget=lambda self:self.__品詞)
    品詞細分類1 = property(fget=lambda self:self.__品詞細分類1)
    品詞細分類2 = property(fget=lambda self:self.__品詞細分類2)    
    品詞細分類3 = property(fget=lambda self:self.__品詞細分類3)
    活用型 = property(fget=lambda self:self.__活用型)
    原形 = property(fget=lambda self:self.__原形)    

EOS = 単語("EOS", None, None, None, None, None)
BOS = 単語("BOS", None, None, None, None, None)
