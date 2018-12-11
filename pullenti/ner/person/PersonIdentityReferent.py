# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.person.internal.MetaPersonIdentity import MetaPersonIdentity

class PersonIdentityReferent(Referent):
    """ Удостоверение личности (паспорт и пр.) """
    
    def __init__(self) -> None:
        super().__init__(PersonIdentityReferent.OBJ_TYPENAME)
        self.instance_of = MetaPersonIdentity._global_meta
    
    OBJ_TYPENAME = "PERSONIDENTITY"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_DATE = "DATE"
    
    ATTR_ORG = "ORG"
    
    ATTR_STATE = "STATE"
    
    ATTR_ADDRESS = "ADDRESS"
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        print(Utils.ifNotNull(self.typ, "?"), end="", file=res)
        if (self.number is not None): 
            print(" №{0}".format(self.number), end="", file=res, flush=True)
        if (self.state is not None): 
            print(", {0}".format(self.state.toString(True, lang, lev + 1)), end="", file=res, flush=True)
        if (not short_variant): 
            dat = self.getStringValue(PersonIdentityReferent.ATTR_DATE)
            org0_ = self.getStringValue(PersonIdentityReferent.ATTR_ORG)
            if (dat is not None or org0_ is not None): 
                print(", выдан", end="", file=res)
                if (dat is not None): 
                    print(" {0}".format(dat), end="", file=res, flush=True)
                if (org0_ is not None): 
                    print(" {0}".format(org0_), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def typ(self) -> str:
        """ Тип документа """
        return self.getStringValue(PersonIdentityReferent.ATTR_TYPE)
    @typ.setter
    def typ(self, value) -> str:
        self.addSlot(PersonIdentityReferent.ATTR_TYPE, value, True, 0)
        return value
    
    @property
    def number(self) -> str:
        """ Номер (вместе с серией) """
        return self.getStringValue(PersonIdentityReferent.ATTR_NUMBER)
    @number.setter
    def number(self, value) -> str:
        self.addSlot(PersonIdentityReferent.ATTR_NUMBER, value, True, 0)
        return value
    
    @property
    def state(self) -> 'Referent':
        """ Государство """
        return Utils.asObjectOrNull(self.getSlotValue(PersonIdentityReferent.ATTR_STATE), Referent)
    @state.setter
    def state(self, value) -> 'Referent':
        self.addSlot(PersonIdentityReferent.ATTR_STATE, value, True, 0)
        return value
    
    @property
    def address(self) -> 'Referent':
        """ Адрес регистрации """
        return Utils.asObjectOrNull(self.getSlotValue(PersonIdentityReferent.ATTR_ADDRESS), Referent)
    @address.setter
    def address(self, value) -> 'Referent':
        self.addSlot(PersonIdentityReferent.ATTR_ADDRESS, value, True, 0)
        return value
    
    def canBeEquals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        id0_ = Utils.asObjectOrNull(obj, PersonIdentityReferent)
        if (id0_ is None): 
            return False
        if (self.typ != id0_.typ): 
            return False
        if (self.number != id0_.number): 
            return False
        if (self.state is not None and id0_.state is not None): 
            if (self.state != id0_.state): 
                return False
        return True