import hashlib
import os
import Utils
from worlds.Files import APDeltaPatch
USHASH = '2a2152976e503eaacd9815f44c262d73'
ROM_PLAYER_LIMIT = 65535

item_values = {
    0x198401: [0x1550, 0x01],
    0x198402: [0x1550, 0x02],
    0x198403: [0x1550, 0x03],
    0x198404: [0x1550, 0x04],
    0x198405: [0x1550, 0x05],
    0x198406: [0x1550, 0x06],
    0x198407: [0x1550, 0x07],
    0x198408: [0x1550, 0x08],
    0x198409: [0x1550, 0x09],
    0x19840A: [0x1550, 0x0A],
    0x19840B: [0x1550, 0x0B],
    0x19840C: [0x1550, 0x0C],
    0x19840D: [0x1550, 0x0D],
    0x19840E: [0x1550, 0x0E],
    0x19840F: [0x1550, 0x0F],
    0x198410: [0x1550, 0x10],
    0x198411: [0x1550, 0x11],
    0x198412: [0x1550, 0x12],
    0x198413: [0x1550, 0x13],
    0x198414: [0x1550, 0x14],
    0x198415: [0x1550, 0x15],
    0x198416: [0x1550, 0x16],
    0x198417: [0x1550, 0x17],
    0x198418: [0x1550, 0x18],
    0x198419: [0x1550, 0x19],
    0x19841A: [0x1550, 0x1A],
    0x19841B: [0x1550, 0x1B],
    0x19841C: [0x1550, 0x1C],
    0x19841D: [0x1550, 0x1D],
    0x19841E: [0x1550, 0x1E],
    0x19841F: [0x1550, 0x1F],
    0x198420: [0x1550, 0x20],
    0x198421: [0x1550, 0x21],
    0x198422: [0x1550, 0x22],
    0x198423: [0x1550, 0x23],
    0x198424: [0x1550, 0x24],
    0x198425: [0x1550, 0x25],
    0x198426: [0x1550, 0x26],
    0x198427: [0x1550, 0x27],
    0x198428: [0x1550, 0x28],
    0x198429: [0x1550, 0x29],
    0x19842A: [0x1550, 0x2A],
    0x19842B: [0x1550, 0x2B],
    0x19842C: [0x1550, 0x2C],
    0x19842D: [0x1550, 0x2D],
    0x19842E: [0x1550, 0x2E]

}

location_table = {
    0x198400: [0x1555, 3],
    0x198401: [0x1555, 4],
    0x198402: [0x1555, 5],
    0x198403: [0x1564, 3],
    0x198404: [0x1564, 4],
    0x198405: [0x1564, 5],

    0x198406: [0x1556, 3],
    0x198407: [0x1556, 4],
    0x198408: [0x1556, 5],
    0x198409: [0x1565, 3],
    0x19840A: [0x1565, 4],
    0x19840B: [0x1565, 5],

    0x19840C: [0x1557, 3],
    0x19840D: [0x1557, 4],
    0x19840E: [0x1557, 5],
    0x19840F: [0x1566, 3],
    0x198410: [0x1566, 4],
    0x198411: [0x1566, 5],

    0x198412: [0x1558, 3],
    0x198413: [0x1558, 4],
    0x198414: [0x1558, 5],
    0x198415: [0x1567, 3],
    0x198416: [0x1567, 4],
    0x198417: [0x1567, 5],

    0x198418: [0x1559, 3],
    0x198419: [0x1559, 4],
    0x19841A: [0x1559, 5],
    0x19841B: [0x1568, 3],
    0x19841C: [0x1568, 4],
    0x19841D: [0x1568, 5],

    0x19841E: [0x155A, 3],
    0x19841F: [0x155A, 4],
    0x198420: [0x155A, 5],
    0x198421: [0x1569, 3],
    0x198422: [0x1569, 4],
    0x198423: [0x1569, 5],

    0x198424: [0x155B, 3],
    0x198425: [0x155B, 4],
    0x198426: [0x155B, 5],
    0x198427: [0x156A, 3],
    0x198428: [0x156A, 4],
    0x198429: [0x156A, 5],

    0x19842A: [0x155C, 3],
    0x19842B: [0x155C, 4],
    0x19842C: [0x155C, 5],
    0x19842D: [0x156B, 3],
    0x19842E: [0x156B, 4],
    0x19842F: [0x156B, 5],

    0x198430: [0x155D, 3],
    0x198431: [0x155D, 4],
    0x198432: [0x155D, 5],
    0x198433: [0x156C, 3],
    0x198434: [0x156C, 4],
    0x198435: [0x156C, 5],

    0x198436: [0x155E, 3],
    0x198437: [0x155E, 4],
    0x198438: [0x155E, 5],
    0x198439: [0x156D, 3],
    0x19843A: [0x156D, 4],
    0x19843B: [0x156D, 5],

    0x19843C: [0x155F, 3],
    0x19843D: [0x155F, 4],
    0x19843E: [0x155F, 5],
    0x19843F: [0x156E, 3],
    0x198440: [0x156E, 4],
    0x198441: [0x156E, 5],

    0x198442: [0x1560, 3],
    0x198443: [0x1560, 4],
    0x198444: [0x1560, 5],
    0x198445: [0x156F, 3],
    0x198446: [0x156F, 4],
    0x198447: [0x156F, 5],

    0x198448: [0x1561, 3],
    0x198449: [0x1561, 4],
    0x19844A: [0x1561, 5],
    0x19844B: [0x1570, 3],
    0x19844C: [0x1570, 4],
    0x19844D: [0x1570, 5],

    0x19844E: [0x1562, 3],
    0x19844F: [0x1562, 4],
    0x198450: [0x1562, 5],
    0x198451: [0x1571, 3],
    0x198452: [0x1571, 4],
    0x198453: [0x1571, 5],

    0x198454: [0x1563, 3],
    0x198455: [0x1563, 4],
    0x198456: [0x1563, 5],
    0x198457: [0x1572, 3],
    0x198458: [0x1572, 4],
    0x198459: [0x1572, 5],

    0x19845A: [0x15AA, 0],
    0x19845B: [0x15AC, 0],
    0x19845C: [0x15AE, 0],
    0x19845D: [0x15A0, 0],
    0x19845E: [0x159A, 0],
    0x19845F: [0x159C, 0],
    0x198460: [0x159E, 0],
    0x198461: [0x15A8, 0],
    0x198462: [0x15A2, 0],
    0x198463: [0x15A4, 0],
    0x198464: [0x15A6, 0],
    0x198465: [0x1588, 0],
    0x198466: [0x1582, 0],
    0x198467: [0x1584, 0],
    0x198468: [0x1586, 0],
    0x198469: [0x1590, 0],
    0x19846A: [0x158A, 0],
    0x19846B: [0x158C, 0],
    0x19846C: [0x158E, 0],
    0x19846D: [0x1598, 0],
    0x19846E: [0x1592, 0],
    0x19846F: [0x1594, 0],
    0x198470: [0x1596, 0],

    0x198471: [0x15AA, 1],
    0x198472: [0x15AC, 1],
    0x198473: [0x15AE, 1],
    0x198474: [0x15A0, 1],
    0x198475: [0x159A, 1],
    0x198476: [0x159C, 1],
    0x198477: [0x159E, 1],
    0x198478: [0x15A8, 1],
    0x198479: [0x15A2, 1],
    0x19847A: [0x15A4, 1],
    0x19847B: [0x15A6, 1],
    0x19847C: [0x1588, 1],
    0x19847D: [0x1582, 1],
    0x19847E: [0x1584, 1],
    0x19847F: [0x1586, 1],
    0x198480: [0x1590, 1],
    0x198481: [0x158A, 1],
    0x198482: [0x158C, 1],
    0x198483: [0x158E, 1],
    0x198484: [0x1598, 1],
    0x198485: [0x1592, 1],
    0x198486: [0x1594, 1],
    0x198487: [0x1596, 1],

    0x198488: [0x15AA, 2],
    0x198489: [0x15AC, 2],
    0x19848A: [0x15AE, 2],
    0x19848B: [0x15A0, 2],
    0x19848C: [0x159A, 2],
    0x19848D: [0x159C, 2],
    0x19848E: [0x159E, 2],
    0x19848F: [0x15A8, 2],
    0x198490: [0x15A2, 2],
    0x198491: [0x15A4, 2],
    0x198492: [0x15A6, 2],
    0x198493: [0x1588, 2],
    0x198494: [0x1582, 2],
    0x198495: [0x1584, 2],
    0x198496: [0x1586, 2],
    0x198497: [0x1590, 2],
    0x198498: [0x158A, 2],
    0x198499: [0x158C, 2],
    0x19849A: [0x158E, 2],
    0x19849B: [0x1598, 2],
    0x19849C: [0x1592, 2],
    0x19849D: [0x1594, 2],
    0x19849E: [0x1596, 2],

    0x19849F: [0x15AA, 3],
    0x1984A0: [0x15AC, 3],
    0x1984A1: [0x15AE, 3],
    0x1984A2: [0x15A0, 3],
    0x1984A3: [0x159A, 3],
    0x1984A4: [0x159C, 3],
    0x1984A5: [0x159E, 3],
    0x1984A6: [0x15A8, 3],
    0x1984A7: [0x15A2, 3],
    0x1984A8: [0x15A4, 3],
    0x1984A9: [0x15A6, 3],
    0x1984AA: [0x1588, 3],
    0x1984AB: [0x1582, 3],
    0x1984AC: [0x1584, 3],
    0x1984AD: [0x1586, 3],
    0x1984AE: [0x1590, 3],
    0x1984AF: [0x158A, 3],
    0x1984B0: [0x158C, 3],
    0x1984B1: [0x158E, 3],
    0x1984B2: [0x1598, 3],
    0x1984B3: [0x1592, 3],
    0x1984B4: [0x1594, 3],
    0x1984B5: [0x1596, 3],

    0x1984B6: [0x15AA, 4],
    0x1984B7: [0x15AC, 4],
    0x1984B8: [0x15AE, 4],
    0x1984B9: [0x15A0, 4],
    0x1984BA: [0x159A, 4],
    0x1984BB: [0x159C, 4],
    0x1984BC: [0x159E, 4],
    0x1984BD: [0x15A8, 4],
    0x1984BE: [0x15A2, 4],
    0x1984BF: [0x15A4, 4],
    0x1984C0: [0x15A6, 4],
    0x1984c1: [0x1588, 4],
    0x1984c2: [0x1582, 4],
    0x1984C3: [0x1584, 4],
    0x1984C4: [0x1586, 4],
    0x1984C5: [0x1590, 4],
    0x1984C6: [0x158A, 4],
    0x1984C7: [0x158C, 4],
    0x1984C8: [0x158E, 4],
    0x1984C9: [0x1598, 4],
    0x1984CA: [0x1592, 4],
    0x1984CB: [0x1594, 4],
    0x1984CC: [0x1596, 4],

    0x1984CD: [0x15AA, 5],
    0x1984CE: [0x15AC, 5],
    0x1984CF: [0x15AE, 5],
    0x1984D0: [0x15A0, 5],
    0x1984D1: [0x159A, 5],
    0x1984D2: [0x159C, 5],
    0x1984D3: [0x159E, 5],
    0x1984D4: [0x15A8, 5],
    0x1984D5: [0x15A2, 5],
    0x1984D6: [0x15A4, 5],
    0x1984D7: [0x15A6, 5],
    0x1984D8: [0x1588, 5],
    0x1984D9: [0x1582, 5],
    0x1984DA: [0x1584, 5],
    0x1984DB: [0x1586, 5],
    0x1984DC: [0x1590, 5],
    0x1984DD: [0x158A, 5],
    0x1984DE: [0x158C, 5],
    0x1984DF: [0x158E, 5],
    0x1984E0: [0x1598, 5],
    0x1984E1: [0x1592, 5],
    0x1984E2: [0x1594, 5],
    0x1984E3: [0x1596, 5],

    0x1984E4: [0x15AA, 6],
    0x1984E5: [0x15AC, 6],
    0x1984E6: [0x15AE, 6],
    0x1984E7: [0x15A0, 6],
    0x1984E8: [0x159A, 6],
    0x1984E9: [0x159C, 6],
    0x1984EA: [0x159E, 6],
    0x1984EB: [0x15A8, 6],
    0x1984EC: [0x15A2, 6],
    0x1984ED: [0x15A4, 6],
    0x1984EE: [0x15A6, 6],
    0x1984EF: [0x1588, 6],
    0x1984F0: [0x1582, 6],
    0x1984F1: [0x1584, 6],
    0x1984F2: [0x1586, 6],
    0x1984F3: [0x1590, 6],
    0x1984F4: [0x158A, 6],
    0x1984F5: [0x158C, 6],
    0x1984F6: [0x158E, 6],
    0x1984F7: [0x1598, 6],
    0x1984F8: [0x1592, 6],
    0x1984F9: [0x1594, 6],
    0x1984FA: [0x1596, 6],

    0x1984FB: [0x15AA, 7],
    0x1984FC: [0x15AC, 7],
    0x1984FD: [0x15AE, 7],
    0x1984FE: [0x15A0, 7],
    0x1984FF: [0x159A, 7],
    0x198500: [0x159C, 7],
    0x198501: [0x159E, 7],
    0x198502: [0x15A8, 7],
    0x198503: [0x15A2, 7],
    0x198504: [0x15A4, 7],
    0x198505: [0x15A6, 7],
    0x198506: [0x1588, 7],
    0x198507: [0x1582, 7],
    0x198508: [0x1584, 7],
    0x198509: [0x1586, 7],
    0x19850A: [0x1590, 7],
    0x19850B: [0x158A, 7],
    0x19850C: [0x158C, 7],
    0x19850D: [0x158E, 7],
    0x19850E: [0x1598, 7],
    0x19850F: [0x1592, 7],
    0x198510: [0x1594, 7],
    0x198511: [0x1596, 7],

    0x198512: [0x15AB, 0],
    0x198513: [0x15AD, 0],
    0x198514: [0x15AF, 0],
    0x198515: [0x15A1, 0],
    0x198516: [0x159B, 0],
    0x198517: [0x159D, 0],
    0x198518: [0x159F, 0],
    0x198519: [0x15A9, 0],
    0x19851A: [0x15A3, 0],
    0x19851B: [0x15A5, 0],
    0x19851C: [0x15A7, 0],
    0x19851D: [0x1589, 0],
    0x19851E: [0x1583, 0],
    0x19851F: [0x1585, 0],
    0x198520: [0x1587, 0],
    0x198521: [0x1591, 0],
    0x198522: [0x158B, 0],
    0x198523: [0x158D, 0],
    0x198524: [0x158F, 0],
    0x198525: [0x1599, 0],
    0x198526: [0x1593, 0],
    0x198527: [0x1595, 0],
    0x198528: [0x1597, 0],

    0x198529: [0x15AB, 1],
    0x19852A: [0x15AD, 1],
    0x19852B: [0x15AF, 1],
    0x19852C: [0x15A1, 1],
    0x19852D: [0x159B, 1],
    0x19852E: [0x159D, 1],
    0x19852F: [0x159F, 1],
    0x198530: [0x15A9, 1],
    0x198531: [0x15A3, 1],
    0x198532: [0x15A5, 1],
    0x198533: [0x15A7, 1],
    0x198534: [0x1589, 1],
    0x198535: [0x1583, 1],
    0x198536: [0x1585, 1],
    0x198537: [0x1587, 1],
    0x198538: [0x1591, 1],
    0x198539: [0x158B, 1],
    0x19853A: [0x158D, 1],
    0x19853B: [0x158F, 1],
    0x19853C: [0x1599, 1],
    0x19853D: [0x1593, 1],
    0x19853E: [0x1595, 1],
    0x19853F: [0x1597, 1],

    0x198540: [0x15AB, 2],
    0x198541: [0x15AD, 2],
    0x198542: [0x15AF, 2],
    0x198543: [0x15A1, 2],
    0x198544: [0x159B, 2],
    0x198545: [0x159D, 2],
    0x198546: [0x159F, 2],
    0x198547: [0x15A9, 2],
    0x198548: [0x15A3, 2],
    0x198549: [0x15A5, 2],
    0x19854A: [0x15A7, 2],
    0x19854B: [0x1589, 2],
    0x19854C: [0x1583, 2],
    0x19854D: [0x1585, 2],
    0x19854E: [0x1587, 2],
    0x19854F: [0x1591, 2],
    0x198550: [0x158B, 2],
    0x198551: [0x158D, 2],
    0x198552: [0x158F, 2],
    0x198553: [0x1599, 2],
    0x198554: [0x1593, 2],
    0x198555: [0x1595, 2],
    0x198556: [0x1597, 2],

    0x198557: [0x15AB, 3],
    0x198558: [0x15AD, 3],
    0x198559: [0x15AF, 3],
    0x19855A: [0x15A1, 3],
    0x19855B: [0x159B, 3],
    0x19855C: [0x159D, 3],
    0x19855D: [0x159F, 3],
    0x19855E: [0x15A9, 3],
    0x19855F: [0x15A3, 3],
    0x198560: [0x15A5, 3],
    0x198561: [0x15A7, 3],
    0x198562: [0x1589, 3],
    0x198563: [0x1583, 3],
    0x198564: [0x1585, 3],
    0x198565: [0x1587, 3],
    0x198566: [0x1591, 3],
    0x198567: [0x158B, 3],
    0x198568: [0x158D, 3],
    0x198569: [0x158F, 3],
    0x19856A: [0x1599, 3],
    0x19856B: [0x1593, 3],
    0x19856C: [0x1595, 3],
    0x19856D: [0x1597, 3],

    0x19856E: [0x15AB, 4],
    0x19856F: [0x15AD, 4],
    0x198570: [0x15AF, 4],
    0x198571: [0x15A1, 4],
    0x198572: [0x159B, 4],
    0x198573: [0x159D, 4],
    0x198574: [0x159F, 4],
    0x198575: [0x15A9, 4],
    0x198576: [0x15A3, 4],
    0x198577: [0x15A5, 4],
    0x198578: [0x15A7, 4],
    0x198579: [0x1589, 4],
    0x19857A: [0x1583, 4],
    0x19857B: [0x1585, 4],
    0x19857C: [0x1587, 4],
    0x19857D: [0x1591, 4],
    0x19857E: [0x158B, 4],
    0x19857F: [0x158D, 4],
    0x198580: [0x158F, 4],
    0x198581: [0x1599, 4],
    0x198582: [0x1593, 4],
    0x198583: [0x1595, 4],
    0x198584: [0x1597, 4],

    0x198585: [0x15AB, 5],
    0x198586: [0x15AD, 5],
    0x198587: [0x15AF, 5],
    0x198588: [0x15A1, 5],
    0x198589: [0x159B, 5],
    0x19858A: [0x159D, 5],
    0x19858B: [0x159F, 5],
    0x19858C: [0x15A9, 5],
    0x19858D: [0x15A3, 5],
    0x19858E: [0x15A5, 5],
    0x19858F: [0x15A7, 5],
    0x198590: [0x1589, 5],
    0x198591: [0x1583, 5],
    0x198592: [0x1585, 5],
    0x198593: [0x1587, 5],
    0x198594: [0x1591, 5],
    0x198595: [0x158B, 5],
    0x198596: [0x158D, 5],
    0x198597: [0x158F, 5],
    0x198598: [0x1599, 5],
    0x198599: [0x1593, 5],
    0x19859A: [0x1595, 5],
    0x19859B: [0x1597, 5],

    0x19859C: [0x15AB, 6],
    0x19859D: [0x15AD, 6],
    0x19859E: [0x15AF, 6],
    0x19859F: [0x15A1, 6],
    0x1985A0: [0x159B, 6],
    0x1985A1: [0x159D, 6],
    0x1985A2: [0x159F, 6],
    0x1985A3: [0x15A9, 6],
    0x1985A4: [0x15A3, 6],
    0x1985A5: [0x15A5, 6],
    0x1985A6: [0x15A7, 6],
    0x1985A7: [0x1589, 6],
    0x1985A8: [0x1583, 6],
    0x1985A9: [0x1585, 6],
    0x1985AA: [0x1587, 6],
    0x1985AB: [0x1591, 6],
    0x1985AC: [0x158B, 6],
    0x1985AD: [0x158D, 6],
    0x1985AE: [0x158F, 6],
    0x1985AF: [0x1599, 6],
    0x1985B0: [0x1593, 6],
    0x1985B1: [0x1595, 6],
    0x1985B2: [0x1597, 6]
}

class LocalRom(object):

    def __init__(self, file, vanillaRom=None, name=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = Utils.read_snes_rom(stream)

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())

def rom_code(rom):
    rom.write_bytes(0x008510, bytearray([0x48, 0xa9, 0x69, 0x42, 0x8d, 0x45, 0x15, 0x68, 0x80, 0x22]))
    rom.write_bytes(0x002FE3, bytearray([0x5c, 0x03, 0xff, 0x02]))
    rom.write_bytes(0x00ACF5, bytearray([0x5c, 0x48, 0xff, 0x02]))
    rom.write_bytes(0x0028FB, bytearray([0x5c, 0x70, 0xff, 0x02]))
    rom.write_bytes(0x004EC8, bytearray([0x4C, 0x40, 0xCF]))
    rom.write_bytes(0x009FBC, bytearray([0x80]))
    rom.write_bytes(0x0057EA, bytearray([0xEA, 0xEA]))
    rom.write_bytes(0x0057F2, bytearray([0x80]))
    rom.write_bytes(0x005827, bytearray([0x5c, 0x5B, 0xFF, 0x08]))
    rom.write_bytes(0x006C1C, bytearray([0x5c, 0x81, 0xFF, 0x02]))
    rom.write_bytes(0x005808, bytearray([0xC9, 0x01, 0x00, 0x80, 0x11]))
    rom.write_bytes(0x00AC75, bytearray([0x5c, 0x50, 0xFE, 0x08]))
    rom.write_bytes(0x00ACFA, bytearray([0x08, 0x00, 0x10, 0x00, 0x20, 0x00]))
    rom.write_bytes(0x0029AE, bytearray([0x5c, 0x80, 0xFE, 0x08]))
    rom.write_bytes(0x002738, bytearray([0x80]))
    rom.write_bytes(0x002945, bytearray([0x5c, 0xB3, 0xFE, 0x08]))
    rom.write_bytes(0x00707C, bytearray([0x01, 0x02, 0x04, 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20]))
    rom.write_bytes(0x00F8C3, bytearray([0x5c, 0xE0, 0xFE, 0x12]))
    rom.write_bytes(0x00F4AB, bytearray([0x5c, 0xEB, 0xFE, 0x08]))
    rom.write_bytes(0x0064F5, bytearray([0x5c, 0xF8, 0xFE, 0x08]))
    rom.write_bytes(0x0054CA, bytearray([0xA9, 0x00]))
    rom.write_bytes(0x01088E, bytearray([0x5C, 0xA9, 0xFF, 0x08]))
    rom.write_bytes(0x00A48E, bytearray([0x5C, 0xC6, 0xFF, 0x08]))
    rom.write_bytes(0x00294E, bytearray([0xEA, 0xEA, 0xEA]))
    rom.write_bytes(0x004ECB, bytearray([0xf8, 0xce, 0xfa, 0xce, 0xfc, 0xce, 0xfe, 0xce, 0xfc, 0xce, 0x00, 0xcf, 0x02, 0xcf, 0xfa, 0xce]))
    rom.write_bytes(0x004EDB, bytearray([0x00, 0xcf, 0xfc, 0xce, 0x00, 0xcf, 0x00, 0xcf, 0x02, 0xcf, 0xfe, 0xce, 0xf8, 0xce, 0x2e, 0x32]))
    rom.write_bytes(0x004EEB, bytearray([0x32, 0x2e, 0x32, 0x30, 0x30, 0x32, 0x30, 0x32, 0x30, 0x30, 0x30, 0x2e, 0x2e, 0x32, 0x30, 0x30]))
    rom.write_bytes(0x004EFB, bytearray([0x2e, 0x2e, 0x30, 0x30, 0x32, 0x2e, 0x32, 0x32, 0x2e]))
    rom.write_bytes(0x001B35, bytearray([0x5C, 0x1D, 0xFF, 0x12]))


    rom.write_bytes(0x017F03, bytearray([0x8b, 0xa9, 0x7e, 0x48, 0xab, 0xa9, 0x00, 0xeb, 0xad, 0x02, 0x05, 0xaa, 0xbd, 0x55, 0x15, 0x29]))
    rom.write_bytes(0x017F13, bytearray([0x07, 0x8d, 0x0a, 0x05, 0xf0, 0x27, 0xad, 0x08, 0x05, 0xd0, 0x1a, 0xad, 0x0a, 0x05, 0x89, 0x01]))
    rom.write_bytes(0x017F23, bytearray([0xf0, 0x07, 0xa9, 0x01, 0x8d, 0x08, 0x05, 0x80, 0x0c, 0x89, 0x02, 0xf0, 0x04, 0xa9, 0x02, 0x80]))
    rom.write_bytes(0x017F33, bytearray([0xf3, 0xa9, 0x04, 0x80, 0xef, 0xad, 0x0a, 0x05, 0xab, 0x5c, 0xe8, 0xaf, 0x80, 0x9c, 0x08, 0x05]))
    rom.write_bytes(0x017F43, bytearray([0xab, 0x5c, 0x09, 0xb0, 0x80, 0x8b, 0xda, 0xe2, 0x20, 0x48, 0xa9, 0x7e, 0x48, 0xab, 0xa9, 0x00]))
    rom.write_bytes(0x017F53, bytearray([0xeb, 0xad, 0x02, 0x05, 0xaa, 0xbd, 0x55, 0x15, 0x8d, 0x53, 0x15, 0x68, 0x0c, 0x53, 0x15, 0xad]))
    rom.write_bytes(0x017F63, bytearray([0x53, 0x15, 0x9d, 0x55, 0x15, 0xc2, 0x20, 0xfa, 0xab, 0x5c, 0xf9, 0xac, 0x81, 0xe2, 0x20, 0xee]))
    rom.write_bytes(0x017F73, bytearray([0x54, 0x15, 0xc2, 0x20, 0xa9, 0x84, 0x03, 0x8d, 0x65, 0x05, 0x5c, 0x01, 0xa9, 0x80, 0xe2, 0x20]))
    rom.write_bytes(0x017F83, bytearray([0x8b, 0xa9, 0x7e, 0x48, 0xab, 0xad, 0x39, 0x00, 0xc9, 0x04, 0xd0, 0x28, 0xad, 0x04, 0x05, 0xf0]))
    rom.write_bytes(0x017F93, bytearray([0x23, 0xce, 0x04, 0x05, 0xa9, 0x05, 0x8d, 0x93, 0x05, 0x22, 0xa7, 0x82, 0x80, 0x68, 0x68, 0x68]))
    rom.write_bytes(0x017FA3, bytearray([0x68, 0x68, 0x68, 0x68, 0x68, 0x68, 0xab, 0x28, 0xc2, 0x20, 0xa9, 0x93, 0x01, 0x8d, 0x95, 0x05]))
    rom.write_bytes(0x017FB3, bytearray([0x5c, 0xa3, 0xd4, 0x80, 0xab, 0xc2, 0x20, 0xae, 0x85, 0x06, 0xbd, 0x65, 0x0d, 0x5c, 0x22, 0xec]))
    rom.write_bytes(0x017FC3, bytearray([0x80]))

    rom.write_bytes(0x047E50, bytearray([0x22, 0x03, 0x92, 0x80, 0xe0, 0x28, 0x00, 0x90, 0x23, 0xda, 0xe2, 0x20, 0xbd, 0xd2, 0xac, 0x8f]))
    rom.write_bytes(0x047E60, bytearray([0x53, 0x15, 0x7e, 0x8b, 0x20, 0x94, 0xff, 0xa9, 0x00, 0xeb, 0xad, 0x02, 0x05, 0xaa, 0xbd, 0x55]))
    rom.write_bytes(0x047E70, bytearray([0x15, 0x18, 0x2c, 0x53, 0x15, 0xd0, 0x01, 0x38, 0xc2, 0x20, 0xab, 0xfa, 0x5c, 0x7c, 0xac, 0x81]))
    rom.write_bytes(0x047E80, bytearray([0xe2, 0x20, 0x8b, 0xad, 0x53, 0x05, 0xaa, 0xbf, 0x7c, 0xf0, 0x00, 0x48, 0x20, 0x94, 0xff, 0x68]))
    rom.write_bytes(0x047E90, bytearray([0x8d, 0x53, 0x15, 0xad, 0x02, 0x05, 0xaa, 0xbd, 0x64, 0x15, 0x2c, 0x53, 0x15, 0xf0, 0x07, 0xab]))
    rom.write_bytes(0x047EA0, bytearray([0xc2, 0x20, 0x5c, 0xbc, 0xa9, 0x80, 0xab, 0xc2, 0x20, 0xae, 0x08, 0x05, 0xbd, 0x28, 0xaf, 0x5c]))
    rom.write_bytes(0x047EB0, bytearray([0xb4, 0xa9, 0x80, 0xe2, 0x20, 0x8b, 0xae, 0x53, 0x05, 0xbf, 0x7c, 0xf0, 0x00, 0x48, 0x20, 0x94]))
    rom.write_bytes(0x047EC0, bytearray([0xff, 0x68, 0x8d, 0x53, 0x15, 0xa9, 0x00, 0xeb, 0xad, 0x02, 0x05, 0xaa, 0xbd, 0x64, 0x15, 0x0c]))
    rom.write_bytes(0x047ED0, bytearray([0x53, 0x15, 0xad, 0x53, 0x15, 0x9d, 0x64, 0x15, 0xee, 0x4f, 0x15, 0xc2, 0x20, 0xae, 0x51, 0x05]))
    rom.write_bytes(0x047EE0, bytearray([0xab, 0xbd, 0x2d, 0xaf, 0x0d, 0x4f, 0x05, 0x5c, 0x4b, 0xa9, 0x80, 0x20, 0x05, 0xff, 0xad, 0x55]))
    rom.write_bytes(0x047EF0, bytearray([0x08, 0xc9, 0x80, 0x00, 0x5c, 0xb1, 0xf4, 0x81, 0x20, 0x05, 0xff, 0xad, 0x55, 0x08, 0xc9, 0x60]))
    rom.write_bytes(0x047F00, bytearray([0x00, 0x5c, 0xfb, 0xe4, 0x80, 0xa9, 0x00, 0x00, 0xda, 0x5a, 0x8b, 0xe2, 0x20, 0x20, 0x94, 0xff]))
    rom.write_bytes(0x047F10, bytearray([0x48, 0xab, 0xad, 0x50, 0x15, 0xf0, 0x39, 0xa0, 0x00, 0x00, 0xc9, 0x2e, 0xf0, 0x38, 0xc9, 0x04]))
    rom.write_bytes(0x047F20, bytearray([0x90, 0x06, 0x38, 0xe9, 0x03, 0xc8, 0x80, 0xf2, 0xaa, 0xbf, 0x7f, 0xf0, 0x00, 0x48, 0xb9, 0x55]))
    rom.write_bytes(0x047F30, bytearray([0x15, 0x8d, 0x53, 0x15, 0x68, 0x0c, 0x53, 0x15, 0xad, 0x53, 0x15, 0x99, 0x55, 0x15, 0xa0, 0x01]))
    rom.write_bytes(0x047F40, bytearray([0x00, 0x9c, 0x50, 0x15, 0xc2, 0x20, 0xa9, 0x04, 0x00, 0xab, 0x22, 0x03, 0x92, 0x80, 0x80, 0x03]))
    rom.write_bytes(0x047F50, bytearray([0xc2, 0x20, 0xab, 0x7a, 0xfa, 0x60, 0xee, 0x4e, 0x15, 0x80, 0xe3, 0xda, 0x8b, 0xe0, 0x0a, 0x00]))
    rom.write_bytes(0x047F60, bytearray([0xd0, 0x1d, 0xe2, 0x20, 0x20, 0x94, 0xff, 0xad, 0x04, 0x05, 0xc9, 0x02, 0xf0, 0x2b, 0xaa, 0xbd]))
    rom.write_bytes(0x047F70, bytearray([0x40, 0x15, 0xd0, 0x0b, 0xad, 0x4e, 0x15, 0xf0, 0x14, 0xce, 0x4e, 0x15, 0xfe, 0x40, 0x15, 0xc2]))
    rom.write_bytes(0x047F80, bytearray([0x20, 0xa9, 0x01, 0x00, 0xab, 0xfa, 0x8d, 0xc3, 0x0d, 0x5c, 0x2d, 0xd8, 0x80, 0xc2, 0x20, 0xa9]))
    rom.write_bytes(0x047F90, bytearray([0x00, 0x00, 0xf0, 0xf0, 0xa9, 0x7e, 0x48, 0xab, 0x60, 0xad, 0x4f, 0x15, 0xcf, 0x10, 0xff, 0x1f]))
    rom.write_bytes(0x047FA0, bytearray([0xb0, 0xdd, 0xc2, 0x20, 0xa9, 0x00, 0x00, 0x80, 0xdb, 0x48, 0xe2, 0x20, 0xad, 0x7b, 0x12, 0xc9]))
    rom.write_bytes(0x047FB0, bytearray([0xea, 0xd0, 0x06, 0xa9, 0x69, 0x8f, 0x43, 0x15, 0x7e, 0xc2, 0x20, 0x68, 0x7d, 0x7b, 0x12, 0x9d]))
    rom.write_bytes(0x047FC0, bytearray([0x7b, 0x12, 0x5c, 0x94, 0x88, 0x82, 0xad, 0x02, 0x05, 0xaa, 0xe2, 0x20, 0xbd, 0x64, 0x15, 0xda]))
    rom.write_bytes(0x047FD0, bytearray([0x8d, 0x53, 0x15, 0xad, 0x53, 0x05, 0xaa, 0xbf, 0x83, 0xf0, 0x00, 0x0c, 0x53, 0x15, 0xad, 0x53]))
    rom.write_bytes(0x047FE0, bytearray([0x15, 0xfa, 0x9d, 0x64, 0x15, 0xc2, 0x20, 0xad, 0x02, 0x05, 0x0a, 0x5c, 0x92, 0xa4, 0x81]))

    rom.write_bytes(0x097EE0, bytearray([0xae, 0x85, 0x06, 0xda, 0x8a, 0xe2, 0x20, 0xa2, 0x00, 0x00, 0xdd, 0x31, 0x15, 0xf0, 0x03, 0xe8]))
    rom.write_bytes(0x097EF0, bytearray([0x80, 0xf8, 0xbf, 0x7c, 0xf0, 0x00, 0x8d, 0x30, 0x15, 0xad, 0x02, 0x05, 0xaa, 0xbd, 0x64, 0x15]))
    rom.write_bytes(0x097F00, bytearray([0x29, 0x07, 0x0c, 0x30, 0x15, 0xf0, 0x0c, 0xa9, 0xff, 0x8d, 0x4f, 0x05, 0xc2, 0x20, 0xfa, 0x5c]))
    rom.write_bytes(0x097F10, bytearray([0xce, 0xf8, 0x81, 0x9c, 0x4f, 0x05, 0xc2, 0x20, 0xfa, 0x5c, 0xcf, 0xf8, 0x81, 0xda, 0xb9, 0x5e]))
    rom.write_bytes(0x097F20, bytearray([0x9b, 0x8d, 0x02, 0x05, 0xe2, 0x20, 0xeb, 0xa9, 0x00, 0xeb, 0x0a, 0xaa, 0xc2, 0x20, 0xbf, 0xcb]))
    rom.write_bytes(0x097F30, bytearray([0xce, 0x80, 0xaa, 0xbd, 0x00, 0x00, 0x8d, 0x31, 0x15, 0xe2, 0x20, 0xae, 0x02, 0x05, 0xbf, 0xe9]))
    rom.write_bytes(0x097F40, bytearray([0xce, 0x80, 0x8d, 0x33, 0x15, 0xc2, 0x20, 0xfa, 0x5c, 0x3b, 0x9b, 0x00, 0xc9, 0x10, 0xd0, 0x02]))
    rom.write_bytes(0x097F50, bytearray([0xa9, 0x08, 0x8d, 0x73, 0x15, 0xe0, 0x0a, 0x00, 0xb0, 0x56, 0x48, 0x20, 0x80, 0xff, 0xeb, 0xa9]))
    rom.write_bytes(0x097F60, bytearray([0x00, 0xeb, 0x20, 0x94, 0xff, 0x68, 0x20, 0x9f, 0xff, 0xad, 0x74, 0x15, 0x18, 0x6d, 0x75, 0x15]))
    rom.write_bytes(0x097F70, bytearray([0xaa, 0xbd, 0x82, 0x15, 0xc2, 0x20, 0x0d, 0x80, 0x15, 0x9d, 0x82, 0x15, 0x5c, 0x12, 0xb5, 0x80]))
    rom.write_bytes(0x097F80, bytearray([0xda, 0xc2, 0x20, 0xae, 0x02, 0x05, 0x8a, 0x0a, 0xaa, 0xbf, 0x04, 0xcf, 0x80, 0x8d, 0x80, 0x15]))
    rom.write_bytes(0x097F90, bytearray([0xfa, 0xe2, 0x20, 0x60, 0x8a, 0x4a, 0xaa, 0xbf, 0x22, 0xcf, 0x80, 0x8d, 0x75, 0x15, 0x60, 0xa2]))
    rom.write_bytes(0x097FA0, bytearray([0x00, 0x00, 0xc9, 0x01, 0xf0, 0x05, 0x4a, 0xe8, 0xe8, 0x80, 0xf7, 0x8a, 0x8d, 0x74, 0x15, 0x60]))
    rom.write_bytes(0x097FB0, bytearray([0xa2, 0x00, 0x00, 0xad, 0x73, 0x15, 0xc9, 0x20, 0xf0, 0x04, 0x4a, 0xe8, 0x80, 0xf8, 0x8e, 0x74]))
    rom.write_bytes(0x097FC0, bytearray([0x15, 0x20, 0x80, 0xff, 0xeb, 0xa9, 0x00, 0xeb, 0xad, 0x74, 0x15, 0x0a, 0xaa, 0xc2, 0x20, 0xbd]))
    rom.write_bytes(0x097FD0, bytearray([0xaa, 0x15, 0x0d, 0x80, 0x15, 0x9d, 0xaa, 0x15, 0x5c, 0x12, 0xb5, 0x80]))

    rom.write_bytes(0x004F04, bytearray([0x01, 0x00, 0x02, 0x00, 0x04, 0x00, 0x08, 0x00, 0x10, 0x00, 0x20, 0x00, 0x40, 0x00, 0x80, 0x00]))
    rom.write_bytes(0x004F14, bytearray([0x00, 0x01, 0x00, 0x02, 0x00, 0x04, 0x00, 0x08, 0x00, 0x10, 0x00, 0x20, 0x00, 0x40, 0x00, 0x08]))
    rom.write_bytes(0x004F24, bytearray([0x10, 0x18, 0x20]))


def patch_rom(world, rom, player: int, multiworld):
    rom_code(rom)
    if world.options.computer_sanity.value == 1:
        rom.write_bytes(0x00350C, bytearray([0x5C, 0x4C, 0xFF, 0x12]))
    rom.write_bytes(0x001B5E, bytearray(world.city_order))
    rom.write_byte(0x0FFF10, world.options.required_artifacts.value)
    rom.write_byte(0x0FFF11, world.options.death_link.value)

    from Main import __version__
    rom.name = bytearray(f'MarioMissingAP{__version__.replace(".", "")[0:3]}_{player}_{multiworld.seed:11}\0', 'utf8')[:15]
    rom.name.extend([0] * (15 - len(rom.name)))
    rom.write_bytes(0x007FC0, rom.name)

class MIMDeltaPatch(APDeltaPatch):
    hash = USHASH
    game: str = "Mario is Missing"
    patch_file_ending = ".apmim"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()



def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str = "") -> str:
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["mariomissing_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
