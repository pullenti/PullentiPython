# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.instrument.internal.InstrumentArtefactMeta import InstrumentArtefactMeta

class InstrumentArtefact(Referent):
    """ Участник НПА (для договора: продавец, агент, исполнитель и т.п.) """
    
    def __init__(self) -> None:
        super().__init__(InstrumentArtefact.OBJ_TYPENAME)
        self.instance_of = InstrumentArtefactMeta.GLOBAL_META
    
    OBJ_TYPENAME = "INSTRARTEFACT"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_REF = "REF"
    
    @property
    def typ(self) -> str:
        return self.get_string_value(InstrumentArtefact.ATTR_TYPE)
    @typ.setter
    def typ(self, value_) -> str:
        self.add_slot(InstrumentArtefact.ATTR_TYPE, (None if value_ is None else value_.upper()), True, 0)
        return value_
    
    @property
    def value(self) -> object:
        return self.get_slot_value(InstrumentArtefact.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> object:
        self.add_slot(InstrumentArtefact.ATTR_VALUE, value_, False, 0)
        return value_
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        print(MiscHelper.convert_first_char_upper_and_other_lower(Utils.ifNotNull(self.typ, "?")), end="", file=res)
        val = self.value
        if (val is not None): 
            print(": {0}".format(val), end="", file=res, flush=True)
        if (not short_variant and (lev < 30)): 
            re = Utils.asObjectOrNull(self.get_slot_value(InstrumentArtefact.ATTR_REF), Referent)
            if (re is not None): 
                print(" ({0})".format(re.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        p = Utils.asObjectOrNull(obj, InstrumentArtefact)
        if (p is None): 
            return False
        if (self.typ != p.typ): 
            return False
        if (self.value != p.value): 
            return False
        return True
    
    @staticmethod
    def _new1506(_arg1 : str) -> 'InstrumentArtefact':
        res = InstrumentArtefact()
        res.typ = _arg1
        return res