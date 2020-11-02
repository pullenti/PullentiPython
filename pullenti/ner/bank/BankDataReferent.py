# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.bank.internal.MetaBank import MetaBank
from pullenti.ner.uri.UriReferent import UriReferent

class BankDataReferent(Referent):
    """ Банковские данные (реквизиты)
    
    """
    
    def __init__(self) -> None:
        super().__init__(BankDataReferent.OBJ_TYPENAME)
        self.instance_of = MetaBank._global_meta
    
    OBJ_TYPENAME = "BANKDATA"
    """ Имя типа сущности TypeName ("BANKDATA") """
    
    ATTR_ITEM = "ITEM"
    """ Имя атрибута - реквизит (обычно UriReferent) """
    
    ATTR_BANK = "BANK"
    """ Имя атрибута - банк (обычно OrganizationReferent) """
    
    ATTR_CORBANK = "CORBANK"
    """ Имя атрибута - банк К/С """
    
    ATTR_MISC = "MISC"
    """ Имя атрибута - разное """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        for s in self.slots: 
            if (isinstance(s.value, UriReferent)): 
                if (s.value.scheme == "Р/С"): 
                    print(str(s.value), end="", file=res)
                    break
        if (res.tell() == 0): 
            print(Utils.ifNotNull(self.get_string_value(BankDataReferent.ATTR_ITEM), "?"), end="", file=res)
        if (self.parent_referent is not None and not short_variant and (lev < 20)): 
            print(", {0}".format(self.parent_referent.to_string(True, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.get_slot_value(BankDataReferent.ATTR_BANK), Referent)
    
    def find_value(self, schema : str) -> str:
        for s in self.slots: 
            if (isinstance(s.value, UriReferent)): 
                ur = Utils.asObjectOrNull(s.value, UriReferent)
                if (ur.scheme == schema): 
                    return ur.value
        return None
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        bd = Utils.asObjectOrNull(obj, BankDataReferent)
        if (bd is None): 
            return False
        for s in self.slots: 
            if (s.type_name == BankDataReferent.ATTR_ITEM): 
                ur = Utils.asObjectOrNull(s.value, UriReferent)
                val = bd.find_value(ur.scheme)
                if (val is not None): 
                    if (val != ur.value): 
                        return False
            elif (s.type_name == BankDataReferent.ATTR_BANK): 
                b1 = Utils.asObjectOrNull(s.value, Referent)
                b2 = Utils.asObjectOrNull(bd.get_slot_value(BankDataReferent.ATTR_BANK), Referent)
                if (b2 is not None): 
                    if (b1 != b2 and not b1.can_be_equals(b2, ReferentsEqualType.WITHINONETEXT)): 
                        return False
        return True