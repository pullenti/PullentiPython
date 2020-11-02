# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ConjunctionType import ConjunctionType
from pullenti.semantic.internal.SentItemType import SentItemType
from pullenti.semantic.internal.NGLinkType import NGLinkType
from pullenti.ner.core.ConjunctionToken import ConjunctionToken
from pullenti.semantic.SemFraglinkType import SemFraglinkType
from pullenti.semantic.internal.DelimType import DelimType
from pullenti.semantic.internal.DelimToken import DelimToken

class Subsent:
    
    def __init__(self) -> None:
        self.owner = None;
        self.items = list()
        self.delims = list()
        self.res_frag = None;
        self.is_or = False
        self.question = None;
        self.is_then_else_root = False
        self.typ = SemFraglinkType.UNDEFINED
    
    @property
    def owner_root(self) -> 'Subsent':
        k = 0
        s = self.owner
        while s is not None and (k < 100): 
            if (s.owner is None): 
                return s
            s = self.owner; k += 1
        return None
    
    def check(self, typ_ : 'DelimType') -> bool:
        for d in self.delims: 
            if ((isinstance(d, DelimToken)) and (((d.typ) & (typ_))) != (DelimType.UNDEFINED)): 
                return True
            elif ((isinstance(d, ConjunctionToken)) and typ_ == DelimType.AND): 
                return True
        return False
    
    def check_or(self) -> bool:
        for d in self.delims: 
            if ((isinstance(d, ConjunctionToken)) and d.typ == ConjunctionType.OR): 
                return True
        return False
    
    def only_conj(self) -> bool:
        for d in self.delims: 
            if (isinstance(d, DelimToken)): 
                return False
        return True
    
    def can_be_next_in_list(self, next0_ : 'Subsent') -> bool:
        if (len(next0_.delims) == 0): 
            return True
        for d in next0_.delims: 
            if (isinstance(d, DelimToken)): 
                if (not self.check(d.typ)): 
                    return False
        return True
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.is_or): 
            print("OR ", end="", file=tmp)
        if (self.question is not None): 
            print("({0}?) ".format(self.question), end="", file=tmp, flush=True)
        for it in self.delims: 
            print("<{0}> ".format(it), end="", file=tmp, flush=True)
        print('[', end="", file=tmp)
        for it in self.items: 
            if (it != self.items[0]): 
                print(", ", end="", file=tmp)
            print(it, end="", file=tmp)
        print("]", end="", file=tmp)
        if (self.owner is not None): 
            print(" -> {0}".format(self.owner), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def __has_comma_and(self, b : int, e0_ : int) -> bool:
        for it in self.items: 
            if (it.typ == SentItemType.CONJ): 
                if (it.source.begin_token.begin_char >= b and it.source.end_token.end_char <= e0_): 
                    return True
        return False
    
    @staticmethod
    def create_subsents(sent : 'Sentence') -> typing.List['Subsent']:
        if (len(sent.items) == 0): 
            return None
        res = list()
        begin = sent.items[0].begin_token.begin_char
        end = sent.items[len(sent.items) - 1].end_token.end_char
        map0_ = Utils.newArrayOfBytes((end + 1) - begin, 0)
        if (sent.best_var is not None): 
            for seg in sent.best_var.segs: 
                if (seg is not None): 
                    for li in seg.links: 
                        if (li is not None and li.typ == NGLinkType.LIST): 
                            i = (li.to_verb.begin_char if li.to is None else li.to.source.begin_token.begin_char)
                            while i <= li.from0_.source.end_token.end_char: 
                                po = i - begin
                                if (po >= 0 and (po < len(map0_))): 
                                    map0_[po] = (1)
                                i += 1
        ss = Subsent()
        has_verb = False
        i = 0
        first_pass3961 = True
        while True:
            if first_pass3961: first_pass3961 = False
            else: i += 1
            if (not (i < len(sent.items))): break
            it = sent.items[i]
            delim = False
            if (it.typ == SentItemType.DELIM): 
                delim = True
            elif (it.typ == SentItemType.CONJ and map0_[it.begin_token.begin_char - begin] == (0)): 
                delim = True
                if (it.source.typ == ConjunctionType.COMMA): 
                    if (not has_verb): 
                        delim = False
            if (not delim): 
                if (it.typ == SentItemType.VERB): 
                    has_verb = True
                ss.items.append(it)
                continue
            if (len(ss.items) == 0): 
                ss.delims.append(it.source)
                continue
            if (len(ss.items) > 0): 
                res.append(ss)
            ss = Subsent()
            has_verb = False
            ss.delims.append(it.source)
        if (len(ss.items) > 0): 
            res.append(ss)
        i = 0
        first_pass3962 = True
        while True:
            if first_pass3962: first_pass3962 = False
            else: i += 1
            if (not (i < len(res))): break
            r = res[i]
            if (r.check(DelimType.IF)): 
                has_then = False
                has_else = False
                j = (i + 1)
                while j < len(res): 
                    if (res[j].check(DelimType.THEN)): 
                        if (has_then): 
                            break
                        res[j].owner = r
                        res[j].question = "если"
                        res[j].typ = SemFraglinkType.IFTHEN
                        has_then = True
                        r.is_then_else_root = True
                    elif (res[j].check(DelimType.ELSE)): 
                        if (has_else): 
                            break
                        res[j].owner = r
                        res[j].question = "иначе"
                        res[j].typ = SemFraglinkType.IFELSE
                        has_else = True
                        r.is_then_else_root = True
                    elif (res[j].check(DelimType.IF)): 
                        if (res[j].check(DelimType.AND)): 
                            res[j].owner = r
                        else: 
                            break
                    j += 1
                if (not has_then and i > 0): 
                    if (res[0].owner is None and res[0].only_conj()): 
                        res[0].owner = r
                        res[0].question = "если"
                        r.is_then_else_root = True
                        res[0].typ = SemFraglinkType.IFTHEN
                    elif (res[0].owner is not None): 
                        r.owner = res[0]
                        r.question = "если"
                        r.typ = SemFraglinkType.IFTHEN
                continue
            if (r.check(DelimType.BECAUSE)): 
                has_then = False
                j = (i + 1)
                while j < len(res): 
                    if (res[j].check(DelimType.THEN)): 
                        if (has_then): 
                            break
                        res[j].owner = r
                        res[j].question = "по причине"
                        res[j].typ = SemFraglinkType.BECAUSE
                        has_then = True
                        r.is_then_else_root = True
                    j += 1
                if (not has_then and i > 0): 
                    if (res[0].owner is None and res[0].only_conj()): 
                        res[0].owner = r
                        res[0].question = "по причине"
                        r.is_then_else_root = True
                        res[0].typ = SemFraglinkType.BECAUSE
                        continue
                if (not has_then and ((i + 1) < len(res))): 
                    if (res[i + 1].owner is None and res[i + 1].only_conj()): 
                        res[i + 1].owner = r
                        res[i + 1].question = "по причине"
                        r.is_then_else_root = True
                        res[i + 1].typ = SemFraglinkType.BECAUSE
                        continue
                continue
            if (r.check(DelimType.BUT)): 
                if (i > 0): 
                    if (res[i - 1].owner is None and res[i - 1].only_conj()): 
                        res[i - 1].owner = r
                        res[i - 1].question = "но"
                        r.is_then_else_root = True
                        res[i - 1].typ = SemFraglinkType.BUT
                        continue
            if (r.check(DelimType.WHAT)): 
                if (i > 0): 
                    if (res[i - 1].owner is None and res[i - 1].only_conj()): 
                        res[i - 1].owner = r
                        res[i - 1].question = "что"
                        r.is_then_else_root = True
                        res[i - 1].typ = SemFraglinkType.WHAT
                        continue
            if (r.check(DelimType.FOR)): 
                if ((i + 1) < len(res)): 
                    if (res[i + 1].owner is None and res[i + 1].only_conj()): 
                        res[i + 1].owner = r
                        res[i + 1].question = "чтобы"
                        r.is_then_else_root = True
                        res[i + 1].typ = SemFraglinkType.FOR
                        continue
                if (i > 0): 
                    if (res[i - 1].owner is None and res[i - 1].only_conj()): 
                        res[i - 1].owner = r
                        res[i - 1].question = "чтобы"
                        r.is_then_else_root = True
                        res[i - 1].typ = SemFraglinkType.FOR
                        continue
        i = 1
        first_pass3963 = True
        while True:
            if first_pass3963: first_pass3963 = False
            else: i += 1
            if (not (i < len(res))): break
            r = res[i]
            if (not r.check(DelimType.AND) or r.owner is not None): 
                continue
            for j in range(i - 1, -1, -1):
                rr = res[j]
                if (rr.can_be_next_in_list(r) and ((rr.owner is None or ((rr.owner_root is not None and rr.owner_root.can_be_next_in_list(r)))))): 
                    if (r.check_or()): 
                        rr.is_or = True
                    rr.items.extend(r.items)
                    del res[i]
                    i -= 1
                    break
        return res