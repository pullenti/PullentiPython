# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphMiscInfo import MorphMiscInfo
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.morph.MorphVoice import MorphVoice

class MorphCollection(MorphBaseInfo):
    """ Коллекция морфологических вариантов """
    
    def __init__(self, source : 'MorphCollection'=None) -> None:
        super().__init__(None)
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
                mi = (Utils.asObjectOrNull((it).clone(), MorphWordForm))
            else: 
                mi = MorphBaseInfo()
                it.copyTo(mi)
            if (self.__m_items is None): 
                self.__m_items = list()
            self.__m_items.append(mi)
        self.__m_class = MorphClass(source.__m_class)
        self.__m_gender = source.__m_gender
        self.__m_case = MorphCase(source.__m_case)
        self.__m_number = source.__m_number
        self.__m_language = MorphLang(source.__m_language)
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
            res.__m_class = MorphClass(self.__m_class)
            res.__m_gender = self.__m_gender
            res.__m_case = MorphCase(self.__m_case)
            res.__m_number = self.__m_number
            res.__m_language = MorphLang(self.__m_language)
            res.__m_need_recalc = False
            res.__m_voice = self.__m_voice
        return res
    
    @property
    def items_count(self) -> int:
        """ Количество морфологических вариантов """
        return (0 if self.__m_items is None else len(self.__m_items))
    
    def getIndexerItem(self, ind : int) -> 'MorphBaseInfo':
        if (self.__m_items is None or (ind < 0) or ind >= len(self.__m_items)): 
            return None
        else: 
            return self.__m_items[ind]
    
    __m_empty_items = None
    
    @property
    def items(self) -> typing.List['MorphBaseInfo']:
        """ Морфологические варианты """
        return Utils.ifNotNull(self.__m_items, MorphCollection.__m_empty_items)
    
    def addItem(self, item : 'MorphBaseInfo') -> None:
        if (self.__m_items is None): 
            self.__m_items = list()
        self.__m_items.append(item)
        self.__m_need_recalc = True
    
    def insertItem(self, ind : int, item : 'MorphBaseInfo') -> None:
        if (self.__m_items is None): 
            self.__m_items = list()
        self.__m_items.insert(ind, item)
        self.__m_need_recalc = True
    
    def removeItem(self, o : object) -> None:
        if (isinstance(o, int)): 
            self.__removeItemInt(o)
        elif (isinstance(o, MorphBaseInfo)): 
            self.__removeItemMorphBaseInfo(Utils.asObjectOrNull(o, MorphBaseInfo))
    
    def __removeItemInt(self, i : int) -> None:
        if (self.__m_items is not None and i >= 0 and (i < len(self.__m_items))): 
            del self.__m_items[i]
            self.__m_need_recalc = True
    
    def __removeItemMorphBaseInfo(self, item : 'MorphBaseInfo') -> None:
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
                        v = (it).misc.voice
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
    
    def containsAttr(self, attr_value : str, cla : 'MorphClass'=None) -> bool:
        for it in self.items: 
            if (cla is not None and cla.value != (0) and (((it.class0_.value) & (cla.value))) == 0): 
                continue
            if (it.containsAttr(attr_value, cla)): 
                return True
        return False
    
    def checkAccord(self, v : 'MorphBaseInfo', ignore_gender : bool=False) -> bool:
        for it in self.items: 
            if (it.checkAccord(v, ignore_gender)): 
                return True
        return super().checkAccord(v, ignore_gender)
    
    def check(self, cl : 'MorphClass') -> bool:
        return (((self.class0_.value) & (cl.value))) != 0
    
    def removeItems(self, it : object, eq : bool=False) -> None:
        """ Удалить элементы, не соответствующие элементу
        
        Args:
            it(object): 
        """
        if (isinstance(it, MorphCase)): 
            self.__removeItemsMorphCase(it)
        elif (isinstance(it, MorphClass)): 
            self.__removeItemsMorphClass(it, eq)
        elif (isinstance(it, MorphBaseInfo)): 
            self.__removeItemsMorphBaseInfo(it)
        elif (isinstance(it, MorphNumber)): 
            self.__removeItemsMorphNumber(Utils.valToEnum(it, MorphNumber))
        elif (isinstance(it, MorphGender)): 
            self._removeItemsMorphGender(Utils.valToEnum(it, MorphGender))
    
    def __removeItemsMorphCase(self, cas : 'MorphCase') -> None:
        if (self.__m_items is None): 
            return
        if (len(self.__m_items) == 0): 
            self.__m_case = ((self.__m_case) & cas)
        for i in range(len(self.__m_items) - 1, -1, -1):
            if (((self.__m_items[i].case_) & cas).is_undefined): 
                del self.__m_items[i]
                self.__m_need_recalc = True
            elif ((((self.__m_items[i].case_) & cas)) != self.__m_items[i].case_): 
                self.__m_items[i] = (Utils.asObjectOrNull(self.__m_items[i].clone(), MorphBaseInfo))
                self.__m_items[i].case_ = (self.__m_items[i].case_) & cas
                self.__m_need_recalc = True
        self.__m_need_recalc = True
    
    def __removeItemsMorphClass(self, cl : 'MorphClass', eq : bool) -> None:
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
    
    def __removeItemsMorphBaseInfo(self, inf : 'MorphBaseInfo') -> None:
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
                if ((((it.gender) & (inf.gender))) == (MorphGender.UNDEFINED)): 
                    ok = False
            ch_num = False
            if (inf.number != MorphNumber.PLURAL): 
                if ((((it.number) & (inf.number))) == (MorphNumber.UNDEFINED)): 
                    ok = False
                ch_num = True
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
                    if ((it.gender) != (((inf.gender) & (it.gender)))): 
                        it.gender = Utils.valToEnum(((inf.gender) & (it.gender)), MorphGender)
                        self.__m_need_recalc = True
                if (ch_num): 
                    if ((it.number) != (((inf.number) & (it.number)))): 
                        it.number = Utils.valToEnum(((inf.number) & (it.number)), MorphNumber)
                        self.__m_need_recalc = True
    
    def removeItemsByPreposition(self, prep : 'Token') -> None:
        """ Убрать элементы, не соответствующие по падежу предлогу
        
        Args:
            prep(Token): 
        """
        from pullenti.ner.TextToken import TextToken
        if (not ((isinstance(prep, TextToken)))): 
            return
        mc = LanguageHelper.getCaseAfterPreposition((prep).lemma)
        if (((mc) & self.case_).is_undefined): 
            return
        self.removeItems(mc, False)
    
    def removeNotInDictionaryItems(self) -> None:
        """ Удалить элементы не из словаря (если все не из словаря, то ничего не удаляется).
         То есть оставить только словарный вариант. """
        if (self.__m_items is None): 
            return
        has_in_dict = False
        for i in range(len(self.__m_items) - 1, -1, -1):
            if ((isinstance(self.__m_items[i], MorphWordForm)) and (self.__m_items[i]).is_in_dictionary): 
                has_in_dict = True
                break
        if (has_in_dict): 
            for i in range(len(self.__m_items) - 1, -1, -1):
                if ((isinstance(self.__m_items[i], MorphWordForm)) and not (self.__m_items[i]).is_in_dictionary): 
                    del self.__m_items[i]
                    self.__m_need_recalc = True
    
    def removeProperItems(self) -> None:
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            if (self.__m_items[i].class0_.is_proper): 
                del self.__m_items[i]
                self.__m_need_recalc = True
    
    def __removeItemsMorphNumber(self, num : 'MorphNumber') -> None:
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            if ((((self.__m_items[i].number) & (num))) == (MorphNumber.UNDEFINED)): 
                del self.__m_items[i]
                self.__m_need_recalc = True
    
    def _removeItemsMorphGender(self, gen : 'MorphGender') -> None:
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            if ((((self.__m_items[i].gender) & (gen))) == (MorphGender.UNDEFINED)): 
                del self.__m_items[i]
                self.__m_need_recalc = True
    
    def removeItemsEx(self, col : 'MorphCollection', cla : 'MorphClass') -> None:
        """ Удалить элементы, не соответствующие другой морфологической коллекции
        
        Args:
            col(MorphCollection): 
        """
        if (self.__m_items is None): 
            return
        for i in range(len(self.__m_items) - 1, -1, -1):
            if (not cla.is_undefined): 
                if ((((self.__m_items[i].class0_.value) & (cla.value))) == 0): 
                    if (((self.__m_items[i].class0_.is_proper or self.__m_items[i].class0_.is_noun)) and ((cla.is_proper or cla.is_noun))): 
                        pass
                    else: 
                        del self.__m_items[i]
                        self.__m_need_recalc = True
                        continue
            ok = False
            for it in col.items: 
                if (not it.case_.is_undefined and not self.__m_items[i].case_.is_undefined): 
                    if (((self.__m_items[i].case_) & it.case_).is_undefined): 
                        continue
                if (it.gender != MorphGender.UNDEFINED and self.__m_items[i].gender != MorphGender.UNDEFINED): 
                    if ((((it.gender) & (self.__m_items[i].gender))) == (MorphGender.UNDEFINED)): 
                        continue
                if (it.number != MorphNumber.UNDEFINED and self.__m_items[i].number != MorphNumber.UNDEFINED): 
                    if ((((it.number) & (self.__m_items[i].number))) == (MorphNumber.UNDEFINED)): 
                        continue
                ok = True
                break
            if (not ok): 
                del self.__m_items[i]
                self.__m_need_recalc = True
    
    def findItem(self, cas : 'MorphCase', num : 'MorphNumber'=MorphNumber.UNDEFINED, gen : 'MorphGender'=MorphGender.UNDEFINED) -> 'MorphBaseInfo':
        if (self.__m_items is None): 
            return None
        res = None
        max_coef = 0
        for it in self.__m_items: 
            if (not cas.is_undefined): 
                if (((it.case_) & cas).is_undefined): 
                    continue
            if (num != MorphNumber.UNDEFINED): 
                if ((((num) & (it.number))) == (MorphNumber.UNDEFINED)): 
                    continue
            if (gen != MorphGender.UNDEFINED): 
                if ((((gen) & (it.gender))) == (MorphGender.UNDEFINED)): 
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
        SerializerHelper.serializeShort(stream, self.__m_class.value)
        SerializerHelper.serializeShort(stream, self.__m_case.value)
        SerializerHelper.serializeShort(stream, self.__m_gender)
        SerializerHelper.serializeShort(stream, self.__m_number)
        SerializerHelper.serializeShort(stream, self.__m_voice)
        SerializerHelper.serializeShort(stream, self.__m_language.value)
        if (self.__m_items is None): 
            self.__m_items = list()
        SerializerHelper.serializeInt(stream, len(self.__m_items))
        for it in self.__m_items: 
            self.__serializeItem(stream, it)
    
    def _deserialize(self, stream : io.IOBase) -> None:
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        self.__m_class = MorphClass._new63(SerializerHelper.deserializeShort(stream))
        self.__m_case = MorphCase._new48(SerializerHelper.deserializeShort(stream))
        self.__m_gender = (Utils.valToEnum(SerializerHelper.deserializeShort(stream), MorphGender))
        self.__m_number = (Utils.valToEnum(SerializerHelper.deserializeShort(stream), MorphNumber))
        self.__m_voice = (Utils.valToEnum(SerializerHelper.deserializeShort(stream), MorphVoice))
        self.__m_language = MorphLang._new6(SerializerHelper.deserializeShort(stream))
        cou = SerializerHelper.deserializeInt(stream)
        self.__m_items = list()
        i = 0
        while i < cou: 
            it = self.__deserializeItem(stream)
            if (it is not None): 
                self.__m_items.append(it)
            i += 1
        self.__m_need_recalc = False
    
    def __serializeItem(self, stream : io.IOBase, bi : 'MorphBaseInfo') -> None:
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        ty = 0
        if (isinstance(bi, MorphWordForm)): 
            ty = (1)
        Utils.writeByteIO(stream, ty)
        SerializerHelper.serializeShort(stream, bi.class0_.value)
        SerializerHelper.serializeShort(stream, bi.case_.value)
        SerializerHelper.serializeShort(stream, bi.gender)
        SerializerHelper.serializeShort(stream, bi.number)
        SerializerHelper.serializeShort(stream, bi.language.value)
        wf = Utils.asObjectOrNull(bi, MorphWordForm)
        if (wf is None): 
            return
        SerializerHelper.serializeString(stream, wf.normal_case)
        SerializerHelper.serializeString(stream, wf.normal_full)
        SerializerHelper.serializeShort(stream, wf.undef_coef)
        SerializerHelper.serializeInt(stream, (0 if wf.misc is None else len(wf.misc.attrs)))
        if (wf.misc is not None): 
            for a in wf.misc.attrs: 
                SerializerHelper.serializeString(stream, a)
    
    def __deserializeItem(self, stream : io.IOBase) -> 'MorphBaseInfo':
        from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
        ty = Utils.readByteIO(stream)
        res = (MorphBaseInfo() if ty == 0 else MorphWordForm())
        res.class0_ = MorphClass._new63(SerializerHelper.deserializeShort(stream))
        res.case_ = MorphCase._new48(SerializerHelper.deserializeShort(stream))
        res.gender = Utils.valToEnum(SerializerHelper.deserializeShort(stream), MorphGender)
        res.number = Utils.valToEnum(SerializerHelper.deserializeShort(stream), MorphNumber)
        res.language = MorphLang._new6(SerializerHelper.deserializeShort(stream))
        if (ty == 0): 
            return res
        wf = Utils.asObjectOrNull(res, MorphWordForm)
        wf.normal_case = SerializerHelper.deserializeString(stream)
        wf.normal_full = SerializerHelper.deserializeString(stream)
        wf.undef_coef = SerializerHelper.deserializeShort(stream)
        cou = SerializerHelper.deserializeInt(stream)
        i = 0
        while i < cou: 
            if (wf.misc is None): 
                wf.misc = MorphMiscInfo()
            wf.misc.attrs.append(SerializerHelper.deserializeString(stream))
            i += 1
        return res
    
    @staticmethod
    def _new604(_arg1 : 'MorphClass') -> 'MorphCollection':
        res = MorphCollection()
        res.class0_ = _arg1
        return res
    
    @staticmethod
    def _new2221(_arg1 : 'MorphGender') -> 'MorphCollection':
        res = MorphCollection()
        res.gender = _arg1
        return res
    
    @staticmethod
    def _new2262(_arg1 : 'MorphCase') -> 'MorphCollection':
        res = MorphCollection()
        res.case_ = _arg1
        return res
    
    # static constructor for class MorphCollection
    @staticmethod
    def _static_ctor():
        MorphCollection.__m_empty_items = list()

MorphCollection._static_ctor()