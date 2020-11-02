# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.utils.QuestionType import QuestionType
from pullenti.semantic.internal.NextModelItem import NextModelItem

class ControlModelOld:
    
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
        wrapcas02906 = RefOutArgWrapper(None)
        inoutres2907 = Utils.tryGetValue(self.nexts, Utils.ifNotNull(prep, ""), wrapcas02906)
        cas0 = wrapcas02906.value
        if (not inoutres2907): 
            return False
        return not ((cas0) & cas).is_undefined
    
    def _deserialize(self, str0_ : 'ByteArrayWrapper', pos : int) -> None:
        b = str0_.deserialize_byte(pos)
        self.transitive = b != (0)
        sh = str0_.deserialize_short(pos)
        self.questions = (Utils.valToEnum(sh, QuestionType))
        sh = str0_.deserialize_short(pos)
        if (sh != 0): 
            pr = str0_.deserialize_string(pos)
            cas = MorphCase()
            cas.value = (sh)
            self.agent = NextModelItem(pr, cas)
        sh = str0_.deserialize_short(pos)
        if (sh != 0): 
            pr = str0_.deserialize_string(pos)
            cas = MorphCase()
            cas.value = (sh)
            self.pacient = NextModelItem(pr, cas)
        sh = str0_.deserialize_short(pos)
        if (sh != 0): 
            pr = str0_.deserialize_string(pos)
            cas = MorphCase()
            cas.value = (sh)
            self.instrument = NextModelItem(pr, cas)
        cou = str0_.deserialize_short(pos)
        while cou > 0: 
            pref = str0_.deserialize_string(pos)
            if (pref is None): 
                pref = ""
            cas = MorphCase()
            sh = str0_.deserialize_short(pos)
            cas.value = (sh)
            if (self.nexts is None): 
                self.nexts = dict()
            self.nexts[pref] = cas
            cou -= 1