# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.person.internal.FioTemplateType import FioTemplateType
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.person.PersonPropertyKind import PersonPropertyKind
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.person.internal.PersonMorphCollection import PersonMorphCollection
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.IntOntologyItem import IntOntologyItem


class PersonReferent(Referent):
    """ Сущность, описывающее физическое лицо """
    
    def __init__(self) -> None:
        from pullenti.ner.person.internal.MetaPerson import MetaPerson
        super().__init__(PersonReferent.OBJ_TYPENAME)
        self._m_person_identity_typ = FioTemplateType.UNDEFINED
        self.__m_surname_occurs = list()
        self.__m_name_occurs = list()
        self.__m_sec_occurs = list()
        self.__m_ident_occurs = list()
        self.instance_of = MetaPerson._global_meta
    
    OBJ_TYPENAME = "PERSON"
    
    ATTR_SEX = "SEX"
    
    ATTR_IDENTITY = "IDENTITY"
    
    ATTR_FIRSTNAME = "FIRSTNAME"
    
    ATTR_MIDDLENAME = "MIDDLENAME"
    
    ATTR_LASTNAME = "LASTNAME"
    
    ATTR_NICKNAME = "NICKNAME"
    
    ATTR_ATTR = "ATTRIBUTE"
    
    ATTR_AGE = "AGE"
    
    ATTR_BORN = "BORN"
    
    ATTR_DIE = "DIE"
    
    ATTR_CONTACT = "CONTACT"
    
    ATTR_IDDOC = "IDDOC"
    
    @property
    def is_male(self) -> bool:
        """ Это мужчина """
        from pullenti.ner.person.internal.MetaPerson import MetaPerson
        return self.getStringValue(PersonReferent.ATTR_SEX) == MetaPerson.ATTR_SEXMALE
    @is_male.setter
    def is_male(self, value) -> bool:
        from pullenti.ner.person.internal.MetaPerson import MetaPerson
        self.addSlot(PersonReferent.ATTR_SEX, MetaPerson.ATTR_SEXMALE, True, 0)
        return value
    
    @property
    def is_female(self) -> bool:
        """ Это женщина """
        from pullenti.ner.person.internal.MetaPerson import MetaPerson
        return self.getStringValue(PersonReferent.ATTR_SEX) == MetaPerson.ATTR_SEXFEMALE
    @is_female.setter
    def is_female(self, value) -> bool:
        from pullenti.ner.person.internal.MetaPerson import MetaPerson
        self.addSlot(PersonReferent.ATTR_SEX, MetaPerson.ATTR_SEXFEMALE, True, 0)
        return value
    
    @property
    def age(self) -> int:
        """ Возраст """
        i = self.getIntValue(PersonReferent.ATTR_AGE, 0)
        if (i > 0): 
            return i
        return 0
    @age.setter
    def age(self, value) -> int:
        self.addSlot(PersonReferent.ATTR_AGE, str(value), True, 0)
        return value
    
    def _addContact(self, contact : 'Referent') -> None:
        for s in self.slots: 
            if (s.type_name == PersonReferent.ATTR_CONTACT): 
                r = Utils.asObjectOrNull(s.value, Referent)
                if (r is not None): 
                    if (r.canBeGeneralFor(contact)): 
                        self.uploadSlot(s, contact)
                        return
                    if (r.canBeEquals(contact, Referent.EqualType.WITHINONETEXT)): 
                        return
        self.addSlot(PersonReferent.ATTR_CONTACT, contact, False, 0)
    
    def __getPrefix(self) -> str:
        if (self.is_male): 
            return "г-н "
        if (self.is_female): 
            return "г-жа "
        return ""
    
    def __findForSurname(self, attr_name : str, surname : str, find_shortest : bool=False) -> str:
        rus = LanguageHelper.isCyrillicChar(surname[0])
        res = None
        for a in self.slots: 
            if (a.type_name == attr_name): 
                v = str(a.value)
                if (LanguageHelper.isCyrillicChar(v[0]) != rus): 
                    continue
                if (res is None): 
                    res = v
                elif (find_shortest and (len(v) < len(res))): 
                    res = v
        return res
    
    def __findShortestValue(self, attr_name : str) -> str:
        res = None
        for a in self.slots: 
            if (a.type_name == attr_name): 
                v = str(a.value)
                if (res is None or (len(v) < len(res))): 
                    res = v
        return res
    
    def __findShortestKingTitul(self, do_name : bool=False) -> str:
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        res = None
        for s in self.slots: 
            if (isinstance(s.value, PersonPropertyReferent)): 
                pr = Utils.asObjectOrNull(s.value, PersonPropertyReferent)
                if (pr.kind != PersonPropertyKind.KING): 
                    continue
                for ss in pr.slots: 
                    if (ss.type_name == PersonPropertyReferent.ATTR_NAME): 
                        n = Utils.asObjectOrNull(ss.value, str)
                        if (res is None): 
                            res = n
                        elif (len(res) > len(n)): 
                            res = n
        if (res is not None or not do_name): 
            return res
        return None
    
    def toSortString(self) -> str:
        sur = None
        for a in self.slots: 
            if (a.type_name == PersonReferent.ATTR_IDENTITY): 
                return str(a.value)
            elif (a.type_name == PersonReferent.ATTR_LASTNAME): 
                sur = str(a.value)
                break
        if (sur is None): 
            tit = self.__findShortestKingTitul(False)
            if (tit is None): 
                return "?"
            s = self.getStringValue(PersonReferent.ATTR_FIRSTNAME)
            if (s is None): 
                return "?"
            return "{0} {1}".format(tit, s)
        n = self.__findForSurname(PersonReferent.ATTR_FIRSTNAME, sur, False)
        if (n is None): 
            return sur
        else: 
            return "{0} {1}".format(sur, n)
    
    def getCompareStrings(self) -> typing.List[str]:
        res = list()
        for s in self.slots: 
            if (s.type_name == PersonReferent.ATTR_LASTNAME or s.type_name == PersonReferent.ATTR_IDENTITY): 
                res.append(str(s.value))
        tit = self.__findShortestKingTitul(False)
        if (tit is not None): 
            nam = self.getStringValue(PersonReferent.ATTR_FIRSTNAME)
            if (nam is not None): 
                res.append("{0} {1}".format(tit, nam))
        if (len(res) > 0): 
            return res
        else: 
            return super().getCompareStrings()
    
    SHOW_LASTNAME_ON_FIRST_POSITION = False
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (short_variant): 
            return self.__toShortString(lang)
        else: 
            res = self.__toFullString(PersonReferent.SHOW_LASTNAME_ON_FIRST_POSITION, lang)
            if (self.findSlot(PersonReferent.ATTR_NICKNAME, None, True) is None): 
                return res
            niks = self.getStringValues(PersonReferent.ATTR_NICKNAME)
            if (len(niks) == 1): 
                return "{0} ({1})".format(res, MiscHelper.convertFirstCharUpperAndOtherLower(niks[0]))
            tmp = io.StringIO()
            print(res, end="", file=tmp)
            print(" (", end="", file=tmp)
            for s in niks: 
                if (s != niks[0]): 
                    print(", ", end="", file=tmp)
                print(MiscHelper.convertFirstCharUpperAndOtherLower(s), end="", file=tmp)
            print(")", end="", file=tmp)
            return Utils.toStringStringIO(tmp)
    
    def __toShortString(self, lang : 'MorphLang') -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        id0_ = None
        for a in self.slots: 
            if (a.type_name == PersonReferent.ATTR_IDENTITY): 
                s = str(a.value)
                if (id0_ is None or (len(s) < len(id0_))): 
                    id0_ = s
        if (id0_ is not None): 
            return MiscHelper.convertFirstCharUpperAndOtherLower(id0_)
        n = self.getStringValue(PersonReferent.ATTR_LASTNAME)
        if (n is not None): 
            res = io.StringIO()
            print(n, end="", file=res)
            s = self.__findForSurname(PersonReferent.ATTR_FIRSTNAME, n, True)
            if (s is not None): 
                print(" {0}.".format(s[0]), end="", file=res, flush=True)
                s = self.__findForSurname(PersonReferent.ATTR_MIDDLENAME, n, False)
                if (s is not None): 
                    print("{0}.".format(s[0]), end="", file=res, flush=True)
            return MiscHelper.convertFirstCharUpperAndOtherLower(Utils.toStringStringIO(res))
        tit = self.__findShortestKingTitul(True)
        if (tit is not None): 
            nam = self.getStringValue(PersonReferent.ATTR_FIRSTNAME)
            if (nam is not None): 
                return MiscHelper.convertFirstCharUpperAndOtherLower("{0} {1}".format(tit, nam))
        return self.__toFullString(False, lang)
    
    def __toFullString(self, last_name_first : bool, lang : 'MorphLang') -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        id0_ = None
        for a in self.slots: 
            if (a.type_name == PersonReferent.ATTR_IDENTITY): 
                s = str(a.value)
                if (id0_ is None or len(s) > len(id0_)): 
                    id0_ = s
        if (id0_ is not None): 
            return MiscHelper.convertFirstCharUpperAndOtherLower(id0_)
        sss = self.getStringValue("NAMETYPE")
        if (sss == "china"): 
            last_name_first = True
        n = self.getStringValue(PersonReferent.ATTR_LASTNAME)
        if (n is not None): 
            res = io.StringIO()
            if (last_name_first): 
                print("{0} ".format(n), end="", file=res, flush=True)
            s = self.__findForSurname(PersonReferent.ATTR_FIRSTNAME, n, False)
            if (s is not None): 
                print("{0}".format(s), end="", file=res, flush=True)
                if (PersonReferent.__isInitial(s)): 
                    print('.', end="", file=res)
                else: 
                    print(' ', end="", file=res)
                s = self.__findForSurname(PersonReferent.ATTR_MIDDLENAME, n, False)
                if (s is not None): 
                    print("{0}".format(s), end="", file=res, flush=True)
                    if (PersonReferent.__isInitial(s)): 
                        print('.', end="", file=res)
                    else: 
                        print(' ', end="", file=res)
            if (not last_name_first): 
                print(n, end="", file=res)
            elif (Utils.getCharAtStringIO(res, res.tell() - 1) == ' '): 
                Utils.setLengthStringIO(res, res.tell() - 1)
            if (LanguageHelper.isCyrillicChar(n[0])): 
                nl = None
                for sl in self.slots: 
                    if (sl.type_name == PersonReferent.ATTR_LASTNAME): 
                        ss = Utils.asObjectOrNull(sl.value, str)
                        if (len(ss) > 0 and LanguageHelper.isLatinChar(ss[0])): 
                            nl = ss
                            break
                if (nl is not None): 
                    nal = self.__findForSurname(PersonReferent.ATTR_FIRSTNAME, nl, False)
                    if (nal is None): 
                        print(" ({0})".format(nl), end="", file=res, flush=True)
                    elif (PersonReferent.SHOW_LASTNAME_ON_FIRST_POSITION): 
                        print(" ({0} {1})".format(nl, nal), end="", file=res, flush=True)
                    else: 
                        print(" ({0} {1})".format(nal, nl), end="", file=res, flush=True)
            return MiscHelper.convertFirstCharUpperAndOtherLower(Utils.toStringStringIO(res))
        else: 
            n = self.getStringValue(PersonReferent.ATTR_FIRSTNAME)
            if ((n) is not None): 
                s = self.__findForSurname(PersonReferent.ATTR_MIDDLENAME, n, False)
                if (s is not None): 
                    n = "{0} {1}".format(n, s)
                n = MiscHelper.convertFirstCharUpperAndOtherLower(n)
                nik = self.getStringValue(PersonReferent.ATTR_NICKNAME)
                tit = self.__findShortestKingTitul(False)
                if (tit is not None): 
                    n = "{0} {1}".format(tit, n)
                if (nik is not None): 
                    n = "{0} {1}".format(n, nik)
                return n
        return "?"
    
    def _addFioIdentity(self, last_name : 'PersonMorphCollection', first_name : 'PersonMorphCollection', middle_name : object) -> None:
        if (last_name is not None): 
            if (last_name.number > 0): 
                num = NumberHelper.getNumberRoman(last_name.number)
                if (num is None): 
                    num = str(last_name.number)
                self.addSlot(PersonReferent.ATTR_NICKNAME, num, False, 0)
            else: 
                last_name.correct()
                self.__m_surname_occurs.append(last_name)
                for v in last_name.values: 
                    self.addSlot(PersonReferent.ATTR_LASTNAME, v, False, 0)
        if (first_name is not None): 
            first_name.correct()
            if (first_name.head is not None and len(first_name.head) > 2): 
                self.__m_name_occurs.append(first_name)
            for v in first_name.values: 
                self.addSlot(PersonReferent.ATTR_FIRSTNAME, v, False, 0)
            if (isinstance(middle_name, str)): 
                self.addSlot(PersonReferent.ATTR_MIDDLENAME, middle_name, False, 0)
            elif (isinstance(middle_name, PersonMorphCollection)): 
                mm = (Utils.asObjectOrNull(middle_name, PersonMorphCollection))
                if (mm.head is not None and len(mm.head) > 2): 
                    self.__m_sec_occurs.append(mm)
                for v in mm.values: 
                    self.addSlot(PersonReferent.ATTR_MIDDLENAME, v, False, 0)
        self._correctData()
    
    def _addIdentity(self, ident : 'PersonMorphCollection') -> None:
        if (ident is None): 
            return
        self.__m_ident_occurs.append(ident)
        for v in ident.values: 
            self.addSlot(PersonReferent.ATTR_IDENTITY, v, False, 0)
        self._correctData()
    
    @staticmethod
    def __isInitial(str0_ : str) -> bool:
        if (str0_ is None): 
            return False
        if (len(str0_) == 1): 
            return True
        if (str0_ == "ДЖ"): 
            return True
        return False
    
    def addAttribute(self, attr : object) -> None:
        self.addSlot(PersonReferent.ATTR_ATTR, attr, False, 0)
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        p = Utils.asObjectOrNull(obj, PersonReferent)
        if (p is None): 
            return False
        for a in self.slots: 
            if (a.type_name == PersonReferent.ATTR_IDENTITY): 
                for aa in p.slots: 
                    if (aa.type_name == a.type_name): 
                        if (PersonReferent._DelSurnameEnd(Utils.asObjectOrNull(a.value, str)) == PersonReferent._DelSurnameEnd(Utils.asObjectOrNull(aa.value, str))): 
                            return True
        nick1 = self.getStringValue(PersonReferent.ATTR_NICKNAME)
        nick2 = obj.getStringValue(PersonReferent.ATTR_NICKNAME)
        if (nick1 is not None and nick2 is not None): 
            if (nick1 != nick2): 
                return False
        if (self.findSlot(PersonReferent.ATTR_LASTNAME, None, True) is not None and p.findSlot(PersonReferent.ATTR_LASTNAME, None, True) is not None): 
            if (not self.__compareSurnamesPers(p)): 
                return False
            if (self.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is not None and p.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is not None): 
                if (not self.__checkNames(PersonReferent.ATTR_FIRSTNAME, p)): 
                    return False
                if (self.findSlot(PersonReferent.ATTR_MIDDLENAME, None, True) is not None and p.findSlot(PersonReferent.ATTR_MIDDLENAME, None, True) is not None): 
                    if (not self.__checkNames(PersonReferent.ATTR_MIDDLENAME, p)): 
                        return False
                elif (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    if (self.findSlot(PersonReferent.ATTR_MIDDLENAME, None, True) is not None or p.findSlot(PersonReferent.ATTR_MIDDLENAME, None, True) is not None): 
                        return str(self) == str(p)
                    names1 = list()
                    names2 = list()
                    for s in self.slots: 
                        if (s.type_name == PersonReferent.ATTR_FIRSTNAME): 
                            nam = str(s.value)
                            if (not PersonReferent.__isInitial(nam)): 
                                names1.append(nam)
                    for s in p.slots: 
                        if (s.type_name == PersonReferent.ATTR_FIRSTNAME): 
                            nam = str(s.value)
                            if (not PersonReferent.__isInitial(nam)): 
                                if (nam in names1): 
                                    return True
                                names2.append(nam)
                    if (len(names1) == 0 and len(names2) == 0): 
                        return True
                    return False
            elif (typ == Referent.EqualType.DIFFERENTTEXTS and ((self.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is not None or p.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is not None))): 
                return False
            return True
        tit1 = self.__findShortestKingTitul(False)
        tit2 = p.__findShortestKingTitul(False)
        if (((tit1 is not None or tit2 is not None)) or ((nick1 is not None and nick1 == nick2))): 
            if (tit1 is None or tit2 is None): 
                if (nick1 is not None and nick1 == nick2): 
                    pass
                else: 
                    return False
            elif (tit1 != tit2): 
                if (not tit2 in tit1 and not tit1 in tit2): 
                    return False
            if (self.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is not None and p.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is not None): 
                if (not self.__checkNames(PersonReferent.ATTR_FIRSTNAME, p)): 
                    return False
                return True
        return False
    
    def canBeGeneralFor(self, obj : 'Referent') -> bool:
        if (not self.canBeEquals(obj, Referent.EqualType.WITHINONETEXT)): 
            return False
        p = Utils.asObjectOrNull(obj, PersonReferent)
        if (p is None): 
            return False
        if (self.findSlot(PersonReferent.ATTR_LASTNAME, None, True) is None or p.findSlot(PersonReferent.ATTR_LASTNAME, None, True) is None): 
            return False
        if (not self.__compareSurnamesPers(p)): 
            return False
        if (self.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is None): 
            if (p.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is not None): 
                return True
            else: 
                return False
        if (p.findSlot(PersonReferent.ATTR_FIRSTNAME, None, True) is None): 
            return False
        if (not self.__checkNames(PersonReferent.ATTR_FIRSTNAME, p)): 
            return False
        if (self.findSlot(PersonReferent.ATTR_MIDDLENAME, None, True) is not None and p.findSlot(PersonReferent.ATTR_MIDDLENAME, None, True) is None): 
            if (not PersonReferent.__isInitial(self.getStringValue(PersonReferent.ATTR_FIRSTNAME))): 
                return False
        name_inits = 0
        name_fulls = 0
        sec_inits = 0
        sec_fulls = 0
        name_inits1 = 0
        name_fulls1 = 0
        sec_inits1 = 0
        sec_fulls1 = 0
        for s in self.slots: 
            if (s.type_name == PersonReferent.ATTR_FIRSTNAME): 
                if (PersonReferent.__isInitial(Utils.asObjectOrNull(s.value, str))): 
                    name_inits += 1
                else: 
                    name_fulls += 1
            elif (s.type_name == PersonReferent.ATTR_MIDDLENAME): 
                if (PersonReferent.__isInitial(Utils.asObjectOrNull(s.value, str))): 
                    sec_inits += 1
                else: 
                    sec_fulls += 1
        for s in p.slots: 
            if (s.type_name == PersonReferent.ATTR_FIRSTNAME): 
                if (PersonReferent.__isInitial(Utils.asObjectOrNull(s.value, str))): 
                    name_inits1 += 1
                else: 
                    name_fulls1 += 1
            elif (s.type_name == PersonReferent.ATTR_MIDDLENAME): 
                if (PersonReferent.__isInitial(Utils.asObjectOrNull(s.value, str))): 
                    sec_inits1 += 1
                else: 
                    sec_fulls1 += 1
        if (sec_fulls > 0): 
            return False
        if (name_inits == 0): 
            if (name_inits1 > 0): 
                return False
        elif (name_inits1 > 0): 
            if ((sec_inits + sec_fulls) > 0): 
                return False
        if (sec_inits == 0): 
            if ((sec_inits1 + sec_fulls1) == 0): 
                if (name_inits1 == 0 and name_inits > 0): 
                    return True
                else: 
                    return False
        elif (sec_inits1 > 0): 
            return False
        return True
    
    def __compareSurnamesPers(self, p : 'PersonReferent') -> bool:
        for a in self.slots: 
            if (a.type_name == PersonReferent.ATTR_LASTNAME): 
                s = str(a.value)
                for aa in p.slots: 
                    if (aa.type_name == a.type_name): 
                        ss = str(aa.value)
                        if (self.__compareSurnamesStrs(s, ss)): 
                            return True
        return False
    
    def __compareSurnamesStrs(self, s1 : str, s2 : str) -> bool:
        """ Сравнение с учётом возможных окончаний
        
        Args:
            s1(str): 
            s2(str): 
        
        """
        from pullenti.ner.core.MiscHelper import MiscHelper
        if (s1.startswith(s2) or s2.startswith(s1)): 
            return True
        if (PersonReferent._DelSurnameEnd(s1) == PersonReferent._DelSurnameEnd(s2)): 
            return True
        n1 = MiscHelper.getAbsoluteNormalValue(s1, False)
        if (n1 is not None): 
            if (n1 == MiscHelper.getAbsoluteNormalValue(s2, False)): 
                return True
        if (MiscHelper.canBeEquals(s1, s2, True, True, False)): 
            return True
        return False
    
    @staticmethod
    def _DelSurnameEnd(s : str) -> str:
        if (len(s) < 3): 
            return s
        if (LanguageHelper.endsWithEx(s, "А", "У", "Е", None)): 
            return s[0:0+len(s) - 1]
        if (LanguageHelper.endsWith(s, "ОМ") or LanguageHelper.endsWith(s, "ЫМ")): 
            return s[0:0+len(s) - 2]
        if (LanguageHelper.endsWithEx(s, "Я", "Ю", None, None)): 
            ch1 = s[len(s) - 2]
            if (ch1 == 'Н' or ch1 == 'Л'): 
                return s[0:0+len(s) - 1] + "Ь"
        return s
    
    def __checkNames(self, attr_name : str, p : 'PersonReferent') -> bool:
        from pullenti.ner.core.MiscHelper import MiscHelper
        names1 = list()
        inits1 = list()
        normn1 = list()
        for s in self.slots: 
            if (s.type_name == attr_name): 
                n = str(s.value)
                if (PersonReferent.__isInitial(n)): 
                    inits1.append(n)
                else: 
                    names1.append(n)
                    sn = MiscHelper.getAbsoluteNormalValue(n, False)
                    if (sn is not None): 
                        normn1.append(sn)
        names2 = list()
        inits2 = list()
        normn2 = list()
        for s in p.slots: 
            if (s.type_name == attr_name): 
                n = str(s.value)
                if (PersonReferent.__isInitial(n)): 
                    inits2.append(n)
                else: 
                    names2.append(n)
                    sn = MiscHelper.getAbsoluteNormalValue(n, False)
                    if (sn is not None): 
                        normn2.append(sn)
        if (len(names1) > 0 and len(names2) > 0): 
            for n in names1: 
                if (n in names2): 
                    return True
            for n in normn1: 
                if (n in normn2): 
                    return True
            return False
        if (len(inits1) > 0): 
            for n in inits1: 
                if (n in inits2): 
                    return True
                for nn in names2: 
                    if (nn.startswith(n)): 
                        return True
        if (len(inits2) > 0): 
            for n in inits2: 
                if (n in inits1): 
                    return True
                for nn in names1: 
                    if (nn.startswith(n)): 
                        return True
        return False
    
    def mergeSlots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().mergeSlots(obj, merge_statistic)
        p = Utils.asObjectOrNull(obj, PersonReferent)
        self.__m_surname_occurs.extend(p.__m_surname_occurs)
        self.__m_name_occurs.extend(p.__m_name_occurs)
        self.__m_sec_occurs.extend(p.__m_sec_occurs)
        self.__m_ident_occurs.extend(p.__m_ident_occurs)
        if (p._m_person_identity_typ != FioTemplateType.UNDEFINED): 
            self._m_person_identity_typ = p._m_person_identity_typ
        self._correctData()
    
    def _correctData(self) -> None:
        g = MorphGender.UNDEFINED
        while True:
            ch = False
            if (PersonMorphCollection.intersect(self.__m_surname_occurs)): 
                ch = True
            if (PersonMorphCollection.intersect(self.__m_name_occurs)): 
                ch = True
            if (PersonMorphCollection.intersect(self.__m_sec_occurs)): 
                ch = True
            if (PersonMorphCollection.intersect(self.__m_ident_occurs)): 
                ch = True
            if (not ch): 
                break
            if (g == MorphGender.UNDEFINED and len(self.__m_surname_occurs) > 0 and self.__m_surname_occurs[0].gender != MorphGender.UNDEFINED): 
                g = self.__m_surname_occurs[0].gender
            if (g == MorphGender.UNDEFINED and len(self.__m_name_occurs) > 0 and self.__m_name_occurs[0].gender != MorphGender.UNDEFINED): 
                g = self.__m_name_occurs[0].gender
            if (g == MorphGender.UNDEFINED and len(self.__m_ident_occurs) > 0 and self.__m_ident_occurs[0].gender != MorphGender.UNDEFINED): 
                g = self.__m_ident_occurs[0].gender
            if (g != MorphGender.UNDEFINED): 
                PersonMorphCollection.setGender(self.__m_surname_occurs, g)
                PersonMorphCollection.setGender(self.__m_name_occurs, g)
                PersonMorphCollection.setGender(self.__m_sec_occurs, g)
                PersonMorphCollection.setGender(self.__m_ident_occurs, g)
        if (g != MorphGender.UNDEFINED): 
            if (not self.is_female and not self.is_male): 
                if (g == MorphGender.MASCULINE): 
                    self.is_male = True
                else: 
                    self.is_female = True
        self.__correctSurnames()
        self.__correctIdentifiers()
        self.__correctAttrs()
        self.__removeSlots(PersonReferent.ATTR_LASTNAME, self.__m_surname_occurs)
        self.__removeSlots(PersonReferent.ATTR_FIRSTNAME, self.__m_name_occurs)
        self.__removeSlots(PersonReferent.ATTR_MIDDLENAME, self.__m_sec_occurs)
        self.__removeSlots(PersonReferent.ATTR_IDENTITY, self.__m_ident_occurs)
        self.__removeInitials(PersonReferent.ATTR_FIRSTNAME)
        self.__removeInitials(PersonReferent.ATTR_MIDDLENAME)
    
    def __correctSurnames(self) -> None:
        if (not self.is_male and not self.is_female): 
            return
        i = 0
        while i < len(self.slots): 
            if (self.slots[i].type_name == PersonReferent.ATTR_LASTNAME): 
                s = str(self.slots[i].value)
                j = i + 1
                while j < len(self.slots): 
                    if (self.slots[j].type_name == PersonReferent.ATTR_LASTNAME): 
                        s1 = str(self.slots[j].value)
                        if (s != s1 and PersonReferent._DelSurnameEnd(s) == PersonReferent._DelSurnameEnd(s1) and len(s1) != len(s)): 
                            if (self.is_male): 
                                s = PersonReferent._DelSurnameEnd(s)
                                self.uploadSlot(self.slots[i], s)
                                del self.slots[j]
                                j -= 1
                            else: 
                                del self.slots[i]
                                i -= 1
                                break
                    j += 1
            i += 1
    
    def __correctIdentifiers(self) -> None:
        if (self.is_female): 
            return
        i = 0
        while i < len(self.slots): 
            if (self.slots[i].type_name == PersonReferent.ATTR_IDENTITY): 
                s = str(self.slots[i].value)
                j = i + 1
                while j < len(self.slots): 
                    if (self.slots[j].type_name == PersonReferent.ATTR_IDENTITY): 
                        s1 = str(self.slots[j].value)
                        if (s != s1 and PersonReferent._DelSurnameEnd(s) == PersonReferent._DelSurnameEnd(s1)): 
                            s = PersonReferent._DelSurnameEnd(s)
                            self.uploadSlot(self.slots[i], s)
                            del self.slots[j]
                            j -= 1
                            self.is_male = True
                    j += 1
            i += 1
    
    def __removeSlots(self, attr_name : str, cols : typing.List['PersonMorphCollection']) -> None:
        vars0_ = list()
        for col in cols: 
            for v in col.values: 
                if (not v in vars0_): 
                    vars0_.append(v)
        if (len(vars0_) < 1): 
            return
        for i in range(len(self.slots) - 1, -1, -1):
            if (self.slots[i].type_name == attr_name): 
                v = str(self.slots[i].value)
                if (not v in vars0_): 
                    j = 0
                    first_pass3127 = True
                    while True:
                        if first_pass3127: first_pass3127 = False
                        else: j += 1
                        if (not (j < len(self.slots))): break
                        if (j != i and self.slots[j].type_name == self.slots[i].type_name): 
                            if (attr_name == PersonReferent.ATTR_LASTNAME): 
                                ee = False
                                for vv in vars0_: 
                                    if (self.__compareSurnamesStrs(v, vv)): 
                                        ee = True
                                if (not ee): 
                                    continue
                            del self.slots[i]
                            break
    
    def __removeInitials(self, attr_name : str) -> None:
        for s in self.slots: 
            if (s.type_name == attr_name): 
                if (PersonReferent.__isInitial(str(s.value))): 
                    for ss in self.slots: 
                        if (ss.type_name == s.type_name and s != ss): 
                            v = str(ss.value)
                            if (not PersonReferent.__isInitial(v) and v.startswith(str(s.value))): 
                                if (attr_name == PersonReferent.ATTR_FIRSTNAME and len(v) == 2 and self.findSlot(PersonReferent.ATTR_MIDDLENAME, v[1:], True) is not None): 
                                    self.slots.remove(ss)
                                else: 
                                    self.slots.remove(s)
                                return
    
    def __correctAttrs(self) -> None:
        from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
        attrs = list()
        for s in self.slots: 
            if (s.type_name == PersonReferent.ATTR_ATTR and (isinstance(s.value, PersonPropertyReferent))): 
                attrs.append(Utils.asObjectOrNull(s.value, PersonPropertyReferent))
        if (len(attrs) < 2): 
            return
        for a in attrs: 
            a.tag = None
        i = 0
        while i < (len(attrs) - 1): 
            j = i + 1
            while j < len(attrs): 
                if (attrs[i].general_referent == attrs[j] or attrs[j].canBeGeneralFor(attrs[i])): 
                    attrs[j].tag = attrs[i]
                elif (attrs[j].general_referent == attrs[i] or attrs[i].canBeGeneralFor(attrs[j])): 
                    attrs[i].tag = attrs[j]
                j += 1
            i += 1
        for i in range(len(self.slots) - 1, -1, -1):
            if (self.slots[i].type_name == PersonReferent.ATTR_ATTR and (isinstance(self.slots[i].value, PersonPropertyReferent))): 
                if ((Utils.asObjectOrNull(self.slots[i].value, PersonPropertyReferent)).tag is not None): 
                    pr = Utils.asObjectOrNull((Utils.asObjectOrNull(self.slots[i].value, PersonPropertyReferent)).tag, PersonPropertyReferent)
                    if (pr is not None and pr.general_referent is None): 
                        pr.general_referent = Utils.asObjectOrNull(self.slots[i].value, PersonPropertyReferent)
                    del self.slots[i]
    
    def createOntologyItem(self) -> 'IntOntologyItem':
        from pullenti.ner.core.Termin import Termin
        oi = IntOntologyItem(self)
        tit = self.__findShortestKingTitul(False)
        for a in self.slots: 
            if (a.type_name == PersonReferent.ATTR_IDENTITY): 
                oi.termins.append(Termin._new2473(str(a.value), True))
            elif (a.type_name == PersonReferent.ATTR_LASTNAME): 
                t = Termin(str(a.value))
                if (len(t.terms) > 20): 
                    pass
                if (self.is_male): 
                    t.gender = MorphGender.MASCULINE
                elif (self.is_female): 
                    t.gender = MorphGender.FEMINIE
                oi.termins.append(t)
            elif (a.type_name == PersonReferent.ATTR_FIRSTNAME and tit is not None): 
                t = Termin("{0} {1}".format(tit, str(a.value)))
                if (self.is_male): 
                    t.gender = MorphGender.MASCULINE
                elif (self.is_female): 
                    t.gender = MorphGender.FEMINIE
                oi.termins.append(t)
        return oi