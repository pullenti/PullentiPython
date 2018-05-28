﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.decree.DecreeChangeValueKind import DecreeChangeValueKind



class DecreeChangeValueReferent(Referent):
    """ Значение изменения СЭ НПА """
    
    def __init__(self) -> None:
        from pullenti.ner.decree.internal.MetaDecreeChangeValue import MetaDecreeChangeValue
        super().__init__(DecreeChangeValueReferent.OBJ_TYPENAME)
        self.instance_of = MetaDecreeChangeValue.GLOBAL_META
    
    OBJ_TYPENAME = "DECREECHANGEVALUE"
    
    ATTR_KIND = "KIND"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_NEWITEM = "NEWITEM"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.internal.MetaDecreeChangeValue import MetaDecreeChangeValue
        res = Utils.newStringIO(None)
        nws = self.new_items
        if (len(nws) > 0): 
            for p in nws: 
                dpr = DecreePartReferent()
                ii = p.find(' ')
                if (ii < 0): 
                    dpr.add_slot(p, "", False, 0)
                else: 
                    dpr.add_slot(p[0 : (ii)], p[ii + 1 : ], False, 0)
                print(" новый '{0}'".format(dpr.to_string(True, MorphLang(), 0)), end="", file=res, flush=True)
        if (self.kind != DecreeChangeValueKind.UNDEFINED): 
            print(" {0}".format(str(MetaDecreeChangeValue.KIND_FEATURE.convert_inner_value_to_outer_value(self.kind, lang)).lower()), end="", file=res, flush=True)
        if (self.number is not None): 
            print(" {0}".format(self.number), end="", file=res, flush=True)
        val = self.value
        if (val is not None): 
            if (len(val) > 100): 
                val = (val[0 : 100] + "...")
            print(" '{0}'".format(val), end="", file=res, flush=True)
            Utils.replaceStringIO(res, '\n', ' ')
            Utils.replaceStringIO(res, '\r', ' ')
        return Utils.toStringStringIO(res).strip()
    
    @property
    def kind(self) -> 'DecreeChangeValueKind':
        """ Тип значение """
        s = self.get_string_value(DecreeChangeValueReferent.ATTR_KIND)
        if (s is None): 
            return DecreeChangeValueKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, DecreeChangeValueKind)
            if (isinstance(res, DecreeChangeValueKind)): 
                return Utils.valToEnum(res, DecreeChangeValueKind)
        except Exception as ex1037: 
            pass
        return DecreeChangeValueKind.UNDEFINED
    
    @kind.setter
    def kind(self, value_) -> 'DecreeChangeValueKind':
        if (value_ != DecreeChangeValueKind.UNDEFINED): 
            self.add_slot(DecreeChangeValueReferent.ATTR_KIND, Utils.enumToString(value_), True, 0)
        return value_
    
    @property
    def value(self) -> str:
        """ Значение """
        return self.get_string_value(DecreeChangeValueReferent.ATTR_VALUE)
    
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(DecreeChangeValueReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def number(self) -> str:
        """ Номер (для предложений и сносок) """
        return self.get_string_value(DecreeChangeValueReferent.ATTR_NUMBER)
    
    @number.setter
    def number(self, value_) -> str:
        self.add_slot(DecreeChangeValueReferent.ATTR_NUMBER, value_, True, 0)
        return value_
    
    @property
    def new_items(self) -> typing.List[str]:
        """ Новые структурные элементы, которые добавляются этим значением 
         (дополнить ... статьями 10.1 и 10.2 следующего содержания) """
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeChangeValueReferent.ATTR_NEWITEM and isinstance(s.value, str)): 
                res.append(s.value if isinstance(s.value, str) else None)
        return res
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        return obj == self

    
    @staticmethod
    def _new751(_arg1 : 'DecreeChangeValueKind') -> 'DecreeChangeValueReferent':
        res = DecreeChangeValueReferent()
        res.kind = _arg1
        return res