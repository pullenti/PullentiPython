# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.decree.internal.MetaDecreePart import MetaDecreePart
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeReferent import DecreeReferent

class DecreePartReferent(Referent):
    """ Сущность, представляющая ссылку на структурную часть НПА
    
    """
    
    def __init__(self) -> None:
        super().__init__(DecreePartReferent.OBJ_TYPENAME)
        self.instance_of = MetaDecreePart.GLOBAL_META
    
    OBJ_TYPENAME = "DECREEPART"
    """ Имя типа сущности TypeName ("DECREEPART") """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование """
    
    ATTR_OWNER = "OWNER"
    """ Имя атрибута - владелец (DecreeReferent) """
    
    ATTR_LOCALTYP = "LOCALTYP"
    """ Имя атрибута - тип локального владельца (ст.10 этого закона) """
    
    ATTR_DOCPART = "DOCPART"
    """ Имя атрибута - часть документа (например, часть 1 Налогового кодекса) """
    
    ATTR_APPENDIX = "APPENDIX"
    """ Имя атрибута - приложение """
    
    ATTR_SECTION = "SECTION"
    """ Имя атрибута - раздел """
    
    ATTR_SUBSECTION = "SUBSECTION"
    """ Имя атрибута - подраздел """
    
    ATTR_CHAPTER = "CHAPTER"
    """ Имя атрибута - глава """
    
    ATTR_CLAUSE = "CLAUSE"
    """ Имя атрибута - статья """
    
    ATTR_PARAGRAPH = "PARAGRAPH"
    """ Имя атрибута - параграф """
    
    ATTR_SUBPARAGRAPH = "SUBPARAGRAPH"
    """ Имя атрибута - подпараграф """
    
    ATTR_PART = "PART"
    """ Имя атрибута - часть статьи (не путать с частью документа!) """
    
    ATTR_ITEM = "ITEM"
    """ Имя атрибута - пункт """
    
    ATTR_SUBITEM = "SUBITEM"
    """ Имя атрибута - подпункт """
    
    ATTR_INDENTION = "INDENTION"
    """ Имя атрибута - абзац """
    
    ATTR_SUBINDENTION = "SUBINDENTION"
    """ Имя атрибута - подабзац """
    
    ATTR_PREAMBLE = "PREAMPLE"
    """ Имя атрибута - преамбула """
    
    ATTR_NOTICE = "NOTICE"
    """ Имя атрибута - примечание """
    
    ATTR_SUBPROGRAM = "SUBPROGRAM"
    """ Имя атрибута - подпрограмма """
    
    ATTR_ADDAGREE = "ADDAGREE"
    """ Имя атрибута - дополнительное соглашение """
    
    ATTR_PAGE = "PAGE"
    """ Имя атрибута - страница """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        if (self.sub_indention is not None): 
            print(" подабз.{0}".format(self.sub_indention), end="", file=res, flush=True)
        if (self.indention is not None): 
            print(" абз.{0}".format(self.indention), end="", file=res, flush=True)
        if (self.notice is not None): 
            print(" прим.{0}".format(self.notice), end="", file=res, flush=True)
        if (self.sub_item is not None): 
            print(" пп.{0}".format(self.sub_item), end="", file=res, flush=True)
        if (self.item is not None): 
            print(" п.{0}".format(self.item), end="", file=res, flush=True)
        if (self.part is not None): 
            print(" ч.{0}".format(self.part), end="", file=res, flush=True)
        if (self.preamble is not None): 
            print(" преамб.{0}".format(("" if self.preamble == "0" else self.preamble)), end="", file=res, flush=True)
        if (self.page is not None): 
            print(" стр.{0}".format(self.page), end="", file=res, flush=True)
        if (self.clause is not None): 
            print(" ст.{0}".format(self.clause), end="", file=res, flush=True)
        if (self.sub_paragraph is not None): 
            print(" подпар.{0}".format(self.sub_paragraph), end="", file=res, flush=True)
        if (self.paragraph is not None): 
            print(" пар.{0}".format(self.paragraph), end="", file=res, flush=True)
        if (self.chapter is not None): 
            print(" гл.{0}".format(self.chapter), end="", file=res, flush=True)
        if (self.sub_section is not None): 
            print(" подразд.{0}".format(self.sub_section), end="", file=res, flush=True)
        if (self.section is not None): 
            print(" разд.{0}".format(self.section), end="", file=res, flush=True)
        if (self.doc_part is not None): 
            print(" док.часть {0}".format(self.doc_part), end="", file=res, flush=True)
        app = self.appendix
        if (app == "0"): 
            print(" приложение", end="", file=res)
        elif (app is not None): 
            print(" приложение {0}".format(app), end="", file=res, flush=True)
        if (self.subprogram is not None): 
            print(" подпрограмма \"{0}\"".format(Utils.ifNotNull(self.name, "?")), end="", file=res, flush=True)
        if (self.addagree is not None): 
            if (self.addagree == "0"): 
                print(" допсоглашение".format(), end="", file=res, flush=True)
            else: 
                print(" допсоглашение {0}".format(self.addagree), end="", file=res, flush=True)
        if (((self.owner is not None or res.tell() > 0)) and not short_variant): 
            if (not short_variant and self.subprogram is None): 
                s = self.__get_short_name()
                if (s is not None): 
                    print(" ({0})".format(s), end="", file=res, flush=True)
            if (self.owner is not None and (lev < 20)): 
                if (res.tell() > 0): 
                    print("; ", end="", file=res)
                print(self.owner.to_string(short_variant, lang, lev + 1), end="", file=res)
            elif (self.local_typ is not None): 
                print("; {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(self.local_typ)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    @property
    def name(self) -> str:
        """ Наименование (если несколько, то самое короткое) """
        nam = None
        for s in self.slots: 
            if (s.type_name == DecreePartReferent.ATTR_NAME): 
                n = str(s.value)
                if (nam is None or len(nam) > len(n)): 
                    nam = n
        return nam
    
    def __get_short_name(self) -> str:
        nam = self.name
        if (nam is None): 
            return None
        if (len(nam) > 100): 
            i = 100
            while i < len(nam): 
                if (not str.isalpha(nam[i])): 
                    break
                i += 1
            if (i < len(nam)): 
                nam = (nam[0:0+i] + "...")
        return MiscHelper.convert_first_char_upper_and_other_lower(nam)
    
    @property
    def local_typ(self) -> str:
        """ Локальный тип (при ссылке на текущий документ) """
        return self.get_string_value(DecreePartReferent.ATTR_LOCALTYP)
    @local_typ.setter
    def local_typ(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_LOCALTYP, value, True, 0)
        return value
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        from pullenti.ner.decree.internal.PartToken import PartToken
        tag_ = None
        if (isinstance(attr_value, PartToken.PartValue)): 
            tag_ = attr_value.source_value
            attr_value = (attr_value.value)
        s = super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
        if (tag_ is not None): 
            s.tag = tag_
        return s
    
    @property
    def clause(self) -> str:
        """ Статья """
        return self.get_string_value(DecreePartReferent.ATTR_CLAUSE)
    @clause.setter
    def clause(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_CLAUSE, value, True, 0)
        return value
    
    @property
    def part(self) -> str:
        """ Часть статьи """
        return self.get_string_value(DecreePartReferent.ATTR_PART)
    @part.setter
    def part(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_PART, value, True, 0)
        return value
    
    @property
    def doc_part(self) -> str:
        """ Часть документа (например, часть 2 Налогового кодекса) """
        return self.get_string_value(DecreePartReferent.ATTR_DOCPART)
    @doc_part.setter
    def doc_part(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_DOCPART, value, True, 0)
        return value
    
    @property
    def section(self) -> str:
        """ Раздел """
        return self.get_string_value(DecreePartReferent.ATTR_SECTION)
    @section.setter
    def section(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_SECTION, value, True, 0)
        return value
    
    @property
    def sub_section(self) -> str:
        """ Подраздел """
        return self.get_string_value(DecreePartReferent.ATTR_SUBSECTION)
    @sub_section.setter
    def sub_section(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_SUBSECTION, value, True, 0)
        return value
    
    @property
    def appendix(self) -> str:
        """ Приложение """
        return self.get_string_value(DecreePartReferent.ATTR_APPENDIX)
    @appendix.setter
    def appendix(self, value) -> str:
        if (value is not None and len(value) == 0): 
            value = "0"
        self.add_slot(DecreePartReferent.ATTR_APPENDIX, value, True, 0)
        return value
    
    @property
    def chapter(self) -> str:
        """ Глава """
        return self.get_string_value(DecreePartReferent.ATTR_CHAPTER)
    @chapter.setter
    def chapter(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_CHAPTER, value, True, 0)
        return value
    
    @property
    def paragraph(self) -> str:
        """ Параграф """
        return self.get_string_value(DecreePartReferent.ATTR_PARAGRAPH)
    @paragraph.setter
    def paragraph(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_PARAGRAPH, value, True, 0)
        return value
    
    @property
    def sub_paragraph(self) -> str:
        """ Подпараграф """
        return self.get_string_value(DecreePartReferent.ATTR_SUBPARAGRAPH)
    @sub_paragraph.setter
    def sub_paragraph(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_SUBPARAGRAPH, value, True, 0)
        return value
    
    @property
    def item(self) -> str:
        """ Пункт """
        return self.get_string_value(DecreePartReferent.ATTR_ITEM)
    @item.setter
    def item(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_ITEM, value, True, 0)
        return value
    
    @property
    def sub_item(self) -> str:
        """ Подпункт """
        return self.get_string_value(DecreePartReferent.ATTR_SUBITEM)
    @sub_item.setter
    def sub_item(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_SUBITEM, value, True, 0)
        return value
    
    @property
    def indention(self) -> str:
        """ Абзац """
        return self.get_string_value(DecreePartReferent.ATTR_INDENTION)
    @indention.setter
    def indention(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_INDENTION, value, True, 0)
        return value
    
    @property
    def sub_indention(self) -> str:
        """ Подабзац """
        return self.get_string_value(DecreePartReferent.ATTR_SUBINDENTION)
    @sub_indention.setter
    def sub_indention(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_SUBINDENTION, value, True, 0)
        return value
    
    @property
    def preamble(self) -> str:
        """ Преамбула """
        return self.get_string_value(DecreePartReferent.ATTR_PREAMBLE)
    @preamble.setter
    def preamble(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_PREAMBLE, value, True, 0)
        return value
    
    @property
    def notice(self) -> str:
        """ Примечание """
        return self.get_string_value(DecreePartReferent.ATTR_NOTICE)
    @notice.setter
    def notice(self, value) -> str:
        if (value is not None and len(value) == 0): 
            value = "0"
        self.add_slot(DecreePartReferent.ATTR_NOTICE, value, True, 0)
        return value
    
    @property
    def page(self) -> str:
        """ Страница """
        return self.get_string_value(DecreePartReferent.ATTR_PAGE)
    @page.setter
    def page(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_PAGE, value, True, 0)
        return value
    
    @property
    def subprogram(self) -> str:
        """ Подпрограмма """
        return self.get_string_value(DecreePartReferent.ATTR_SUBPROGRAM)
    @subprogram.setter
    def subprogram(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_SUBPROGRAM, value, True, 0)
        return value
    
    @property
    def addagree(self) -> str:
        """ Дополнительное соглашение """
        return self.get_string_value(DecreePartReferent.ATTR_ADDAGREE)
    @addagree.setter
    def addagree(self, value) -> str:
        self.add_slot(DecreePartReferent.ATTR_ADDAGREE, value, True, 0)
        return value
    
    @property
    def owner(self) -> 'DecreeReferent':
        """ НПА - владелец """
        res = Utils.asObjectOrNull(self.get_slot_value(DecreePartReferent.ATTR_OWNER), DecreeReferent)
        if (res is None): 
            return None
        return res
    @owner.setter
    def owner(self, value) -> 'DecreeReferent':
        self.add_slot(DecreePartReferent.ATTR_OWNER, value, True, 0)
        if (value is not None and self.local_typ is not None): 
            self.local_typ = None
        return value
    
    @property
    def parent_referent(self) -> 'Referent':
        return self.owner
    
    def _add_name(self, name_ : str) -> None:
        if (name_ is None or len(name_) == 0): 
            return
        if (name_[len(name_) - 1] == '.'): 
            name_ = name_[0:0+len(name_) - 1]
        name_ = name_.strip().upper()
        self.add_slot(DecreePartReferent.ATTR_NAME, name_, False, 0)
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)
        if (self.owner is not None and self.local_typ is not None): 
            self.local_typ = None
    
    def __get_level(self, typ : str) -> int:
        if (typ == DecreePartReferent.ATTR_ADDAGREE or typ == DecreePartReferent.ATTR_SUBPROGRAM): 
            return 0
        if (typ == DecreePartReferent.ATTR_DOCPART): 
            return 1
        if (typ == DecreePartReferent.ATTR_APPENDIX): 
            return 1
        if (typ == DecreePartReferent.ATTR_SECTION): 
            return 2
        if (typ == DecreePartReferent.ATTR_SUBSECTION): 
            return 3
        if (typ == DecreePartReferent.ATTR_CHAPTER): 
            return 4
        if (typ == DecreePartReferent.ATTR_PARAGRAPH): 
            return 5
        if (typ == DecreePartReferent.ATTR_SUBPARAGRAPH): 
            return 6
        if (typ == DecreePartReferent.ATTR_PAGE): 
            return 6
        if (typ == DecreePartReferent.ATTR_CLAUSE): 
            return 7
        if (typ == DecreePartReferent.ATTR_PREAMBLE): 
            return 8
        if (typ == DecreePartReferent.ATTR_PART): 
            return 8
        if (typ == DecreePartReferent.ATTR_ITEM): 
            return 9
        if (typ == DecreePartReferent.ATTR_NOTICE): 
            return 10
        if (typ == DecreePartReferent.ATTR_SUBITEM): 
            return 11
        if (typ == DecreePartReferent.ATTR_INDENTION): 
            return 12
        if (typ == DecreePartReferent.ATTR_SUBINDENTION): 
            return 13
        return -1
    
    def __has_less_level_attr(self, typ : str) -> bool:
        l_ = self.__get_level(typ)
        if (l_ < 0): 
            return False
        for s in self.slots: 
            l1 = self.__get_level(s.type_name)
            if (l1 >= 0 and l1 > l_): 
                return True
        return False
    
    def _add_high_level_info(self, dp : 'DecreePartReferent') -> None:
        # Добавить информацию о вышележащих элементах
        if (dp.addagree is not None and self.addagree is None): 
            self.addagree = dp.addagree
        elif (dp.addagree != self.addagree): 
            return
        if (dp.appendix is not None and self.appendix is None): 
            self.appendix = dp.appendix
        elif (self.appendix != dp.appendix): 
            return
        if (dp.doc_part is not None and self.doc_part is None): 
            self.doc_part = dp.doc_part
        elif (self.doc_part != dp.doc_part): 
            return
        if (dp.section is not None and self.section is None and self.__has_less_level_attr(DecreePartReferent.ATTR_SECTION)): 
            self.section = dp.section
        elif (self.section != dp.section): 
            return
        if (dp.sub_section is not None and self.sub_section is None and self.__has_less_level_attr(DecreePartReferent.ATTR_SUBSECTION)): 
            self.sub_section = dp.sub_section
        elif (self.sub_section != dp.sub_section): 
            return
        if (dp.chapter is not None and self.chapter is None and self.__has_less_level_attr(DecreePartReferent.ATTR_CHAPTER)): 
            self.chapter = dp.chapter
        elif (dp.chapter != self.chapter): 
            return
        if (dp.paragraph is not None and self.paragraph is None and self.__has_less_level_attr(DecreePartReferent.ATTR_PARAGRAPH)): 
            self.paragraph = dp.paragraph
        elif (self.paragraph != dp.paragraph): 
            return
        if (dp.sub_paragraph is not None and self.sub_paragraph is None and self.__has_less_level_attr(DecreePartReferent.ATTR_SUBPARAGRAPH)): 
            self.sub_paragraph = dp.sub_paragraph
        elif (self.sub_paragraph != dp.sub_paragraph): 
            return
        if (dp.clause is not None and self.clause is None and self.__has_less_level_attr(DecreePartReferent.ATTR_CLAUSE)): 
            self.clause = dp.clause
        elif (dp.clause != self.clause): 
            return
        if (dp.part is not None and self.part is None and self.__has_less_level_attr(DecreePartReferent.ATTR_PART)): 
            self.part = dp.part
        elif (dp.part != self.part): 
            return
        if (dp.item is not None and self.item is None and self.__has_less_level_attr(DecreePartReferent.ATTR_ITEM)): 
            if (self.sub_item is not None and self.sub_item.find('.') > 0): 
                pass
            else: 
                self.item = dp.item
        elif (dp.item != self.item): 
            return
        if (dp.sub_item is not None and self.sub_item is None and self.__has_less_level_attr(DecreePartReferent.ATTR_SUBITEM)): 
            self.sub_item = dp.sub_item
        elif (dp.sub_item != self.sub_item): 
            return
        if (dp.indention is not None and self.indention is None and self.__has_less_level_attr(DecreePartReferent.ATTR_INDENTION)): 
            self.indention = dp.indention
    
    def _is_all_items_less_level(self, upper_parts : 'Referent', ignore_equals : bool) -> bool:
        # Проверить, что все элементы находятся на более низком уровне, чем у аргумента
        if (isinstance(upper_parts, DecreeReferent)): 
            return True
        for s in self.slots: 
            l_ = self.__get_level(s.type_name)
            if (l_ < 0): 
                continue
            if (upper_parts.find_slot(s.type_name, None, True) is not None): 
                if (upper_parts.find_slot(s.type_name, s.value, True) is None): 
                    return False
                continue
            for ss in upper_parts.slots: 
                ll = self.__get_level(ss.type_name)
                if (ll >= l_): 
                    return False
        return True
    
    def _is_all_items_over_this_level(self, typ : 'ItemType') -> bool:
        from pullenti.ner.decree.internal.PartToken import PartToken
        l0 = self.__get_level(PartToken._get_attr_name_by_typ(typ))
        if (l0 <= 0): 
            return False
        for s in self.slots: 
            l_ = self.__get_level(s.type_name)
            if (l_ <= 0): 
                continue
            if (l_ >= l0): 
                return False
        return True
    
    def _get_min_level(self) -> int:
        min0_ = 0
        for s in self.slots: 
            l_ = self.__get_level(s.type_name)
            if (l_ <= 0): 
                continue
            if (min0_ == 0): 
                min0_ = l_
            elif (min0_ > l_): 
                min0_ = l_
        return min0_
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType') -> bool:
        b = self.__can_be_equals(obj, typ, False)
        return b
    
    def __can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType', ignore_geo : bool) -> bool:
        dr = Utils.asObjectOrNull(obj, DecreePartReferent)
        if (dr is None): 
            return False
        if (self.owner is not None and dr.owner is not None): 
            if (self.owner != dr.owner): 
                return False
        elif (typ == ReferentsEqualType.DIFFERENTTEXTS): 
            return False
        else: 
            ty1 = (self.local_typ if self.owner is None else self.owner.typ)
            ty2 = (dr.local_typ if dr.owner is None else dr.owner.typ)
            if (ty1 != ty2): 
                ty1 = (self.local_typ if self.owner is None else self.owner.typ0)
                ty2 = (dr.local_typ if dr.owner is None else dr.owner.typ0)
                if (ty1 != ty2): 
                    return False
        if (self.clause != dr.clause): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.clause is None or dr.clause is None))): 
                pass
            else: 
                return False
        if (self.part != dr.part): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.part is None or dr.part is None))): 
                pass
            else: 
                return False
        if (self.paragraph != dr.paragraph): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.paragraph is None or dr.paragraph is None))): 
                pass
            else: 
                return False
        if (self.sub_paragraph != dr.sub_paragraph): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.sub_paragraph is None or dr.sub_paragraph is None))): 
                pass
            else: 
                return False
        if (self.item != dr.item): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.item is None or dr.item is None))): 
                pass
            else: 
                return False
        if (self.sub_item != dr.sub_item): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.sub_item is None or dr.sub_item is None))): 
                pass
            else: 
                return False
        if (self.notice != dr.notice): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.notice is None or dr.notice is None))): 
                pass
            else: 
                return False
        if (self.indention != dr.indention): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.indention is None or dr.indention is None))): 
                pass
            else: 
                return False
        if (self.sub_indention != dr.sub_indention): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.sub_indention is None or dr.sub_indention is None))): 
                pass
            else: 
                return False
        if (self.appendix != dr.appendix): 
            if (self.appendix is not None and dr.appendix is not None): 
                return False
            if (self.clause is None and self.paragraph is None and self.item is None): 
                return False
        if (self.chapter != dr.chapter): 
            if (self.chapter is not None and dr.chapter is not None): 
                return False
            if (self.clause is None and self.paragraph is None and self.item is None): 
                return False
        if (self.section != dr.section): 
            if (self.section is not None and dr.section is not None): 
                return False
            if ((self.clause is None and self.paragraph is None and self.item is None) and self.sub_section is None): 
                return False
        if (self.sub_section != dr.sub_section): 
            if (self.sub_section is not None and dr.sub_section is not None): 
                return False
            if (self.clause is None and self.paragraph is None and self.item is None): 
                return False
        if (self.subprogram is not None or dr.subprogram is not None): 
            if (self.name != dr.name): 
                return False
            return True
        if (self.addagree is not None or dr.addagree is not None): 
            if (self.addagree != dr.addagree): 
                return False
        if (self.doc_part != dr.doc_part): 
            if (typ == ReferentsEqualType.FORMERGING and ((self.doc_part is None or dr.doc_part is None))): 
                pass
            else: 
                return False
        if (self.page != dr.page): 
            return False
        return True
    
    @staticmethod
    def create_range_referent(min0_ : 'DecreePartReferent', max0_ : 'DecreePartReferent') -> 'DecreePartReferent':
        res = Utils.asObjectOrNull(min0_.clone(), DecreePartReferent)
        cou = 0
        for s in res.slots: 
            ss = max0_.find_slot(s.type_name, None, True)
            if (ss is None): 
                return None
            if (ss.value == s.value): 
                continue
            if (max0_.find_slot(s.type_name, s.value, True) is not None): 
                continue
            cou += 1
            if (cou > 1): 
                return None
            res.upload_slot(s, "{0}-{1}".format(s.value, ss.value))
        if (cou != 1): 
            return None
        return res
    
    @staticmethod
    def _new1108(_arg1 : 'DecreeReferent') -> 'DecreePartReferent':
        res = DecreePartReferent()
        res.owner = _arg1
        return res