# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphMiscInfo import MorphMiscInfo
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphWordForm import MorphWordForm

class MorphCollection(MorphBaseInfo):
    """ Коллекция морфологических вариантов
    Морфология токена
    """
    
    def __init__(self, source : 'MorphCollection'=None) -> None:
        super().__init__()
        self.__m_class = MorphClass()
        self.__m_gender = MorphGender.UNDEFINED
        self.__m_number = MorphNumber.UNDEFINED
        self.__m_case = MorphCase()
        self.__m_language = MorphLang()
        self.__m_voice = MorphVoice.UNDEFINED
        self.__m_need_recalc = True
        self.__m_items = None
        if (source is None): 
            return
        for it in source.items: 
            mi = None
            if (isinstance(it, MorphWordForm)): 
                wf = MorphWordForm()
                wf.copy_from_word_form(Utils.asObjectOrNull(it, MorphWordForm))
                mi = (wf)
            else: 
                mi = MorphBaseInfo()
                mi.copy_from(it)
            if (self.__m_items is None): 
                self.__m_items = list()
            self.__m_items.append(mi)
        self.__m_class = MorphClass._new53(source.__m_class.value)
        self.__m_gender = source.__m_gender
        self.__m_case = MorphCase._new29(source.__m_case.value)
        self.__m_number = source.__m_number
        self.__m_language = MorphLang._new56(source.__m_language.value)
        self.__m_voice = source.__m_voice
        self.__m_need_recalc = False
    
    def __str__(self) -> str:
        res = super().__str__()
        if (self.voice != MorphVoice.UNDEFINED): 
            if (self.voice == MorphVoice.ACTIVE): 
                res += " действ.з."
            elif (self.voice == MorphVoice.PASSIVE): 
                res += " страд.з."
            elif (self.voice == MorphVoice.MIDDLE): 
                res += " сред. з."
        return res
    
    def clone(self) -> 'MorphCollection':
        """ Создать копию
        
        """
        res = MorphCollection()
        if (self.__m_items is not None): 
            res.__m_items = list()
            try: 
                res.__m_items.extend(self.__m_items)
            except Exception as ex: 
                pass
        if (not self.__m_need_recalc): 
            res.__m_class = MorphClass._new53(self.__m_class.value)
            res.__m_gender = self.__m_gender
            res.__m_case = MorphCase._new29(self.__m_case.value)
            res.__m_number = self.__m_number
            res.__m_language = MorphLang._new56(self.__m_language.value)
            res.__m_need_recalc = False
            res.__m_voice = self.__m_voice
        return res
    
    @property
    def items_count(self) -> int:
        """ Количество морфологических вариантов """
        return (0 if self.__m_items is None else len(self.__m_items))
    
    def get_indexer_item(self, ind : int) -> 'MorphBaseInfo':
        if (self.__m_items is None or (ind < 0) or ind >= len(self.__m_items)): 
            return None
        else: 
            return self.__m_items[ind]
    
    __m_empty_items = None
    
    @property
    def items(self) -> typing.List['MorphBaseInfo']:
        """ Морфологические варианты """
        return Utils.ifNotNull(self.__m_items, MorphCollection.__m_empty_items)
    
    def add_item(self, item : 'MorphBaseInfo') -> None:
        if (self.__m_items is None): 
            self.__m_items = list()
        self.__m_items.append(item)
        self.__m_need_recalc = True
    
    def insert_item(self, ind : int, item : 'MorphBaseInfo') -> None:
        if (self.__m_items is None): 
            self.__m_items = list()
        self.__m_items.insert(ind, item)
        self.__m_need_recalc = True
    
    def remove_item(self, o : object) -> None:
        if (isinstance(o, int)): 
            self.__remove_item_int(o)
        elif (isinstance(o, MorphBaseInfo)): 
            self.__remove_item_morph_base_info(Utils.asObjectOrNull(o, MorphBaseInfo))
    
    def __remove_item_int(self, i : int) -> None:
        if (self.__m_items is not None and i >= 0 and (i < len(self.__m_items))): 
            del self.__m_items[i]
            self.__m_need_recalc = True
    
    def __remove_item_morph_base_info(self, item : 'MorphBaseInfo') -> None:
        if (self.__m_items is not None and item in self.__m_items): 
            self.__m_items.remove(item)
            self.__m_need_recalc = True
    
    def __recalc(self) -> None:
        self.__m_need_recalc = False
        if (self.__m_items is None or len(self.__m_items) == 0): 
            return
        self.__m_class = MorphClass()
        self.__m_gender = MorphGender.UNDEFINED
        g = self.__m_gender == MorphGender.UNDEFINED
        self.__m_number = MorphNumber.UNDEFINED
        n = self.__m_number == MorphNumber.UNDEFINED
        self.__m_case = MorphCase()
        ca = self.__m_case.is_undefined
        la = self.__m_language is None or self.__m_language.is_undefined
        self.__m_voice = MorphVoice.UNDEFINED
        verb_has_undef = False
        if (self.__m_items is not None): 
            for it in self.__m_items: 
                self.__m_class.value |= it.class0_.value
                if (g): 
                    self.__m_gender = (Utils.valToEnum((self.__m_gender) | (it.gender), MorphGender))
                if (ca): 
                    self.__m_case |= it.case_
                if (n): 
                    self.__m_number = (Utils.valToEnum((self.__m_number) | (it.number), MorphNumber))
                if (la): 
                    self.__m_language.value |= it.language.value
                if (it.class0_.is_verb): 
                    if (isinstance(it, MorphWordForm)): 
                        v = it.misc.voice
                        if (v == MorphVoice.UNDEFINED): 
                            verb_has_undef = True
                        else: 
                            self.__m_voice = (Utils.valToEnum((self.__m_voice) | (v), MorphVoice))
        if (verb_has_undef): 
            self.__m_voice = MorphVoice.UNDEFINED
    
    @property
    def class0_(self) -> 'MorphClass':
        if (self.__m_need_recalc): 
            self.__recalc()
        return self.__m_class
    @class0_.setter
    def class0_(self, value) -> 'MorphClass':
        self.__m_class = value
        return value
    
    @property
    def case_(self) -> 'MorphCase':
        if (self.__m_need_recalc): 
            self.__recalc()
        return self.__m_case
    @case_.setter
    def case_(self, value) -> 'MorphCase':
        self.__m_case = value
        return value
    
    @property
    def gender(self) -> 'MorphGender':
        if (self.__m_need_recalc): 
            self.__recalc()
        return self.__m_gender
    @gender.setter
    def gender(self, value) -> 'MorphGender':
        self.__m_gender = value
        return value
    
    @property
    def number(self) -> 'MorphNumber':
        if (self.__m_need_recalc): 
            self.__recalc()
        return self.__m_number
    @number.setter
    def number(self, value) -> 'MorphNumber':
        self.__m_number = value
        return value
    
    @property
    def language(self) -> 'MorphLang':
        if (self.__m_need_recalc): 
            self.__recalc()
        return self.__m_language
    @language.setter
    def language(self, value) -> 'MorphLang':
        self.__m_language = value
        return value
    
    @property
    def voice(self) -> 'MorphVoice':
        """ Залог (для глаголов) """
        if (self.__m_need_recalc): 
            self.__recalc()
        return self.__m_voice
    @voice.setter
    def voice(self, value) -> 'MorphVoice':
        if (self.__m_need_recalc): 
            self.__recalc()
        self.__m_voice = value
        return value
    
    def contains_attr(self, attr_value : str, cla : 'MorphClass'=None) -> bool:
        for it in self.items: 
            if (cla is not None and cla.value != (0) and (((it.class0_.value) & (cla.value))) == 0): 
                continue
            if (it.contains_attr(attr_value, cla)): 
                return True
        return False
    
    def check_accord(self, v : 'MorphBaseInfo', ignore_gender : bool=False, ignore_number : bool=False) -> bool:
        for it in self.items: 
            if (isinstance(v, MorphCollection)): 
                if (v.check_accord(it, ignore_gender, ignore_number)): 
                    return True
            elif (it.check_accord(v, ignore_gender, ignore_number)): 
                return True
        if (len(self.items) > 0): 
            return False
        return super().check_accord(v, ignore_gender, ignore_number)
    
    def check(self, cl : 'MorphClass') -> bool:
        return (((self.class0_.value) & (cl.value))) != 0
    
    def remove_items(self, it : object, eq : bool=False) -> None:
        """ Удалить элементы, не соответствующие элементу
        
        Args:
            it(object): 
        """
        if (isinstance(it, MorphCase)): 
            self.__remove_items_morph_case(it)
        elif (isinstance(it, MorphClass)): 
            self.__remove_items_morph_class(it, eq)
        elif (isinstance(it, MorphBaseInfo)): 
            self.__remove_items_morph_base_info(it)
        elif (isinstance(it, MorphNumber)): 
            self.__remove_items_morph_number(Utils.valToEnum(it, MorphNumber))
        elif (isinstance(it, MorphGender)): 
            self._remove_items_morph_gender(Utils.valToEnum(it, MorphGender))
    
    def __remove_items_morph_case(self, cas : 'MorphCase') -> None:
        if (self.__m_items is None): 
            return
        if (len(self.__m_items) == 0): 
            self.__m_case = ((self.__m_case) & cas)
        for i in range(len(self.__m_items) - 1, -1, -1):
            if (((self.__m_items[i].case_) & cas).is_undefined): 
                del self.__m_items[i]
                self.__m_need_recalc = True
            elif ((((self.__m_items[i].case_) & cas)) != self.__m_items[i].case_): 
                if (isinstance(self.__m_items[i], MorphWordForm)): 
                    wf = MorphWordForm()
                    wf.copy_from_word_form(Utils.asObjectOrNull(self.__m_items[i], MorphWordForm))
                    wf.case_ = (wf.case_) & cas
                    self.__m_items[i] = (wf)
                else: 
                    bi = MorphBaseInfo()
                    bi.copy_from(self.__m_items[i])
                    bi.case_ = (bi.case_) & cas
                    self.__m_items[i] = bi
                self.__m_need_recalc = True
        self.__m_need_recalc = True
    
    def __remove_items_morph_class(self, cl : 'MorphClass', eq : bool) -> None:
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            ok = False
            if ((((self.__m_items[i].class0_.value) & (cl.value))) == 0): 
                ok = True
            elif (eq and self.__m_items[i].class0_.value != cl.value): 
                ok = True
            if (ok): 
                del self.__m_items[i]
                self.__m_need_recalc = True
        self.__m_need_recalc = True
    
    def __remove_items_morph_base_info(self, inf : 'MorphBaseInfo') -> None:
        if (self.__m_items is None): 
            return
        if (len(self.__m_items) == 0): 
            if (inf.gender != MorphGender.UNDEFINED): 
                self.__m_gender = (Utils.valToEnum((self.__m_gender) & (inf.gender), MorphGender))
            if (inf.number != MorphNumber.UNDEFINED): 
                self.__m_number = (Utils.valToEnum((self.__m_number) & (inf.number), MorphNumber))
            if (not inf.case_.is_undefined): 
                self.__m_case &= inf.case_
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            ok = True
            it = self.__m_items[i]
            if (inf.gender != MorphGender.UNDEFINED): 
                if (((it.gender) & (inf.gender)) == (MorphGender.UNDEFINED)): 
                    ok = False
            ch_num = False
            if (inf.number != MorphNumber.PLURAL and inf.number != MorphNumber.UNDEFINED): 
                if (((it.number) & (inf.number)) == (MorphNumber.UNDEFINED)): 
                    ok = False
                ch_num = True
            if (not inf.class0_.is_undefined): 
                if (((inf.class0_) & it.class0_).is_undefined): 
                    ok = False
            if (not inf.case_.is_undefined): 
                if (((inf.case_) & it.case_).is_undefined): 
                    ok = False
            if (not ok): 
                del self.__m_items[i]
                self.__m_need_recalc = True
            else: 
                if (not inf.case_.is_undefined): 
                    if (it.case_ != (((inf.case_) & it.case_))): 
                        it.case_ = ((inf.case_) & it.case_)
                        self.__m_need_recalc = True
                if (inf.gender != MorphGender.UNDEFINED): 
                    if ((it.gender) != ((inf.gender) & (it.gender))): 
                        it.gender = Utils.valToEnum((inf.gender) & (it.gender), MorphGender)
                        self.__m_need_recalc = True
                if (ch_num): 
                    if ((it.number) != ((inf.number) & (it.number))): 
                        it.number = Utils.valToEnum((inf.number) & (it.number), MorphNumber)
                        self.__m_need_recalc = True
    
    def remove_items_by_preposition(self, prep : 'Token') -> None:
        """ Убрать элементы, не соответствующие по падежу предлогу
        
        Args:
            prep(Token): 
        """
        from pullenti.ner.TextToken import TextToken
        if (not (isinstance(prep, TextToken))): 
            return
        mc = LanguageHelper.get_case_after_preposition(prep.lemma)
        if (((mc) & self.case_).is_undefined): 
            return
        self.remove_items(mc, False)
    
    def remove_not_in_dictionary_items(self) -> None:
        """ Удалить элементы не из словаря (если все не из словаря, то ничего не удаляется).
        То есть оставить только словарный вариант. """
        if (self.__m_items is None): 
            return
        has_in_dict = False
        for i in range(len(self.__m_items) - 1, -1, -1):
            if ((isinstance(self.__m_items[i], MorphWordForm)) and self.__m_items[i].is_in_dictionary): 
                has_in_dict = True
                break
        if (has_in_dict): 
            for i in range(len(self.__m_items) - 1, -1, -1):
                if ((isinstance(self.__m_items[i], MorphWordForm)) and not self.__m_items[i].is_in_dictionary): 
                    del self.__m_items[i]
                    self.__m_need_recalc = True
    
    def remove_proper_items(self) -> None:
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            if (self.__m_items[i].class0_.is_proper): 
                del self.__m_items[i]
                self.__m_need_recalc = True
    
    def __remove_items_morph_number(self, num : 'MorphNumber') -> None:
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            if (((self.__m_items[i].number) & (num)) == (MorphNumber.UNDEFINED)): 
                del self.__m_items[i]
                self.__m_need_recalc = True
    
    def _remove_items_morph_gender(self, gen : 'MorphGender') -> None:
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            if (((self.__m_items[i].gender) & (gen)) == (MorphGender.UNDEFINED)): 
                del self.__m_items[i]
                self.__m_need_recalc = True
    
    def remove_items_list_cla(self, bis : typing.List['MorphBaseInfo'], cla : 'MorphClass') -> None:
        """ Удалить элементы, не соответствующие заданным параметрам
        
        Args:
            bis(typing.List[MorphBaseInfo]): 
            cla(MorphClass): 
        """
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            if (cla is not None and not cla.is_undefined): 
                if ((((self.__m_items[i].class0_.value) & (cla.value))) == 0): 
                    if (((self.__m_items[i].class0_.is_proper or self.__m_items[i].class0_.is_noun)) and ((cla.is_proper or cla.is_noun))): 
                        pass
                    else: 
                        del self.__m_items[i]
                        self.__m_need_recalc = True
                        continue
            ok = False
            for it in bis: 
                if (not it.case_.is_undefined and not self.__m_items[i].case_.is_undefined): 
                    if (((self.__m_items[i].case_) & it.case_).is_undefined): 
                        continue
                if (it.gender != MorphGender.UNDEFINED and self.__m_items[i].gender != MorphGender.UNDEFINED): 
                    if (((it.gender) & (self.__m_items[i].gender)) == (MorphGender.UNDEFINED)): 
                        continue
                if (it.number != MorphNumber.UNDEFINED and self.__m_items[i].number != MorphNumber.UNDEFINED): 
                    if (((it.number) & (self.__m_items[i].number)) == (MorphNumber.UNDEFINED)): 
                        continue
                ok = True
                break
            if (not ok): 
                del self.__m_items[i]
                self.__m_need_recalc = True
    
    def remove_items_ex(self, col : 'MorphCollection', cla : 'MorphClass') -> None:
        """ Удалить элементы, не соответствующие другой морфологической коллекции
        
        Args:
            col(MorphCollection): 
        """
        self.remove_items_list_cla(col.items, cla)
    
    def find_item(self, cas : 'MorphCase', num : 'MorphNumber'=MorphNumber.UNDEFINED, gen : 'MorphGender'=MorphGender.UNDEFINED) -> 'MorphBaseInfo':
        if (self.__m_items is None): 
            return None
        res = None
        max_coef = 0
        for it in self.__m_items: 
            if (not cas.is_undefined): 
                if (((it.case_) & cas).is_undefined): 
                    continue
            if (num != MorphNumber.UNDEFINED): 
                if (((num) & (it.number)) == (MorphNumber.UNDEFINED)): 
                    continue
            if (gen != MorphGender.UNDEFINED): 
                if (((gen) & (it.gender)) == (MorphGender.UNDEFINED)): 
                    continue
            wf = Utils.asObjectOrNull(it, MorphWordForm)
            if (wf is not None and wf.undef_coef > (0)): 
                if (wf.undef_coef > max_coef): 
                    max_coef = (wf.undef_coef)
                    res = it
                continue
            return it
        return res
    
    def _serialize(self, stream : io.IOBase) -> None:
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        SerializerHelper.serialize_short(stream, self.__m_class.value)
        SerializerHelper.serialize_short(stream, self.__m_case.value)
        SerializerHelper.serialize_short(stream, self.__m_gender)
        SerializerHelper.serialize_short(stream, self.__m_number)
        SerializerHelper.serialize_short(stream, self.__m_voice)
        SerializerHelper.serialize_short(stream, self.__m_language.value)
        if (self.__m_items is None): 
            self.__m_items = list()
        SerializerHelper.serialize_int(stream, len(self.__m_items))
        for it in self.__m_items: 
            self.__serialize_item(stream, it)
    
    def _deserialize(self, stream : io.IOBase) -> None:
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        self.__m_class = MorphClass._new53(SerializerHelper.deserialize_short(stream))
        self.__m_case = MorphCase._new29(SerializerHelper.deserialize_short(stream))
        self.__m_gender = (Utils.valToEnum(SerializerHelper.deserialize_short(stream), MorphGender))
        self.__m_number = (Utils.valToEnum(SerializerHelper.deserialize_short(stream), MorphNumber))
        self.__m_voice = (Utils.valToEnum(SerializerHelper.deserialize_short(stream), MorphVoice))
        self.__m_language = MorphLang._new56(SerializerHelper.deserialize_short(stream))
        cou = SerializerHelper.deserialize_int(stream)
        self.__m_items = list()
        i = 0
        while i < cou: 
            it = self.__deserialize_item(stream)
            if (it is not None): 
                self.__m_items.append(it)
            i += 1
        self.__m_need_recalc = False
    
    def __serialize_item(self, stream : io.IOBase, bi : 'MorphBaseInfo') -> None:
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        ty = 0
        if (isinstance(bi, MorphWordForm)): 
            ty = (1)
        Utils.writeByteIO(stream, ty)
        SerializerHelper.serialize_short(stream, bi.class0_.value)
        SerializerHelper.serialize_short(stream, bi.case_.value)
        SerializerHelper.serialize_short(stream, bi.gender)
        SerializerHelper.serialize_short(stream, bi.number)
        SerializerHelper.serialize_short(stream, bi.language.value)
        wf = Utils.asObjectOrNull(bi, MorphWordForm)
        if (wf is None): 
            return
        SerializerHelper.serialize_string(stream, wf.normal_case)
        SerializerHelper.serialize_string(stream, wf.normal_full)
        SerializerHelper.serialize_short(stream, wf.undef_coef)
        SerializerHelper.serialize_int(stream, (0 if wf.misc is None else len(wf.misc.attrs)))
        if (wf.misc is not None): 
            for a in wf.misc.attrs: 
                SerializerHelper.serialize_string(stream, a)
    
    def __deserialize_item(self, stream : io.IOBase) -> 'MorphBaseInfo':
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        ty = Utils.readByteIO(stream)
        res = (MorphBaseInfo() if ty == 0 else MorphWordForm())
        res.class0_ = MorphClass._new53(SerializerHelper.deserialize_short(stream))
        res.case_ = MorphCase._new29(SerializerHelper.deserialize_short(stream))
        res.gender = Utils.valToEnum(SerializerHelper.deserialize_short(stream), MorphGender)
        res.number = Utils.valToEnum(SerializerHelper.deserialize_short(stream), MorphNumber)
        res.language = MorphLang._new56(SerializerHelper.deserialize_short(stream))
        if (ty == 0): 
            return res
        wf = Utils.asObjectOrNull(res, MorphWordForm)
        wf.normal_case = SerializerHelper.deserialize_string(stream)
        wf.normal_full = SerializerHelper.deserialize_string(stream)
        wf.undef_coef = SerializerHelper.deserialize_short(stream)
        cou = SerializerHelper.deserialize_int(stream)
        i = 0
        while i < cou: 
            if (wf.misc is None): 
                wf.misc = MorphMiscInfo()
            wf.misc.attrs.append(SerializerHelper.deserialize_string(stream))
            i += 1
        return res
    
    @staticmethod
    def _new513(_arg1 : 'MorphClass') -> 'MorphCollection':
        res = MorphCollection()
        res.class0_ = _arg1
        return res
    
    @staticmethod
    def _new2365(_arg1 : 'MorphGender') -> 'MorphCollection':
        res = MorphCollection()
        res.gender = _arg1
        return res
    
    @staticmethod
    def _new2446(_arg1 : 'MorphCase') -> 'MorphCollection':
        res = MorphCollection()
        res.case_ = _arg1
        return res
    
    # static constructor for class MorphCollection
    @staticmethod
    def _static_ctor():
        MorphCollection.__m_empty_items = list()

MorphCollection._static_ctor()