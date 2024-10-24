# -*- coding: utf-8 -*-



import re
import traceback
from math import floor, fmod
from random import randint
import mod.client.extraClientApi as _clientApi
import mod.server.extraServerApi as _serverApi
from Zb_Script_chest.modCommon.modConfig import ModName


def print_error(isClient=True):
    """
    打印错误信息。

    :param isClient: 错误出现位置是否为客户端
    :return: None
    """
    errorInfo = traceback.format_exc()
    errorLine = errorInfo.split("\n")
    print errorInfo
    for i in range(len(errorLine)):
        error = errorLine[i]
        if not i:
            text = ("§4§l《%s》运行出错！请将以下错误代码截图并向作者反馈：\n§r" % ModName) + error
        else:
            text = error
        if isClient:
            ClientCompFactory = _clientApi.GetEngineCompFactory()
            ClientCompFactory.CreateTextNotifyClient(_clientApi.GetLocalPlayerId()).SetLeftCornerNotify(text)
        else:
            ServerCompFactory = _serverApi.GetEngineCompFactory()
            ServerCompFactory.CreateGame(_serverApi.GetLevelId()).SetNotifyMsg(text)


def find_all_index(findList, element):
    """
    获取某元素在列表中所有出现位置的下标。

    :param findList: 列表
    :param element: 元素
    :return: 元素所有出现位置的下标列表
    """
    result = []
    if findList:
        for i in range(len(findList)):
            if findList[i] == element:
                result.append(i)
    return result


def check_string(string, checkList):
    """
    检测字符串是否只含有指定字符。

    :param string: 字符串
    :param checkList: 检测列表 ("a-z"表示小写字母, "A-Z"表示大写字母, "0-9"表示数字)
    :return: 符合要求返回True, 否则返回False
    """
    result = []
    for i in range(len(string)):
        if string[i] in checkList \
                or ("a-z" in checkList and re.match("[a-z]", string[i])) \
                or ("A-Z" in checkList and re.match("[A-Z]", string[i])) \
                or ("0-9" in checkList and re.match("[0-9]", string[i])):
            result.append(True)
        else:
            result.append(False)
    return False not in result


def check_string2(string, checkList):
    """
    检测字符串是否只含有指定字符, 返回指定字符之外的字符的列表。

    :param string: 字符串
    :param checkList: 检测列表 ("a-z"表示小写字母, "A-Z"表示大写字母, "0-9"表示数字)
    :return: 指定字符之外的字符的列表
    """
    result = []
    for i in range(len(string)):
        if string[i] in checkList \
                or ("a-z" in checkList and re.match("[a-z]", string[i])) \
                or ("A-Z" in checkList and re.match("[A-Z]", string[i])) \
                or ("0-9" in checkList and re.match("[0-9]", string[i])):
            continue
        else:
            result.append(string[i])
    return result


def check_is_number(string, emptyReturnTrue=True):
    """
    检测字符串是否是一个数字。

    :param string: 字符串
    :param emptyReturnTrue: 空字符串是否返回True
    :return: 是则返回True, 否则返回False
    """
    if emptyReturnTrue and string == "":
        return True
    if check_string(string, ["0-9", ".", "-"]):
        if string.count(".") >= 2 or string.count("-") >= 2 or string == "." or string == "-":
            return False
        else:
            index1 = string.find(".")
            if index1 == 0 or index1 == len(string) - 1:
                return False
            if index1 != -1 and (string[index1 - 1] == "-" or string[index1 + 1] == "-"):
                return False
            index2 = string.find("-")
            if index2 != 0 and index2 != -1:
                return False
        return True
    else:
        return False


def perlin_noise(x, y, z):
    """
    柏林噪声算法。

    :param x: x坐标
    :param y: y坐标
    :param z: z坐标
    :return: -1~1的随机数
    """
    GRAD3 = ((1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
             (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
             (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
             (1, 1, 0), (0, -1, 1), (-1, 1, 0), (0, -1, -1))
    permutation = (151, 160, 137, 91, 90, 15, 23, 66, 215, 61, 156, 180, 29, 24, 72, 243, 141, 128, 195, 78, 114,
                   131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10,
                   190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33,
                   88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166,
                   77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244,
                   102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196,
                   135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123,
                   5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42,
                   223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
                   129, 22, 39, 253, 9, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228,
                   251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107,
                   49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254,
                   138, 236, 205, 93, 222, 67)
    period = len(permutation)
    permutation *= 2
    perm = list(range(period))
    perm_right = period - 1
    for i in perm:
        j = randint(0, perm_right)
        perm[i], perm[j] = perm[j], perm[i]
    permutation = tuple(perm) * 2
    i = int(fmod(floor(x), 127))
    j = int(fmod(floor(y), 127))
    k = int(fmod(floor(z), 127))
    ii = (i + 1) % 127
    jj = (j + 1) % 127
    kk = (k + 1) % 127
    x -= floor(x)
    y -= floor(y)
    z -= floor(z)
    fx = x ** 3 * (x * (x * 6 - 15) + 10)
    fy = y ** 3 * (y * (y * 6 - 15) + 10)
    fz = z ** 3 * (z * (z * 6 - 15) + 10)
    A = permutation[i]
    AA = permutation[A + j]
    AB = permutation[A + jj]
    B = permutation[ii]
    BA = permutation[B + j]
    BB = permutation[B + jj]
    def lerp(t, a, b):
        return a + t * (b - a)
    def grad3(h, xx, yy, zz):
        g = GRAD3[h % 9]
        return xx * g[0] + yy * g[1] + zz * g[2]
    return lerp(fz, lerp(fy, lerp(fx, grad3(permutation[AA + k], x, y, z), grad3(permutation[BA + k], x - 1, y, z)),
                         lerp(fx, grad3(permutation[AB + k], x, y - 1, z),
                              grad3(permutation[BB + k], x - 1, y - 1, z))),
                lerp(fy, lerp(fx, grad3(permutation[AA + kk], x, y, z - 1),
                              grad3(permutation[BA + kk], x - 1, y, z - 1)),
                     lerp(fx, grad3(permutation[AB + kk], x, y - 1, z - 1),
                          grad3(permutation[BB + kk], x - 1, y - 1, z - 1))))


def turn_dict_value_to_tuple(origDict):
    """
    将字典值中的列表全部转换为元组。（改变原字典）

    :param origDict: 字典
    :return: None
    """
    if not isinstance(origDict, dict):
        return
    for key, value in origDict.items():
        if isinstance(value, list):
            newValue = turn_list_to_tuple(value)
            origDict[key] = newValue


def turn_list_to_tuple(lst):
    """
    将一个列表，及其所有子元素转换成元组。

    :param lst: 列表
    :return: 转换后的元组
    """
    if not isinstance(lst, list):
        return
    newLst = []
    for i in lst:
        if isinstance(i, list):
            newLst.append(turn_list_to_tuple(i))
        else:
            newLst.append(i)
    return tuple(newLst)


def is_same_item(itemDict1, itemDict2):
    """
    判断两个物品是否是同种物品。

    :param itemDict1: 物品信息字典1
    :param itemDict2: 物品信息字典2
    :return: 相同则返回True，否则返回False
    """
    if (is_empty_item(itemDict1) and not is_empty_item(itemDict2)) \
            or (not is_empty_item(itemDict1) and is_empty_item(itemDict2)):
        return False
    elif is_empty_item(itemDict1) and is_empty_item(itemDict2):
        return True
    newItemName1 = itemDict1['newItemName']
    newAuxValue1 = itemDict1['newAuxValue']
    oldItemName1 = itemDict1.get('itemName', newItemName1)
    oldAuxValue1 = itemDict1.get('auxValue', newAuxValue1)
    newItemName2 = itemDict2['newItemName']
    newAuxValue2 = itemDict2['newAuxValue']
    oldItemName2 = itemDict2.get('itemName', newItemName2)
    oldAuxValue2 = itemDict2.get('auxValue', newAuxValue2)
    return (newItemName1 == newItemName2 and newAuxValue1 == newAuxValue2) \
        or (oldItemName1 == oldItemName2 and oldAuxValue1 == oldAuxValue2) \
        or (newItemName1 == oldItemName2 and newAuxValue1 == oldAuxValue2) \
        or (oldItemName1 == newItemName2 and oldAuxValue1 == newAuxValue2)


def is_empty_item(itemDict, zeroCountIsEmp=True):
    """
    判断物品是否是空物品。

    :param itemDict: 物品信息字典
    :param zeroCountIsEmp: 是否把数量为0的物品视为空物品
    :return: 是空物品则返回True，否则返回False
    """
    return not itemDict \
        or (zeroCountIsEmp and itemDict.get('count', 1) <= 0) \
        or ('newItemName' not in itemDict and 'itemName' not in itemDict) \
        or (not itemDict.get('newItemName', "") and not itemDict.get('itemName', "")) \
        or itemDict.get('newItemName', "") == "minecraft:air" \
        or itemDict.get('itemName', "") == "minecraft:air"








