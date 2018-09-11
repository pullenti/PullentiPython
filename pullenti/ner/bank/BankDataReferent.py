# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent


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
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.uri.UriReferent import UriReferent
        res = io.StringIO()
        for s in self.slots: 
            if (isinstance(s.value, UriReferent)): 
                if ((s.value if isinstance(s.value, UriReferent) else None).scheme == "Р/С"): 
                    print(str(s.value), end="", file=res)
                    break
        if (res.tell() == 0): 
            print(Utils.ifNotNull(self.get_string_value(BankDataReferent.ATTR_ITEM), "?"), end="", file=res)
        if (self.parent_referent is not None and not short_variant and (lev < 20)): 
            print(", {0}".format(self.parent_referent.to_string(True, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return (self.get_value(BankDataReferent.ATTR_BANK) if isinstance(self.get_value(BankDataReferent.ATTR_BANK), Referent) else None)
    
    def find_value(self, schema : str) -> str:
        from pullenti.ner.uri.UriReferent import UriReferent
        for s in self.slots: 
            if (isinstance(s.value, UriReferent)): 
                ur = (s.value if isinstance(s.value, UriReferent) else None)
                if (ur.scheme == schema): 
                    return ur.value
        return None
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        from pullenti.ner.uri.UriReferent import UriReferent
        bd = (obj if isinstance(obj, BankDataReferent) else None)
        if (bd is None): 
            return False
        for s in self.slots: 
            if (s.type_name == BankDataReferent.ATTR_ITEM): 
                ur = (s.value if isinstance(s.value, UriReferent) else None)
                val = bd.find_value(ur.scheme)
                if (val is not None): 
                    if (val != ur.value): 
                        return False
            elif (s.type_name == BankDataReferent.ATTR_BANK): 
                b1 = (s.value if isinstance(s.value, Referent) else None)
                b2 = (bd.get_value(BankDataReferent.ATTR_BANK) if isinstance(bd.get_value(BankDataReferent.ATTR_BANK), Referent) else None)
                if (b2 is not None): 
                    if (b1 != b2 and not b1.can_be_equals(b2, Referent.EqualType.WITHINONETEXT)): 
                        return False
        return True