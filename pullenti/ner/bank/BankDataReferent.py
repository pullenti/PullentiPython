# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.morph.MorphLang import MorphLang


class BankDataReferent(Referent):
    """ Банковские данные (реквизиты) """
    
    def __init__(self) -> None:
        from pullenti.ner.bank.internal.MetaBank import MetaBank
        super().__init__(BankDataReferent.OBJ_TYPENAME)
        self.instance_of = MetaBank._global_meta
    
    OBJ_TYPENAME = "BANKDATA"
    
    ATTR_ITEM = "ITEM"
    
    ATTR_BANK = "BANK"
    
    ATTR_CORBANK = "CORBANK"
    
    ATTR_MISC = "MISC"
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        from pullenti.ner.uri.UriReferent import UriReferent
        res = io.StringIO()
        for s in self.slots: 
            if (isinstance(s.value, UriReferent)): 
                if ((Utils.asObjectOrNull(s.value, UriReferent)).scheme == "Р/С"): 
                    print(str(s.value), end="", file=res)
                    break
        if (res.tell() == 0): 
            print(Utils.ifNotNull(self.getStringValue(BankDataReferent.ATTR_ITEM), "?"), end="", file=res)
        if (self.parent_referent is not None and not short_variant and (lev < 20)): 
            print(", {0}".format(self.parent_referent.toString(True, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.getSlotValue(BankDataReferent.ATTR_BANK), Referent)
    
    def findValue(self, schema : str) -> str:
        from pullenti.ner.uri.UriReferent import UriReferent
        for s in self.slots: 
            if (isinstance(s.value, UriReferent)): 
                ur = Utils.asObjectOrNull(s.value, UriReferent)
                if (ur.scheme == schema): 
                    return ur.value
        return None
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        from pullenti.ner.uri.UriReferent import UriReferent
        bd = Utils.asObjectOrNull(obj, BankDataReferent)
        if (bd is None): 
            return False
        for s in self.slots: 
            if (s.type_name == BankDataReferent.ATTR_ITEM): 
                ur = Utils.asObjectOrNull(s.value, UriReferent)
                val = bd.findValue(ur.scheme)
                if (val is not None): 
                    if (val != ur.value): 
                        return False
            elif (s.type_name == BankDataReferent.ATTR_BANK): 
                b1 = Utils.asObjectOrNull(s.value, Referent)
                b2 = Utils.asObjectOrNull(bd.getSlotValue(BankDataReferent.ATTR_BANK), Referent)
                if (b2 is not None): 
                    if (b1 != b2 and not b1.canBeEquals(b2, Referent.EqualType.WITHINONETEXT)): 
                        return False
        return True