# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.internal.TextsCompareType import TextsCompareType
from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
from pullenti.ner.TextAnnotation import TextAnnotation
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType

class Referent:
    """ Базовый класс для всех именованных сущностей
    
    Именованная сущность
    """
    
    def __init__(self, typ : str) -> None:
        self.__m_object_type = None;
        self.__instanceof = None;
        self.ontology_items = None;
        self.__m_slots = list()
        self.__m_level = 0
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
        return self.to_string(False, MorphLang.UNKNOWN, 0)
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        """ Специализированное строковое представление сущности
        
        Args:
            short_variant(bool): Сокращённый вариант
            lang(MorphLang): Язык
        
        """
        return self.type_name
    
    def to_sort_string(self) -> str:
        # По этой строке можно осуществлять сортировку среди сущностей одного типа
        return self.to_string(False, MorphLang.UNKNOWN, 0)
    
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
        """ Значения атрибутов - список элементов типа Slot
        
        """
        return self.__m_slots
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        """ Добавить значение атрибута
        
        Args:
            attr_name(str): имя
            attr_value(object): значение
            clear_old_value(bool): если true и слот существует, то значение перезапишется
        
        Returns:
            Slot: слот(атрибут)
        """
        from pullenti.ner.Slot import Slot
        if (clear_old_value): 
            for i in range(len(self.slots) - 1, -1, -1):
                if (self.slots[i].type_name == attr_name): 
                    del self.slots[i]
        if (attr_value is None): 
            return None
        for r in self.slots: 
            if (r.type_name == attr_name): 
                if (self.__compare_values(r.value, attr_value, True)): 
                    r.count = r.count + stat_count
                    return r
        res = Slot()
        res.owner = self
        res.value = attr_value
        res.type_name = attr_name
        res.count = stat_count
        self.slots.append(res)
        return res
    
    def upload_slot(self, slot : 'Slot', new_val : object) -> None:
        if (slot is not None): 
            slot.value = new_val
    
    def find_slot(self, attr_name : str, val : object=None, use_can_be_equals_for_referents : bool=True) -> 'Slot':
        """ Найти слот (атрибут)
        
        Args:
            attr_name(str): имя атрибута
            val(object): возможное значение
            use_can_be_equals_for_referents(bool): для значений-сущностей использовать метод CanBeEquals для сравнения
        
        Returns:
            Slot: подходящий слот или null
        
        """
        if (self.__m_level > 10): 
            return None
        if (attr_name is None): 
            if (val is None): 
                return None
            self.__m_level += 1
            for r in self.slots: 
                if (self.__compare_values(val, r.value, use_can_be_equals_for_referents)): 
                    self.__m_level -= 1
                    return r
            self.__m_level -= 1
            return None
        for r in self.slots: 
            if (r.type_name == attr_name): 
                if (val is None): 
                    return r
                self.__m_level += 1
                if (self.__compare_values(val, r.value, use_can_be_equals_for_referents)): 
                    self.__m_level -= 1
                    return r
                self.__m_level -= 1
        return None
    
    def __compare_values(self, val1 : object, val2 : object, use_can_be_equals_for_referents : bool) -> bool:
        if (val1 is None): 
            return val2 is None
        if (val2 is None): 
            return val1 is None
        if (val1 == val2): 
            return True
        if ((isinstance(val1, Referent)) and (isinstance(val2, Referent))): 
            if (use_can_be_equals_for_referents): 
                return val1.can_be_equals(Utils.asObjectOrNull(val2, Referent), ReferentsEqualType.DIFFERENTTEXTS)
            else: 
                return False
        if (isinstance(val1, str)): 
            if (not (isinstance(val2, str))): 
                return False
            s1 = val1
            s2 = val2
            i = Utils.compareStrings(s1, s2, True)
            return i == 0
        return val1 == val2
    
    def get_slot_value(self, attr_name : str) -> object:
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
    
    def get_string_value(self, attr_name : str) -> str:
        """ Получить строковое значение (если их несколько, то вернёт первое)
        
        Args:
            attr_name(str): имя атрибута
        
        Returns:
            str: значение или null
        
        """
        for v in self.slots: 
            if (v.type_name == attr_name): 
                return (None if v.value is None else str(v.value))
        return None
    
    def get_string_values(self, attr_name : str) -> typing.List[str]:
        """ Получить все строовые значения заданного атрибута
        
        Args:
            attr_name(str): имя атрибута
        
        Returns:
            typing.List[str]: список значений string
        
        """
        res = list()
        for v in self.slots: 
            if (v.type_name == attr_name and v.value is not None): 
                if (isinstance(v.value, str)): 
                    res.append(Utils.asObjectOrNull(v.value, str))
                else: 
                    res.append(str(v))
        return res
    
    def get_int_value(self, attr_name : str, def_value : int) -> int:
        """ Получить числовое значение (если их несколько, то вернёт первое)
        
        Args:
            attr_name(str): имя атрибута
            def_value(int): дефолтовое значение, если не найдено
        
        Returns:
            int: число
        """
        str0_ = self.get_string_value(attr_name)
        if (Utils.isNullOrEmpty(str0_)): 
            return def_value
        wrapres2854 = RefOutArgWrapper(0)
        inoutres2855 = Utils.tryParseInt(str0_, wrapres2854)
        res = wrapres2854.value
        if (not inoutres2855): 
            return def_value
        return res
    
    @property
    def occurrence(self) -> typing.List['TextAnnotation']:
        """ Вхождение сущности в исходный текст (список аннотаций TextAnnotation)
        
        """
        if (self.__m_occurrence is None): 
            self.__m_occurrence = list()
        return self.__m_occurrence
    
    def find_near_occurence(self, t : 'Token') -> 'TextAnnotation':
        """ Найти ближайшую к токену аннотацию
        
        Args:
            t(Token): токен
        
        Returns:
            TextAnnotation: ближайшая аннотация
        """
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
    
    def add_occurence_of_ref_tok(self, rt : 'ReferentToken') -> None:
        self.add_occurence(TextAnnotation._new714(rt.kit.sofa, rt.begin_char, rt.end_char, rt.referent))
    
    def add_occurence(self, anno : 'TextAnnotation') -> None:
        """ Добавить аннотацию
        
        Args:
            anno(TextAnnotation): аннотация
        """
        for l_ in self.occurrence: 
            typ = l_._compare_with(anno)
            if (typ == TextsCompareType.NONCOMPARABLE): 
                continue
            if (typ == TextsCompareType.EQUIVALENT or typ == TextsCompareType.CONTAINS): 
                return
            if (typ == TextsCompareType.IN or typ == TextsCompareType.INTERSECT): 
                l_._merge(anno)
                return
        if (anno.occurence_of != self and anno.occurence_of is not None): 
            anno = TextAnnotation._new2857(anno.begin_char, anno.end_char, anno.sofa)
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
    
    def check_occurence(self, begin_char : int, end_char : int) -> bool:
        """ Проверка, что ссылки на элемент имеются на заданном участке текста
        
        Args:
            begin_char(int): начальная позиция
            end_char(int): конечная позиция
        
        Returns:
            bool: да или нет
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
        from pullenti.ner.Slot import Slot
        res = ProcessorService.create_referent(self.type_name)
        if (res is None): 
            res = Referent(self.type_name)
        res.occurrence.extend(self.occurrence)
        res.ontology_items = self.ontology_items
        for r in self.slots: 
            rr = Slot._new2858(r.type_name, r.value, r.count)
            rr.owner = res
            res.slots.append(rr)
        return res
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        """ Проверка возможной тождественности сущностей
        
        Args:
            obj(Referent): другая сущность
            typ(ReferentsEqualType): тип сравнения
        
        Returns:
            bool: результат
        
        """
        if (obj is None or obj.type_name != self.type_name): 
            return False
        for r in self.slots: 
            if (r.value is not None and obj.find_slot(r.type_name, r.value, False) is None): 
                return False
        for r in obj.slots: 
            if (r.value is not None and self.find_slot(r.type_name, r.value, True) is None): 
                return False
        return True
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        """ Объединение значений атрибутов со значениями атрибутов другой сущности
        
        Args:
            obj(Referent): Другая сущшность, считающаяся эквивалентной
            merge_statistic(bool): Объединять ли вместе со статистикой
        """
        if (obj is None): 
            return
        for r in obj.slots: 
            s = self.find_slot(r.type_name, r.value, True)
            if (s is None and r.value is not None): 
                s = self.add_slot(r.type_name, r.value, False, 0)
            if (s is not None and merge_statistic): 
                s.count = s.count + r.count
        self._merge_ext_referents(obj)
    
    @property
    def parent_referent(self) -> 'Referent':
        """ Ссылка на родительскую сущность. Для разных типов сущностей здесь могут быть свои сущности,
        например, для организаций - вышестоящая организация, для пункта закона - сам закон и т.д.
        
        """
        return None
    
    def get_image_id(self) -> str:
        """ Получить идентификатор иконки. Саму иконку ImageWrapper можно получить через функцию
        GetImageById(imageId) статического класса ProcessorService.
        
        Returns:
            str: идентификатор иконки
        """
        if (self.instance_of is None): 
            return None
        return self.instance_of.get_image_id(self)
    
    ATTR_GENERAL = "GENERAL"
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        """ Проверка, может ли текущая сущность быть обобщением для другой сущности
        
        Args:
            obj(Referent): более частная сущность
        
        Returns:
            bool: да-нет
        """
        return False
    
    @property
    def general_referent(self) -> 'Referent':
        """ Ссылка на сущность-обобщение """
        res = Utils.asObjectOrNull(self.get_slot_value(Referent.ATTR_GENERAL), Referent)
        if (res is None or res == self): 
            return None
        return res
    @general_referent.setter
    def general_referent(self, value) -> 'Referent':
        if (value == self.general_referent): 
            return value
        if (value == self): 
            return value
        self.add_slot(Referent.ATTR_GENERAL, value, True, 0)
        return value
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        # Создать элемент онтологии
        return None
    
    def get_compare_strings(self) -> typing.List[str]:
        # Используется внутренним образом
        res = list()
        res.append(str(self))
        s = self.to_string(True, MorphLang.UNKNOWN, 0)
        if (s != res[0]): 
            res.append(s)
        return res
    
    def add_ext_referent(self, rt : 'ReferentToken') -> None:
        if (rt is None): 
            return
        if (self._m_ext_referents is None): 
            self._m_ext_referents = list()
        if (not rt in self._m_ext_referents): 
            self._m_ext_referents.append(rt)
        if (len(self._m_ext_referents) > 100): 
            pass
    
    def move_ext_referent(self, target : 'Referent', r : 'Referent') -> None:
        if (self._m_ext_referents is not None): 
            for rt in self._m_ext_referents: 
                if (rt.referent == r): 
                    target.add_ext_referent(rt)
                    self._m_ext_referents.remove(rt)
                    break
    
    def _merge_ext_referents(self, obj : 'Referent') -> None:
        if (obj._m_ext_referents is not None): 
            for rt in obj._m_ext_referents: 
                self.add_ext_referent(rt)
    
    def serialize(self, stream : io.IOBase) -> None:
        SerializerHelper.serialize_string(stream, self.type_name)
        SerializerHelper.serialize_int(stream, len(self.__m_slots))
        for s in self.__m_slots: 
            SerializerHelper.serialize_string(stream, s.type_name)
            SerializerHelper.serialize_int(stream, s.count)
            if ((isinstance(s.value, Referent)) and (isinstance(s.value.tag, int))): 
                SerializerHelper.serialize_int(stream, - (s.value.tag))
            elif (isinstance(s.value, str)): 
                SerializerHelper.serialize_string(stream, Utils.asObjectOrNull(s.value, str))
            elif (s.value is None): 
                SerializerHelper.serialize_int(stream, 0)
            else: 
                SerializerHelper.serialize_string(stream, str(s.value))
        if (self.__m_occurrence is None): 
            SerializerHelper.serialize_int(stream, 0)
        else: 
            SerializerHelper.serialize_int(stream, len(self.__m_occurrence))
            for o in self.__m_occurrence: 
                SerializerHelper.serialize_int(stream, o.begin_char)
                SerializerHelper.serialize_int(stream, o.end_char)
                attr = 0
                if (o.essential_for_occurence): 
                    attr = 1
                SerializerHelper.serialize_int(stream, attr)
    
    def deserialize(self, stream : io.IOBase, all0_ : typing.List['Referent'], sofa : 'SourceOfAnalysis') -> None:
        typ = SerializerHelper.deserialize_string(stream)
        cou = SerializerHelper.deserialize_int(stream)
        i = 0
        while i < cou: 
            typ = SerializerHelper.deserialize_string(stream)
            c = SerializerHelper.deserialize_int(stream)
            id0_ = SerializerHelper.deserialize_int(stream)
            val = None
            if ((id0_ < 0) and all0_ is not None): 
                id1 = (- id0_) - 1
                if (id1 < len(all0_)): 
                    val = (all0_[id1])
            elif (id0_ > 0): 
                stream.seek(stream.tell() - (4), io.SEEK_SET)
                val = (SerializerHelper.deserialize_string(stream))
            self.add_slot(typ, val, False, c)
            i += 1
        cou = SerializerHelper.deserialize_int(stream)
        self.__m_occurrence = list()
        i = 0
        while i < cou: 
            a = TextAnnotation._new2859(sofa, self)
            self.__m_occurrence.append(a)
            a.begin_char = SerializerHelper.deserialize_int(stream)
            a.end_char = SerializerHelper.deserialize_int(stream)
            attr = SerializerHelper.deserialize_int(stream)
            if (((attr & 1)) != 0): 
                a.essential_for_occurence = True
            i += 1