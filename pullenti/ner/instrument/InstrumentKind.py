# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class InstrumentKind(IntEnum):
    """ Классы частей НПА """
    UNDEFINED = 0
    DOCUMENT = 1
    INTERNALDOCUMENT = 2
    HEAD = 3
    CONTENT = 4
    TAIL = 5
    APPENDIX = 6
    DOCPART = 7
    SECTION = 8
    SUBSECTION = 9
    CHAPTER = 10
    PARAGRAPH = 11
    SUBPARAGRAPH = 12
    CLAUSE = 13
    CLAUSEPART = 14
    ITEM = 15
    SUBITEM = 16
    INDENTION = 17
    LISTITEM = 18
    LISTHEAD = 19
    PREAMBLE = 20
    INDEX = 21
    INDEXITEM = 22
    NOTICE = 23
    NUMBER = 24
    CASENUMBER = 25
    CASEINFO = 26
    NAME = 27
    TYP = 28
    SIGNER = 29
    ORGANIZATION = 30
    PLACE = 31
    DATE = 32
    CONTACT = 33
    INITIATOR = 34
    DIRECTIVE = 35
    EDITIONS = 36
    APPROVED = 37
    DOCREFERENCE = 38
    KEYWORD = 39
    COMMENT = 40
    CITATION = 41
    QUESTION = 42
    ANSWER = 43
    TABLE = 44
    TABLEROW = 45
    TABLECELL = 46
    IGNORED = 47
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)