# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.Referent import Referent
from pullenti.ner.measure.internal.MeasureHelper import MeasureHelper


class MeasureReferent(Referent):
    """ Величина или диапазон величин, измеряемая в некоторых единицах """
    
    def __init__(self) -> None:
        from pullenti.ner.measure.internal.MeasureMeta import MeasureMeta
        super().__init__(MeasureReferent.OBJ_TYPENAME)
        self.instance_of = MeasureMeta.GLOBAL_META
    
    OBJ_TYPENAME = "MEASURE"
    
    ATTR_TEMPLATE = "TEMPLATE"
    
    ATTR_VALUE = "VALUE"
    
    ATTR_UNIT = "UNIT"
    
    ATTR_REF = "REF"
    
    ATTR_NAME = "NAME"
    
    @property
    def template(self) -> str:
        """ Шаблон для значений, например, [1..2], 1x2, 1 ]..1] """
        return Utils.ifNotNull(self.get_string_value(MeasureReferent.ATTR_TEMPLATE), "1")
    
    @template.setter
    def template(self, value) -> str:
        self.add_slot(MeasureReferent.ATTR_TEMPLATE, value, True, 0)
        return value
    
    @property
    def double_values(self) -> typing.List[float]:
        res = list()
        for s in self.slots: 
            if (s.type_name == MeasureReferent.ATTR_VALUE and (isinstance(s.value, str))): 
                inoutarg1608 = RefOutArgWrapper(0)
                inoutres1609 = MeasureHelper.try_parse_double(s.value if isinstance(s.value, str) else None, inoutarg1608)
                d = inoutarg1608.value
                if (inoutres1609): 
                    res.append(d)
        return res
    
    def add_value(self, d : float) -> None:
        self.add_slot(MeasureReferent.ATTR_VALUE, MeasureHelper.double_to_string(d), False, 0)
    
    @property
    def units(self) -> typing.List['UnitReferent']:
        from pullenti.ner.measure.UnitReferent import UnitReferent
        res = list()
        for s in self.slots: 
            if (s.type_name == MeasureReferent.ATTR_UNIT and (isinstance(s.value, UnitReferent))): 
                res.append(s.value if isinstance(s.value, UnitReferent) else None)
        return res
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.measure.UnitReferent import UnitReferent
        res = Utils.newStringIO(self.template)
        vals = list()
        for s in self.slots: 
            if (s.type_name == MeasureReferent.ATTR_VALUE): 
                if (isinstance(s.value, str)): 
                    vals.append(s.value if isinstance(s.value, str) else None)
                elif (isinstance(s.value, Referent)): 
                    vals.append((s.value if isinstance(s.value, Referent) else None).to_string(True, lang, 0))
        for i in range(res.tell() - 1, -1, -1):
            ch = Utils.getCharAtStringIO(res, i)
            if (not str.isdigit(ch)): 
                continue
            j = ((ord(ch)) - (ord('1')))
            if ((j < 0) or j >= len(vals)): 
                continue
            Utils.removeStringIO(res, i, 1)
            Utils.insertStringIO(res, i, vals[j])
        uu = self.units
        if (len(uu) > 0): 
            print(uu[0].to_string(True, lang, 0), end="", file=res)
            i = 1
            while i < len(uu): 
                pow0_ = uu[i].get_string_value(UnitReferent.ATTR_POW)
                if (not Utils.isNullOrEmpty(pow0_) and pow0_[0] == '-'): 
                    print("/{0}".format(uu[i].to_string(True, lang, 1)), end="", file=res, flush=True)
                    if (pow0_ != "-1"): 
                        print("<{0}>".format(pow0_[1:]), end="", file=res, flush=True)
                else: 
                    print("*{0}".format(uu[i].to_string(True, lang, 0)), end="", file=res, flush=True)
                i += 1
        if (not short_variant): 
            nam = self.get_string_value(MeasureReferent.ATTR_NAME)
            if (nam is not None): 
                print(" - {0}".format(nam), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == MeasureReferent.ATTR_REF and (isinstance(s.value, MeasureReferent))): 
                    print(" / {0}".format((s.value if isinstance(s.value, MeasureReferent) else None).to_string(True, lang, 0)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        mr = (obj if isinstance(obj, MeasureReferent) else None)
        if (mr is None): 
            return False
        if (self.template != mr.template): 
            return False
        vals1 = self.get_string_values(MeasureReferent.ATTR_VALUE)
        vals2 = mr.get_string_values(MeasureReferent.ATTR_VALUE)
        if (len(vals1) != len(vals2)): 
            return False
        i = 0
        while i < len(vals2): 
            if (vals1[i] != vals2[i]): 
                return False
            i += 1
        units1 = self.units
        units2 = mr.units
        if (len(units1) != len(units2)): 
            return False
        i = 0
        while i < len(units2): 
            if (units1[i] != units2[i]): 
                return False
            i += 1
        for s in self.slots: 
            if (s.type_name == MeasureReferent.ATTR_REF or s.type_name == MeasureReferent.ATTR_NAME): 
                if (mr.find_slot(s.type_name, s.value, True) is None): 
                    return False
        for s in mr.slots: 
            if (s.type_name == MeasureReferent.ATTR_REF or s.type_name == MeasureReferent.ATTR_NAME): 
                if (self.find_slot(s.type_name, s.value, True) is None): 
                    return False
        return True