# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.instrument.internal.MetaInstrumentBlock import MetaInstrumentBlock
from pullenti.ner.decree.DecreeReferent import DecreeReferent

class InstrumentBlockReferent(Referent):
    """ Представление фрагмента документа. Фрагменты образуют дерево с вершиной в InstrumentReferent.
    
    """
    
    def __init__(self, typename : str=None) -> None:
        super().__init__(Utils.ifNotNull(typename, InstrumentBlockReferent.OBJ_TYPENAME))
        self.__m_children = None;
        self.instance_of = MetaInstrumentBlock.GLOBAL_META
    
    OBJ_TYPENAME = "INSTRBLOCK"
    """ Имя типа сущности TypeName ("INSTRBLOCK") """
    
    ATTR_KIND = "KIND"
    """ Имя атрибута - тип фрагмента (InstrumentKind) """
    
    ATTR_KIND2 = "KIND_SEC"
    
    ATTR_CHILD = "CHILD"
    """ Имя атрибута - ссылки на дочерние фрагменты (InstrumentBlockReferent) """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение (например, текст) """
    
    ATTR_REF = "REF"
    """ Имя атрибута - ссылка на сущность (если есть) """
    
    ATTR_EXPIRED = "EXPIRED"
    """ Имя атрибута - признак утраты силы """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование фрагмента """
    
    ATTR_NUMBER = "NUMBER"
    """ Имя атрибута - номер фрагмента (для диапазона - максимальный номер) """
    
    ATTR_MINNUMBER = "MINNUMBER"
    """ Имя атрибута - для диапазона - минимальный номер """
    
    ATTR_SUBNUMBER = "ADDNUMBER"
    """ Имя атрибута - подномер """
    
    ATTR_SUB2NUMBER = "ADDSECNUMBER"
    """ Имя атрибута - второй подномер """
    
    ATTR_SUB3NUMBER = "ADDTHIRDNUMBER"
    """ Имя атрибута - третий подномер """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        ki = self.kind
        str0_ = (Utils.asObjectOrNull(MetaInstrumentBlock.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(Utils.enumToString(ki), lang), str))
        if (str0_ is not None): 
            print(str0_, end="", file=res)
            if (self.kind2 != InstrumentKind.UNDEFINED): 
                str0_ = (Utils.asObjectOrNull(MetaInstrumentBlock.GLOBAL_META.kind_feature.convert_inner_value_to_outer_value(Utils.enumToString(self.kind2), lang), str))
                if (str0_ is not None): 
                    print(" ({0})".format(str0_), end="", file=res, flush=True)
        if (self.number > 0): 
            if (ki == InstrumentKind.TABLE): 
                print(" {0} строк, {1} столбцов".format(len(self.children), self.number), end="", file=res, flush=True)
            else: 
                print(" №{0}".format(self.number), end="", file=res, flush=True)
                if (self.sub_number > 0): 
                    print(".{0}".format(self.sub_number), end="", file=res, flush=True)
                    if (self.sub_number2 > 0): 
                        print(".{0}".format(self.sub_number2), end="", file=res, flush=True)
                        if (self.sub_number3 > 0): 
                            print(".{0}".format(self.sub_number3), end="", file=res, flush=True)
                if (self.min_number > 0): 
                    for i in range(res.tell() - 1, -1, -1):
                        if (Utils.getCharAtStringIO(res, i) == ' ' or Utils.getCharAtStringIO(res, i) == '.'): 
                            Utils.insertStringIO(res, i + 1, "{0}-".format(self.min_number))
                            break
        ignore_ref = False
        if (self.is_expired): 
            print(" (утратить силу)", end="", file=res)
            ignore_ref = True
        elif (ki != InstrumentKind.EDITIONS and ki != InstrumentKind.APPROVED and (isinstance(self.ref, DecreeReferent))): 
            print(" (*)", end="", file=res)
            ignore_ref = True
        str0_ = self.get_string_value(InstrumentBlockReferent.ATTR_NAME)
        if ((str0_) is None): 
            str0_ = self.get_string_value(InstrumentBlockReferent.ATTR_VALUE)
        if (str0_ is not None): 
            if (len(str0_) > 100): 
                str0_ = (str0_[0:0+100] + "...")
            print(" \"{0}\"".format(str0_), end="", file=res, flush=True)
        elif (not ignore_ref and (isinstance(self.ref, Referent)) and (lev < 30)): 
            print(" \"{0}\"".format(self.ref.to_string(short_variant, lang, lev + 1)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    @property
    def kind(self) -> 'InstrumentKind':
        """ Тип фрагмента """
        s = self.get_string_value(InstrumentBlockReferent.ATTR_KIND)
        if (s is None): 
            return InstrumentKind.UNDEFINED
        try: 
            if (s == "Part" or s == "Base" or s == "Special"): 
                return InstrumentKind.UNDEFINED
            res = Utils.valToEnum(s, InstrumentKind)
            if (isinstance(res, InstrumentKind)): 
                return Utils.valToEnum(res, InstrumentKind)
        except Exception as ex1578: 
            pass
        return InstrumentKind.UNDEFINED
    @kind.setter
    def kind(self, value_) -> 'InstrumentKind':
        if (value_ != InstrumentKind.UNDEFINED): 
            self.add_slot(InstrumentBlockReferent.ATTR_KIND, Utils.enumToString(value_).upper(), True, 0)
        return value_
    
    @property
    def kind2(self) -> 'InstrumentKind':
        s = self.get_string_value(InstrumentBlockReferent.ATTR_KIND2)
        if (s is None): 
            return InstrumentKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, InstrumentKind)
            if (isinstance(res, InstrumentKind)): 
                return Utils.valToEnum(res, InstrumentKind)
        except Exception as ex1579: 
            pass
        return InstrumentKind.UNDEFINED
    @kind2.setter
    def kind2(self, value_) -> 'InstrumentKind':
        if (value_ != InstrumentKind.UNDEFINED): 
            self.add_slot(InstrumentBlockReferent.ATTR_KIND2, Utils.enumToString(value_).upper(), True, 0)
        return value_
    
    @property
    def value(self) -> str:
        """ Значение фрагмента """
        return self.get_string_value(InstrumentBlockReferent.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(InstrumentBlockReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def ref(self) -> 'Referent':
        """ Ссылка на сущность """
        return Utils.asObjectOrNull(self.get_slot_value(InstrumentBlockReferent.ATTR_REF), Referent)
    
    @property
    def is_expired(self) -> bool:
        """ Признак утраты силы """
        return self.get_string_value(InstrumentBlockReferent.ATTR_EXPIRED) == "true"
    @is_expired.setter
    def is_expired(self, value_) -> bool:
        self.add_slot(InstrumentBlockReferent.ATTR_EXPIRED, ("true" if value_ else None), True, 0)
        return value_
    
    @property
    def number(self) -> int:
        """ Номер (для диапазона - максимальный номер) """
        str0_ = self.get_string_value(InstrumentBlockReferent.ATTR_NUMBER)
        if (str0_ is None): 
            return 0
        wrapi1580 = RefOutArgWrapper(0)
        inoutres1581 = Utils.tryParseInt(str0_, wrapi1580)
        i = wrapi1580.value
        if (inoutres1581): 
            return i
        return 0
    @number.setter
    def number(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_NUMBER, str(value_), True, 0)
        return value_
    
    @property
    def sub_number(self) -> int:
        """ Дополнительный номер (через точку за основным) """
        str0_ = self.get_string_value(InstrumentBlockReferent.ATTR_SUBNUMBER)
        if (str0_ is None): 
            return 0
        wrapi1582 = RefOutArgWrapper(0)
        inoutres1583 = Utils.tryParseInt(str0_, wrapi1582)
        i = wrapi1582.value
        if (inoutres1583): 
            return i
        return 0
    @sub_number.setter
    def sub_number(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_SUBNUMBER, str(value_), True, 0)
        return value_
    
    @property
    def sub_number2(self) -> int:
        """ Дополнительный второй номер (через точку за дополнительным) """
        str0_ = self.get_string_value(InstrumentBlockReferent.ATTR_SUB2NUMBER)
        if (str0_ is None): 
            return 0
        wrapi1584 = RefOutArgWrapper(0)
        inoutres1585 = Utils.tryParseInt(str0_, wrapi1584)
        i = wrapi1584.value
        if (inoutres1585): 
            return i
        return 0
    @sub_number2.setter
    def sub_number2(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_SUB2NUMBER, str(value_), True, 0)
        return value_
    
    @property
    def sub_number3(self) -> int:
        """ Дополнительный третий номер (через точку за вторым дополнительным) """
        str0_ = self.get_string_value(InstrumentBlockReferent.ATTR_SUB3NUMBER)
        if (str0_ is None): 
            return 0
        wrapi1586 = RefOutArgWrapper(0)
        inoutres1587 = Utils.tryParseInt(str0_, wrapi1586)
        i = wrapi1586.value
        if (inoutres1587): 
            return i
        return 0
    @sub_number3.setter
    def sub_number3(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_SUB3NUMBER, str(value_), True, 0)
        return value_
    
    @property
    def min_number(self) -> int:
        """ Минимальный номер, если задан диапазон """
        str0_ = self.get_string_value(InstrumentBlockReferent.ATTR_MINNUMBER)
        if (str0_ is None): 
            return 0
        wrapi1588 = RefOutArgWrapper(0)
        inoutres1589 = Utils.tryParseInt(str0_, wrapi1588)
        i = wrapi1588.value
        if (inoutres1589): 
            return i
        return 0
    @min_number.setter
    def min_number(self, value_) -> int:
        self.add_slot(InstrumentBlockReferent.ATTR_MINNUMBER, str(value_), True, 0)
        return value_
    
    @property
    def name(self) -> str:
        """ Наименование """
        return self.get_string_value(InstrumentBlockReferent.ATTR_NAME)
    @name.setter
    def name(self, value_) -> str:
        self.add_slot(InstrumentBlockReferent.ATTR_NAME, value_, True, 0)
        return value_
    
    @property
    def children(self) -> typing.List['InstrumentBlockReferent']:
        """ Дочерние узлы: список InstrumentBlockReferent """
        if (self.__m_children is None): 
            self.__m_children = list()
            for s in self.slots: 
                if (s.type_name == InstrumentBlockReferent.ATTR_CHILD): 
                    if (isinstance(s.value, InstrumentBlockReferent)): 
                        self.__m_children.append(Utils.asObjectOrNull(s.value, InstrumentBlockReferent))
        return self.__m_children
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        self.__m_children = (None)
        return super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        return obj == self
    
    @staticmethod
    def kind_to_rus_string(typ : 'InstrumentKind', short_val : bool) -> str:
        """ Представить тип строкой русского языка.
        
        Args:
            typ(InstrumentKind): тип
            short_val(bool): сокращённый или полный (например, ст. или статья)
        
        Returns:
            str: слово
        """
        if (typ == InstrumentKind.APPENDIX): 
            return ("прил." if short_val else "Приложение")
        if (typ == InstrumentKind.CLAUSE): 
            return ("ст." if short_val else "Статья")
        if (typ == InstrumentKind.CHAPTER): 
            return ("гл." if short_val else "Глава")
        if (typ == InstrumentKind.ITEM): 
            return ("п." if short_val else "Пункт")
        if (typ == InstrumentKind.PARAGRAPH): 
            return ("§" if short_val else "Параграф")
        if (typ == InstrumentKind.SUBPARAGRAPH): 
            return ("подпарагр." if short_val else "Подпараграф")
        if (typ == InstrumentKind.DOCPART): 
            return ("ч." if short_val else "Часть")
        if (typ == InstrumentKind.SECTION): 
            return ("раздел" if short_val else "Раздел")
        if (typ == InstrumentKind.INTERNALDOCUMENT): 
            return "Документ"
        if (typ == InstrumentKind.SUBITEM): 
            return ("пп." if short_val else "Подпункт")
        if (typ == InstrumentKind.SUBSECTION): 
            return ("подразд." if short_val else "Подраздел")
        if (typ == InstrumentKind.CLAUSEPART): 
            return ("ч." if short_val else "Часть")
        if (typ == InstrumentKind.INDENTION): 
            return ("абз." if short_val else "Абзац")
        if (typ == InstrumentKind.PREAMBLE): 
            return ("преамб." if short_val else "Преамбула")
        return None