# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import datetime
from pullenti.unisharp.Utils import Utils

from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.decree.internal.DecreeToken import DecreeToken
from pullenti.ner.instrument.internal.MetaInstrument import MetaInstrument
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent
from pullenti.ner.decree.internal.DecreeHelper import DecreeHelper

class InstrumentReferent(InstrumentBlockReferent):
    """ Представление всего документа
    
    """
    
    def __init__(self) -> None:
        super().__init__(InstrumentReferent.OBJ_TYPENAME)
        self.instance_of = MetaInstrument.GLOBAL_META
    
    OBJ_TYPENAME = "INSTRUMENT"
    """ Имя типа сущности TypeName ("INSTRUMENT") """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип документа """
    
    ATTR_REGNUMBER = "NUMBER"
    """ Имя атрибута - регистрационный номер """
    
    ATTR_CASENUMBER = "CASENUMBER"
    """ Имя атрибута - номер судебного дела """
    
    ATTR_DATE = "DATE"
    """ Имя атрибута - дата """
    
    ATTR_SIGNER = "SIGNER"
    """ Имя атрибута - подписант """
    
    ATTR_SOURCE = "SOURCE"
    """ Имя атрибута - публикующий орган """
    
    ATTR_GEO = "GEO"
    """ Имя атрибута - географический объект """
    
    ATTR_PART = "PART"
    """ Имя атрибута - номер части (если это часть другого документа) """
    
    ATTR_APPENDIX = "APPENDIX"
    """ Имя атрибута - номер приложения (если это приложение) """
    
    ATTR_PARTICIPANT = "PARTICIPANT"
    """ Имя атрибута - участник (InstrumentParticipant) """
    
    ATTR_ARTEFACT = "ARTEFACT"
    """ Имя атрибута - артефакт (InstrumentArtefact) """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        str0_ = self.get_string_value(InstrumentReferent.ATTR_APPENDIX)
        if ((str0_) is not None): 
            strs = self.get_string_values(InstrumentReferent.ATTR_APPENDIX)
            if (len(strs) == 1): 
                print("Приложение{0}{1}; ".format(("" if len(str0_) == 0 else " "), str0_), end="", file=res, flush=True)
            else: 
                print("Приложения ", end="", file=res)
                i = 0
                while i < len(strs): 
                    if (i > 0): 
                        print(",", end="", file=res)
                    print(strs[i], end="", file=res)
                    i += 1
                print("; ", end="", file=res)
        str0_ = self.get_string_value(InstrumentReferent.ATTR_PART)
        if ((str0_) is not None): 
            print("Часть {0}; ".format(str0_), end="", file=res, flush=True)
        if (self.typ is not None): 
            print(MiscHelper.convert_first_char_upper_and_other_lower(self.typ), end="", file=res)
        else: 
            print("Документ", end="", file=res)
        if (self.reg_number is not None): 
            print(" №{0}".format(self.reg_number), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == InstrumentReferent.ATTR_REGNUMBER and str(s.value) != self.reg_number): 
                    print("/{0}".format(s.value), end="", file=res, flush=True)
        if (self.case_number is not None): 
            print(" дело №{0}".format(self.case_number), end="", file=res, flush=True)
        dt = self.get_string_value(InstrumentReferent.ATTR_DATE)
        if (dt is not None): 
            print(" от {0}".format(dt), end="", file=res, flush=True)
        str0_ = self.get_string_value(InstrumentBlockReferent.ATTR_NAME)
        if ((str0_) is not None): 
            if (len(str0_) > 100): 
                str0_ = (str0_[0:0+100] + "...")
            print(" \"{0}\"".format(str0_), end="", file=res, flush=True)
        str0_ = self.get_string_value(InstrumentReferent.ATTR_GEO)
        if ((str0_) is not None): 
            print(" ({0})".format(str0_), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    @property
    def typ(self) -> str:
        """ Тип """
        return self.get_string_value(InstrumentReferent.ATTR_TYPE)
    @typ.setter
    def typ(self, value_) -> str:
        self.add_slot(InstrumentReferent.ATTR_TYPE, value_, True, 0)
        return value_
    
    @property
    def reg_number(self) -> str:
        """ Номер """
        return self.get_string_value(InstrumentReferent.ATTR_REGNUMBER)
    @reg_number.setter
    def reg_number(self, value_) -> str:
        if (Utils.isNullOrEmpty(value_)): 
            self.add_slot(InstrumentReferent.ATTR_REGNUMBER, None, True, 0)
            return value_
        if (".,".find(value_[len(value_) - 1]) >= 0): 
            value_ = value_[0:0+len(value_) - 1]
        self.add_slot(InstrumentReferent.ATTR_REGNUMBER, value_, True, 0)
        return value_
    
    @property
    def case_number(self) -> str:
        """ Номер дела """
        return self.get_string_value(InstrumentReferent.ATTR_CASENUMBER)
    @case_number.setter
    def case_number(self, value_) -> str:
        if (Utils.isNullOrEmpty(value_)): 
            return value_
        if (".,".find(value_[len(value_) - 1]) >= 0): 
            value_ = value_[0:0+len(value_) - 1]
        self.add_slot(InstrumentReferent.ATTR_CASENUMBER, value_, True, 0)
        return value_
    
    @property
    def date(self) -> datetime.datetime:
        """ Дата подписания """
        s = self.get_string_value(InstrumentReferent.ATTR_DATE)
        if (s is None): 
            return None
        return DecreeHelper.parse_date_time(s)
    
    def _add_date(self, dt : object) -> bool:
        if (dt is None): 
            return False
        if (isinstance(dt, DecreeToken)): 
            if (isinstance(dt.ref, ReferentToken)): 
                return self._add_date(dt.ref.referent)
            if (dt.value is not None): 
                self.add_slot(InstrumentReferent.ATTR_DATE, dt.value, True, 0)
                return True
            return False
        if (isinstance(dt, ReferentToken)): 
            return self._add_date(dt.referent)
        if (isinstance(dt, DateReferent)): 
            dr = Utils.asObjectOrNull(dt, DateReferent)
            year = dr.year
            mon = dr.month
            day = dr.day
            if (year == 0): 
                return dr.pointer == DatePointerType.UNDEFINED
            ex_date = self.date
            if (ex_date is not None and ex_date.year == year): 
                if (mon == 0 and ex_date.month > 0): 
                    return False
                if (day == 0 and ex_date.day > 0): 
                    return False
                del_exist = False
                if (mon > 0 and ex_date.month == 0): 
                    del_exist = True
                if (del_exist): 
                    for s in self.slots: 
                        if (s.type_name == InstrumentReferent.ATTR_DATE): 
                            self.slots.remove(s)
                            break
            tmp = io.StringIO()
            print(year, end="", file=tmp)
            if (mon > 0): 
                print(".{0}".format("{:02d}".format(mon)), end="", file=tmp, flush=True)
            if (day > 0): 
                print(".{0}".format("{:02d}".format(day)), end="", file=tmp, flush=True)
            self.add_slot(DecreeReferent.ATTR_DATE, Utils.toStringStringIO(tmp), False, 0)
            return True
        if (isinstance(dt, str)): 
            self.add_slot(InstrumentReferent.ATTR_DATE, Utils.asObjectOrNull(dt, str), True, 0)
            return True
        return False
    
    def can_be_equals(self, obj : 'Referent', typ_ : 'ReferentsEqualType') -> bool:
        return obj == self