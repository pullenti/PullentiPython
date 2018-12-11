# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NumberExToken import NumberExToken

class MeasureHelper:
    
    @staticmethod
    def tryParseDouble(val : str, f : float) -> bool:
        f.value = (0)
        if (Utils.isNullOrEmpty(val)): 
            return False
        inoutres1518 = Utils.tryParseFloat(val.replace(',', '.'), f)
        if (val.find(',') >= 0 and inoutres1518): 
            return True
        inoutres1517 = Utils.tryParseFloat(val, f)
        if (inoutres1517): 
            return True
        return False
    
    @staticmethod
    def doubleToString(d : float) -> str:
        return NumberExToken.convertToString(d)
    
    @staticmethod
    def isMultChar(t : 'Token') -> bool:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        if (tt.length_char == 1): 
            if (tt.isCharOf("*xXхХ·×◦∙•")): 
                return True
        return False
    
    @staticmethod
    def isMultCharEnd(t : 'Token') -> bool:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        term = tt.term
        if (term.endswith("X") or term.endswith("Х")): 
            return True
        return False