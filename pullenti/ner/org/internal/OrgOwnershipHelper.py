# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.org.OrganizationKind import OrganizationKind
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent

class OrgOwnershipHelper:
    
    @staticmethod
    def can_be_higher(higher : 'OrganizationReferent', lower : 'OrganizationReferent', robust : bool=False) -> bool:
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
        if (higher.can_be_equals(lower, ReferentsEqualType.WITHINONETEXT)): 
            return False
        if (lower.higher is None and lower.find_slot(OrganizationReferent.ATTR_HIGHER, None, True) is not None): 
            return False
        htyps = higher.types
        ltyps = lower.types
        if (hk != OrganizationKind.BANK): 
            for v in htyps: 
                if (v in ltyps): 
                    return False
        if (hk != OrganizationKind.DEPARTMENT and lk == OrganizationKind.DEPARTMENT): 
            if (OrgOwnershipHelper.__contains(ltyps, "курс", None) or OrgOwnershipHelper.__contains(ltyps, "группа", "група")): 
                return hk == OrganizationKind.STUDY or OrgOwnershipHelper.__contains(htyps, "институт", "інститут")
            if (OrgOwnershipHelper.__contains(ltyps, "епархия", "єпархія") or OrgOwnershipHelper.__contains(ltyps, "патриархия", "патріархія")): 
                return hk == OrganizationKind.CHURCH
            if (hk == OrganizationKind.UNDEFINED): 
                if (OrgOwnershipHelper.__contains(htyps, "управление", "управління")): 
                    return False
            return True
        if (lower.contains_profile(OrgProfile.UNIT) or OrgOwnershipHelper.__contains(ltyps, "department", None)): 
            if (not higher.contains_profile(OrgProfile.UNIT) and lk != OrganizationKind.DEPARTMENT): 
                return True
        if (OrgOwnershipHelper.__contains(htyps, "правительство", "уряд")): 
            if (lk == OrganizationKind.GOVENMENT): 
                return ((("агентство" in ltyps or "федеральная служба" in ltyps or "федеральна служба" in ltyps) or "департамент" in ltyps or "комиссия" in ltyps) or "комитет" in ltyps or "комісія" in ltyps) or "комітет" in ltyps
        if (hk == OrganizationKind.GOVENMENT): 
            if (lk == OrganizationKind.GOVENMENT): 
                if (OrgOwnershipHelper.__contains(ltyps, "комиссия", "комісія") or OrgOwnershipHelper.__contains(ltyps, "инспекция", "інспекція") or OrgOwnershipHelper.__contains(ltyps, "комитет", "комітет")): 
                    if ((not OrgOwnershipHelper.__contains(htyps, "комиссия", "комісія") and not OrgOwnershipHelper.__contains(htyps, "инспекция", "інспекція") and not OrgOwnershipHelper.__contains(ltyps, "государственный комитет", None)) and not OrgOwnershipHelper.__contains(htyps, "комитет", "комітет") and ((not OrgOwnershipHelper.__contains(htyps, "совет", "рада") or "Верховн" in str(higher)))): 
                        return True
                if (higher.find_slot(OrganizationReferent.ATTR_NAME, "ФЕДЕРАЛЬНОЕ СОБРАНИЕ", True) is not None or "конгресс" in htyps or "парламент" in htyps): 
                    if ((lower.find_slot(OrganizationReferent.ATTR_NAME, "СОВЕТ ФЕДЕРАЦИИ", True) is not None or lower.find_slot(OrganizationReferent.ATTR_NAME, "ГОСУДАРСТВЕННАЯ ДУМА", True) is not None or lower.find_slot(OrganizationReferent.ATTR_NAME, "ВЕРХОВНА РАДА", True) is not None) or OrgOwnershipHelper.__contains(ltyps, "палата", None) or OrgOwnershipHelper.__contains(ltyps, "совет", None)): 
                        return True
                if (higher.find_slot(OrganizationReferent.ATTR_NAME, "ФСБ", True) is not None): 
                    if (lower.find_slot(OrganizationReferent.ATTR_NAME, "ФПС", True) is not None): 
                        return True
                if (OrgOwnershipHelper.__contains(htyps, "государственный комитет", None)): 
                    if ((OrgOwnershipHelper.__contains(ltyps, "комиссия", "комісія") or OrgOwnershipHelper.__contains(ltyps, "инспекция", "інспекція") or OrgOwnershipHelper.__contains(ltyps, "комитет", "комітет")) or OrgOwnershipHelper.__contains(ltyps, "департамент", None)): 
                        return True
            elif (lk == OrganizationKind.UNDEFINED): 
                if ((OrgOwnershipHelper.__contains(ltyps, "комиссия", "комісія") or OrgOwnershipHelper.__contains(ltyps, "инспекция", "інспекція") or OrgOwnershipHelper.__contains(ltyps, "комитет", "комітет")) or OrgOwnershipHelper.__contains(ltyps, "управление", "управління") or OrgOwnershipHelper.__contains(ltyps, "служба", None)): 
                    return True
            elif (lk == OrganizationKind.BANK): 
                pass
        if (OrgOwnershipHelper.__contains(htyps, "министерство", "міністерство")): 
            if ((((((OrgOwnershipHelper.__contains(ltyps, "институт", "інститут") or OrgOwnershipHelper.__contains(ltyps, "университет", "університет") or OrgOwnershipHelper.__contains(ltyps, "училище", None)) or OrgOwnershipHelper.__contains(ltyps, "школа", None) or OrgOwnershipHelper.__contains(ltyps, "лицей", "ліцей")) or OrgOwnershipHelper.__contains(ltyps, "НИИ", "НДІ") or OrgOwnershipHelper.__contains(ltyps, "Ф", None)) or OrgOwnershipHelper.__contains(ltyps, "департамент", None) or OrgOwnershipHelper.__contains(ltyps, "управление", "управління")) or OrgOwnershipHelper.__contains(ltyps, "комитет", "комітет") or OrgOwnershipHelper.__contains(ltyps, "комиссия", "комісія")) or OrgOwnershipHelper.__contains(ltyps, "инспекция", "інспекція") or OrgOwnershipHelper.__contains(ltyps, "центр", None)): 
                return True
            if (OrgOwnershipHelper.__contains(ltyps, "академия", "академія")): 
                pass
            if (OrgOwnershipHelper.__contains(ltyps, "служба", None) and not OrgOwnershipHelper.__contains(ltyps, "федеральная служба", "федеральна служба")): 
                return True
            if (lk == OrganizationKind.CULTURE or lk == OrganizationKind.MEDICAL): 
                return True
        if (OrgOwnershipHelper.__contains(htyps, "академия", "академія")): 
            if (OrgOwnershipHelper.__contains(ltyps, "институт", "інститут") or OrgOwnershipHelper.__contains(ltyps, "научн", "науков") or OrgOwnershipHelper.__contains(ltyps, "НИИ", "НДІ")): 
                return True
        if (OrgOwnershipHelper.__contains(htyps, "факультет", None)): 
            if (OrgOwnershipHelper.__contains(ltyps, "курс", None) or OrgOwnershipHelper.__contains(ltyps, "кафедра", None)): 
                return True
        if (OrgOwnershipHelper.__contains(htyps, "university", None)): 
            if (OrgOwnershipHelper.__contains(ltyps, "school", None) or OrgOwnershipHelper.__contains(ltyps, "college", None)): 
                return True
        hr = OrgOwnershipHelper.__military_rank(htyps)
        lr = OrgOwnershipHelper.__military_rank(ltyps)
        if (hr > 0): 
            if (lr > 0): 
                return hr < lr
            elif (hr == 3 and (("войсковая часть" in ltyps or "військова частина" in ltyps))): 
                return True
        elif ("войсковая часть" in htyps or "військова частина" in htyps): 
            if (lr >= 6): 
                return True
        if (lr >= 6): 
            if (higher.contains_profile(OrgProfile.POLICY) or higher.contains_profile(OrgProfile.UNION)): 
                return True
        if (hk == OrganizationKind.STUDY or OrgOwnershipHelper.__contains(htyps, "институт", "інститут") or OrgOwnershipHelper.__contains(htyps, "академия", "академія")): 
            if (((OrgOwnershipHelper.__contains(ltyps, "магистратура", "магістратура") or OrgOwnershipHelper.__contains(ltyps, "аспирантура", "аспірантура") or OrgOwnershipHelper.__contains(ltyps, "докторантура", None)) or OrgOwnershipHelper.__contains(ltyps, "факультет", None) or OrgOwnershipHelper.__contains(ltyps, "кафедра", None)) or OrgOwnershipHelper.__contains(ltyps, "курс", None)): 
                return True
        if (hk != OrganizationKind.DEPARTMENT): 
            if (((((OrgOwnershipHelper.__contains(ltyps, "департамент", None) or OrgOwnershipHelper.__contains(ltyps, "центр", None))) and hk != OrganizationKind.MEDICAL and hk != OrganizationKind.SCIENCE) and not OrgOwnershipHelper.__contains(htyps, "центр", None) and not OrgOwnershipHelper.__contains(htyps, "департамент", None)) and not OrgOwnershipHelper.__contains(htyps, "управление", "управління")): 
                return True
            if (OrgOwnershipHelper.__contains(htyps, "департамент", None) or robust): 
                if (OrgOwnershipHelper.__contains(ltyps, "центр", None)): 
                    return True
                if (lk == OrganizationKind.STUDY): 
                    return True
            if (OrgOwnershipHelper.__contains(htyps, "служба", None) or OrgOwnershipHelper.__contains(htyps, "штаб", None)): 
                if (OrgOwnershipHelper.__contains(ltyps, "управление", "управління")): 
                    return True
            if (hk == OrganizationKind.BANK): 
                if (OrgOwnershipHelper.__contains(ltyps, "управление", "управління") or OrgOwnershipHelper.__contains(ltyps, "департамент", None)): 
                    return True
            if (hk == OrganizationKind.PARTY or hk == OrganizationKind.FEDERATION): 
                if (OrgOwnershipHelper.__contains(ltyps, "комитет", "комітет")): 
                    return True
            if ((lk == OrganizationKind.FEDERATION and hk != OrganizationKind.FEDERATION and hk != OrganizationKind.GOVENMENT) and hk != OrganizationKind.PARTY): 
                if (not OrgOwnershipHelper.__contains(htyps, "фонд", None) and hk != OrganizationKind.UNDEFINED): 
                    return True
        elif (OrgOwnershipHelper.__contains(htyps, "управление", "управління") or OrgOwnershipHelper.__contains(htyps, "департамент", None)): 
            if (not OrgOwnershipHelper.__contains(ltyps, "управление", "управління") and not OrgOwnershipHelper.__contains(ltyps, "департамент", None) and lk == OrganizationKind.DEPARTMENT): 
                return True
            if (OrgOwnershipHelper.__contains(htyps, "главное", "головне") and OrgOwnershipHelper.__contains(htyps, "управление", "управління")): 
                if (OrgOwnershipHelper.__contains(ltyps, "департамент", None)): 
                    return True
                if (OrgOwnershipHelper.__contains(ltyps, "управление", "управління")): 
                    if (not "главное управление" in ltyps and not "головне управління" in ltyps and not "пограничное управление" in ltyps): 
                        return True
            if (OrgOwnershipHelper.__contains(htyps, "управление", "управління") and OrgOwnershipHelper.__contains(ltyps, "центр", None)): 
                return True
            if (OrgOwnershipHelper.__contains(htyps, "департамент", None) and OrgOwnershipHelper.__contains(ltyps, "управление", "управління")): 
                return True
        elif ((lk == OrganizationKind.GOVENMENT and OrgOwnershipHelper.__contains(ltyps, "служба", None) and higher.higher is not None) and higher.higher.kind == OrganizationKind.GOVENMENT): 
            return True
        elif (OrgOwnershipHelper.__contains(htyps, "отдел", "відділ") and lk == OrganizationKind.DEPARTMENT and ((OrgOwnershipHelper.__contains(ltyps, "стол", "стіл") or OrgOwnershipHelper.__contains(ltyps, "направление", "напрямок") or OrgOwnershipHelper.__contains(ltyps, "отделение", "відділ")))): 
            return True
        if (hk == OrganizationKind.BANK): 
            if ("СБЕРЕГАТЕЛЬНЫЙ БАНК" in higher.names): 
                if (lk == OrganizationKind.BANK and not "СБЕРЕГАТЕЛЬНЫЙ БАНК" in lower.names): 
                    return True
        if (lk == OrganizationKind.MEDICAL): 
            if ("департамент" in htyps): 
                return True
        if (lk == OrganizationKind.DEPARTMENT): 
            if (hk == OrganizationKind.DEPARTMENT and higher.higher is not None and len(htyps) == 0): 
                if (OrgOwnershipHelper.can_be_higher(higher.higher, lower, False)): 
                    if (OrgOwnershipHelper.__contains(ltyps, "управление", "управління") or OrgOwnershipHelper.__contains(ltyps, "отдел", "відділ")): 
                        return True
            if (OrgOwnershipHelper.__contains(ltyps, "офис", "офіс")): 
                if (OrgOwnershipHelper.__contains(htyps, "филиал", "філіал") or OrgOwnershipHelper.__contains(htyps, "отделение", "відділення")): 
                    return True
        if (OrgOwnershipHelper.__contains(ltyps, "управление", "управління") or OrgOwnershipHelper.__contains(ltyps, "отдел", "відділ")): 
            str0_ = higher.to_string(True, None, 0)
            if (Utils.startsWithString(str0_, "ГУ", True)): 
                return True
        return False
    
    @staticmethod
    def __military_rank(li : typing.List[str]) -> int:
        if (OrgOwnershipHelper.__contains(li, "фронт", None)): 
            return 1
        if (OrgOwnershipHelper.__contains(li, "группа армий", "група армій")): 
            return 2
        if (OrgOwnershipHelper.__contains(li, "армия", "армія")): 
            return 3
        if (OrgOwnershipHelper.__contains(li, "корпус", None)): 
            return 4
        if (OrgOwnershipHelper.__contains(li, "округ", None)): 
            return 5
        if (OrgOwnershipHelper.__contains(li, "дивизия", "дивізія")): 
            return 6
        if (OrgOwnershipHelper.__contains(li, "бригада", None)): 
            return 7
        if (OrgOwnershipHelper.__contains(li, "полк", None)): 
            return 8
        if (OrgOwnershipHelper.__contains(li, "батальон", "батальйон") or OrgOwnershipHelper.__contains(li, "дивизион", "дивізіон")): 
            return 9
        if (OrgOwnershipHelper.__contains(li, "рота", None) or OrgOwnershipHelper.__contains(li, "батарея", None) or OrgOwnershipHelper.__contains(li, "эскадрон", "ескадрон")): 
            return 10
        if (OrgOwnershipHelper.__contains(li, "взвод", None) or OrgOwnershipHelper.__contains(li, "отряд", "загін")): 
            return 11
        return -1
    
    @staticmethod
    def __contains(li : typing.List[str], v : str, v2 : str=None) -> bool:
        for l_ in li: 
            if (v in l_): 
                return True
        if (v2 is not None): 
            for l_ in li: 
                if (v2 in l_): 
                    return True
        return False