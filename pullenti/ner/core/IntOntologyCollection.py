# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminParseAttr import TerminParseAttr



class IntOntologyCollection:
    """ Онтологический словарь """
    
    class OntologyTermin(Termin):
        
        def __init__(self) -> None:
            super().__init__()
            self.owner = None
    
        
        @staticmethod
        def _new501(_arg1 : 'IntOntologyItem', _arg2 : object) -> 'OntologyTermin':
            res = IntOntologyCollection.OntologyTermin()
            res.owner = _arg1
            res.tag = _arg2
            return res
    
    def __init__(self) -> None:
        
        from pullenti.ner.core.TerminCollection import TerminCollection
        self.is_ext_ontology = False
        self.__m_items = list()
        self.__m_termins = TerminCollection()
    
    @property
    def items(self) -> typing.List['IntOntologyItem']:
        """ Список элементов онтологии """
        return self.__m_items
    
    def add_item(self, di : 'IntOntologyItem') -> None:
        """ Добавить элемент (внимание, после добавления нельзя менять термины у элемента)
        
        Args:
            di(IntOntologyItem): 
        """
        
        self.__m_items.append(di)
        di.owner = self
        for i in range(len(di.termins)):
            if (isinstance(di.termins[i], IntOntologyCollection.OntologyTermin)): 
                (di.termins[i] if isinstance(di.termins[i], IntOntologyCollection.OntologyTermin) else None).owner = di
                self.__m_termins.add(di.termins[i])
            else: 
                nt = IntOntologyCollection.OntologyTermin._new501(di, di.termins[i].tag)
                di.termins[i].copy_to(nt)
                self.__m_termins.add(nt)
                di.termins[i] = nt
    
    def add_referent(self, referent : 'Referent') -> bool:
        """ Добавить в онтологию сущность
        
        Args:
            referent(Referent): 
        
        """
        if (referent is None): 
            return False
        oi = None
        if (referent._int_ontology_item is not None and referent._int_ontology_item.owner == self): 
            oi1 = referent.create_ontology_item()
            if (oi1 is None or len(oi1.termins) == len(referent._int_ontology_item.termins)): 
                return True
            for t in referent._int_ontology_item.termins: 
                self.__m_termins.remove(t)
            i = Utils.indexOfList(self.__m_items, referent._int_ontology_item, 0)
            if (i >= 0): 
                del self.__m_items[i]
            oi = oi1
        else: 
            oi = referent.create_ontology_item()
        if (oi is None): 
            return False
        oi.referent = referent
        referent._int_ontology_item = oi
        self.add_item(oi)
        return True
    
    def add_termin(self, di : 'IntOntologyItem', t : 'Termin') -> None:
        """ Добавить термин в существующий элемент
        
        Args:
            di(IntOntologyItem): 
            t(Termin): 
        """
        
        nt = IntOntologyCollection.OntologyTermin._new501(di, t.tag)
        t.copy_to(nt)
        self.__m_termins.add(nt)
    
    def add(self, t : 'Termin') -> None:
        """ Добавить отдельный термин (после добавления нельзя изменять свойства термина)
        
        Args:
            t(Termin): 
        """
        self.__m_termins.add(t)
    
    def find_termin_by_canonic_text(self, text : str) -> typing.List['Termin']:
        return self.__m_termins.find_termin_by_canonic_text(text)
    
    def try_attach(self, t : 'Token', referent_type_name : str=None, can_be_geo_object : bool=False) -> typing.List['IntOntologyToken']:
        """ Привязать с указанной позиции
        
        Args:
            t(Token): 
            can_be_geo_object(bool): при True внутри может быть географический объект (Министерство РФ по делам ...)
        
        """
        
        from pullenti.ner.core.IntOntologyToken import IntOntologyToken
        tts = self.__m_termins.try_parse_all(t, (TerminParseAttr.CANBEGEOOBJECT if can_be_geo_object else TerminParseAttr.NO))
        if (tts is None): 
            return None
        res = list()
        dis = list()
        for tt in tts: 
            di = None
            if (isinstance(tt.termin, IntOntologyCollection.OntologyTermin)): 
                di = (tt.termin if isinstance(tt.termin, IntOntologyCollection.OntologyTermin) else None).owner
            if (di is not None): 
                if (di.referent is not None and referent_type_name is not None): 
                    if (di.referent.type_name != referent_type_name): 
                        continue
                if (di in dis): 
                    continue
                dis.append(di)
            res.append(IntOntologyToken._new503(tt.begin_token, tt.end_token, di, tt.termin, tt.morph))
        return (None if len(res) == 0 else res)
    
    def try_attach_by_item(self, item : 'IntOntologyItem') -> typing.List['IntOntologyItem']:
        """ Найти похожие онтологические объекты
        
        Args:
            item(IntOntologyItem): 
        
        """
        
        if (item is None): 
            return None
        res = None
        for t in item.termins: 
            li = self.__m_termins.try_attach(t)
            if (li is not None): 
                for tt in li: 
                    if (isinstance(tt, IntOntologyCollection.OntologyTermin)): 
                        oi = (tt if isinstance(tt, IntOntologyCollection.OntologyTermin) else None).owner
                        if (res is None): 
                            res = list()
                        if (not oi in res): 
                            res.append(oi)
        return res
    
    def try_attach_by_referent(self, referent : 'Referent', item : 'IntOntologyItem'=None, must_be_single : bool=False) -> typing.List['Referent']:
        """ Найти эквивалентные сущности через онтологические объекты
        
        Args:
            item(IntOntologyItem): 
            referent(Referent): 
        
        """
        from pullenti.ner.Referent import Referent
        if (referent is None): 
            return None
        if (item is None): 
            item = referent.create_ontology_item()
        if (item is None): 
            return None
        li = self.try_attach_by_item(item)
        if (li is None): 
            return None
        res = None
        for oi in li: 
            r = Utils.ifNotNull(oi.referent, (oi.tag if isinstance(oi.tag, Referent) else None))
            if (r is not None): 
                if (referent.can_be_equals(r, Referent.EqualType.WITHINONETEXT)): 
                    if (res is None): 
                        res = list()
                    if (not r in res): 
                        res.append(r)
        if (must_be_single): 
            if (res is not None and len(res) > 1): 
                i = 0
                while i < (len(res) - 1): 
                    for j in range(i + 1, len(res), 1):
                        if (not res[i].can_be_equals(res[j], Referent.EqualType.FORMERGING)): 
                            return None
                    i += 1
        return res
    
    def remove(self, r : 'Referent') -> None:
        """ Произвести привязку, если элемент найдётся, то установить ссылку на OntologyElement
        
        Args:
            referent: 
            mergeSlots: 
        
        Удалить всё, что связано с сущностью
            r(Referent): 
        """
        i = 0
        while i < len(self.__m_items): 
            if (self.__m_items[i].referent == r): 
                oi = self.__m_items[i]
                oi.referent = None
                r._int_ontology_item = None
                del self.__m_items[i]
                for t in oi.termins: 
                    self.__m_termins.remove(t)
                break
            i += 1

    
    @staticmethod
    def _new2613(_arg1 : bool) -> 'IntOntologyCollection':
        res = IntOntologyCollection()
        res.is_ext_ontology = _arg1
        return res