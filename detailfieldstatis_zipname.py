import os
import zipfile
from xml.dom.minidom import parseString
from copy import deepcopy
import time
import datetime
import xml.etree.ElementTree as ETree

def bcpdealall():
    bcpgetall = []
    localpath = []
    for root, dirs, files in os.walk("./data", topdown=False):
        for allfiles in files:
            localpath.append(os.path.join(root, allfiles))
        # for allpath in dirs:
        # 	localpath.append(os.path.join(root,allpath))

    for zipnum in localpath:
        try:
            if '/dns/' not in zipnum and '/tmp/' not in zipnum and 'https' not in zipnum:
                if zipfile.is_zipfile(zipnum):
                    print("zipname:", zipnum)
                    realzip = zipfile.ZipFile(zipnum)
                    files = realzip.namelist()
                    for i in files:
                        if i == 'GAB_ZIP_INDEX.xml':
                            xmlget = realzip.read(i)
                            dictItem, source = anaIndexXml(xmlget)
                            xmlok = True
                            break
                        else:
                            continue
                    if xmlok:
                        for bcp in files:
                            if bcp.endswith('.bcp'):
                                bcpget = realzip.read(bcp)
                                bcpget = str(bcpget)
                                bcplist = bcpget.split('\\n')
                                for bcpitem in bcplist:
                                    if bcpitem != '' and '\\t' in bcpitem:
                                        bcpitemlist = bcpitem.split('\\t')
                                        for childNum, key in zip(bcpitemlist, dictItem.keys()):
                                            dictItem[key] = childNum
                                        dictItem['H010005'] = zipnum
                                        bcpgetall.append(dictItem)
                                        dictItem = deepcopy(dictItem)
                    else:
                        realzip.close()
                        continue
                    realzip.close()
                    #os.remove(zipnum)
                else:
                    continue
        except:
            continue
    return bcpgetall

def walkXml(root_node, level, result_list):
    temp_list = [level, root_node.tag,
                 root_node.attrib, root_node, root_node.text]
    result_list.append(temp_list)

    # bianli
    # children_node = root_node.getchildren()
    # python 3.7+ use list(root_node) instead of root_node.getchildren()
    children_node = list(root_node)
    if len(children_node) == 0:
        return
    for child in children_node:
        walkXml(child, level + 1, result_list)
    return

def anaIndexXml(xmlContent):
    dictItem = {}
    if xmlContent == '':
        return dictItem
    root = ETree.fromstring(xmlContent)
    source = ''
    listXmlNode = []
    walkXml(root, 1, listXmlNode)
    for xmlNode in listXmlNode:
        if xmlNode[1] == 'ITEM' and 'key' in xmlNode[2] and xmlNode[2]['key'] == "A010004":
            source = xmlNode[2]['val']
        if xmlNode[1] == 'DATASET' and 'rmk' in xmlNode[2] and xmlNode[2]['rmk'] == 'BCP_JIEGOU':
            listNode = xmlNode[3].find('DATA').findall('ITEM')
            nIndex = 0
            for node in listNode:
                dictItem[node.attrib['key']] = nIndex
                nIndex += 1
    return dictItem, source

def isChinese(word):
    for ch in word:
        if not '\u4e00' <= ch <= '\u9fff':
            return False
    return True

def bcpcfieldstatistic(bcpgetall,now_time):
    if len(bcpgetall) > 1:
        bcpallnum = len(bcpgetall)

        dinggouAll = 0
        thingsname = 0
        shouhuoren = 0
        deliinfo = 0
        shopperinfo = 0

        kuaidiNo = 0
        fajianrenshoujianren = 0

        thingsterminal = 0

        H040001 = 0  # liaotianneirong
        H010019 = 0  # liaotiaotupian

        thingsofphone = 0
        thingsofimei = 0

        # wixinxinxi
        weixinname = 0

        # zhenshishenfen
        zhenshishenfen = 0

        # sima
        mobileno = 0
        imeino = 0
        imsino = 0
        macno = 0
        erma = 0

        mobileimei = 0
        mobileimsi = 0
        mobilemac = 0
        imeiimsi = 0
        imeimac = 0
        imsimac = 0

        # cheliangxinxi
        cheliangxinxi = 0
        recheguanlian = 0
        chaliangzhuangtai = 0
        cheliangweizhi = 0

        # loction
        jingweidu = 0

        mobileimeiimsi = 0
        mobileimeimac = 0
        imeiimsimac = 0
        mobileimsimac = 0

        errorbcp = ''
        for bcp in bcpgetall:
            try:
                # danma
                if 'Z002X11' in bcp.keys():
                    if 'MOBILE' in bcp['Z002X11']:
                        mobileno += 1
                    if 'IMEI' in bcp['Z002X11']:
                        imeino += 1
                    if 'IMSI' in bcp['Z002X11']:
                        imsino += 1
                    if 'MAC' in bcp['Z002X11']:
                        macno += 1

                # erma
                if 'Z002X11' in bcp.keys():
                    if 'MOBILE' in bcp['Z002X11'] and 'IMEI' in bcp['Z002X11']:
                        mobileimei += 1
                    if 'MOBILE' in bcp['Z002X11'] and 'IMSI' in bcp['Z002X11']:
                        mobileimsi += 1
                    if 'MOBILE' in bcp['Z002X11'] and 'MAC' in bcp['Z002X11']:
                        mobilemac += 1
                    if 'IMEI' in bcp['Z002X11'] and 'IMSI' in bcp['Z002X11']:
                        imeiimsi += 1
                    if 'IMEI' in bcp['Z002X11'] and 'MAC' in bcp['Z002X11']:
                        imeimac += 1
                    if 'IMSI' in bcp['Z002X11'] and 'MAC' in bcp['Z002X11']:
                        imsimac += 1

                # sanma
                if 'Z002X11' in bcp.keys():
                    if 'MOBILE' in bcp['Z002X11'] and 'IMEI' in bcp['Z002X11'] and 'IMSI' in bcp['Z002X11']:
                        mobileimeiimsi += 1
                    if 'MOBILE' in bcp['Z002X11'] and 'IMEI' in bcp['Z002X11'] and 'MAC' in bcp['Z002X11']:
                        mobileimeimac += 1
                    if 'IMEI' in bcp['Z002X11'] and 'IMSI' in bcp['Z002X11'] and 'MAC' in bcp['Z002X11']:
                        imeiimsimac += 1
                    if 'MOBILE' in bcp['Z002X11'] and 'IMSI' in bcp['Z002X11'] and 'MAC' in bcp['Z002X11']:
                        mobileimsimac += 1

                # jingweidu
                if bcp['H010002'] == '146':
                    if bcp['Z002536'] != '' and bcp['Z002537'] != '' and bcp['F010020'] != '' and bcp['F010021'] != '':
                        jingweidu += 1

                # dinggoushuju
                if bcp['H010002'] == '122':
                    dinggouAll += 1
                    if bcp['C010001'] != '':
                        thingsname += 1
                    if bcp['B020005'] != '' or bcp['B020008'] != '' or bcp['H150002'] != '':
                        shouhuoren += 1
                    if bcp['Z002490'] != '' or bcp['Z002491'] != '':
                        deliinfo += 1
                    if bcp['B050009'] != '' or bcp['B050010'] != '' or bcp['Z002191'] != '':
                        shopperinfo += 1

                # kuajingkuaidi
                    if not isChinese(bcp['B020008']) or not isChinese(bcp['H150002']) or\
                            not isChinese(bcp['H010044']) or not isChinese(bcp['B030403']):
                        fajianrenshoujianren += 1
                        kuaidiNo += 1

                # _0027
                if bcp['H010002'] == '124':
                    if not isChinese(bcp['B020012']) or not isChinese(bcp['B020015']):
                        if bcp['Z002492'] != '':
                            kuaidiNo += 1
                # kuaidi fajianren shou jian ren
                    if not isChinese(bcp['B020012']) or not isChinese(bcp['B020015']):
                        if bcp['B020010'] != '' or bcp['B020011'] != '' or bcp['B020012'] != ''\
                                or bcp['B020013'] != '' or bcp['B020014'] != '' or bcp['B020015'] != '':
                            fajianrenshoujianren += 1

                # liaotian neirong H040001
                if bcp['H010002'] == '103':
                    if bcp['H040001'] != '':
                        H040001 += 1
                if bcp['H010002'] == '133':
                    if bcp['H040001'] != '':
                        H040001 += 1
                if bcp['H010002'] == '145':
                    if bcp['H040001'] != '':
                        H040001 += 1
                if bcp['H010002'] == '104':
                    if bcp['H040001'] != '':
                        H040001 += 1
                if bcp['H010002'] == '106':
                    if bcp['H040001'] != '':
                        H040001 += 1
                # liaotian tupiand deng H010019
                if bcp['H010002'] == '103':
                    if bcp['H010019'] != '':
                        H010019 += 1
                if bcp['H010002'] == '133':
                    if bcp['H010019'] != '':
                        H010019 += 1
                if bcp['H010002'] == '145':
                    if bcp['H010019'] != '':
                        H010019 += 1
                if bcp['H010002'] == '104':
                    if bcp['H010019'] != '':
                        H010019 += 1
                if bcp['H010002'] == '106':
                    if bcp['H010019'] != '':
                        H010019 += 1

                # wulianwang zhongduan
                if bcp['H010002'] == 'F68':
                    if bcp['I070012'] != '' or bcp['I070011'] != '' \
                            or bcp['B050009'] != '' or bcp['H070005'] != '' \
                            or bcp['Z002223'] != '' or bcp['F030005'] != '':
                        thingsterminal += 1

                # wulianwang kahao
                if bcp['H010002'] == 'F68' or bcp['H010002'] == 'J1D':
                    if bcp['Z0024A4'] != '' or bcp['Z0021B1'] != '':
                        thingsofphone += 1

                if bcp['H010002'] == '109' or bcp['H010002'] == 'F68' or bcp['H010002'] == 'J1D' or bcp['H010002'] == 'JIE':
                    if bcp['Z0024A4'] != '':
                        thingsofphone += 1

                # #car info
                if bcp['H010002'] == '124' or bcp['H010002'] == 'A3D' or bcp['H010002'] == 'F4E' or\
                        bcp['H010002'] == '153' or bcp['H010002'] == 'F1A' or bcp['H010002'] == 'F59' or\
                        bcp['H010002'] == 'J1D' or bcp['H010002'] == 'JIE' or bcp['H010002'] == 'F68':
                    if bcp['C030002'] != '':
                        cheliangxinxi += 1

                if bcp['H010002'] == 'F4E':
                    if bcp['C030003'] != '':
                        cheliangxinxi += 1

                if bcp['H010002'] == '153' or bcp['H010002'] == 'J1D' or bcp['H010002'] == 'F4E':
                    if bcp['C030004'] != '':
                        cheliangxinxi += 1

                if bcp['H010002'] == 'J1D':
                    if bcp['C030026'] != '':
                        cheliangxinxi += 1

                # ren che guanlian
                if bcp['H010002'] == 'F4E':
                    if bcp['H230041'] != '' or bcp['H230043'] != '' or bcp['H230044'] != '' or\
                            bcp['B050027'] != '' or bcp['B070004'] != '' or bcp['Z0021TA'] != '' or\
                            bcp['Z0021IB'] != '' or bcp['Z0021SQ'] != '' or bcp['H090010'] != '' or\
                            bcp['H090009'] != '' or bcp['B030012'] != '' or bcp['B020005'] != '':
                        if bcp['H230041'] != '' or bcp['H230043'] != '' or bcp['H230044'] != '' or bcp['B050027'] != '':
                            recheguanlian += 1

                if bcp['H010002'] == '153':
                    if bcp['B070004'] != '' or bcp['B020005'] != '':
                        if bcp['C030002'] != '' or bcp['C030004'] != '' or bcp['C010002'] != '':
                            recheguanlian += 1

                if bcp['H010002'] == 'F1A':
                    if bcp['B070004'] != '' or bcp['H090009'] != '' or bcp['H090009'] != '':
                        if bcp['C030002'] != '':
                            recheguanlian += 1

                if bcp['H010002'] == 'F68':
                    if bcp['B020005'] != '':
                        if bcp['C030002'] != '' or bcp['C030004'] != '':
                            recheguanlian += 1

                if bcp['H010002'] == 'F59':
                    if bcp['Z002459'] != '' or bcp['Z002152'] != '' or bcp['Z0021E3'] != '' or bcp['B020005'] != '':
                        if bcp['C030002'] != '' or bcp['C010002'] != '' or bcp['C010003'] != '':
                            recheguanlian += 1

                if bcp['H010002'] == 'J1D':
                    if bcp['Z002459'] != '' or bcp['B030038'] != '' or bcp['B020005'] != '':
                        if bcp['C030002'] != '' or bcp['C030026'] != '' or bcp['C030004'] != '' or bcp['C030015'] != '':
                            recheguanlian += 1

                # cheliangzhuangtai
                if bcp['H010002'] == 'F68':
                    if bcp['F010027'] != '' or bcp['I050051'] != '':
                        chaliangzhuangtai += 1

                if bcp['H010002'] == 'J1D':
                    if bcp['Z002169'] != '' or bcp['Z002290'] != '' or bcp['C030045'] != '' or bcp['Z0027P2'] != '':
                        chaliangzhuangtai += 1

                # cheliang weizhi
                if bcp['H010002'] == 'F59':
                    if bcp['G020016'] != '' or bcp['J030007'] != '' or bcp['Z002518'] != '' or bcp['D010002'] != ''\
                            or bcp['K000713'] != '' or bcp['K000716'] != '':
                        cheliangweizhi += 1

                if bcp['H010002'] == 'J1D':
                    if bcp['H230017'] != '' or bcp['H230018'] != '':
                        cheliangweizhi += 1

                # zhenshishenfen
                if bcp['H010002'] == '117' or bcp['H010002'] == '123' or bcp['H010002'] == '124' or\
                        bcp['H010002'] == '132' or bcp['H010002'] == '126' or bcp['H010002'] == '130' or\
                        bcp['H010002'] == '131' or bcp['H010002'] == '143' or bcp['H010002'] == '145' or\
                        bcp['H010002'] == '152' or bcp['H010002'] == 'A3D' or bcp['H010002'] == 'A8C' or\
                        bcp['H010002'] == '153' or bcp['H010002'] == 'F1A' or bcp['H010002'] == 'J1C' or\
                        bcp['H010002'] == 'J1D':
                    if bcp['H090011'] != '' or bcp['B070002'] != '':
                        zhenshishenfen += 1

                if bcp['H010002'] == '124' or bcp['H010002'] == 'A3D' or bcp['H010002'] == 'F4E' or\
                        bcp['H010002'] == '153' or bcp['H010002'] == 'F1A' or bcp['H010002'] == 'F68' or\
                        bcp['H010002'] == 'F59' or bcp['H010002'] == 'J1D' or bcp['H010002'] == 'JIE':
                    if bcp['C030002'] != '':
                        zhenshishenfen += 1

                if bcp['H010002'] == '122' or bcp['H010002'] == '123' or bcp['H010002'] == '126' or\
                        bcp['H010002'] == '129' or bcp['H010002'] == '130' or bcp['H010002'] == 'A3D' or\
                        bcp['H010002'] == 'F4E' or bcp['H010002'] == '153' or bcp['H010002'] == 'E0L':
                    if bcp['H090009'] != '':
                        zhenshishenfen += 1

                if bcp['H010002'] == '114' or bcp['H010002'] == 'A3D' or bcp['H010002'] == 'J1D' or\
                        bcp['H010002'] == 'J1A':
                    if bcp['B030303'] != '':
                        zhenshishenfen += 1

                if bcp['H010002'] == '119' or bcp['H010002'] == '120' or bcp['H010002'] == '123' or\
                        bcp['H010002'] == '126' or bcp['H010002'] == '132' or bcp['H010002'] == 'D62' or\
                        bcp['H010002'] == 'F4E' or bcp['H010002'] == 'F2B' or bcp['H010002'] == '153' or\
                        bcp['H010002'] == 'F1A' or bcp['H010002'] == 'J1C':
                    if bcp['B070004'] != '':
                        zhenshishenfen += 1

                if bcp['H010002'] == 'J1C':
                    if bcp['K000002'] != '' or bcp['Z002459'] != '':
                        zhenshishenfen += 1

                if bcp['H010002'] == '101' or bcp['H010002'] == '103' or bcp['H010002'] == '104' or\
                        bcp['H010002'] == '107' or bcp['H010002'] == '120' or bcp['H010002'] == '115' or\
                        bcp['H010002'] == '122' or bcp['H010002'] == '124' or bcp['H010002'] == '126' or\
                        bcp['H010002'] == '127' or bcp['H010002'] == '132' or bcp['H010002'] == '133' or\
                        bcp['H010002'] == '138' or bcp['H010002'] == '142' or bcp['H010002'] == '143' or\
                        bcp['H010002'] == '145' or bcp['H010002'] == '152' or bcp['H010002'] == 'A3D' or\
                        bcp['H010002'] == 'A89' or bcp['H010002'] == 'A8C' or bcp['H010002'] == 'F4E' or\
                        bcp['H010002'] == 'F2B' or bcp['H010002'] == 'F2D' or bcp['H010002'] == '153' or\
                        bcp['H010002'] == 'C3F' or bcp['H010002'] == 'E0L' or bcp['H010002'] == 'F1A' or\
                        bcp['H010002'] == 'E0K' or bcp['H010002'] == 'F1B' or bcp['H010002'] == 'F2E':
                    if bcp['B020005'] != '':
                        zhenshishenfen += 1

                # weixin name
                if bcp['H010002'] == '103':
                    if bcp['Z0021F9'] != '' or bcp['B060005'] != '' \
                            or bcp['Z0021G3'] != '' or bcp['Z0021G4'] != '' \
                            or bcp['D020004'] != '' or bcp['Z0023A5'] != ''\
                            or bcp['Z0021G5'] != '' or bcp['B040003'] != '' or bcp['B040004'] != '':
                        weixinname += 1
                if bcp['H010002'] == 'J1A':
                    if bcp['Z002619'] != '' or bcp['C060001'] != '':
                        weixinname += 1
                if bcp['H010002'] == '143':
                    if bcp['Z0021F9'] != '':
                        weixinname += 1
                if bcp['H010002'] == 'A3D':
                    if bcp['Z0021G4'] != '':
                        weixinname += 1

            except Exception as e:
                errorbcp = str(bcp)
                continue
        outlog = 'allbcpnum            : ' + str(bcpallnum) \
            + '\n' + 'kuaijingdanhao       : ' + str(kuaidiNo) \
            + '\n' + 'fajianrenshoujianren : ' + str(fajianrenshoujianren) \
            + '\n' + 'thingsname           : ' + str(thingsname) \
            + '\n' + 'shouhuoren           : ' + str(shouhuoren) \
            + '\n' + 'deliinfo             : ' + str(deliinfo) \
            + '\n' + 'shopperinfo          : ' + str(shopperinfo)\
            + '\n' + 'wulianwang           : ' + str(thingsterminal)\
            + '\n' + 'wulianwang No        : ' + str(thingsofphone+thingsofimei)\
            + '\n' + 'im No                : ' + str(H040001)\
            + '\n' + 'imfile No            : ' + str(H010019)\
            + '\n' + 'zhenshi shenfen      : ' + str(zhenshishenfen)\
            + '\n' + 'weixin shenfen       : ' + str(weixinname) \
            + '\n' + 'mobile               : ' + str(mobileno) \
            + '\n' + 'imei                 : ' + str(imeino) \
            + '\n' + 'imsi                 : ' + str(imsino) \
            + '\n' + 'mac                  : ' + str(macno) \
            + '\n' + 'mobile&imei          : ' + str(mobileimei) \
            + '\n' + 'mobile&imsi          : ' + str(mobileimsi) \
            + '\n' + 'mobile&mac           : ' + str(mobilemac) \
            + '\n' + 'imei&imsi            : ' + str(imeiimsi) \
            + '\n' + 'imei&mac             : ' + str(imeimac) \
            + '\n' + 'imsi&mac             : ' + str(imsimac) \
            + '\n' + 'MOBILE&IMEI&IMSI     : ' + str(mobileimeiimsi) \
            + '\n' + 'MOBILE&IMEI&MAC      : ' + str(mobileimeimac) \
            + '\n' + 'IMEI&IMSI&MAC        : ' + str(imeiimsimac) \
            + '\n' + 'MOBILE&IMSI&MAC      : ' + str(mobileimsimac) \
            + '\n' + 'LAT&LON              : ' + str(jingweidu)\
            + '\n' + 'carinfo              : ' + str(cheliangxinxi)\
            + '\n' + 'rencheguanlian       : ' + str(recheguanlian)\
            + '\n' + 'cheliangzhuangtai    : ' + str(chaliangzhuangtai)\
            + '\n' + 'cheliangweizhixinx   : ' + str(cheliangweizhi)

        now_time = datetime.datetime.now()
        localtime = datetime.datetime.strptime(
        str(now_time).split('.')[0], '%Y-%m-%d %H:%M:%S')
        logfile = str(localtime).replace(' ', '_').replace(':', '_')+'.log'
        errorlog = str(localtime).replace(' ', '_').replace(':', '_')+'_error.log'
        fbcpall = open(logfile, 'w', encoding='utf-8')
        fbcpall.write(outlog)
        fbcpall.close()
        if errorbcp != '':
            fbcperr = open(errorlog, 'w', encoding='utf-8')
            fbcperr.write(errorbcp)
            fbcperr.close()

def delcommomfield(bcpgetall):
    # delete all common fields except H010002
    commonkey = ['H010006', 'H010007', 'B020001', 'H010018', 'F020004', 'F020010', 'F020005', 'F020011', 'F020006', 'F020012', 'F020007', 'F020013', 'H040002', 'H010014', 'B050016', 'G020014', 'H010013', 'B040021', 'B040022', 'B020007', 'C050001', 'C040004', 'C040003', 'B030001', 'B030004', 'B030005', 'G020004', 'F010001', 'F010002', 'F010009', 'F030002', 'B030020', 'B030021', 'H010034', 'I010009', 'F020001', 'B030002', 'B010001', 'H010031', 'H010032', 'H010033', 'H010035', 'H010036', 'H010037', 'F040007', 'G020013', 'F030013', 'F030014', 'F010008', 'G020036', 'F020016','F020017', 'C020017', 'C020011', 'C020009', 'C020005', 'H070003', 'C020006', 'C020007', 'C020021', 'C020022', 'H010041', 'H010042', 'Z002600', 'Z002606', 'Z002700', 'Z002504', 'Z002505', 'Z002604', 'Z002605', 'Z002603', 'Z002101', 'Z002534', 'Z002570', 'Z002050', 'Z002051', 'Z002052', 'Z002053', 'Z002054', 'Z002055', 'Z002056', 'Z002057', 'F030017', 'F030020', 'Z002060', 'Z002061', 'Z002080', 'Z002716', 'Z002049', 'Z0025A4', 'Z002091', 'Z0020A1', 'Z0020A2', 'Z0020A3', 'Z0020A4', 'I070005', 'Z002742', 'Z0020AE', 'Z0020AF', 'Z0020AG', 'Z0020AH', 'Z002X49', 'Z002X48', 'Z002X11', 'Z002X10']
    for i in bcpgetall:
        for com in commonkey:
            try:
                del i[com]
            except:
                continue
    for nozero in bcpgetall:
        for non in nozero:
            if nozero[non] == '0':
                nozero[non] = ''
    return bcpgetall

def dealallprivatefield(bcpgetall):
    # append the nonzero-field to a new fields
    #allfield = []
    allfields = {}
    for bcp in bcpgetall:
        for eachbcp in bcp:
            try:
                if bcp[eachbcp] != '':
                    # bcpfieldcountshu = []
                    # bcpfieldcountshu.append(tuple(bcp['H010002'],bcp['H010001'],bcp['H010003'],eachbcp))
                    # # bcpfieldcountshu.append(bcp['H010002'])
                    # # bcpfieldcountshu.append(bcp['H010001'])
                    # # bcpfieldcountshu.append(bcp['H010003'])
                    # # bcpfieldcountshu.append(eachbcp)
                    # allfield.append(bcpfieldcountshu)
                    if bcp['H010005'] not in allfields:
                        allfields[bcp['H010005']] = {}
                    if bcp['H010002'] not in allfields[bcp['H010005']]:
                        allfields[bcp['H010005']][bcp['H010002']] = {}
                    if bcp['H010001'] not in allfields[bcp['H010005']][bcp['H010002']]:
                        allfields[bcp['H010005']][bcp['H010002']][bcp['H010001']] = {}
                    if bcp['H010003'] not in allfields[bcp['H010005']][bcp['H010002']][bcp['H010001']]:
                        allfields[bcp['H010005']][bcp['H010002']][bcp['H010001']][bcp['H010003']] = {}
                    if eachbcp not in allfields[bcp['H010005']][bcp['H010002']][bcp['H010001']][bcp['H010003']]:
                        allfields[bcp['H010005']][bcp['H010002']][bcp['H010001']][bcp['H010003']][eachbcp] = 0
                    allfields[bcp['H010005']][bcp['H010002']][bcp['H010001']][bcp['H010003']][eachbcp] += 1
            except:
                continue
    return allfields

def privitefieldcount(allfield):
    # counting man func
    output = []
    outputcount = []
    for eachdalei in allfield:
        output.append(tuple(eachdalei))
    for eachbcp in range(0,len(output)):
        tuplecount = {'FIELDKEY':'','COUNT':0}
        for pcbhcae in range(0,len(output)):
            if output[eachbcp] == output[pcbhcae]:
                jugelye = False
                if len(outputcount) > 0:
                    for jugel in range(0,len(outputcount)):
                            if outputcount[jugel]['FIELDKEY'] == output[eachbcp]:
                                jugelye = True
                                break
                    if jugelye:
                        tuplecount['COUNT'] += 1
                    else:
                        outputcount.append(tuplecount)
                        tuplecount['FIELDKEY'] = output[eachbcp]
                        tuplecount['COUNT'] += 1
                else:
                    outputcount.append(tuplecount)
                    tuplecount['FIELDKEY'] = output[eachbcp]
                    tuplecount['COUNT'] += 1
        tuplecount = deepcopy(tuplecount)
    return outputcount

def fieldsdetailoutput(outputcount,now_time):
    privitefields = delcommomfield(outputcount)
    out = dealallprivatefield(privitefields)
    # outlog = privitefieldcount(out)
    localtime = datetime.datetime.strptime(str(now_time).split('.')[0], '%Y-%m-%d %H:%M:%S')
    logfile = str(localtime).replace(' ', '_').replace(':', '_')+'_APP_TYPE_SMTYPE_ACTION_FIELD_COUNT.log'
    fbcpall = open(logfile, 'w', encoding='utf-8')
    fbcpall.write(str(out)+'\n')
    #now_time = datetime.datetime.now()
    fbcpall.close()

def run():
    fields = bcpdealall()
    now_time = datetime.datetime.now()
    # bcpcfieldstatistic(fields,now_time)
    fieldsdetailoutput(fields,now_time)

if __name__ == "__main__":
    run()
