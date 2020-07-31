﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.instrument.internal.InstrumentParticipantMeta import InstrumentParticipantMeta

class InstrumentParticipant(Referent):
    """ Участник НПА (для договора: продавец, агент, исполнитель и т.п.) """
    
    def __init__(self) -> None:
        super().__init__(InstrumentParticipant.OBJ_TYPENAME)
        self.instance_of = InstrumentParticipantMeta.GLOBAL_META
    
    OBJ_TYPENAME = "INSTRPARTICIPANT"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_REF = "REF"
    
    ATTR_DELEGATE = "DELEGATE"
    
    ATTR_GROUND = "GROUND"
    
    @property
    def typ(self) -> str:
        """ Тип участника """
        return self.get_string_value(InstrumentParticipant.ATTR_TYPE)
    @typ.setter
    def typ(self, value) -> str:
        self.add_slot(InstrumentParticipant.ATTR_TYPE, (None if value is None else value.upper()), True, 0)
        return value
    
    @property
    def ground(self) -> object:
        """ Основание """
        return self.get_slot_value(InstrumentParticipant.ATTR_GROUND)
    @ground.setter
    def ground(self, value) -> object:
        self.add_slot(InstrumentParticipant.ATTR_GROUND, value, False, 0)
        return value
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        print(MiscHelper.convert_first_char_upper_and_other_lower(Utils.ifNotNull(self.typ, "?")), end="", file=res)
        org0_ = Utils.asObjectOrNull(self.get_slot_value(InstrumentParticipant.ATTR_REF), Referent)
        del0_ = Utils.asObjectOrNull(self.get_slot_value(InstrumentParticipant.ATTR_DELEGATE), Referent)
        if (org0_ is not None): 
            print(": {0}".format(org0_.to_string(short_variant, lang, 0)), end="", file=res, flush=True)
            if (not short_variant and del0_ is not None): 
                print(" (в лице {0})".format(del0_.to_string(True, lang, lev + 1)), end="", file=res, flush=True)
        elif (del0_ is not None): 
            print(": в лице {0}".format(del0_.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        p = Utils.asObjectOrNull(obj, InstrumentParticipant)
        if (p is None): 
            return False
        if (self.typ != p.typ): 
            return False
        re1 = Utils.asObjectOrNull(self.get_slot_value(InstrumentParticipant.ATTR_REF), Referent)
        re2 = Utils.asObjectOrNull(obj.get_slot_value(InstrumentParticipant.ATTR_REF), Referent)
        if (re1 is not None and re2 is not None): 
            if (not re1.can_be_equals(re2, typ_)): 
                return False
        return True
    
    def _contains_ref(self, r : 'Referent') -> bool:
        for s in self.slots: 
            if (((s.type_name == InstrumentParticipant.ATTR_REF or s.type_name == InstrumentParticipant.ATTR_DELEGATE)) and (isinstance(s.value, Referent))): 
                if (r == s.value or r.can_be_equals(Utils.asObjectOrNull(s.value, Referent), Referent.EqualType.WITHINONETEXT)): 
                    return True
        return False
    
    @staticmethod
    def _new1492(_arg1 : str) -> 'InstrumentParticipant':
        res = InstrumentParticipant()
        res.typ = _arg1
        return res