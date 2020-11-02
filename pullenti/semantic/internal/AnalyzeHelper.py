# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import ProgressEventArgs

from pullenti.semantic.internal.SentItemType import SentItemType
from pullenti.ner.TextToken import TextToken
from pullenti.semantic.SemDocument import SemDocument
from pullenti.semantic.SemBlock import SemBlock
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.semantic.internal.Sentence import Sentence
from pullenti.semantic.internal.OptimizerHelper import OptimizerHelper

class AnalyzeHelper:
    
    @staticmethod
    def process(ar : 'AnalysisResult', pars : 'SemProcessParams') -> 'SemDocument':
        txt = SemDocument()
        t = ar.first_token
        while t is not None: 
            t.tag = None
            t = t.next0_
        if (pars.progress is not None): 
            pars.progress.call(None, ProgressEventArgs(0, None))
        pers0 = 0
        t = ar.first_token
        while t is not None: 
            if (pars.progress is not None): 
                p = t.begin_char
                if (len(ar.sofa.text) < 100000): 
                    p = (math.floor((p * 100) / len(ar.sofa.text)))
                else: 
                    p = math.floor(p / ((math.floor(len(ar.sofa.text) / 100))))
                if (p != pers0): 
                    pers0 = p
                    pars.progress.call(None, ProgressEventArgs(p, None))
            t1 = t
            tt = t.next0_
            while tt is not None: 
                if (tt.is_newline_before): 
                    if (MiscHelper.can_be_start_of_sentence(tt)): 
                        break
                t1 = tt
                tt = tt.next0_
            try: 
                AnalyzeHelper.__process_block(txt, ar, t, t1)
            except Exception as ex: 
                pass
            t = t1
            if (pars.max_char > 0 and t.end_char > pars.max_char): 
                break
            t = t.next0_
        OptimizerHelper.optimize(txt, pars)
        if (pars.progress is not None): 
            pars.progress.call(None, ProgressEventArgs(100, None))
        return txt
    
    @staticmethod
    def __process_block(res : 'SemDocument', ar : 'AnalysisResult', t0 : 'Token', t1 : 'Token') -> None:
        blk = SemBlock(res)
        t = t0
        while t is not None and t.end_char <= t1.end_char: 
            te = t
            tt = t.next0_
            while tt is not None and tt.end_char <= t1.end_char: 
                if (MiscHelper.can_be_start_of_sentence(tt)): 
                    break
                else: 
                    te = tt
                tt = tt.next0_
            AnalyzeHelper.__process_sentence(blk, ar, t, te)
            t = te
            t = t.next0_
        if (len(blk.fragments) > 0): 
            res.blocks.append(blk)
    
    @staticmethod
    def __process_sentence(blk : 'SemBlock', ar : 'AnalysisResult', t0 : 'Token', t1 : 'Token') -> None:
        cou = 0
        t = t0
        while t is not None and (t.end_char < t1.end_char): 
            pass
            t = t.next0_; cou += 1
        if (cou > 70): 
            cou2 = 0
            t = t0
            while t is not None and (t.end_char < t1.end_char): 
                if (cou2 >= 70): 
                    t1 = t
                    break
                t = t.next0_; cou2 += 1
        sents = Sentence.parse_variants(t0, t1, 0, 100, SentItemType.UNDEFINED)
        if (sents is None): 
            return
        max0_ = -1
        best = None
        alt = None
        for s in sents: 
            if ((isinstance(t1, TextToken)) and not t1.chars.is_letter): 
                s.last_char = (Utils.asObjectOrNull(t1, TextToken))
            s.calc_coef(False)
            if (s.coef > max0_): 
                max0_ = s.coef
                best = s
                alt = (None)
            elif (s.coef == max0_ and max0_ > 0): 
                alt = s
        if (best is not None and best.res_block is not None): 
            best.add_to_block(blk, None)