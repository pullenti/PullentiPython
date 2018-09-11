# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NumberHelper import NumberHelper


class OrgItemNumberToken(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        self.number = None
        super().__init__(begin, end, None)
    
    def __str__(self) -> str:
        return "№ {0}".format(Utils.ifNotNull(self.number, "?"))
    
    @staticmethod
    def try_attach(t : 'Token', can_be_pure_number : bool=False, typ : 'OrgItemTypeToken'=None) -> 'OrgItemNumberToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return None
        tt = (t if isinstance(t, TextToken) else None)
        if (tt is not None): 
            t1 = MiscHelper.check_number_prefix(tt)
            if ((isinstance(t1, NumberToken)) and not t1.is_newline_before): 
                return OrgItemNumberToken._new1698(tt, t1, str((t1 if isinstance(t1, NumberToken) else None).value))
        if ((t.is_hiphen and (isinstance(t.next0_, NumberToken)) and not t.is_whitespace_before) and not t.is_whitespace_after): 
            if (NumberHelper.try_parse_age(t.next0_) is None): 
                return OrgItemNumberToken._new1698(t, t.next0_, str((t.next0_ if isinstance(t.next0_, NumberToken) else None).value))
        if (isinstance(t, NumberToken)): 
            if ((not t.is_whitespace_before and t.previous is not None and t.previous.is_hiphen)): 
                return OrgItemNumberToken._new1698(t, t, str((t if isinstance(t, NumberToken) else None).value))
            if (typ is not None and typ.typ is not None and (((typ.typ == "войсковая часть" or typ.typ == "військова частина" or "колония" in typ.typ) or "колонія" in typ.typ))): 
                if (t.length_char >= 4 or t.length_char <= 6): 
                    res = OrgItemNumberToken._new1698(t, t, str((t if isinstance(t, NumberToken) else None).value))
                    if (t.next0_ is not None and ((t.next0_.is_hiphen or t.next0_.is_char_of("\\/"))) and not t.next0_.is_whitespace_after): 
                        if ((isinstance(t.next0_.next0_, NumberToken)) and ((t.length_char + t.next0_.next0_.length_char) < 9)): 
                            res.end_token = t.next0_.next0_
                            res.number = "{0}-{1}".format(res.number, (res.end_token if isinstance(res.end_token, NumberToken) else None).value)
                        elif ((isinstance(t.next0_.next0_, TextToken)) and t.next0_.next0_.length_char == 1 and t.next0_.next0_.chars.is_letter): 
                            res.end_token = t.next0_.next0_
                            res.number = "{0}{1}".format(res.number, (res.end_token if isinstance(res.end_token, TextToken) else None).term)
                    elif ((isinstance(t.next0_, TextToken)) and t.next0_.length_char == 1 and t.next0_.chars.is_letter): 
                        res.end_token = t.next0_
                        res.number = "{0}{1}".format(res.number, (res.end_token if isinstance(res.end_token, TextToken) else None).term)
                    return res
        if (((isinstance(t, TextToken)) and t.length_char == 1 and t.chars.is_letter) and not t.is_whitespace_after): 
            if (typ is not None and typ.typ is not None and (((typ.typ == "войсковая часть" or typ.typ == "військова частина" or "колония" in typ.typ) or "колонія" in typ.typ))): 
                tt1 = t.next0_
                if (tt1 is not None and tt1.is_hiphen): 
                    tt1 = tt1.next0_
                if ((isinstance(tt1, NumberToken)) and not tt1.is_whitespace_before): 
                    res = OrgItemNumberToken(t, tt1)
                    res.number = "{0}{1}".format((t if isinstance(t, TextToken) else None).term, (tt1 if isinstance(tt1, NumberToken) else None).value)
                    return res
        return None
    
    @staticmethod
    def _new1698(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'OrgItemNumberToken':
        res = OrgItemNumberToken(_arg1, _arg2)
        res.number = _arg3
        return res