# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.money.internal.MoneyMeta import MoneyMeta

class MoneyReferent(Referent):
    """ Сущность - денежная сумма
    
    """
    
    def __init__(self) -> None:
        super().__init__(MoneyReferent.OBJ_TYPENAME)
        self.instance_of = MoneyMeta.GLOBAL_META
    
    OBJ_TYPENAME = "MONEY"
    """ Имя типа сущности TypeName ("MONEY") """
    
    ATTR_CURRENCY = "CURRENCY"
    """ Имя атрибута - валюта (3-х значный код ISO 4217) """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение (целая часть) """
    
    ATTR_ALTVALUE = "ALTVALUE"
    """ Имя атрибута - альтернативное значение (когда в скобках ошибочно указано другле число) """
    
    ATTR_REST = "REST"
    """ Имя атрибута - дробная часть ("копейки") """
    
    ATTR_ALTREST = "ALTREST"
    """ Имя атрибута - альтернативная дробная часть (когда в скобках указано другое число) """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        v = self.get_string_value(MoneyReferent.ATTR_VALUE)
        r = self.rest
        if (v is not None or r > 0): 
            print(Utils.ifNotNull(v, "0"), end="", file=res)
            cou = 0
            for i in range(res.tell() - 1, 0, -1):
                cou += 1
                if (cou == 3): 
                    Utils.insertStringIO(res, i, '.')
                    cou = 0
        else: 
            print("?", end="", file=res)
        if (r > 0): 
            print(",{0}".format("{:02d}".format(r)), end="", file=res, flush=True)
        print(" {0}".format(self.currency), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def currency(self) -> str:
        """ Тип валюты (3-х значный код ISO 4217) """
        return self.get_string_value(MoneyReferent.ATTR_CURRENCY)
    @currency.setter
    def currency(self, value_) -> str:
        self.add_slot(MoneyReferent.ATTR_CURRENCY, value_, True, 0)
        return value_
    
    @property
    def value(self) -> float:
        """ Значение целой части """
        val = self.get_string_value(MoneyReferent.ATTR_VALUE)
        if (val is None): 
            return 0
        wrapv1746 = RefOutArgWrapper(0)
        inoutres1747 = Utils.tryParseFloat(val, wrapv1746)
        v = wrapv1746.value
        if (not inoutres1747): 
            return 0
        return v
    
    @property
    def alt_value(self) -> float:
        """ Альтернативное значение (если есть, то значит неправильно написали сумму
        числом и далее прописью в скобках) """
        val = self.get_string_value(MoneyReferent.ATTR_ALTVALUE)
        if (val is None): 
            return None
        wrapv1748 = RefOutArgWrapper(0)
        inoutres1749 = Utils.tryParseFloat(val, wrapv1748)
        v = wrapv1748.value
        if (not inoutres1749): 
            return None
        return v
    
    @property
    def rest(self) -> int:
        """ Остаток (от 0 до 99) - копеек, центов и т.п. """
        val = self.get_string_value(MoneyReferent.ATTR_REST)
        if (val is None): 
            return 0
        wrapv1750 = RefOutArgWrapper(0)
        inoutres1751 = Utils.tryParseInt(val, wrapv1750)
        v = wrapv1750.value
        if (not inoutres1751): 
            return 0
        return v
    
    @property
    def alt_rest(self) -> int:
        """ Альтернативный остаток (от 0 до 99) - копеек, центов и т.п. """
        val = self.get_string_value(MoneyReferent.ATTR_ALTREST)
        if (val is None): 
            return None
        wrapv1752 = RefOutArgWrapper(0)
        inoutres1753 = Utils.tryParseInt(val, wrapv1752)
        v = wrapv1752.value
        if (not inoutres1753): 
            return None
        return v
    
    @property
    def real_value(self) -> float:
        """ Действительное значение (вместе с копейками) """
        return (self.value) + (((self.rest) / (100)))
    @real_value.setter
    def real_value(self, value_) -> float:
        val = NumberHelper.double_to_string(value_)
        ii = val.find('.')
        if (ii > 0): 
            val = val[0:0+ii]
        self.add_slot(MoneyReferent.ATTR_VALUE, val, True, 0)
        re = ((value_ - self.value)) * (100)
        self.add_slot(MoneyReferent.ATTR_REST, str(math.floor((re + 0.0001))), True, 0)
        return value_
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        s = Utils.asObjectOrNull(obj, MoneyReferent)
        if (s is None): 
            return False
        if (s.currency != self.currency): 
            return False
        if (s.value != self.value): 
            return False
        if (s.rest != self.rest): 
            return False
        if (s.alt_value != self.alt_value): 
            return False
        if (s.alt_rest != self.alt_rest): 
            return False
        return True
    
    @staticmethod
    def _new838(_arg1 : str, _arg2 : float) -> 'MoneyReferent':
        res = MoneyReferent()
        res.currency = _arg1
        res.real_value = _arg2
        return res