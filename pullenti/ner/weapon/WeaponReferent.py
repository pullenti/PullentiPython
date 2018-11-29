# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.LanguageHelper import LanguageHelper


class WeaponReferent(Referent):
    
    def __init__(self) -> None:
        from pullenti.ner.weapon.internal.MetaWeapon import MetaWeapon
        super().__init__(WeaponReferent.OBJ_TYPENAME)
        self.instance_of = MetaWeapon._global_meta
    
    OBJ_TYPENAME = "WEAPON"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_BRAND = "BRAND"
    
    ATTR_MODEL = "MODEL"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_DATE = "DATE"
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=MorphLang(), lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = io.StringIO()
        str0_ = None
        for s in self.slots: 
            if (s.type_name == WeaponReferent.ATTR_TYPE): 
                n = s.value
                if (str0_ is None or (len(n) < len(str0_))): 
                    str0_ = n
        if (str0_ is not None): 
            print(str0_.lower(), end="", file=res)
        str0_ = self.getStringValue(WeaponReferent.ATTR_BRAND)
        if ((str0_) is not None): 
            print(" {0}".format(MiscHelper.convertFirstCharUpperAndOtherLower(str0_)), end="", file=res, flush=True)
        str0_ = self.getStringValue(WeaponReferent.ATTR_MODEL)
        if ((str0_) is not None): 
            print(" {0}".format(str0_), end="", file=res, flush=True)
        str0_ = self.getStringValue(WeaponReferent.ATTR_NAME)
        if ((str0_) is not None): 
            print(" \"{0}\"".format(MiscHelper.convertFirstCharUpperAndOtherLower(str0_)), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == WeaponReferent.ATTR_NAME and str0_ != (s.value)): 
                    if (LanguageHelper.isCyrillicChar(str0_[0]) != LanguageHelper.isCyrillicChar((s.value)[0])): 
                        print(" ({0})".format(MiscHelper.convertFirstCharUpperAndOtherLower(s.value)), end="", file=res, flush=True)
                        break
        str0_ = self.getStringValue(WeaponReferent.ATTR_NUMBER)
        if ((str0_) is not None): 
            print(", номер {0}".format(str0_), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        tr = Utils.asObjectOrNull(obj, WeaponReferent)
        if (tr is None): 
            return False
        s1 = self.getStringValue(WeaponReferent.ATTR_NUMBER)
        s2 = tr.getStringValue(WeaponReferent.ATTR_NUMBER)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            else: 
                if (s1 != s2): 
                    return False
                return True
        eq_types = False
        for t in self.getStringValues(WeaponReferent.ATTR_TYPE): 
            if (tr.findSlot(WeaponReferent.ATTR_TYPE, t, True) is not None): 
                eq_types = True
                break
        if (not eq_types): 
            return False
        s1 = self.getStringValue(WeaponReferent.ATTR_BRAND)
        s2 = tr.getStringValue(WeaponReferent.ATTR_BRAND)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            elif (s1 != s2): 
                return False
        s1 = self.getStringValue(WeaponReferent.ATTR_MODEL)
        s2 = tr.getStringValue(WeaponReferent.ATTR_MODEL)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            else: 
                if (self.findSlot(WeaponReferent.ATTR_MODEL, s2, True) is not None): 
                    return True
                if (tr.findSlot(WeaponReferent.ATTR_MODEL, s1, True) is not None): 
                    return True
                return False
        for s in self.slots: 
            if (s.type_name == WeaponReferent.ATTR_NAME): 
                if (tr.findSlot(WeaponReferent.ATTR_NAME, s.value, True) is not None): 
                    return True
        if (s1 is not None and s2 is not None): 
            return True
        return False
    
    def mergeSlots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().mergeSlots(obj, merge_statistic)