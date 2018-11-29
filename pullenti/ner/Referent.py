# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.Slot import Slot
from pullenti.ner.core.internal.TextsCompareType import TextsCompareType
from pullenti.ner.core.internal.SerializerHelper import SerializerHelper


class Referent:
    """ Базовый класс для всех сущностей """
    
    class EqualType(IntEnum):
        """ Типы сравнение объектов """
        WITHINONETEXT = 0
        DIFFERENTTEXTS = 1
        FORMERGING = 2
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, typ : str) -> None:
        self.__m_object_type = None;
        self.__instanceof = None;
        self.ontology_items = None;
        self.__m_slots = list()
        self.__m_occurrence = None;
        self.__tag = None;
        self._int_ontology_item = None;
        self._m_ext_referents = None;
        self.__m_object_type = typ
    
    @property
    def type_name(self) -> str:
        """ Имя типа (= InstanceOf.Name) """
        return self.__m_object_type
    
    def __str__(self) -> str:
        return self.toString(False, MorphLang.UNKNOWN, 0)
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        """ Специализированное строковое представление сущности
        
        Args:
            short_variant(bool): Сокращённый вариант
            lang(MorphLang): Язык
        
        """
        return self.type_name
    
    def toSortString(self) -> str:
        """ По этой строке можно осуществлять сортировку среди объектов одного типа
        
        """
        return self.toString(False, MorphLang.UNKNOWN, 0)
    
    @property
    def instance_of(self) -> 'ReferentClass':
        """ Ссылка на описание из модели данных """
        return self.__instanceof
    @instance_of.setter
    def instance_of(self, value) -> 'ReferentClass':
        self.__instanceof = value
        return self.__instanceof
    
    @property
    def slots(self) -> typing.List['Slot']:
        """ Значения атрибутов """
        return self.__m_slots
    
    def addSlot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        """ Добавить значение атрибута
        
        Args:
            attr_name(str): имя
            attr_value(object): значение
            clear_old_value(bool): если true и слот существует, то значение перезапишется
        
        """
        if (clear_old_value): 
            for i in range(len(self.slots) - 1, -1, -1):
                if (self.slots[i].type_name == attr_name): 
                    del self.slots[i]
        if (attr_value is None): 
            return None
        for r in self.slots: 
            if (r.type_name == attr_name): 
                if (self.__compareValues(r.value, attr_value, True)): 
                    r.count = r.count + stat_count
                    return r
        res = Slot()
        res.owner = self
        res.value = attr_value
        res.type_name = attr_name
        res.count = stat_count
        self.slots.append(res)
        return res
    
    def uploadSlot(self, slot : 'Slot', new_val : object) -> None:
        if (slot is not None): 
            slot.value = new_val
    
    def findSlot(self, attr_name : str, val : object=None, use_can_be_equals_for_referents : bool=True) -> 'Slot':
        """ Найти слот
        
        Args:
            attr_name(str): 
            val(object): 
            use_can_be_equals_for_referents(bool): 
        
        """
        if (attr_name is None): 
            if (val is None): 
                return None
            for r in self.slots: 
                if (self.__compareValues(val, r.value, use_can_be_equals_for_referents)): 
                    return r
            return None
        for r in self.slots: 
            if (r.type_name == attr_name): 
                if (val is None): 
                    return r
                if (self.__compareValues(val, r.value, use_can_be_equals_for_referents)): 
                    return r
        return None
    
    def __compareValues(self, val1 : object, val2 : object, use_can_be_equals_for_referents : bool) -> bool:
        if (val1 is None): 
            return val2 is None
        if (val2 is None): 
            return val1 is None
        if (val1 == val2): 
            return True
        if ((isinstance(val1, Referent)) and (isinstance(val2, Referent))): 
            if (use_can_be_equals_for_referents): 
                return (Utils.asObjectOrNull(val1, Referent)).canBeEquals(Utils.asObjectOrNull(val2, Referent), Referent.EqualType.DIFFERENTTEXTS)
            else: 
                return False
        if (isinstance(val1, str)): 
            if (not ((isinstance(val2, str)))): 
                return False
            s1 = val1
            s2 = val2
            i = Utils.compareStrings(s1, s2, True)
            return i == 0
        return val1 == val2
    
    def getSlotValue(self, attr_name : str) -> object:
        """ Получить значение слота-атрибута (если их несколько, то вернёт первое)
        
        Args:
            attr_name(str): имя слота
        
        Returns:
            object: значение (поле Value)
        """
        for v in self.slots: 
            if (v.type_name == attr_name): 
                return v.value
        return None
    
    def getStringValue(self, attr_name : str) -> str:
        """ Получить строковое значение (если их несколько, то вернёт первое)
        
        Args:
            attr_name(str): 
        
        """
        for v in self.slots: 
            if (v.type_name == attr_name): 
                return (None if v.value is None else str(v.value))
        return None
    
    def getStringValues(self, attr_name : str) -> typing.List[str]:
        """ Получить все строовые значения заданного атрибута
        
        Args:
            attr_name(str): 
        
        """
        res = list()
        for v in self.slots: 
            if (v.type_name == attr_name and v.value is not None): 
                if (isinstance(v.value, str)): 
                    res.append(Utils.asObjectOrNull(v.value, str))
                else: 
                    res.append(str(v))
        return res
    
    def getIntValue(self, attr_name : str, def_value : int) -> int:
        """ Получить числовое значение (если их несколько, то вернёт первое)
        
        Args:
            attr_name(str): 
            def_value(int): 
        
        """
        str0_ = self.getStringValue(attr_name)
        if (Utils.isNullOrEmpty(str0_)): 
            return def_value
        wrapres2696 = RefOutArgWrapper(0)
        inoutres2697 = Utils.tryParseInt(str0_, wrapres2696)
        res = wrapres2696.value
        if (not inoutres2697): 
            return def_value
        return res
    
    @property
    def occurrence(self) -> typing.List['TextAnnotation']:
        """ Привязка элемента к текстам (аннотации) """
        if (self.__m_occurrence is None): 
            self.__m_occurrence = list()
        return self.__m_occurrence
    
    def findNearOccurence(self, t : 'Token') -> 'TextAnnotation':
        min0_ = -1
        res = None
        for oc in self.occurrence: 
            if (oc.sofa == t.kit.sofa): 
                len0_ = oc.begin_char - t.begin_char
                if (len0_ < 0): 
                    len0_ = (- len0_)
                if ((min0_ < 0) or (len0_ < min0_)): 
                    min0_ = len0_
                    res = oc
        return res
    
    def addOccurenceOfRefTok(self, rt : 'ReferentToken') -> None:
        from pullenti.ner.TextAnnotation import TextAnnotation
        self.addOccurence(TextAnnotation._new727(rt.kit.sofa, rt.begin_char, rt.end_char, rt.referent))
    
    def addOccurence(self, anno : 'TextAnnotation') -> None:
        """ Добавить аннотацию
        
        Args:
            anno(TextAnnotation): 
        """
        from pullenti.ner.TextAnnotation import TextAnnotation
        for l_ in self.occurrence: 
            typ = l_._compareWith(anno)
            if (typ == TextsCompareType.NONCOMPARABLE): 
                continue
            if (typ == TextsCompareType.EQUIVALENT or typ == TextsCompareType.CONTAINS): 
                return
            if (typ == TextsCompareType.IN or typ == TextsCompareType.INTERSECT): 
                l_._merge(anno)
                return
        if (anno.occurence_of != self and anno.occurence_of is not None): 
            anno = TextAnnotation._new2699(anno.begin_char, anno.end_char, anno.sofa)
        if (self.__m_occurrence is None): 
            self.__m_occurrence = list()
        anno.occurence_of = self
        if (len(self.__m_occurrence) == 0): 
            anno.essential_for_occurence = True
            self.__m_occurrence.append(anno)
            return
        if (anno.begin_char < self.__m_occurrence[0].begin_char): 
            self.__m_occurrence.insert(0, anno)
            return
        if (anno.begin_char >= self.__m_occurrence[len(self.__m_occurrence) - 1].begin_char): 
            self.__m_occurrence.append(anno)
            return
        i = 0
        while i < (len(self.__m_occurrence) - 1): 
            if (anno.begin_char >= self.__m_occurrence[i].begin_char and anno.begin_char <= self.__m_occurrence[i + 1].begin_char): 
                self.__m_occurrence.insert(i + 1, anno)
                return
            i += 1
        self.__m_occurrence.append(anno)
    
    def checkOccurence(self, begin_char : int, end_char : int) -> bool:
        """ Проверка, что ссылки на элемент имеются на заданном участке текста
        
        Args:
            begin_char(int): 
            end_char(int): 
        
        """
        for loc in self.occurrence: 
            cmp = loc._compare(begin_char, end_char)
            if (cmp != TextsCompareType.EARLY and cmp != TextsCompareType.LATER and cmp != TextsCompareType.NONCOMPARABLE): 
                return True
        return False
    
    @property
    def tag(self) -> object:
        """ Используется произвольным образом """
        return self.__tag
    @tag.setter
    def tag(self, value) -> object:
        self.__tag = value
        return self.__tag
    
    def clone(self) -> 'Referent':
        from pullenti.ner.ProcessorService import ProcessorService
        res = ProcessorService.createReferent(self.type_name)
        if (res is None): 
            res = Referent(self.type_name)
        res.occurrence.extend(self.occurrence)
        res.ontology_items = self.ontology_items
        for r in self.slots: 
            rr = Slot._new2700(r.type_name, r.value, r.count)
            rr.owner = res
            res.slots.append(rr)
        return res
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=EqualType.WITHINONETEXT) -> bool:
        """ Проверка возможной тождественности объектов
        
        Args:
            obj(Referent): другой объект
            typ(EqualType): тип сравнения
        
        Returns:
            bool: результат
        """
        if (obj is None or obj.type_name != self.type_name): 
            return False
        for r in self.slots: 
            if (r.value is not None and obj.findSlot(r.type_name, r.value, True) is None): 
                return False
        for r in obj.slots: 
            if (r.value is not None and self.findSlot(r.type_name, r.value, True) is None): 
                return False
        return True
    
    def mergeSlots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        """ Объединение значений атрибутов со значениями атрибутов другого объекта
        
        Args:
            obj(Referent): Другой объект, считающийся эквивалентным
        """
        if (obj is None): 
            return
        for r in obj.slots: 
            s = self.findSlot(r.type_name, r.value, True)
            if (s is None and r.value is not None): 
                s = self.addSlot(r.type_name, r.value, False, 0)
            if (s is not None and merge_statistic): 
                s.count = s.count + r.count
        self._mergeExtReferents(obj)
    
    @property
    def parent_referent(self) -> 'Referent':
        """ Ссылка на родительский объект (для разных типов объектов здесь может быть свои объекты,
         например, для организаций - вышестоящая организация, для пункта закона - сам закон и т.д.) """
        return None
    
    def getImageId(self) -> str:
        """ Получить идентификатор иконки (саму иконку можно получить через функцию
         GetImageById(imageId) статического класса ProcessorService
        
        """
        if (self.instance_of is None): 
            return None
        return self.instance_of.getImageId(self)
    
    ATTR_GENERAL = "GENERAL"
    
    def canBeGeneralFor(self, obj : 'Referent') -> bool:
        """ Проверка, может ли текущий объект быть обобщением для другого объекта
        
        Args:
            obj(Referent): 
        
        """
        return False
    
    @property
    def general_referent(self) -> 'Referent':
        """ Ссылка на объект-обобщение """
        res = Utils.asObjectOrNull(self.getSlotValue(Referent.ATTR_GENERAL), Referent)
        if (res is None or res == self): 
            return None
        return res
    @general_referent.setter
    def general_referent(self, value) -> 'Referent':
        if (value == self.general_referent): 
            return value
        if (value == self): 
            return value
        self.addSlot(Referent.ATTR_GENERAL, value, True, 0)
        return value
    
    def createOntologyItem(self) -> 'IntOntologyItem':
        """ Создать элемент отнологии
        
        """
        return None
    
    def getCompareStrings(self) -> typing.List[str]:
        """ Используется внутренним образом
        
        """
        res = list()
        res.append(str(self))
        s = self.toString(True, MorphLang.UNKNOWN, 0)
        if (s != res[0]): 
            res.append(s)
        return res
    
    def addExtReferent(self, rt : 'ReferentToken') -> None:
        if (rt is None): 
            return
        if (self._m_ext_referents is None): 
            self._m_ext_referents = list()
        if (not rt in self._m_ext_referents): 
            self._m_ext_referents.append(rt)
        if (len(self._m_ext_referents) > 100): 
            pass
    
    def _mergeExtReferents(self, obj : 'Referent') -> None:
        if (obj._m_ext_referents is not None): 
            for rt in obj._m_ext_referents: 
                self.addExtReferent(rt)
    
    def serialize(self, stream : io.IOBase) -> None:
        SerializerHelper.serializeString(stream, self.type_name)
        SerializerHelper.serializeInt(stream, len(self.__m_slots))
        for s in self.__m_slots: 
            SerializerHelper.serializeString(stream, s.type_name)
            SerializerHelper.serializeInt(stream, s.count)
            if ((isinstance(s.value, Referent)) and (isinstance((Utils.asObjectOrNull(s.value, Referent)).tag, int))): 
                SerializerHelper.serializeInt(stream, - ((Utils.asObjectOrNull(s.value, Referent)).tag))
            elif (isinstance(s.value, str)): 
                SerializerHelper.serializeString(stream, Utils.asObjectOrNull(s.value, str))
            elif (s.value is None): 
                SerializerHelper.serializeInt(stream, 0)
            else: 
                SerializerHelper.serializeString(stream, str(s.value))
        if (self.__m_occurrence is None): 
            SerializerHelper.serializeInt(stream, 0)
        else: 
            SerializerHelper.serializeInt(stream, len(self.__m_occurrence))
            for o in self.__m_occurrence: 
                SerializerHelper.serializeInt(stream, o.begin_char)
                SerializerHelper.serializeInt(stream, o.end_char)
                attr = 0
                if (o.essential_for_occurence): 
                    attr = 1
                SerializerHelper.serializeInt(stream, attr)
    
    def deserialize(self, stream : io.IOBase, all0_ : typing.List['Referent'], sofa : 'SourceOfAnalysis') -> None:
        from pullenti.ner.TextAnnotation import TextAnnotation
        typ = SerializerHelper.deserializeString(stream)
        cou = SerializerHelper.deserializeInt(stream)
        i = 0
        while i < cou: 
            typ = SerializerHelper.deserializeString(stream)
            c = SerializerHelper.deserializeInt(stream)
            id0_ = SerializerHelper.deserializeInt(stream)
            val = None
            if (id0_ < 0): 
                val = (all0_[(- id0_) - 1])
            elif (id0_ > 0): 
                stream.seek(stream.tell() - (4), io.SEEK_SET)
                val = (SerializerHelper.deserializeString(stream))
            self.addSlot(typ, val, False, c)
            i += 1
        cou = SerializerHelper.deserializeInt(stream)
        self.__m_occurrence = list()
        i = 0
        while i < cou: 
            a = TextAnnotation._new2701(sofa, self)
            self.__m_occurrence.append(a)
            a.begin_char = SerializerHelper.deserializeInt(stream)
            a.end_char = SerializerHelper.deserializeInt(stream)
            attr = SerializerHelper.deserializeInt(stream)
            if (((attr & 1)) != 0): 
                a.essential_for_occurence = True
            i += 1