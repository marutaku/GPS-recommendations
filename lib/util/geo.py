from math import *


class GEOUtil(object):
    @staticmethod
    def cal_phi(ra,rb,lat):
        return atan(rb/ra*tan(lat))

    @staticmethod
    def cal_rho(lat_a,lon_a,lat_b,lon_b):
        ra=6378.140  # equatorial radius (km)
        rb=6356.755  # polar radius (km)
        F=(ra-rb)/ra # flattening of the earth
        rad_lat_a=radians(lat_a)
        rad_lon_a=radians(lon_a)
        rad_lat_b=radians(lat_b)
        rad_lon_b=radians(lon_b)
        pa=GEOUtil.cal_phi(ra,rb,rad_lat_a)
        pb=GEOUtil.cal_phi(ra,rb,rad_lat_b)
        xx=acos(sin(pa)*sin(pb)+cos(pa)*cos(pb)*cos(rad_lon_a-rad_lon_b))
        c1=(sin(xx)-xx)*(sin(pa)+sin(pb))**2/cos(xx/2)**2
        c2=(sin(xx)+xx)*(sin(pa)-sin(pb))**2/sin(xx/2)**2
        dr=F/8*(c1-c2)
        rho=ra*(xx+dr)
        return rho
