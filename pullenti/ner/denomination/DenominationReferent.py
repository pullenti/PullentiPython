# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.Referent import Referent
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.IntOntologyItem import IntOntologyItem


class DenominationReferent(Referent):
    """ Сущность, моделирующая непонятные комбинации (например, Си++, СС-300) """
    
    def __init__(self) -> None:
        from pullenti.ner.denomination.internal.MetaDenom import MetaDenom
        super().__init__(DenominationReferent.OBJ_TYPENAME)
        self.__m_names = None;
        self.instance_of = MetaDenom._global_meta
    
    OBJ_TYPENAME = "DENOMINATION"
    
    ATTR_VALUE = "VALUE"
    
    @property
    def value(self) -> str:
        """ Значение (одно или несколько) """
        return self.getStringValue(DenominationReferent.ATTR_VALUE)
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        return Utils.ifNotNull(self.value, "?")
    
    def _addValue(self, begin : 'Token', end : 'Token') -> None:
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        tmp = io.StringIO()
        t = begin
        first_pass2902 = True
        while True:
            if first_pass2902: first_pass2902 = False
            else: t = t.next0_
            if (not (t is not None and t.previous != end)): break
            if (isinstance(t, NumberToken)): 
                print(t.getSourceText(), end="", file=tmp)
                continue
            if (isinstance(t, TextToken)): 
                s = (Utils.asObjectOrNull(t, TextToken)).term
                if (t.isCharOf("-\\/")): 
                    s = "-"
                print(s, end="", file=tmp)
        i = 0
        while i < tmp.tell(): 
            if (Utils.getCharAtStringIO(tmp, i) == '-' and i > 0 and ((i + 1) < tmp.tell())): 
                ch0 = Utils.getCharAtStringIO(tmp, i - 1)
                ch1 = Utils.getCharAtStringIO(tmp, i + 1)
                if (str.isalnum(ch0) and str.isalnum(ch1)): 
                    if (str.isdigit(ch0) and not str.isdigit(ch1)): 
                        Utils.removeStringIO(tmp, i, 1)
                    elif (not str.isdigit(ch0) and str.isdigit(ch1)): 
                        Utils.removeStringIO(tmp, i, 1)
            i += 1
        self.addSlot(DenominationReferent.ATTR_VALUE, Utils.toStringStringIO(tmp), False, 0)
        self.__m_names = (None)
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        dr = Utils.asObjectOrNull(obj, DenominationReferent)
        if (dr is None): 
            return False
        for n in self.__name_vars: 
            if (n in dr.__name_vars): 
                return True
        return False
    
    @property
    def __name_vars(self) -> typing.List[str]:
        if (self.__m_names is not None): 
            return self.__m_names
        self.__m_names = list()
        nam = self.value
        if (nam is None): 
            return self.__m_names
        self.__m_names.append(nam)
        items = list()
        ty0 = 0
        i0 = 0
        i = 0
        while i <= len(nam): 
            ty = 0
            if (i < len(nam)): 
                if (str.isdigit(nam[i])): 
                    ty = 1
                elif (str.isalpha(nam[i])): 
                    ty = 2
                else: 
                    ty = 3
            if (ty != ty0 or ty == 3): 
                if (i > i0): 
                    vars0_ = list()
                    p = nam[i0:i0+i - i0]
                    DenominationReferent.__addVars(p, vars0_)
                    items.append(vars0_)
                    if (ty == 1 and ty0 == 2): 
                        vars0_ = list()
                        vars0_.append("")
                        vars0_.append("-")
                        items.append(vars0_)
                i0 = i
                ty0 = ty
            i += 1
        inds = Utils.newArray(len(items), 0)
        i = 0
        while i < len(inds): 
            inds[i] = 0
            i += 1
        tmp = io.StringIO()
        while True:
            Utils.setLengthStringIO(tmp, 0)
            i = 0
            while i < len(items): 
                print(items[i][inds[i]], end="", file=tmp)
                i += 1
            v = Utils.toStringStringIO(tmp)
            if (not v in self.__m_names): 
                self.__m_names.append(v)
            if (len(self.__m_names) > 20): 
                break
            for i in range(len(inds) - 1, -1, -1):
                inds[i] += 1
                if (inds[i] < len(items[i])): 
                    break
            else: i = -1
            if (i < 0): 
                break
            i += 1
            while i < len(inds): 
                inds[i] = 0
                i += 1
        return self.__m_names
    
    @staticmethod
    def __addVars(str0_ : str, vars0_ : typing.List[str]) -> None:
        vars0_.append(str0_)
        for k in range(2):
            tmp = io.StringIO()
            i = 0
            while i < len(str0_): 
                wrapv1110 = RefOutArgWrapper(None)
                inoutres1111 = Utils.tryGetValue(DenominationReferent.__m_var_chars, str0_[i], wrapv1110)
                v = wrapv1110.value
                if (not inoutres1111): 
                    break
                if ((len(v) < 2) or v[k] == '-'): 
                    break
                print(v[k], end="", file=tmp)
                i += 1
            if (i >= len(str0_)): 
                v = Utils.toStringStringIO(tmp)
                if (not v in vars0_): 
                    vars0_.append(v)
    
    __m_var_chars = None
    
    def createOntologyItem(self) -> 'IntOntologyItem':
        from pullenti.ner.core.Termin import Termin
        oi = IntOntologyItem(self)
        for v in self.__name_vars: 
            oi.termins.append(Termin(v))
        return oi
    
    # static constructor for class DenominationReferent
    @staticmethod
    def _static_ctor():
        DenominationReferent.__m_var_chars = dict()
        DenominationReferent.__m_var_chars['A'] = "АА"
        DenominationReferent.__m_var_chars['B'] = "БВ"
        DenominationReferent.__m_var_chars['C'] = "ЦС"
        DenominationReferent.__m_var_chars['D'] = "ДД"
        DenominationReferent.__m_var_chars['E'] = "ЕЕ"
        DenominationReferent.__m_var_chars['F'] = "Ф-"
        DenominationReferent.__m_var_chars['G'] = "Г-"
        DenominationReferent.__m_var_chars['H'] = "ХН"
        DenominationReferent.__m_var_chars['I'] = "И-"
        DenominationReferent.__m_var_chars['J'] = "Ж-"
        DenominationReferent.__m_var_chars['K'] = "КК"
        DenominationReferent.__m_var_chars['L'] = "Л-"
        DenominationReferent.__m_var_chars['M'] = "ММ"
        DenominationReferent.__m_var_chars['N'] = "Н-"
        DenominationReferent.__m_var_chars['O'] = "ОО"
        DenominationReferent.__m_var_chars['P'] = "ПР"
        DenominationReferent.__m_var_chars['Q'] = "--"
        DenominationReferent.__m_var_chars['R'] = "Р-"
        DenominationReferent.__m_var_chars['S'] = "С-"
        DenominationReferent.__m_var_chars['T'] = "ТТ"
        DenominationReferent.__m_var_chars['U'] = "У-"
        DenominationReferent.__m_var_chars['V'] = "В-"
        DenominationReferent.__m_var_chars['W'] = "В-"
        DenominationReferent.__m_var_chars['X'] = "ХХ"
        DenominationReferent.__m_var_chars['Y'] = "УУ"
        DenominationReferent.__m_var_chars['Z'] = "З-"
        DenominationReferent.__m_var_chars['А'] = "AA"
        DenominationReferent.__m_var_chars['Б'] = "B-"
        DenominationReferent.__m_var_chars['В'] = "VB"
        DenominationReferent.__m_var_chars['Г'] = "G-"
        DenominationReferent.__m_var_chars['Д'] = "D-"
        DenominationReferent.__m_var_chars['Е'] = "EE"
        DenominationReferent.__m_var_chars['Ж'] = "J-"
        DenominationReferent.__m_var_chars['З'] = "Z-"
        DenominationReferent.__m_var_chars['И'] = "I-"
        DenominationReferent.__m_var_chars['Й'] = "Y-"
        DenominationReferent.__m_var_chars['К'] = "KK"
        DenominationReferent.__m_var_chars['Л'] = "L-"
        DenominationReferent.__m_var_chars['М'] = "MM"
        DenominationReferent.__m_var_chars['Н'] = "NH"
        DenominationReferent.__m_var_chars['О'] = "OO"
        DenominationReferent.__m_var_chars['П'] = "P-"
        DenominationReferent.__m_var_chars['Р'] = "RP"
        DenominationReferent.__m_var_chars['С'] = "SC"
        DenominationReferent.__m_var_chars['Т'] = "TT"
        DenominationReferent.__m_var_chars['У'] = "UY"
        DenominationReferent.__m_var_chars['Ф'] = "F-"
        DenominationReferent.__m_var_chars['Х'] = "HX"
        DenominationReferent.__m_var_chars['Ц'] = "C-"
        DenominationReferent.__m_var_chars['Ч'] = "--"
        DenominationReferent.__m_var_chars['Ш'] = "--"
        DenominationReferent.__m_var_chars['Щ'] = "--"
        DenominationReferent.__m_var_chars['Ы'] = "--"
        DenominationReferent.__m_var_chars['Э'] = "A-"
        DenominationReferent.__m_var_chars['Ю'] = "U-"
        DenominationReferent.__m_var_chars['Я'] = "--"

DenominationReferent._static_ctor()