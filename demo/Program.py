# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import Stopwatch
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
        Sdk.initialize((MorphLang.RU) | MorphLang.EN)
        sw.stop()
        print("OK (by {0} ms), version {1}".format(sw.elapsedMilliseconds, ProcessorService.getVersion()), flush=True)
        txt = "Единственным конкурентом «Трансмаша» на этом сомнительном тендере было ООО «Плассер Алека Рейл Сервис», основным владельцем которого является австрийская компания «СТЦ-Холдинг ГМБХ». До конца 2011 г. эта же фирма была совладельцем «Трансмаша» вместе с «Тако» Краснова. Зато совладельцем «Плассера», также до конца 2011 г., был тот самый Карл Контрус, который имеет четверть акций «Трансмаша». "
        print("Text: {0}".format(txt), flush=True)
        with ProcessorService.createProcessor() as proc: 
            ar = proc.process(SourceOfAnalysis(txt), None, MorphLang())
            print("\r\n==========================================\r\nEntities: ", flush=True)
            for e0_ in ar.entities: 
                print("{0}: {1}".format(e0_.type_name, str(e0_)), flush=True)
                for s in e0_.slots: 
                    print("   {0}: {1}".format(s.type_name, s.value), flush=True)
            print("\r\n==========================================\r\nNoun groups: ", flush=True)
            t = ar.first_token
            first_pass2713 = True
            while True:
                if first_pass2713: first_pass2713 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.getReferent() is not None): 
                    continue
                npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.ADJECTIVECANBELAST, 0)
                if (npt is None): 
                    continue
                print(npt, flush=True)
                t = npt.end_token
        with ProcessorService.createSpecificProcessor(KeywordAnalyzer.ANALYZER_NAME) as proc: 
            ar = proc.process(SourceOfAnalysis(txt), None, MorphLang())
            print("\r\n==========================================\r\nKeywords1: ", flush=True)
            for e0_ in ar.entities: 
                if (isinstance(e0_, KeywordReferent)): 
                    print(e0_, flush=True)
            print("\r\n==========================================\r\nKeywords2: ", flush=True)
            t = ar.first_token
            first_pass2714 = True
            while True:
                if first_pass2714: first_pass2714 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (isinstance(t, ReferentToken)): 
                    kw = Utils.asObjectOrNull(t.getReferent(), KeywordReferent)
                    if (kw is None): 
                        continue
                    kwstr = MiscHelper.getTextValueOfMetaToken(Utils.asObjectOrNull(t, ReferentToken), Utils.valToEnum((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
                    print("{0} = {1}".format(kwstr, kw), flush=True)
        print("Over!", flush=True)

if __name__ == "__main__":
    Program.main(None)
