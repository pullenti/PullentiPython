# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType

class AnalyzerData:
    """ Данные, полученные в ходе обработки одним анализатором. Каждый анализатор сохраняет в своём класса свои данные,
    получаемые в ходе анализа. В конце процессор объединяет их все. Получить экземпляр, связанный с анализатором,
    можно методом AnalyzerKit.GetAnalyzerDataByAnalyzerName.
    Данные анализа
    """
    
    def __init__(self) -> None:
        self.kit = None;
        self._m_referents = list()
        self.__m_reg_ref_level = 0
        self.overflow_level = 0
    
    @property
    def referents(self) -> typing.List['Referent']:
        """ Список выделенных сущностей Referent """
        return self._m_referents
    @referents.setter
    def referents(self, value) -> typing.List['Referent']:
        self._m_referents.clear()
        if (value is not None): 
            self._m_referents.extend(value)
        return value
    
    def register_referent(self, referent : 'Referent') -> 'Referent':
        """ Зарегистрировать новую сущность или привязать к существующей сущности. Сущности, получаемые в ходе анализа,
        должны сохраняться через эту функцию. Именно здесь решается задача кореференции, то есть объединения
        сущностей, соответствующих одному и тому же объекту текста.
        
        Args:
            referent(Referent): сохраняемая сущность
        
        Returns:
            Referent: этот же экземпляр referent или другой, если удалось объединиться с ранее выделенной сущностью
        """
        if (referent is None): 
            return None
        if (referent._m_ext_referents is not None): 
            if (self.__m_reg_ref_level > 2): 
                pass
            else: 
                for rt in referent._m_ext_referents: 
                    old_ref = rt.referent
                    self.__m_reg_ref_level += 1
                    rt.save_to_local_ontology()
                    self.__m_reg_ref_level -= 1
                    if (old_ref == rt.referent or rt.referent is None): 
                        continue
                    for s in referent.slots: 
                        if (s.value == old_ref): 
                            referent.upload_slot(s, rt.referent)
                    if (referent._m_ext_referents is not None): 
                        for rtt in referent._m_ext_referents: 
                            for s in rtt.referent.slots: 
                                if (s.value == old_ref): 
                                    referent.upload_slot(s, rt.referent)
                referent._m_ext_referents = (None)
        eq = None
        if (referent in self._m_referents): 
            return referent
        i = len(self._m_referents) - 1
        while i >= 0 and ((len(self._m_referents) - i) < 1000): 
            p = self._m_referents[i]
            if (p.can_be_equals(referent, ReferentsEqualType.WITHINONETEXT)): 
                if (not p.can_be_general_for(referent) and not referent.can_be_general_for(p)): 
                    if (eq is None): 
                        eq = list()
                    eq.append(p)
            i -= 1
        if (eq is not None): 
            if (len(eq) == 1): 
                eq[0].merge_slots(referent, True)
                return eq[0]
            if (len(eq) > 1): 
                for e0_ in eq: 
                    if (len(e0_.slots) != len(referent.slots)): 
                        continue
                    ok = True
                    for s in referent.slots: 
                        if (e0_.find_slot(s.type_name, s.value, True) is None): 
                            ok = False
                            break
                    if (ok): 
                        for s in e0_.slots: 
                            if (referent.find_slot(s.type_name, s.value, True) is None): 
                                ok = False
                                break
                    if (ok): 
                        return e0_
        self._m_referents.append(referent)
        return referent
    
    def remove_referent(self, r : 'Referent') -> None:
        """ Удалить сущность из списка
        
        Args:
            r(Referent): удаляемая сущность
        """
        if (r in self._m_referents): 
            self._m_referents.remove(r)