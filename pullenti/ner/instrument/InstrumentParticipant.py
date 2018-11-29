# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent


class InstrumentParticipant(Referent):
    """ Участник НПА (для договора: продавец, агент, исполнитель и т.п.) """
    
    def __init__(self) -> None:
        from pullenti.ner.instrument.internal.InstrumentParticipantMeta import InstrumentParticipantMeta
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
        return self.getStringValue(InstrumentParticipant.ATTR_TYPE)
    @typ.setter
    def typ(self, value) -> str:
        self.addSlot(InstrumentParticipant.ATTR_TYPE, (None if value is None else value.upper()), True, 0)
        return value
    
    @property
    def ground(self) -> object:
        """ Основание """
        return self.getSlotValue(InstrumentParticipant.ATTR_GROUND)
    @ground.setter
    def ground(self, value) -> object:
        self.addSlot(InstrumentParticipant.ATTR_GROUND, value, False, 0)
        return value
    
    def toString(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = io.StringIO()
        print(MiscHelper.convertFirstCharUpperAndOtherLower(Utils.ifNotNull(self.typ, "?")), end="", file=res)
        org0_ = Utils.asObjectOrNull(self.getSlotValue(InstrumentParticipant.ATTR_REF), Referent)
        del0_ = Utils.asObjectOrNull(self.getSlotValue(InstrumentParticipant.ATTR_DELEGATE), Referent)
        if (org0_ is not None): 
            print(": {0}".format(org0_.toString(short_variant, lang, 0)), end="", file=res, flush=True)
            if (not short_variant and del0_ is not None): 
                print(" (в лице {0})".format(del0_.toString(True, lang, lev + 1)), end="", file=res, flush=True)
        elif (del0_ is not None): 
            print(": в лице {0}".format(del0_.toString(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def canBeEquals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        p = Utils.asObjectOrNull(obj, InstrumentParticipant)
        if (p is None): 
            return False
        if (self.typ != p.typ): 
            return False
        re1 = Utils.asObjectOrNull(self.getSlotValue(InstrumentParticipant.ATTR_REF), Referent)
        re2 = Utils.asObjectOrNull(obj.getSlotValue(InstrumentParticipant.ATTR_REF), Referent)
        if (re1 is not None and re2 is not None): 
            if (not re1.canBeEquals(re2, typ_)): 
                return False
        return True
    
    def _containsRef(self, r : 'Referent') -> bool:
        for s in self.slots: 
            if (((s.type_name == InstrumentParticipant.ATTR_REF or s.type_name == InstrumentParticipant.ATTR_DELEGATE)) and (isinstance(s.value, Referent))): 
                if (r == s.value or r.canBeEquals(Utils.asObjectOrNull(s.value, Referent), Referent.EqualType.WITHINONETEXT)): 
                    return True
        return False
    
    @staticmethod
    def _new1313(_arg1 : str) -> 'InstrumentParticipant':
        res = InstrumentParticipant()
        res.typ = _arg1
        return res