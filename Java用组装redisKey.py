import base64


def create_key():
    # 北京物美是1 华东物美是2
    venderId = "1"
    orderCreateYMD = "20181211"
    belongsNewcomersCode = "2"  # 2 - 现金券 1 - 新人券 3-满减券
    addressPrefixClean = "北京市海淀区北蜂窝103号院丁楼"
    addressPrefixRedis = base64.b64encode(addressPrefixClean.encode('utf-8'))
    addressPrefixRedis = str(addressPrefixRedis, 'utf-8')
    commonPrefix = "RCS.FK.3.3."
    versionFlag = "A"
    sameAddressPrefixRedisKey = commonPrefix + venderId + "." + belongsNewcomersCode + "." + versionFlag + "." + addressPrefixRedis + "." + orderCreateYMD
    print("sameAddressPrefixRedisKey = " + sameAddressPrefixRedisKey)


if __name__ == "__main__":
    create_key()