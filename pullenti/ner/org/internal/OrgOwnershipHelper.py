# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing

from pullenti.ner.org.OrganizationKind import OrganizationKind
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.Referent import Referent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent

class OrgOwnershipHelper:
    
    @staticmethod
    def canBeHigher(higher : 'OrganizationReferent', lower : 'OrganizationReferent', robust : bool=False) -> bool:
        """ Проверка на отношения "вышестоящий - нижестоящий"
        
        Args:
            higher(OrganizationReferent): 
            lower(OrganizationReferent): 
        
        """
        if (higher is None or lower is None or higher == lower): 
            return False
        if (lower.owner is not None): 
            return False
        hk = higher.kind
        lk = lower.kind
        if (higher.canBeEquals(lower, Referent.EqualType.WITHINONETEXT)): 
            return False
        if (lower.higher is None and lower.findSlot(OrganizationReferent.ATTR_HIGHER, None, True) is not None): 
            return False
        htyps = higher.types
        ltyps = lower.types
        if (hk != OrganizationKind.BANK): 
            for v in htyps: 
                if (v in ltyps): 
                    return False
        if (hk != OrganizationKind.DEPARTMENT and lk == OrganizationKind.DEPARTMENT): 
            if (OrgOwnershipHelper.__Contains(ltyps, "курс", None) or OrgOwnershipHelper.__Contains(ltyps, "группа", "група")): 
                return hk == OrganizationKind.STUDY or OrgOwnershipHelper.__Contains(htyps, "институт", "інститут")
            if (OrgOwnershipHelper.__Contains(ltyps, "епархия", "єпархія") or OrgOwnershipHelper.__Contains(ltyps, "патриархия", "патріархія")): 
                return hk == OrganizationKind.CHURCH
            if (hk == OrganizationKind.UNDEFINED): 
                if (OrgOwnershipHelper.__Contains(htyps, "управление", "управління")): 
                    return False
            return True
        if (lower.containsProfile(OrgProfile.UNIT) or OrgOwnershipHelper.__Contains(ltyps, "department", None)): 
            if (not higher.containsProfile(OrgProfile.UNIT) and lk != OrganizationKind.DEPARTMENT): 
                return True
        if (OrgOwnershipHelper.__Contains(htyps, "правительство", "уряд")): 
            if (lk == OrganizationKind.GOVENMENT): 
                return ((("агентство" in ltyps or "федеральная служба" in ltyps or "федеральна служба" in ltyps) or "департамент" in ltyps or "комиссия" in ltyps) or "комитет" in ltyps or "комісія" in ltyps) or "комітет" in ltyps
        if (hk == OrganizationKind.GOVENMENT): 
            if (lk == OrganizationKind.GOVENMENT): 
                if (OrgOwnershipHelper.__Contains(ltyps, "комиссия", "комісія") or OrgOwnershipHelper.__Contains(ltyps, "инспекция", "інспекція") or OrgOwnershipHelper.__Contains(ltyps, "комитет", "комітет")): 
                    if ((not OrgOwnershipHelper.__Contains(htyps, "комиссия", "комісія") and not OrgOwnershipHelper.__Contains(htyps, "инспекция", "інспекція") and not OrgOwnershipHelper.__Contains(ltyps, "государственный комитет", None)) and not OrgOwnershipHelper.__Contains(htyps, "комитет", "комітет") and ((not OrgOwnershipHelper.__Contains(htyps, "совет", "рада") or "Верховн" in str(higher)))): 
                        return True
                if (higher.findSlot(OrganizationReferent.ATTR_NAME, "ФЕДЕРАЛЬНОЕ СОБРАНИЕ", True) is not None or "конгресс" in htyps or "парламент" in htyps): 
                    if ((lower.findSlot(OrganizationReferent.ATTR_NAME, "СОВЕТ ФЕДЕРАЦИИ", True) is not None or lower.findSlot(OrganizationReferent.ATTR_NAME, "ГОСУДАРСТВЕННАЯ ДУМА", True) is not None or lower.findSlot(OrganizationReferent.ATTR_NAME, "ВЕРХОВНА РАДА", True) is not None) or OrgOwnershipHelper.__Contains(ltyps, "палата", None) or OrgOwnershipHelper.__Contains(ltyps, "совет", None)): 
                        return True
                if (higher.findSlot(OrganizationReferent.ATTR_NAME, "ФСБ", True) is not None): 
                    if (lower.findSlot(OrganizationReferent.ATTR_NAME, "ФПС", True) is not None): 
                        return True
                if (OrgOwnershipHelper.__Contains(htyps, "государственный комитет", None)): 
                    if ((OrgOwnershipHelper.__Contains(ltyps, "комиссия", "комісія") or OrgOwnershipHelper.__Contains(ltyps, "инспекция", "інспекція") or OrgOwnershipHelper.__Contains(ltyps, "комитет", "комітет")) or OrgOwnershipHelper.__Contains(ltyps, "департамент", None)): 
                        return True
            elif (lk == OrganizationKind.UNDEFINED): 
                if ((OrgOwnershipHelper.__Contains(ltyps, "комиссия", "комісія") or OrgOwnershipHelper.__Contains(ltyps, "инспекция", "інспекція") or OrgOwnershipHelper.__Contains(ltyps, "комитет", "комітет")) or OrgOwnershipHelper.__Contains(ltyps, "управление", "управління") or OrgOwnershipHelper.__Contains(ltyps, "служба", None)): 
                    return True
            elif (lk == OrganizationKind.BANK): 
                pass
        if (OrgOwnershipHelper.__Contains(htyps, "министерство", "міністерство")): 
            if ((((((OrgOwnershipHelper.__Contains(ltyps, "институт", "інститут") or OrgOwnershipHelper.__Contains(ltyps, "университет", "університет") or OrgOwnershipHelper.__Contains(ltyps, "училище", None)) or OrgOwnershipHelper.__Contains(ltyps, "школа", None) or OrgOwnershipHelper.__Contains(ltyps, "лицей", "ліцей")) or OrgOwnershipHelper.__Contains(ltyps, "НИИ", "НДІ") or OrgOwnershipHelper.__Contains(ltyps, "Ф", None)) or OrgOwnershipHelper.__Contains(ltyps, "департамент", None) or OrgOwnershipHelper.__Contains(ltyps, "управление", "управління")) or OrgOwnershipHelper.__Contains(ltyps, "комитет", "комітет") or OrgOwnershipHelper.__Contains(ltyps, "комиссия", "комісія")) or OrgOwnershipHelper.__Contains(ltyps, "инспекция", "інспекція") or OrgOwnershipHelper.__Contains(ltyps, "центр", None)): 
                return True
            if (OrgOwnershipHelper.__Contains(ltyps, "академия", "академія")): 
                pass
            if (OrgOwnershipHelper.__Contains(ltyps, "служба", None) and not OrgOwnershipHelper.__Contains(ltyps, "федеральная служба", "федеральна служба")): 
                return True
            if (lk == OrganizationKind.CULTURE or lk == OrganizationKind.MEDICAL): 
                return True
        if (OrgOwnershipHelper.__Contains(htyps, "академия", "академія")): 
            if (OrgOwnershipHelper.__Contains(ltyps, "институт", "інститут") or OrgOwnershipHelper.__Contains(ltyps, "научн", "науков") or OrgOwnershipHelper.__Contains(ltyps, "НИИ", "НДІ")): 
                return True
        if (OrgOwnershipHelper.__Contains(htyps, "факультет", None)): 
            if (OrgOwnershipHelper.__Contains(ltyps, "курс", None) or OrgOwnershipHelper.__Contains(ltyps, "кафедра", None)): 
                return True
        if (OrgOwnershipHelper.__Contains(htyps, "university", None)): 
            if (OrgOwnershipHelper.__Contains(ltyps, "school", None) or OrgOwnershipHelper.__Contains(ltyps, "college", None)): 
                return True
        hr = OrgOwnershipHelper.__militaryRank(htyps)
        if (hr > 0): 
            lr = OrgOwnershipHelper.__militaryRank(ltyps)
            if (lr > 0): 
                return hr < lr
            elif (hr == 3 and (("войсковая часть" in ltyps or "військова частина" in ltyps))): 
                return True
        elif ("войсковая часть" in htyps or "військова частина" in htyps): 
            lr = OrgOwnershipHelper.__militaryRank(ltyps)
            if (lr >= 6): 
                return True
        if (hk == OrganizationKind.STUDY or OrgOwnershipHelper.__Contains(htyps, "институт", "інститут") or OrgOwnershipHelper.__Contains(htyps, "академия", "академія")): 
            if (((OrgOwnershipHelper.__Contains(ltyps, "магистратура", "магістратура") or OrgOwnershipHelper.__Contains(ltyps, "аспирантура", "аспірантура") or OrgOwnershipHelper.__Contains(ltyps, "докторантура", None)) or OrgOwnershipHelper.__Contains(ltyps, "факультет", None) or OrgOwnershipHelper.__Contains(ltyps, "кафедра", None)) or OrgOwnershipHelper.__Contains(ltyps, "курс", None)): 
                return True
        if (hk != OrganizationKind.DEPARTMENT): 
            if (((((OrgOwnershipHelper.__Contains(ltyps, "департамент", None) or OrgOwnershipHelper.__Contains(ltyps, "центр", None))) and hk != OrganizationKind.MEDICAL and hk != OrganizationKind.SCIENCE) and not OrgOwnershipHelper.__Contains(htyps, "центр", None) and not OrgOwnershipHelper.__Contains(htyps, "департамент", None)) and not OrgOwnershipHelper.__Contains(htyps, "управление", "управління")): 
                return True
            if (OrgOwnershipHelper.__Contains(htyps, "департамент", None) or robust): 
                if (OrgOwnershipHelper.__Contains(ltyps, "центр", None)): 
                    return True
                if (lk == OrganizationKind.STUDY): 
                    return True
            if (OrgOwnershipHelper.__Contains(htyps, "служба", None) or OrgOwnershipHelper.__Contains(htyps, "штаб", None)): 
                if (OrgOwnershipHelper.__Contains(ltyps, "управление", "управління")): 
                    return True
            if (hk == OrganizationKind.BANK): 
                if (OrgOwnershipHelper.__Contains(ltyps, "управление", "управління") or OrgOwnershipHelper.__Contains(ltyps, "департамент", None)): 
                    return True
            if (hk == OrganizationKind.PARTY or hk == OrganizationKind.FEDERATION): 
                if (OrgOwnershipHelper.__Contains(ltyps, "комитет", "комітет")): 
                    return True
            if ((lk == OrganizationKind.FEDERATION and hk != OrganizationKind.FEDERATION and hk != OrganizationKind.GOVENMENT) and hk != OrganizationKind.PARTY): 
                if (not OrgOwnershipHelper.__Contains(htyps, "фонд", None) and hk != OrganizationKind.UNDEFINED): 
                    return True
        elif (OrgOwnershipHelper.__Contains(htyps, "управление", "управління") or OrgOwnershipHelper.__Contains(htyps, "департамент", None)): 
            if (not OrgOwnershipHelper.__Contains(ltyps, "управление", "управління") and not OrgOwnershipHelper.__Contains(ltyps, "департамент", None) and lk == OrganizationKind.DEPARTMENT): 
                return True
            if (OrgOwnershipHelper.__Contains(htyps, "главное", "головне") and OrgOwnershipHelper.__Contains(htyps, "управление", "управління")): 
                if (OrgOwnershipHelper.__Contains(ltyps, "департамент", None)): 
                    return True
                if (OrgOwnershipHelper.__Contains(ltyps, "управление", "управління")): 
                    if (not "главное управление" in ltyps and not "головне управління" in ltyps and not "пограничное управление" in ltyps): 
                        return True
            if (OrgOwnershipHelper.__Contains(htyps, "управление", "управління") and OrgOwnershipHelper.__Contains(ltyps, "центр", None)): 
                return True
            if (OrgOwnershipHelper.__Contains(htyps, "департамент", None) and OrgOwnershipHelper.__Contains(ltyps, "управление", "управління")): 
                return True
        elif ((lk == OrganizationKind.GOVENMENT and OrgOwnershipHelper.__Contains(ltyps, "служба", None) and higher.higher is not None) and higher.higher.kind == OrganizationKind.GOVENMENT): 
            return True
        elif (OrgOwnershipHelper.__Contains(htyps, "отдел", "відділ") and lk == OrganizationKind.DEPARTMENT and ((OrgOwnershipHelper.__Contains(ltyps, "стол", "стіл") or OrgOwnershipHelper.__Contains(ltyps, "направление", "напрямок")))): 
            return True
        if (hk == OrganizationKind.BANK): 
            if ("СБЕРЕГАТЕЛЬНЫЙ БАНК" in higher.names): 
                if (lk == OrganizationKind.BANK and not "СБЕРЕГАТЕЛЬНЫЙ БАНК" in lower.names): 
                    return True
        if (lk == OrganizationKind.MEDICAL): 
            if ("департамент" in htyps): 
                return True
        return False
    
    @staticmethod
    def __militaryRank(li : typing.List[str]) -> int:
        if (OrgOwnershipHelper.__Contains(li, "фронт", None)): 
            return 1
        if (OrgOwnershipHelper.__Contains(li, "группа армий", "група армій")): 
            return 2
        if (OrgOwnershipHelper.__Contains(li, "армия", "армія")): 
            return 3
        if (OrgOwnershipHelper.__Contains(li, "корпус", None)): 
            return 4
        if (OrgOwnershipHelper.__Contains(li, "округ", None)): 
            return 5
        if (OrgOwnershipHelper.__Contains(li, "дивизия", "дивізія")): 
            return 6
        if (OrgOwnershipHelper.__Contains(li, "бригада", None)): 
            return 7
        if (OrgOwnershipHelper.__Contains(li, "полк", None)): 
            return 8
        if (OrgOwnershipHelper.__Contains(li, "батальон", "батальйон") or OrgOwnershipHelper.__Contains(li, "дивизион", "дивізіон")): 
            return 9
        if (OrgOwnershipHelper.__Contains(li, "рота", None) or OrgOwnershipHelper.__Contains(li, "батарея", None) or OrgOwnershipHelper.__Contains(li, "эскадрон", "ескадрон")): 
            return 10
        if (OrgOwnershipHelper.__Contains(li, "взвод", None) or OrgOwnershipHelper.__Contains(li, "отряд", "загін")): 
            return 11
        return -1
    
    @staticmethod
    def __Contains(li : typing.List[str], v : str, v2 : str=None) -> bool:
        for l_ in li: 
            if (v in l_): 
                return True
        if (v2 is not None): 
            for l_ in li: 
                if (v2 in l_): 
                    return True
        return False