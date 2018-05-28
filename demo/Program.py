# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import Stopwatch
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr


class Program:
    
    @staticmethod
    def main(args : typing.List[str]) -> None:
        from pullenti.ner.Sdk import Sdk
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.ProcessorService import ProcessorService
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.keyword.KeywordAnalyzer import KeywordAnalyzer
        from pullenti.ner.keyword.KeywordReferent import KeywordReferent
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        sw = Stopwatch()
        print("Initializing ... ", end="", flush=True)
        Sdk.initialize(MorphLang.RU | MorphLang.EN)
        sw.stop()
        print("OK (by {0} ms), version {1}".format(sw.elapsedMilliseconds, ProcessorService._get_version()), flush=True)
        txt = "Единственным конкурентом «Трансмаша» на этом сомнительном тендере было ООО «Плассер Алека Рейл Сервис», основным владельцем которого является австрийская компания «СТЦ-Холдинг ГМБХ». До конца 2011 г. эта же фирма была совладельцем «Трансмаша» вместе с «Тако» Краснова. Зато совладельцем «Плассера», также до конца 2011 г., был тот самый Карл Контрус, который имеет четверть акций «Трансмаша». "
        print("Text: {0}".format(txt), flush=True)
        with ProcessorService.create_processor() as proc: 
            ar = proc.process(SourceOfAnalysis(txt), None, MorphLang())
            print("\r\n==========================================\r\nEntities: ", flush=True)
            for e0 in ar.entities: 
                print("{0}: {1}".format(e0.type_name, str(e0)), flush=True)
                for s in e0.slots: 
                    print("   {0}: {1}".format(s.type_name, s.value), flush=True)
            print("\r\n==========================================\r\nNoun groups: ", flush=True)
            t = ar.first_token
            first_pass2509 = True
            while True:
                if first_pass2509: first_pass2509 = False
                else: t = t.next0
                if (not (t is not None)): break
                if (t.get_referent() is not None): 
                    continue
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.ADJECTIVECANBELAST, 0)
                if (npt is None): 
                    continue
                print(str(npt), flush=True)
                t = npt.end_token
        with ProcessorService.create_specific_processor(KeywordAnalyzer.ANALYZER_NAME) as proc: 
            ar = proc.process(SourceOfAnalysis(txt), None, MorphLang())
            print("\r\n==========================================\r\nKeywords1: ", flush=True)
            for e0 in ar.entities: 
                if (isinstance(e0, KeywordReferent)): 
                    print(str(e0), flush=True)
            print("\r\n==========================================\r\nKeywords2: ", flush=True)
            t = ar.first_token
            first_pass2510 = True
            while True:
                if first_pass2510: first_pass2510 = False
                else: t = t.next0
                if (not (t is not None)): break
                if (isinstance(t, ReferentToken)): 
                    kw = (t.get_referent() if isinstance(t.get_referent(), KeywordReferent) else None)
                    if (kw is None): 
                        continue
                    kwstr = MiscHelper.get_text_value_of_meta_token(t if isinstance(t, ReferentToken) else None, Utils.valToEnum(GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE | GetTextAttr.KEEPREGISTER, GetTextAttr))
                    print("{0} = {1}".format(kwstr, kw), flush=True)
        print("Over!", flush=True)

if __name__ == "__main__":
    Program.main(None)
