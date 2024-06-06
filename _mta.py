#MTA6 protocol device

import ctypes
import math
import time
import struct

class Mta6_Data(ctypes.Structure):
    _fields_ = [
        ("HEADER_ID_PAC", ctypes.c_uint8),
        ("HEADER_OFFS_DATA", ctypes.c_uint8),
        ("HEADER_CNT", ctypes.c_uint8),
        ("HEADER_RESERVE", ctypes.c_uint8),
        ("HEADER_PAR", ctypes.c_uint8),
        ("mFD", ctypes.c_uint8),
        ("Event", ctypes.c_uint8),
        ("Latitude", ctypes.c_uint32),
        ("Longitude", ctypes.c_uint32),
        ("Gps_Second", ctypes.c_uint32),
        ("Gps_Week", ctypes.c_uint16),
        ("TerminalStatus", ctypes.c_uint8),
        ("Altitude", ctypes.c_int16),
        ("SpeedHi", ctypes.c_uint8),
        ("SpeedLo", ctypes.c_uint8),
        ("Azimuth", ctypes.c_uint8),
        ("Kilometrage", ctypes.c_uint32),
        ("FuelConsumption1", ctypes.c_uint32),
        ("FuelConsumption2", ctypes.c_uint32),
        ("EngineHourDiv6", ctypes.c_uint16),
        ("Reserved", ctypes.c_uint16),
        ("Adc0Hi", ctypes.c_uint8),
        ("Adc0Lo", ctypes.c_uint8),
        ("Adc1Hi", ctypes.c_uint8),
        ("Adc1Lo", ctypes.c_uint8),
        ("Adc2Hi", ctypes.c_uint8),
        ("Adc2Lo", ctypes.c_uint8),
        ("Adc3Hi", ctypes.c_uint8),
        ("Adc3Lo", ctypes.c_uint8),
        ("TemperatureExt", ctypes.c_int8),
        ("ContStateCurHi", ctypes.c_uint8),
        ("ContStateCurLo", ctypes.c_uint8),
        ("ContStateOldHi", ctypes.c_uint8),
        ("ContStateOldLo", ctypes.c_uint8),
        ("BoardPwrHiAndBat", ctypes.c_uint8),
        ("BoardPwrLo", ctypes.c_uint8),
        ("TemperatureChip", ctypes.c_int8),
        ("GpsGsm", ctypes.c_uint8)
    ]

def prepare_sending_data(lat:float, lon:float, speed:int, run:int, height:int, voltage:float):
    Mta_Data = Mta6_Data()
    
    # Header
    Mta_Data.HEADER_ID_PAC = 0x32
    Mta_Data.HEADER_OFFS_DATA = 0x05
    Mta_Data.HEADER_CNT = 0x00
    Mta_Data.HEADER_RESERVE = 0x00
    Mta_Data.HEADER_PAR = 0x81
    
    Mta_Data.mFD = 0xFF
    Mta_Data.Event = 0x40
    
    #LAT&LON
    if lat == 0 and lon == 0:
        lat = lon = 0xFFFFFFFF
    else:
        lat *= math.pi / 180.0
        lon *= math.pi / 180.0
    Lat_Bit = struct.unpack('I', struct.pack('f', lat))[0] >> 2
    Lon_Bit = struct.unpack('I', struct.pack('f', lon))[0] >> 2
    Mta_Data.Latitude = Lat_Bit
    Mta_Data.Longitude = Lon_Bit
    
    # GPS&WEEK
    gps_epoch = 315964800
    week_sec = 604800
    end_timeinfo = time.strptime('2024' + '6' + '4' + '9' + '0' + '0', '%y%m%d%H%M%S')    
    end_timestamp = int(time.mktime(end_timeinfo))
    current_time = end_timestamp
    gps_time = current_time - gps_epoch
    Mta_Data.Gps_Week = gps_time // week_sec
    gps_sec = gps_time - Mta_Data.Gps_Week * week_sec
    uiPtr = struct.unpack('I', struct.pack('f', gps_sec))[0] >> 2
    Mta_Data.Gps_Second = uiPtr

    Mta_Data.TerminalStatus = 0x00
    Mta_Data.Altitude = ctypes.c_int16(int(height))
    Mta_Data.SpeedHi = 0x00
    Mta_Data.SpeedLo = int(speed)
    Mta_Data.Azimuth = 0x00
    Mta_Data.Kilometrage = int(run)
    Mta_Data.FuelConsumption1 = 0x00
    Mta_Data.FuelConsumption2 = 0x00
    Mta_Data.EngineHourDiv6 = 0x00
    Mta_Data.Reserved = 0x00
    Mta_Data.Adc0Hi = 0x00
    Mta_Data.Adc0Lo = 0x00
    Mta_Data.Adc1Hi = 0x00
    Mta_Data.Adc1Lo = 0x00
    Mta_Data.Adc2Hi = 0x00
    Mta_Data.Adc2Lo = 0x00
    Mta_Data.Adc3Hi = 0x00
    Mta_Data.Adc3Lo = 0x00
    Mta_Data.TemperatureExt = 0x00
    Mta_Data.ContStateCurHi = 0x00
    Mta_Data.ContStateCurLo = 0x00
    Mta_Data.ContStateOldHi = 0x00
    Mta_Data.ContStateOldLo = 0x00
    Mta_Data.BoardPwrHiAndBat = (0x00 >> 6) & 0xFC; 
    voltage = voltage / 0.1
    Mta_Data.BoardPwrLo = (int(voltage) & 0xFF); 
    Mta_Data.TemperatureChip = 0x00
    Mta_Data.GpsGsm |= (0x00 << 7) & 0xFF
    Mta_Data.GpsGsm |= (0x04 << 4) & 0xFF
    Mta_Data.GpsGsm |= (0x06 & 0xFF)
    return form_data(Mta_Data)


# def form_data_(data_struct):
#     data_bytes = bytes(ctypes.string_at(ctypes.byref(data_struct), ctypes.sizeof(data_struct)))
#     return data_bytes

def form_data(Mta_Data):
    P = 0
    Bin_Data = bytearray(88) 
    Bin_Data[P] = Mta_Data.HEADER_ID_PAC
    P += 1
    Bin_Data[P] = Mta_Data.HEADER_OFFS_DATA
    P += 1
    Bin_Data[P] = Mta_Data.HEADER_CNT
    P += 1
    Bin_Data[P] = Mta_Data.HEADER_RESERVE
    P += 1
    Bin_Data[P] = Mta_Data.HEADER_PAR
    P += 1

    Bin_Data[P] = Mta_Data.mFD
    P += 1
    Bin_Data[P] = Mta_Data.Event
    P += 1

    Bin_Data[P] = (Mta_Data.Latitude >> 24) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.Latitude >> 16) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.Latitude >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.Latitude & 0xFF
    P += 1

    Bin_Data[P] = (Mta_Data.Longitude >> 24) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.Longitude >> 16) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.Longitude >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.Longitude & 0xFF
    P += 1

    Bin_Data[P] =(Mta_Data.Gps_Second >> 24) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.Gps_Second >> 16) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.Gps_Second  >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.Gps_Second  & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.Gps_Week >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.Gps_Week & 0xFF
    P += 1
    
    Bin_Data[P] = Mta_Data.TerminalStatus
    P += 1
    
    Bin_Data[P] = (Mta_Data.Altitude >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.Altitude & 0xFF
    P += 1

    Bin_Data[P] = Mta_Data.SpeedHi
    P += 1
    Bin_Data[P] = Mta_Data.SpeedLo
    P += 1

    Bin_Data[P] = Mta_Data.Azimuth
    P += 1

    Bin_Data[P] = (Mta_Data.Kilometrage >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.Kilometrage & 0xFF
    P += 1
    
    Bin_Data[P] = (Mta_Data.FuelConsumption1 >> 24) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.FuelConsumption1 >> 16) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.FuelConsumption1 >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.FuelConsumption1 & 0xFF
    P += 1

    Bin_Data[P] = (Mta_Data.FuelConsumption2 >> 24) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.FuelConsumption2 >> 16) & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.FuelConsumption2 >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.FuelConsumption2 & 0xFF
    P += 1
    
    Bin_Data[P] = (Mta_Data.EngineHourDiv6 >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.EngineHourDiv6 & 0xFF
    P += 1
    Bin_Data[P] = (Mta_Data.Reserved >> 8) & 0xFF
    P += 1
    Bin_Data[P] = Mta_Data.Reserved & 0xFF
    P += 1
    
    Bin_Data[P] = Mta_Data.Adc0Hi
    P += 1
    Bin_Data[P] = Mta_Data.Adc0Lo
    P += 1
    
    Bin_Data[P] = Mta_Data.Adc1Hi
    P += 1
    Bin_Data[P] = Mta_Data.Adc1Lo
    P += 1
    
    Bin_Data[P] = Mta_Data.Adc2Hi
    P += 1
    Bin_Data[P] = Mta_Data.Adc2Lo
    P += 1

    Bin_Data[P] = Mta_Data.Adc3Hi
    P += 1
    Bin_Data[P] = Mta_Data.Adc3Lo
    P += 1
    
    Bin_Data[P] = Mta_Data.TemperatureExt
    P += 1

    Bin_Data[P] = Mta_Data.ContStateCurHi
    P += 1
    Bin_Data[P] = Mta_Data.ContStateCurLo
    P += 1

    Bin_Data[P] = Mta_Data.ContStateOldHi
    P += 1
    Bin_Data[P] = Mta_Data.ContStateOldLo
    P += 1

    Bin_Data[P] = Mta_Data.BoardPwrHiAndBat
    P += 1
    Bin_Data[P] = Mta_Data.BoardPwrLo
    P += 1

    Bin_Data[P] = Mta_Data.TemperatureChip
    P += 1

    Bin_Data[P] = Mta_Data.GpsGsm
    P += 1
    Bin_Data[P] = 0x00

    return Bin_Data[:P]  