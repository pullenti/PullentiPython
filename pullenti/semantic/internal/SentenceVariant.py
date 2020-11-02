# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.semantic.internal.SentItemType import SentItemType
from pullenti.semantic.internal.NGLinkType import NGLinkType

class SentenceVariant(object):
    
    def __init__(self) -> None:
        self.coef = 0
        self.segs = list()
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("{0}: ".format(self.coef), end="", file=tmp, flush=True)
        for s in self.segs: 
            if (s != self.segs[0]): 
                print("; \r\n", end="", file=tmp)
            if (s is not None): 
                print(str(s), end="", file=tmp)
            else: 
                print("null", end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    def calc_coef(self) -> float:
        self.coef = (0)
        i = 0
        while i < len(self.segs): 
            if (self.segs[i] is not None): 
                self.coef += self.segs[i].coef
            i += 1
        i = 0
        first_pass3957 = True
        while True:
            if first_pass3957: first_pass3957 = False
            else: i += 1
            if (not (i < (len(self.segs) - 1))): break
            seg0 = self.segs[i]
            if (seg0 is None): 
                continue
            seg1 = self.segs[i + 1]
            if (seg1 is None): 
                continue
            has_agent = False
            has_pacient = False
            for li in seg0.links: 
                if (li is not None and li.to_verb == seg1.source.before_verb): 
                    if (li.typ == NGLinkType.AGENT): 
                        has_agent = True
                    elif (li.typ == NGLinkType.PACIENT): 
                        has_pacient = True
                        for lii in li.from0_.links: 
                            if ((lii is not None and lii.typ == NGLinkType.AGENT and lii.coef >= li.coef) and lii.to_verb == li.to_verb): 
                                for liii in seg1.links: 
                                    if (liii is not None and liii.to_verb == li.to_verb and liii.typ == NGLinkType.AGENT): 
                                        if (liii.coef < ((lii.coef / (3)))): 
                                            self.coef = -1
                                            return self.coef
            for li in seg1.links: 
                if (li is not None and li.to_verb == seg1.source.before_verb): 
                    if (li.typ == NGLinkType.AGENT and has_agent): 
                        self.coef = -1
                        return self.coef
                    elif (li.typ == NGLinkType.PACIENT and has_pacient): 
                        self.coef = -1
                        return self.coef
        return self.coef
    
    def compareTo(self, other : 'SentenceVariant') -> int:
        if (self.coef > other.coef): 
            return -1
        if (self.coef < other.coef): 
            return 1
        return 0
    
    def create_alt_links(self) -> None:
        coef0 = self.coef
        i = 0
        first_pass3958 = True
        while True:
            if first_pass3958: first_pass3958 = False
            else: i += 1
            if (not (i < len(self.segs))): break
            seg = self.segs[i]
            if (seg is None): 
                continue
            j = 0
            first_pass3959 = True
            while True:
                if first_pass3959: first_pass3959 = False
                else: j += 1
                if (not (j < len(seg.links))): break
                li = seg.links[j]
                if (li is None or li.typ == NGLinkType.LIST): 
                    continue
                if (len(li.from0_.links) < 2): 
                    continue
                if (li.from0_.source.typ == SentItemType.FORMULA): 
                    continue
                if (li.to is not None and li.to.source.typ == SentItemType.FORMULA): 
                    continue
                for l_ in li.from0_.links: 
                    if (l_ != li and l_.typ != NGLinkType.LIST): 
                        if (l_.to is not None and l_.to.source.typ == SentItemType.FORMULA): 
                            continue
                        if (l_.typ == NGLinkType.ACTANT): 
                            if (li.typ == NGLinkType.AGENT or li.typ == NGLinkType.PACIENT): 
                                continue
                        seg.links[j] = l_
                        seg.calc_coef()
                        coef_ = coef0 - (100)
                        if (seg.coef > 0): 
                            self.calc_coef()
                            coef_ = self.coef
                        self.coef = coef0
                        seg.links[j] = li
                        seg.calc_coef()
                        if (coef_ >= self.coef): 
                            li.alt_link = l_
                            break