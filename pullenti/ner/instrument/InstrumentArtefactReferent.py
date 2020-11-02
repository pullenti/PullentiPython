# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.instrument.internal.InstrumentArtefactMeta import InstrumentArtefactMeta

class InstrumentArtefactReferent(Referent):
    """ Для судебных решений формализованная резолюция (пока). """
    
    def __init__(self) -> None:
        super().__init__(InstrumentArtefactReferent.OBJ_TYPENAME)
        self.instance_of = InstrumentArtefactMeta.GLOBAL_META
    
    OBJ_TYPENAME = "INSTRARTEFACT"
    """ Имя типа сущности TypeName ("INSTRARTEFACT") """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип артефакта """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение артефакта """
    
    ATTR_REF = "REF"
    """ Имя атрибута - ссылка на сущность (если есть) """
    
    @property
    def typ(self) -> str:
        """ Тип """
        return self.get_string_value(InstrumentArtefactReferent.ATTR_TYPE)
    @typ.setter
    def typ(self, value_) -> str:
        self.add_slot(InstrumentArtefactReferent.ATTR_TYPE, (None if value_ is None else value_.upper()), True, 0)
        return value_
    
    @property
    def value(self) -> object:
        """ Значение """
        return self.get_slot_value(InstrumentArtefactReferent.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> object:
        self.add_slot(InstrumentArtefactReferent.ATTR_VALUE, value_, False, 0)
        return value_
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        print(MiscHelper.convert_first_char_upper_and_other_lower(Utils.ifNotNull(self.typ, "?")), end="", file=res)
        val = self.value
        if (val is not None): 
            print(": {0}".format(val), end="", file=res, flush=True)
        if (not short_variant and (lev < 30)): 
            re = Utils.asObjectOrNull(self.get_slot_value(InstrumentArtefactReferent.ATTR_REF), Referent)
            if (re is not None): 
                print(" ({0})".format(re.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        p = Utils.asObjectOrNull(obj, InstrumentArtefactReferent)
        if (p is None): 
            return False
        if (self.typ != p.typ): 
            return False
        if (self.value != p.value): 
            return False
        return True
    
    @staticmethod
    def _new1493(_arg1 : str) -> 'InstrumentArtefactReferent':
        res = InstrumentArtefactReferent()
        res.typ = _arg1
        return res