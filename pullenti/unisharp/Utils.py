import io
import math
import pkg_resources
from pathlib import Path
from pathlib import PurePath
import datetime
import xml.etree.ElementTree

class Utils:    
    @staticmethod
    def enumToString(e):
        s = str(e)
        i = s.find('.')
        if(i > 0):
            s = s[i + 1:]
        return s.upper()

    @staticmethod
    def valToEnum(v, e):
        try:
            if(isinstance(v, e)):
                return v
            if(isinstance(v, str)):
                return e.__dict__[v.upper()]
            return e(v)
        except:
            if(isinstance(v, str)):
                return e(int(v))
            return v

    @staticmethod
    def newException(msg, ie):
        e = Exception()
        e.message = msg
        if(ie is not None): e.inner_exception = ie
        return e

    @staticmethod
    def newArray(cou, ini):
        res = list()
        for i in range(cou):
            res.append(ini)
        return res

    @staticmethod
    def newArrayOfBytes(cou, ini):
        res = bytearray()
        for i in range(cou):
            res.append(ini)
        return res

    @staticmethod
    def indexOfList(li, it, i):
        for ii in range(i, len(li)):
            if(li[ii] == it): return ii
        return -1
    @staticmethod
    def lastIndexOfList(li, it, i):
        if(i < 0): i = len(li) - 1
        for ii in range(i, -1, -1):
            if(li[ii] == it): return ii
        return -1

    @staticmethod
    def tryGetValue(d, key, res):
        if(key in d): 
            res.value = d[key]
            return True
        return False

    @staticmethod
    def tryGetValue0(d, key, res):
        res.value = 0
        if(key in d): 
            res.value = d[key]
            return True
        return False

    @staticmethod
    def tryParseInt(s, res):
        res.value = 0
        if(s is None): return False
        try: 
            res.value = int(s)
            return True
        except:
            return False

    @staticmethod
    def tryParseFloat(s, res):
        res.value = 0
        if(s is None): return False
        try: 
            res.value = float(s)
            return True
        except:
            return False

    @staticmethod
    def mathTruncate(f):
        if(f < 0): return math.ceil(f)
        return math.floor(f)

    @staticmethod
    def ifNotNull(v, altv):
        if(v is None): return altv
        return v

    @staticmethod
    def isNullOrEmpty(v):
        if(v is None): return True
        try:
            if(len(v) == 0): return True
        except:
            pass
        return False

    wsChars = [0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x20, 0x85, 0xA0, 0x1680, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x2028, 0x2029, 0x202F, 0x205F, 0x3000]
   
    @staticmethod
    def isWhitespace(ch):
        co = ord(ch[0])
        return co in Utils.wsChars

    @staticmethod
    def getDate(dt):
        return datetime.datetime(dt.year, dt.month, dt.day)

    @staticmethod
    def getDateShortString(dt):
        return str(datetime.date(dt.year, dt.month, dt.day))

    @staticmethod
    def getTimeShortString(dt):
        return str(datetime.time(dt.hour, dt.minute, dt.second))

    @staticmethod
    def lastDayOfMonth(year, month):
        any_day = datetime.date(year, month, 1) 
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4) 
        dat = next_month - datetime.timedelta(days=next_month.day)
        return dat.day

    @staticmethod
    def compareStrings(s1, s2, ignoreCas = False):
        if(ignoreCas):
            s1 = s1.upper()
            s2 = s2.upper()
        if(s1 == s2): return 0
        if(s1 < s2): return -1
        return 1

    @staticmethod
    def joinStrings(d, s):
        res = ""
        for ss in s:
            if(len(res) > 0): res += d
            res += ss
        return res

    @staticmethod
    def startsWithString(s, sub, ignoreCase = False):
        if(not ignoreCase): return s.startswith(sub)
        return s.upper().startswith(sub.upper())

    @staticmethod
    def endsWithString(s, sub, ignoreCase = False):
        if(not ignoreCase): return s.endswith(sub)
        return s.upper().endswith(sub.upper())

    @staticmethod
    def splitString(s, sep, ignoreEmpty = False):
        if(s is None or sep is None): return None
        res = []
        i0 = 0
        for i in range(len(s)):
            ch = s[i]
            if(isinstance(sep, list)):
                if(not (ch in sep)): continue
            else:
                if(sep.find(ch) < 0): continue
                
            if(i > i0): res.append(s[i0: i])
            else: 
                if((not ignoreEmpty) and i > 0): res.append("")
            i0 = i + 1
        else: i = len(s)
        if(i > i0):
            res.append(s[i0 : i])
        return res

    @staticmethod
    def trimEndString(s):
        for i in range(len(s) - 1, 0, -1):
            if(not s[i].isspace()):
                if(i < len(s) - 1): return s[:i + 1]
                return s
        return ""
    
    @staticmethod
    def trimStartString(s):
        for i in range(len(s)):
            if(not s[i].isspace()):
                if(i > 0): return s[i:]
                return s
        return ""

    @staticmethod
    def getCharAtStringIO(s, i):
        p = s.tell()
        s.seek(i, io.SEEK_SET)
        ret = s.read(1)
        s.seek(p, io.SEEK_SET)
        return ret

    @staticmethod
    def setCharAtStringIO(s, i, ch):
        p = s.tell()
        s.seek(i, io.SEEK_SET)
        s.write(ch)
        s.seek(p, io.SEEK_SET)
        return ch

    @staticmethod
    def setLengthStringIO(s, i):
        s.truncate(i)
        s.seek(0, io.SEEK_END)

    @staticmethod
    def getLengthIO(s):
        p = s.tell()
        s.seek(0, io.SEEK_END)
        le = s.tell()
        s.seek(p, io.SEEK_SET)
        return le

    @staticmethod
    def readTextIO(s):
        ret = s.read(1)
        if(ret is None): return -1
        if(len(ret) != 1): return -1
        return ord(ret[0])

    @staticmethod
    def readLineIO(s):
        ret = s.readline()
        if(ret is None): return None
        if(len(ret) > 0): 
            if(ret[len(ret) - 1] == '\n'): ret = ret[:len(ret) - 1]
        if(len(ret) > 0): 
            if(ret[len(ret) - 1] == '\r'): ret = ret[:len(ret) - 1]
        if(len(ret) > 0): 
            return ret
        if(Utils.getLengthIO(s) >= s.tell()): return None
        return ''

    @staticmethod
    def readByteIO(s):
        ret = s.read(1)
        if(ret is None): return -1
        if(len(ret) != 1): return -1
        return ret[0]

    @staticmethod
    def writeByteIO(s, b):
        arr = bytearray()
        arr.append(b)
        s.write(arr)

    @staticmethod
    def readIO(s, buf, i, le):
        if(i == 0 and len(buf) == le):
            return s.readinto(buf)
        ret = s.read(le)
        if(ret is None): return -1
        le = len(ret)
        if(le == 0): return 0
        for j in range(le):
            buf[i + j] = ret[j]
        return le
    
    @staticmethod
    def writeIO(s, buf, i, le):
        if(i == 0 and len(buf) == le):
            return s.write(buf)
        bb = buf[i:i + le]
        return s.write(bb)

    @staticmethod
    def newStringIO(v):
        res = io.StringIO()
        if(v is not None): print(v, end="", file=res)
        return res

    @staticmethod
    def insertStringIO(s, i, ins):
        v = s.getvalue()
        buf = str(ins) + v[i:]
        s.seek(i, io.SEEK_SET)
        s.write(buf)
        s.seek(0, io.SEEK_END)

    @staticmethod
    def removeStringIO(s, i, l):
        v = s.getvalue()
        vl = len(v)
        if(i + l < vl):
            vv = v[i + l:]
            s.seek(i, io.SEEK_SET)
            s.write(vv)
        s.truncate(vl - l)
        s.seek(0, io.SEEK_END)

    @staticmethod
    def replaceStringIO(s, old, new):
        v = s.getvalue().replace(old, new)
        s.truncate(0)
        s.seek(0, io.SEEK_SET)
        s.write(v)
        s.seek(0, io.SEEK_END)

        
    @staticmethod
    def toStringStringIO(s):
        v = s.getvalue()
        if(len(v) > s.tell()):
            return v[0:s.tell()]
        return v

    @staticmethod
    def getFilenameWithoutExt(f):
        ext = PurePath(f).suffix
        if(ext is None or ext == '.'): return f
        return f[: len(f) - len(ext)]
    
    @staticmethod
    def getResourcesNames(di, exts):
        ee = Utils.splitString(exts, ';', True)
        res = []
        for rn in pkg_resources.ResourceManager().resource_listdir(di, ''):
            for e in ee:
                if(PurePath(rn).suffix == e):
                    res.append(rn)
                    break
        return res
    
    @staticmethod
    def getResourceStream(di, name):
        try:
            for rn in pkg_resources.ResourceManager().resource_listdir(di, ''):
                fname = PurePath(rn).name
                if(Utils.endsWithString(name, fname, True)):
                    return pkg_resources.ResourceManager().resource_stream(di, fname)
        except:
            return None

    @staticmethod
    def getResourceInfo(di, name):
        try:
            for rn in pkg_resources.ResourceManager().resource_listdir(di, ''):
                fname = PurePath(rn).name
                if(Utils.endsWithString(name, fname, True)):
                    return fname
            return None
        except:
            return None

    @staticmethod
    def parseXmlFromString(txt):
        tree = xml.etree.ElementTree.ElementTree()
        root = xml.etree.ElementTree.fromstring(txt)
        tree._root = root
        return tree

    @staticmethod
    def getXmlAttrByName(attrs, tag):
        try:
            return (tag,attrs[tag])
        except:
            return None

    @staticmethod
    def getXmlAttrByIndex(attrs, i):
        try:
            for a in attrs.items():
                if(i == 0): return a
                i -= 1
            return None
        except:
            return None

    @staticmethod
    def getXmlInnerText(e):
        res = ""
        for t in e.itertext():
            res += t
        if(len(res) == 0): return None
        return res
