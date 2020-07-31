# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.utils.QuestionType import QuestionType

class ControlModelOld:
    """ Модель управления группы (всей группы, а не только глаголов)
     СТАРАЯ. Осталась временно, пока не переведём всё на новую """
    
    def __init__(self) -> None:
        self.transitive = False
        self.nexts = None;
        self.questions = QuestionType.UNDEFINED
        self.agent = None;
        self.pacient = None;
        self.instrument = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.transitive): 
            print("Перех.", end="", file=res)
        if (self.agent is not None): 
            print(" Агент:{0}".format(self.agent), end="", file=res, flush=True)
        if (self.pacient is not None): 
            print(" Пациент:{0}".format(self.pacient), end="", file=res, flush=True)
        if (self.instrument is not None): 
            print(" Инстр.:{0}".format(self.instrument), end="", file=res, flush=True)
        if (self.nexts is not None): 
            for kp in self.nexts.items(): 
                print(" [{0} {1}]".format(Utils.ifNotNull(kp[0], ""), kp[1]), end="", file=res, flush=True)
        if ((((self.questions) & (QuestionType.WHERE))) != (QuestionType.UNDEFINED)): 
            print(" ГДЕ?".format(), end="", file=res, flush=True)
        if ((((self.questions) & (QuestionType.WHEREFROM))) != (QuestionType.UNDEFINED)): 
            print(" ОТКУДА?".format(), end="", file=res, flush=True)
        if ((((self.questions) & (QuestionType.WHERETO))) != (QuestionType.UNDEFINED)): 
            print(" КУДА?".format(), end="", file=res, flush=True)
        if ((((self.questions) & (QuestionType.WHEN))) != (QuestionType.UNDEFINED)): 
            print(" КОГДА?".format(), end="", file=res, flush=True)
        if ((((self.questions) & (QuestionType.WHATTODO))) != (QuestionType.UNDEFINED)): 
            print(" ЧТО ДЕЛАТЬ?".format(), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    def check_next(self, prep : str, cas : 'MorphCase') -> bool:
        if (self.nexts is None): 
            return False
        wrapcas02974 = RefOutArgWrapper(None)
        inoutres2975 = Utils.tryGetValue(self.nexts, Utils.ifNotNull(prep, ""), wrapcas02974)
        cas0 = wrapcas02974.value
        if (not inoutres2975): 
            return False
        return not ((cas0) & cas).is_undefined