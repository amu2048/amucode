from math import radians, cos, sin, asin, sqrt
def geodistance(lng1,lat1,lng2,lat2):
    if lng1 == 'null' :
        print("用户定位为空")
        distance = ''
    else:
        lng1, lat1, lng2, lat2 = map(  radians, [ float(lng1), float(lat1), float(lng2), float(lat2) ]  )
        # 经纬度转换成弧度
        dlon=lng2-lng1
        dlat=lat2-lat1
        a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
        distance=round(distance,0)
    return distance
