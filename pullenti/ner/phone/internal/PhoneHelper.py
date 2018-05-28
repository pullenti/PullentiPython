# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper

from pullenti.ner.bank.internal.ResourceHelper import ResourceHelper


class PhoneHelper:
    
    class PhoneNode:
        
        def __init__(self) -> None:
            self.pref = None
            self.children = dict()
            self.countries = None
        
        def __str__(self) -> str:
            if (self.countries is None): 
                return self.pref
            res = Utils.newStringIO(self.pref)
            for c in self.countries: 
                print(" {0}".format(c), end="", file=res, flush=True)
            return Utils.toStringStringIO(res)
    
    @staticmethod
    def initialize() -> None:
        if (PhoneHelper.__m_phone_root is not None): 
            return
        PhoneHelper.__m_phone_root = PhoneHelper.PhoneNode()
        PhoneHelper.__m_all_country_codes = dict()
        str0 = ResourceHelper.get_string("CountryPhoneCodes.txt")
        if (str0 is None): 
            raise Utils.newException("Can't file resource file {0} in Organization analyzer".format("CountryPhoneCodes.txt"), None)
        with io.StringIO(str0) as r: 
            while True:
                line = Utils.readLineIO(r)
                if (line is None): 
                    break
                if (Utils.isNullOrEmpty(line)): 
                    continue
                if (len(line) < 2): 
                    continue
                country = line[0 : 2]
                cod = line[2 : ].strip()
                if (len(cod) < 1): 
                    continue
                if (not country in PhoneHelper.__m_all_country_codes): 
                    PhoneHelper.__m_all_country_codes[country] = cod
                tn = PhoneHelper.__m_phone_root
                for i in range(len(cod)):
                    dig = cod[i]
                    inoutarg2278 = RefOutArgWrapper(None)
                    inoutres2279 = Utils.tryGetValue(tn.children, dig, inoutarg2278)
                    nn = inoutarg2278.value
                    if (not inoutres2279): 
                        nn = PhoneHelper.PhoneNode()
                        nn.pref = cod[0 : (i + 1)]
                        tn.children[dig] = nn
                    tn = nn
                if (tn.countries is None): 
                    tn.countries = list()
                tn.countries.append(country)
    
    __m_all_country_codes = None
    
    @staticmethod
    def get_all_country_codes() -> typing.List['java.util.Map.Entry']:
        return PhoneHelper.__m_all_country_codes
    
    __m_phone_root = None
    
    @staticmethod
    def get_country_prefix(full_number : str) -> str:
        """ Выделить телефонный префикс из "полного" номера
        
        Args:
            full_number(str): 
        
        """
        if (full_number is None): 
            return None
        nod = PhoneHelper.__m_phone_root
        max_ind = -1
        for i in range(len(full_number)):
            dig = full_number[i]
            inoutarg2280 = RefOutArgWrapper(None)
            inoutres2281 = Utils.tryGetValue(nod.children, dig, inoutarg2280)
            nn = inoutarg2280.value
            if (not inoutres2281): 
                break
            if (nn.countries is not None and len(nn.countries) > 0): 
                max_ind = i
            nod = nn
        if (max_ind < 0): 
            return None
        else: 
            return full_number[0 : (max_ind + 1)]