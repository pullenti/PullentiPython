﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.ExtOntologyItem import ExtOntologyItem
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis

class ExtOntology:
    """ Внешняя онтология """
    
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
        r = self.__create_referent(type_name, definition_)
        self.__m_hash = (None)
        res = ExtOntologyItem._new2746(ext_id, r, type_name)
        self.items.append(res)
        return res
    
    def add_referent(self, ext_id : object, referent : 'Referent') -> 'ExtOntologyItem':
        """ Добавить готовую сущность
        
        Args:
            ext_id(object): произвольный объект
            referent(Referent): готовая сущность (например, сфомированная явно)
        
        """
        if (referent is None): 
            return None
        self.__m_hash = (None)
        res = ExtOntologyItem._new2746(ext_id, referent, referent.type_name)
        self.items.append(res)
        return res
    
    def __create_referent(self, type_name : str, definition_ : str) -> 'Referent':
        analyzer = None
        wrapanalyzer2748 = RefOutArgWrapper(None)
        inoutres2749 = Utils.tryGetValue(self.__m_anal_by_type, type_name, wrapanalyzer2748)
        analyzer = wrapanalyzer2748.value
        if (not inoutres2749): 
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
        first_pass3276 = True
        while True:
            if first_pass3276: first_pass3276 = False
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
        if (r0 is not None): 
            r0 = analyzer._persist_analizer_data.register_referent(r0)
        return r0
    
    def refresh(self, item : 'ExtOntologyItem', definition_ : object) -> bool:
        """ Обновить существующий элемент онтологии
        
        Args:
            item(ExtOntologyItem): 
            definition_(object): новое определение
        
        """
        if (item is None): 
            return False
        new_referent = Utils.asObjectOrNull(definition_, Referent)
        if (isinstance(definition_, str)): 
            new_referent = self.__create_referent(item.type_name, Utils.asObjectOrNull(definition_, str))
        analyzer = None
        wrapanalyzer2750 = RefOutArgWrapper(None)
        inoutres2751 = Utils.tryGetValue(self.__m_anal_by_type, item.type_name, wrapanalyzer2750)
        analyzer = wrapanalyzer2750.value
        if (not inoutres2751): 
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
        self.__m_anal_by_type = None;
        self.__m_hash = None
        self.__m_processor = ProcessorService.create_specific_processor(spec_names)
        self.__m_anal_by_type = dict()
        for a in self.__m_processor.analyzers: 
            a._persist_referents_regim = True
            if (a.name == "DENOMINATION"): 
                a.ignore_this_analyzer = True
            else: 
                for t in a.type_system: 
                    if (not t.name in self.__m_anal_by_type): 
                        self.__m_anal_by_type[t.name] = a
    
    def _get_analyzer_data(self, type_name : str) -> 'AnalyzerData':
        """ Используется внутренним образом
        
        Args:
            type_name(str): 
        
        """
        wrapa2752 = RefOutArgWrapper(None)
        inoutres2753 = Utils.tryGetValue(self.__m_anal_by_type, type_name, wrapa2752)
        a = wrapa2752.value
        if (not inoutres2753): 
            return None
        return a._persist_analizer_data
    
    def __init_hash(self) -> None:
        self.__m_hash = dict()
        for it in self.items: 
            if (it.referent is not None): 
                it.referent.ontology_items = (None)
        for it in self.items: 
            if (it.referent is not None): 
                wrapont2755 = RefOutArgWrapper(None)
                inoutres2756 = Utils.tryGetValue(self.__m_hash, it.referent.type_name, wrapont2755)
                ont = wrapont2755.value
                if (not inoutres2756): 
                    ont = IntOntologyCollection._new2754(True)
                    self.__m_hash[it.referent.type_name] = ont
                if (it.referent.ontology_items is None): 
                    it.referent.ontology_items = list()
                it.referent.ontology_items.append(it)
                it.referent._int_ontology_item = (None)
                ont.add_referent(it.referent)
    
    def attach_referent(self, r : 'Referent') -> typing.List['ExtOntologyItem']:
        """ Привязать сущность
        
        Args:
            r(Referent): 
        
        Returns:
            typing.List[ExtOntologyItem]: null или список подходящих элементов
        """
        if (self.__m_hash is None): 
            self.__init_hash()
        wraponto2757 = RefOutArgWrapper(None)
        inoutres2758 = Utils.tryGetValue(self.__m_hash, r.type_name, wraponto2757)
        onto = wraponto2757.value
        if (not inoutres2758): 
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
        """ Используется внутренним образом
        
        Args:
            type_name(str): 
            t(Token): 
        
        """
        if (self.__m_hash is None): 
            self.__init_hash()
        wraponto2759 = RefOutArgWrapper(None)
        inoutres2760 = Utils.tryGetValue(self.__m_hash, type_name, wraponto2759)
        onto = wraponto2759.value
        if (not inoutres2760): 
            return None
        return onto.try_attach(t, None, False)