# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.core.Termin import Termin
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.goods.GoodAttributeReferent import GoodAttributeReferent
from pullenti.ner.goods.internal.GoodMeta import GoodMeta

class GoodReferent(Referent):
    """ Товар """
    
    def __init__(self) -> None:
        super().__init__(GoodReferent.OBJ_TYPENAME)
        self.instance_of = GoodMeta.GLOBAL_META
    
    OBJ_TYPENAME = "GOOD"
    
    ATTR_ATTR = "ATTR"
    
    @property
    def attrs(self) -> typing.List['GoodAttributeReferent']:
        """ Атрибуты товара """
        res = list()
        for s in self.slots: 
            if (isinstance(s.value, GoodAttributeReferent)): 
                res.append(Utils.asObjectOrNull(s.value, GoodAttributeReferent))
        return res
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        for a in self.attrs: 
            print("{0} ".format(a.to_string(True, lang, lev)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        return self == obj
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        re = IntOntologyItem(self)
        for s in self.slots: 
            if (s.type_name == GoodReferent.ATTR_ATTR): 
                re.termins.append(Termin(str(s.value)))
        return re