# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import Stopwatch

from pullenti.ner.keyword.KeywordReferent import KeywordReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.keyword.KeywordAnalyzer import KeywordAnalyzer
from pullenti.ner.Sdk import Sdk

class Program:
    
    @staticmethod
    def main(args : typing.List[str]) -> None:
        sw = Stopwatch()
        # инициализация - необходимо проводить один раз до обработки текстов
        print("Initializing ... ", end="", flush=True)
        # инициализируются движок и все имеющиеся анализаторы
        Sdk.initialize((MorphLang.RU) | MorphLang.EN)
        sw.stop()
        print("OK (by {0} ms), version {1}".format(sw.elapsedMilliseconds, ProcessorService.get_version()), flush=True)
        # анализируемый текст
        txt = "Единственным конкурентом «Трансмаша» на этом сомнительном тендере было ООО «Плассер Алека Рейл Сервис», основным владельцем которого является австрийская компания «СТЦ-Холдинг ГМБХ». До конца 2011 г. эта же фирма была совладельцем «Трансмаша» вместе с «Тако» Краснова. Зато совладельцем «Плассера», также до конца 2011 г., был тот самый Карл Контрус, который имеет четверть акций «Трансмаша». "
        print("Text: {0}".format(txt), flush=True)
        # запускаем обработку на пустом процессоре (без анализаторов NER)
        are = ProcessorService.get_empty_processor().process(SourceOfAnalysis(txt), None, None)
        print("Noun groups: ", end="", flush=True)
        t = are.first_token
        # перебираем токены
        first_pass2837 = True
        while True:
            if first_pass2837: first_pass2837 = False
            else: t = t.next0_
            if (not (t is not None)): break
            # выделяем именную группу с текущего токена
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
            # не получилось
            if (npt is None): 
                continue
            # получилось, выводим в нормализованном виде
            print("[{0}=>{1}] ".format(npt.get_source_text(), npt.get_normal_case_text(None, True, MorphGender.UNDEFINED, False)), end="", flush=True)
            # указатель на последний токен именной группы
            t = npt.end_token
        with ProcessorService.create_processor() as proc: 
            # анализируем текст
            ar = proc.process(SourceOfAnalysis(txt), None, None)
            # результирующие сущности
            print("\r\n==========================================\r\nEntities: ", flush=True)
            for e0_ in ar.entities: 
                print("{0}: {1}".format(e0_.type_name, str(e0_)), flush=True)
                for s in e0_.slots: 
                    print("   {0}: {1}".format(s.type_name, s.value), flush=True)
            # пример выделения именных групп
            print("\r\n==========================================\r\nNoun groups: ", flush=True)
            t = ar.first_token
            first_pass2838 = True
            while True:
                if first_pass2838: first_pass2838 = False
                else: t = t.next0_
                if (not (t is not None)): break
                # токены с сущностями игнорируем
                if (t.get_referent() is not None): 
                    continue
                # пробуем создать именную группу
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.ADJECTIVECANBELAST, 0)
                # не получилось
                if (npt is None): 
                    continue
                print(npt, flush=True)
                # указатель перемещаем на последний токен группы
                t = npt.end_token
        with ProcessorService.create_specific_processor(KeywordAnalyzer.ANALYZER_NAME) as proc: 
            ar = proc.process(SourceOfAnalysis(txt), None, None)
            print("\r\n==========================================\r\nKeywords1: ", flush=True)
            for e0_ in ar.entities: 
                if (isinstance(e0_, KeywordReferent)): 
                    print(e0_, flush=True)
            print("\r\n==========================================\r\nKeywords2: ", flush=True)
            t = ar.first_token
            first_pass2839 = True
            while True:
                if first_pass2839: first_pass2839 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (isinstance(t, ReferentToken)): 
                    kw = Utils.asObjectOrNull(t.get_referent(), KeywordReferent)
                    if (kw is None): 
                        continue
                    kwstr = MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t, ReferentToken), Utils.valToEnum((GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
                    print("{0} = {1}".format(kwstr, kw), flush=True)
        print("Over!", flush=True)

if __name__ == "__main__":
    Program.main(None)
