# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.instrument.InstrumentKind import InstrumentKind

class MetaInstrumentBlock(ReferentClass):
    
    def __init__(self) -> None:
        super().__init__()
        self.kind_feature = None;
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent
        MetaInstrumentBlock.GLOBAL_META = MetaInstrumentBlock()
        MetaInstrumentBlock.GLOBAL_META.kind_feature = MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_KIND, "Класс", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.UNDEFINED), "Неизвестный фрагмент", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.DOCUMENT), "Документ", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.INTERNALDOCUMENT), "Внутренний документ", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.APPENDIX), "Приложение", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.CONTENT), "Содержимое", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.HEAD), "Заголовочная часть", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.TAIL), "Хвостовая часть", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.NAME), "Название", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.NUMBER), "Номер", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.CASENUMBER), "Номер дела", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.CASEINFO), "Информация дела", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.EDITIONS), "Редакции", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.APPROVED), "Одобрен", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.ORGANIZATION), "Организация", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.DOCPART), "Часть документа", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.PLACE), "Место", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.SIGNER), "Подписант", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.SUBITEM), "Подпункт", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.INDENTION), "Абзац", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.CHAPTER), "Глава", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.PARAGRAPH), "Параграф", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.SUBPARAGRAPH), "Подпараграф", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.LISTHEAD), "Заголовок списка", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.LISTITEM), "Элемент списка", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.NOTICE), "Примечание", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.TYP), "Тип", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.SECTION), "Раздел", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.SUBSECTION), "Подраздел", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.CLAUSE), "Статья", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.CLAUSEPART), "Часть", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.DATE), "Дата", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.DIRECTIVE), "Директива", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.INDEX), "Оглавление", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.INDEXITEM), "Элемент оглавления", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.DOCREFERENCE), "Ссылка на документ", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.INITIATOR), "Инициатор", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.PREAMBLE), "Преамбула", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.ITEM), "Пункт", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.KEYWORD), "Ключевое слово", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.COMMENT), "Комментарий", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.QUESTION), "Вопрос", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.CITATION), "Цитата", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.CONTACT), "Контакт", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.TABLE), "Таблица", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.TABLEROW), "Строка таблицы", None, None)
        MetaInstrumentBlock.GLOBAL_META.kind_feature.add_value(Utils.enumToString(InstrumentKind.TABLECELL), "Ячейка таблицы", None, None)
        fi2 = MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_KIND, "Класс (доп.)", 0, 1)
        i = 0
        while i < len(MetaInstrumentBlock.GLOBAL_META.kind_feature.inner_values): 
            fi2.add_value(MetaInstrumentBlock.GLOBAL_META.kind_feature.inner_values[i], MetaInstrumentBlock.GLOBAL_META.kind_feature.outer_values[i], None, None)
            i += 1
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_CHILD, "Внутренний элемент", 0, 0).show_as_parent = True
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_NAME, "Наименование", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_NUMBER, "Номер", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_MINNUMBER, "Минимальный номер", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_SUBNUMBER, "Подномер", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_SUB2NUMBER, "Подномер второй", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_SUB3NUMBER, "Подномер третий", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_VALUE, "Значение", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_REF, "Ссылка на объект", 0, 1)
        MetaInstrumentBlock.GLOBAL_META.add_feature(InstrumentBlockReferent.ATTR_EXPIRED, "Утратил силу", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent
        return InstrumentBlockReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Блок документа"
    
    DOC_IMAGE_ID = "decree"
    
    PART_IMAGE_ID = "part"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaInstrumentBlock.PART_IMAGE_ID
    
    GLOBAL_META = None