# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import io
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.business.BusinessFactKind import BusinessFactKind



class BusinessFactReferent(Referent):
    """ Представление бизнес-факта """
    
    def __init__(self) -> None:
        from pullenti.ner.business.internal.MetaBusinessFact import MetaBusinessFact
        super().__init__(BusinessFactReferent.OBJ_TYPENAME)
        self.instance_of = MetaBusinessFact.GLOBAL_META
    
    OBJ_TYPENAME = "BUSINESSFACT"
    
    ATTR_KIND = "KIND"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_WHO = "WHO"
    
    ATTR_WHOM = "WHOM"
    
    ATTR_WHEN = "WHEN"
    
    ATTR_WHAT = "WHAT"
    
    ATTR_MISC = "MISC"
    
    @property
    def kind(self) -> 'BusinessFactKind':
        """ Классификатор бизнес-факта """
        s = self.get_string_value(BusinessFactReferent.ATTR_KIND)
        if (s is None): 
            return BusinessFactKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, BusinessFactKind)
            if (isinstance(res, BusinessFactKind)): 
                return Utils.valToEnum(res, BusinessFactKind)
        except Exception as ex448: 
            pass
        return BusinessFactKind.UNDEFINED
    
    @kind.setter
    def kind(self, value) -> 'BusinessFactKind':
        if (value != BusinessFactKind.UNDEFINED): 
            self.add_slot(BusinessFactReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def typ(self) -> str:
        """ Краткое описание факта """
        from pullenti.ner.business.internal.MetaBusinessFact import MetaBusinessFact
        from pullenti.morph.MorphLang import MorphLang
        typ_ = self.get_string_value(BusinessFactReferent.ATTR_TYPE)
        if (typ_ is not None): 
            return typ_
        kind_ = self.get_string_value(BusinessFactReferent.ATTR_KIND)
        if (kind_ is not None): 
            typ_ = (MetaBusinessFact.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(kind_, MorphLang()) if isinstance(MetaBusinessFact.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(kind_, MorphLang()), str) else None)
        if (typ_ is not None): 
            return typ_.lower()
        return None
    
    @typ.setter
    def typ(self, value) -> str:
        self.add_slot(BusinessFactReferent.ATTR_TYPE, value, True, 0)
        return value
    
    @property
    def who(self) -> 'Referent':
        """ Кто (действительный залог) """
        return (self.get_value(BusinessFactReferent.ATTR_WHO) if isinstance(self.get_value(BusinessFactReferent.ATTR_WHO), Referent) else None)
    
    @who.setter
    def who(self, value) -> 'Referent':
        self.add_slot(BusinessFactReferent.ATTR_WHO, value, True, 0)
        return value
    
    @property
    def who2(self) -> 'Referent':
        """ Второй "Кто" (действительный залог) """
        i = 2
        for s in self.slots: 
            if (s.type_name == BusinessFactReferent.ATTR_WHO): 
                i -= 1
                if ((i) == 0): 
                    return (s.value if isinstance(s.value, Referent) else None)
        return None
    
    @who2.setter
    def who2(self, value) -> 'Referent':
        self.add_slot(BusinessFactReferent.ATTR_WHO, value, False, 0)
        return value
    
    @property
    def whom(self) -> 'Referent':
        """ Кого (страдательный залог) """
        return (self.get_value(BusinessFactReferent.ATTR_WHOM) if isinstance(self.get_value(BusinessFactReferent.ATTR_WHOM), Referent) else None)
    
    @whom.setter
    def whom(self, value) -> 'Referent':
        self.add_slot(BusinessFactReferent.ATTR_WHOM, value, True, 0)
        return value
    
    @property
    def when(self) -> 'Referent':
        """ Когда (DateReferent или DateRangeReferent) """
        return (self.get_value(BusinessFactReferent.ATTR_WHEN) if isinstance(self.get_value(BusinessFactReferent.ATTR_WHEN), Referent) else None)
    
    @when.setter
    def when(self, value) -> 'Referent':
        self.add_slot(BusinessFactReferent.ATTR_WHEN, value, True, 0)
        return value
    
    @property
    def whats(self) -> typing.List['Referent']:
        """ Что (артефакты события) """
        res = list()
        for s in self.slots: 
            if (s.type_name == BusinessFactReferent.ATTR_WHAT and isinstance(s.value, Referent)): 
                res.append(s.value if isinstance(s.value, Referent) else None)
        return res
    
    def _add_what(self, w : object) -> None:
        if (isinstance(w, Referent)): 
            self.add_slot(BusinessFactReferent.ATTR_WHAT, w, False, 0)
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = Utils.newStringIO(None)
        typ_ = Utils.ifNotNull(self.typ, "Бизнес-факт")
        print(MiscHelper.convert_first_char_upper_and_other_lower(typ_), end="", file=res)
        v = self.get_value(BusinessFactReferent.ATTR_WHO)
        if (isinstance((v), Referent)): 
            print("; Кто: {0}".format((v if isinstance(v, Referent) else None).to_string(True, lang, 0)), end="", file=res, flush=True)
            if (self.who2 is not None): 
                print(" и {0}".format(self.who2.to_string(True, lang, 0)), end="", file=res, flush=True)
        v = self.get_value(BusinessFactReferent.ATTR_WHOM)
        if (isinstance((v), Referent)): 
            print("; Кого: {0}".format((v if isinstance(v, Referent) else None).to_string(True, lang, 0)), end="", file=res, flush=True)
        if (not short_variant): 
            v = self.get_value(BusinessFactReferent.ATTR_WHAT)
            if ((v) is not None): 
                print("; Что: {0}".format(v), end="", file=res, flush=True)
            v = self.get_value(BusinessFactReferent.ATTR_WHEN)
            if (isinstance((v), Referent)): 
                print("; Когда: {0}".format((v if isinstance(v, Referent) else None).to_string(short_variant, lang, 0)), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == BusinessFactReferent.ATTR_MISC): 
                    print("; {0}".format(s.value), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        br = (obj if isinstance(obj, BusinessFactReferent) else None)
        if (br is None): 
            return False
        if (br.kind != self.kind): 
            return False
        if (br.typ != self.typ): 
            return False
        if (br.who != self.who or br.whom != self.whom): 
            return False
        if (self.when is not None and br.when is not None): 
            if (not self.when.can_be_equals(br.when, Referent.EqualType.WITHINONETEXT)): 
                return False
        mi1 = (self.get_value(BusinessFactReferent.ATTR_WHAT) if isinstance(self.get_value(BusinessFactReferent.ATTR_WHAT), Referent) else None)
        mi2 = (br.get_value(BusinessFactReferent.ATTR_WHAT) if isinstance(br.get_value(BusinessFactReferent.ATTR_WHAT), Referent) else None)
        if (mi1 is not None and mi2 is not None): 
            if (not mi1.can_be_equals(mi2, Referent.EqualType.WITHINONETEXT)): 
                return False
        return True

    
    @staticmethod
    def _new436(_arg1 : 'BusinessFactKind') -> 'BusinessFactReferent':
        res = BusinessFactReferent()
        res.kind = _arg1
        return res
    
    @staticmethod
    def _new447(_arg1 : 'BusinessFactKind', _arg2 : str) -> 'BusinessFactReferent':
        res = BusinessFactReferent()
        res.kind = _arg1
        res.typ = _arg2
        return res