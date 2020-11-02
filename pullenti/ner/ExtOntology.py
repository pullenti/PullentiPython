# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.ExtOntologyItem import ExtOntologyItem
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis

class ExtOntology:
    """ Внешняя "онтология". Содержит дополнительтную информацию для обработки (сущностей) -
    это список элементов, связанных с внешними сущностями.
    Подаётся необязательным параметром на вход методу Process() класса Processor.
    Внешняя онтология
    """
    
    def add(self, ext_id : object, type_name : str, definition_ : str) -> 'ExtOntologyItem':
        """ Добавить элемент
        
        Args:
            ext_id(object): произвольный объект
            type_name(str): имя типа сущности
            definition_(str): текстовое определение. Определение может содержать несколько
        отдельных фрагментов, которые разделяются точкой с запятой.
        Например, Министерство Обороны России; Минобороны
        
        Returns:
            ExtOntologyItem: если null, то не получилось...
        """
        if (type_name is None or definition_ is None): 
            return None
        rs = self.__create_referent(type_name, definition_)
        if (rs is None): 
            return None
        self.__m_hash = (None)
        res = ExtOntologyItem._new2803(ext_id, rs[0], type_name)
        if (len(rs) > 1): 
            del rs[0]
            res._refs = rs
        self.items.append(res)
        return res
    
    def add_referent(self, ext_id : object, referent : 'Referent') -> 'ExtOntologyItem':
        """ Добавить готовую сущность
        
        Args:
            ext_id(object): произвольный объект
            referent(Referent): готовая сущность (например, сфомированная явно)
        
        Returns:
            ExtOntologyItem: новая запись словаря
        """
        if (referent is None): 
            return None
        self.__m_hash = (None)
        res = ExtOntologyItem._new2803(ext_id, referent, referent.type_name)
        self.items.append(res)
        return res
    
    def __create_referent(self, type_name : str, definition_ : str) -> typing.List['Referent']:
        analyzer = None
        wrapanalyzer2805 = RefOutArgWrapper(None)
        inoutres2806 = Utils.tryGetValue(self.__m_anal_by_type, type_name, wrapanalyzer2805)
        analyzer = wrapanalyzer2805.value
        if (not inoutres2806): 
            return None
        sf = SourceOfAnalysis(definition_)
        ar = self.__m_processor._process(sf, True, True, None, None)
        if (ar is None or ar.first_token is None): 
            return None
        r0 = ar.first_token.get_referent()
        t = None
        if (r0 is not None): 
            if (r0.type_name != type_name): 
                r0 = (None)
        if (r0 is not None): 
            t = ar.first_token
        else: 
            rt = analyzer.process_ontology_item(ar.first_token)
            if (rt is None): 
                return None
            r0 = rt.referent
            t = rt.end_token
        t = t.next0_
        first_pass3924 = True
        while True:
            if first_pass3924: first_pass3924 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_char(';') and t.next0_ is not None): 
                r1 = t.next0_.get_referent()
                if (r1 is None): 
                    rt = analyzer.process_ontology_item(t.next0_)
                    if (rt is None): 
                        continue
                    t = rt.end_token
                    r1 = rt.referent
                if (r1.type_name == type_name): 
                    r0.merge_slots(r1, True)
                    r1.tag = r0
        if (r0 is None): 
            return None
        r0.tag = r0
        r0 = analyzer._persist_analizer_data.register_referent(r0)
        self.__m_processor._create_res(ar.first_token.kit, ar, None, True)
        res = list()
        res.append(r0)
        for e0_ in ar.entities: 
            if (e0_.tag is None): 
                res.append(e0_)
        return res
    
    def refresh(self, item : 'ExtOntologyItem', definition_ : object) -> bool:
        """ Обновить существующий элемент онтологии
        
        Args:
            item(ExtOntologyItem): обновляемый элемент
            definition_(object): новое определение
        
        Returns:
            bool: признак успешности обновления
        """
        if (item is None): 
            return False
        new_referent = Utils.asObjectOrNull(definition_, Referent)
        if (isinstance(definition_, str)): 
            new_referent = (self.__create_referent(item.type_name, Utils.asObjectOrNull(definition_, str)))
        analyzer = None
        wrapanalyzer2807 = RefOutArgWrapper(None)
        inoutres2808 = Utils.tryGetValue(self.__m_anal_by_type, item.type_name, wrapanalyzer2807)
        analyzer = wrapanalyzer2807.value
        if (not inoutres2808): 
            return False
        if (analyzer._persist_analizer_data is None): 
            return True
        if (item.referent is not None): 
            analyzer._persist_analizer_data.remove_referent(item.referent)
        old_referent = item.referent
        new_referent = analyzer._persist_analizer_data.register_referent(new_referent)
        item.referent = new_referent
        self.__m_hash = (None)
        if (old_referent is not None and new_referent is not None): 
            for a in self.__m_processor.analyzers: 
                if (a._persist_analizer_data is not None): 
                    for rr in a._persist_analizer_data.referents: 
                        for s in new_referent.slots: 
                            if (s.value == old_referent): 
                                new_referent.upload_slot(s, rr)
                        for s in rr.slots: 
                            if (s.value == old_referent): 
                                rr.upload_slot(s, new_referent)
        return True
    
    def __init__(self, spec_names : str=None) -> None:
        self.items = list()
        self.__m_processor = None;
        self.__m_specs = None;
        self.__m_anal_by_type = None;
        self.__m_hash = None
        self.tag = None;
        self.__m_specs = spec_names
        self.__init()
    
    def __init(self) -> None:
        self.__m_processor = ProcessorService.create_specific_processor(self.__m_specs)
        self.__m_anal_by_type = dict()
        for a in self.__m_processor.analyzers: 
            a._persist_referents_regim = True
            if (a.name == "DENOMINATION"): 
                a.ignore_this_analyzer = True
            else: 
                for t in a.type_system: 
                    if (not t.name in self.__m_anal_by_type): 
                        self.__m_anal_by_type[t.name] = a
    
    def serialize(self, stream : io.IOBase) -> None:
        """ Сериализовать весь словарь в поток
        
        Args:
            stream(io.IOBase): поток для сериализации
        """
        SerializerHelper.serialize_string(stream, self.__m_specs)
        SerializerHelper.serialize_int(stream, len(self.items))
        for it in self.items: 
            it._serialize(stream)
    
    def deserialize(self, stream : io.IOBase) -> None:
        """ Восстановить словарь из потока
        
        Args:
            stream(io.IOBase): поток для десериализации
        """
        self.__m_specs = SerializerHelper.deserialize_string(stream)
        self.__init()
        cou = SerializerHelper.deserialize_int(stream)
        while cou > 0: 
            it = ExtOntologyItem()
            it._deserialize(stream)
            self.items.append(it)
            cou -= 1
        self.__init_hash()
    
    def _get_analyzer_data(self, type_name : str) -> 'AnalyzerData':
        wrapa2809 = RefOutArgWrapper(None)
        inoutres2810 = Utils.tryGetValue(self.__m_anal_by_type, type_name, wrapa2809)
        a = wrapa2809.value
        if (not inoutres2810): 
            return None
        return a._persist_analizer_data
    
    def __init_hash(self) -> None:
        self.__m_hash = dict()
        for it in self.items: 
            if (it.referent is not None): 
                it.referent.ontology_items = (None)
        for it in self.items: 
            if (it.referent is not None): 
                wrapont2812 = RefOutArgWrapper(None)
                inoutres2813 = Utils.tryGetValue(self.__m_hash, it.referent.type_name, wrapont2812)
                ont = wrapont2812.value
                if (not inoutres2813): 
                    ont = IntOntologyCollection._new2811(True)
                    self.__m_hash[it.referent.type_name] = ont
                if (it.referent.ontology_items is None): 
                    it.referent.ontology_items = list()
                it.referent.ontology_items.append(it)
                it.referent._int_ontology_item = (None)
                ont.add_referent(it.referent)
    
    def attach_referent(self, r : 'Referent') -> typing.List['ExtOntologyItem']:
        """ Привязать сущность к существующей записи
        
        Args:
            r(Referent): внешняя сущность
        
        Returns:
            typing.List[ExtOntologyItem]: null или список подходящих элементов
        """
        if (self.__m_hash is None): 
            self.__init_hash()
        wraponto2814 = RefOutArgWrapper(None)
        inoutres2815 = Utils.tryGetValue(self.__m_hash, r.type_name, wraponto2814)
        onto = wraponto2814.value
        if (not inoutres2815): 
            return None
        li = onto.try_attach_by_referent(r, None, False)
        if (li is None or len(li) == 0): 
            return None
        res = None
        for rr in li: 
            if (rr.ontology_items is not None): 
                if (res is None): 
                    res = list()
                res.extend(rr.ontology_items)
        return res
    
    def attach_token(self, type_name : str, t : 'Token') -> typing.List['IntOntologyToken']:
        # Используется внутренним образом
        if (self.__m_hash is None): 
            self.__init_hash()
        wraponto2816 = RefOutArgWrapper(None)
        inoutres2817 = Utils.tryGetValue(self.__m_hash, type_name, wraponto2816)
        onto = wraponto2816.value
        if (not inoutres2817): 
            return None
        return onto.try_attach(t, None, False)