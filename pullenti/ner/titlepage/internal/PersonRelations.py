# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing

from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.titlepage.internal.TitleItemToken import TitleItemToken
from pullenti.ner.titlepage.TitlePageReferent import TitlePageReferent
from pullenti.ner.titlepage.internal.PersonRelation import PersonRelation

class PersonRelations:
    
    def __init__(self) -> None:
        self.rels = list()
    
    def add(self, pers : 'PersonReferent', typ : 'Types', coef : float) -> None:
        r = None
        for rr in self.rels: 
            if (rr.person == pers): 
                r = rr
                break
        if (r is None): 
            r = PersonRelation._new2650(pers)
            self.rels.append(r)
        if (not typ in r.coefs): 
            r.coefs[typ] = coef
        else: 
            r.coefs[typ] += coef
    
    def get_persons(self, typ : 'Types') -> typing.List['PersonReferent']:
        res = list()
        for v in self.rels: 
            if (v.best == typ): 
                res.append(v.person)
        return res
    
    @property
    def rel_types(self) -> typing.List['Types']:
        res = list()
        res.append(TitleItemToken.Types.WORKER)
        res.append(TitleItemToken.Types.BOSS)
        res.append(TitleItemToken.Types.EDITOR)
        res.append(TitleItemToken.Types.OPPONENT)
        res.append(TitleItemToken.Types.CONSULTANT)
        res.append(TitleItemToken.Types.ADOPT)
        res.append(TitleItemToken.Types.TRANSLATE)
        return res
    
    def get_attr_name_for_type(self, typ : 'Types') -> str:
        if (typ == TitleItemToken.Types.WORKER): 
            return TitlePageReferent.ATTR_AUTHOR
        if (typ == TitleItemToken.Types.BOSS): 
            return TitlePageReferent.ATTR_SUPERVISOR
        if (typ == TitleItemToken.Types.EDITOR): 
            return TitlePageReferent.ATTR_EDITOR
        if (typ == TitleItemToken.Types.OPPONENT): 
            return TitlePageReferent.ATTR_OPPONENT
        if (typ == TitleItemToken.Types.CONSULTANT): 
            return TitlePageReferent.ATTR_CONSULTANT
        if (typ == TitleItemToken.Types.ADOPT): 
            return TitlePageReferent.ATTR_AFFIRMANT
        if (typ == TitleItemToken.Types.TRANSLATE): 
            return TitlePageReferent.ATTR_TRANSLATOR
        return None
    
    def calc_typ_from_attrs(self, pers : 'PersonReferent') -> 'Types':
        for a in pers.slots: 
            if (a.type_name == PersonReferent.ATTR_ATTR): 
                s = str(a.value)
                if ("руководител" in s): 
                    return TitleItemToken.Types.BOSS
                if ("студент" in s or "слушател" in s): 
                    return TitleItemToken.Types.WORKER
                if ("редактор" in s or "рецензент" in s): 
                    return TitleItemToken.Types.EDITOR
                if ("консультант" in s): 
                    return TitleItemToken.Types.CONSULTANT
                if ("исполнитель" in s): 
                    return TitleItemToken.Types.WORKER
        return TitleItemToken.Types.UNDEFINED