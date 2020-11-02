# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.instrument.internal.InstrumentParticipantMeta import InstrumentParticipantMeta

class InstrumentParticipantReferent(Referent):
    """ Участник НПА (для договора: продавец, агент, исполнитель и т.п.) """
    
    def __init__(self) -> None:
        super().__init__(InstrumentParticipantReferent.OBJ_TYPENAME)
        self.instance_of = InstrumentParticipantMeta.GLOBAL_META
    
    OBJ_TYPENAME = "INSTRPARTICIPANT"
    """ Имя типа сущности TypeName ("INSTRPARTICIPANT") """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип участника (например, продавец, арендатор, ответчик...) """
    
    ATTR_REF = "REF"
    """ Имя атрибута - ссылка на сущность (PersonReferent или OrganizationReferent) """
    
    ATTR_DELEGATE = "DELEGATE"
    """ Имя атрибута - представитель участника (PersonReferent) """
    
    ATTR_GROUND = "GROUND"
    """ Имя атрибута - основание (на основании чего действует) """
    
    @property
    def typ(self) -> str:
        """ Тип участника """
        return self.get_string_value(InstrumentParticipantReferent.ATTR_TYPE)
    @typ.setter
    def typ(self, value) -> str:
        self.add_slot(InstrumentParticipantReferent.ATTR_TYPE, (None if value is None else value.upper()), True, 0)
        return value
    
    @property
    def ground(self) -> object:
        """ Основание """
        return self.get_slot_value(InstrumentParticipantReferent.ATTR_GROUND)
    @ground.setter
    def ground(self, value) -> object:
        self.add_slot(InstrumentParticipantReferent.ATTR_GROUND, value, False, 0)
        return value
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        print(MiscHelper.convert_first_char_upper_and_other_lower(Utils.ifNotNull(self.typ, "?")), end="", file=res)
        org0_ = Utils.asObjectOrNull(self.get_slot_value(InstrumentParticipantReferent.ATTR_REF), Referent)
        del0_ = Utils.asObjectOrNull(self.get_slot_value(InstrumentParticipantReferent.ATTR_DELEGATE), Referent)
        if (org0_ is not None): 
            print(": {0}".format(org0_.to_string(short_variant, lang, 0)), end="", file=res, flush=True)
            if (not short_variant and del0_ is not None): 
                print(" (в лице {0})".format(del0_.to_string(True, lang, lev + 1)), end="", file=res, flush=True)
        elif (del0_ is not None): 
            print(": в лице {0}".format(del0_.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        p = Utils.asObjectOrNull(obj, InstrumentParticipantReferent)
        if (p is None): 
            return False
        if (self.typ != p.typ): 
            return False
        re1 = Utils.asObjectOrNull(self.get_slot_value(InstrumentParticipantReferent.ATTR_REF), Referent)
        re2 = Utils.asObjectOrNull(obj.get_slot_value(InstrumentParticipantReferent.ATTR_REF), Referent)
        if (re1 is not None and re2 is not None): 
            if (not re1.can_be_equals(re2, typ_)): 
                return False
        return True
    
    def _contains_ref(self, r : 'Referent') -> bool:
        for s in self.slots: 
            if (((s.type_name == InstrumentParticipantReferent.ATTR_REF or s.type_name == InstrumentParticipantReferent.ATTR_DELEGATE)) and (isinstance(s.value, Referent))): 
                if (r == s.value or r.can_be_equals(Utils.asObjectOrNull(s.value, Referent), ReferentsEqualType.WITHINONETEXT)): 
                    return True
        return False
    
    @staticmethod
    def _new1479(_arg1 : str) -> 'InstrumentParticipantReferent':
        res = InstrumentParticipantReferent()
        res.typ = _arg1
        return res