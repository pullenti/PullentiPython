# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import math
from pullenti.unisharp.Utils import Utils


class MeasureHelper:
    
    @staticmethod
    def try_parse_double(val : str, f : float) -> bool:
        f.value = (0)
        if (Utils.isNullOrEmpty(val)): 
            return False
        inoutres1507 = Utils.tryParseFloat(val.replace(',', '.'), f)
        if (val.find(',') >= 0 and inoutres1507): 
            return True
        inoutres1506 = Utils.tryParseFloat(val, f)
        if (inoutres1506): 
            return True
        return False
    
    @staticmethod
    def double_to_string(d : float) -> str:
        from pullenti.ner.core.NumberExToken import NumberExToken
        return NumberExToken.convert_to_string(d)
    
    @staticmethod
    def is_mult_char(t : 'Token') -> bool:
        from pullenti.ner.TextToken import TextToken
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is None): 
            return False
        if (tt.length_char == 1): 
            if (tt.is_char_of("*xXхХ·×◦∙•")): 
                return True
        return False
    
    # static constructor for class MeasureHelper
    @staticmethod
    def _static_ctor(): pass

MeasureHelper._static_ctor()