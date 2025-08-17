# scripts/results_mapping.py

### Current trains 
URL_CURRENT_TRAINS = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML"
FIELD_MAP_CURRENT_TRAINS = {
    'TrainCode'        : 'TrainCode',
    'Direction'        : 'Direction',
    'TrainStatus'      : 'TrainStatus',
    'TrainDate'        : 'TrainDate',
    'PublicMessage'    : 'PublicMessage',
    'TrainLatitude'    : 'TrainLatitude',
    'TrainLongitude'   : 'TrainLongitude',
    'TrainType'        : 'TrainType',
    # Additional columns from helper_functions.py
    'delay_minutes'    : 'delay_minutes',
    'current_location' : 'current_location',
    'train_category'   : 'train_category',
    'train_type_code'  : 'train_type_code',
    'enhanced_at'      : 'enhanced_at',
    'collected_at'     : 'collected_at',
    'message_type'     : 'message_type',
    'train_type'       : 'train_type'
}

### Station information 
URL_STATION_INFO = "http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML"
FIELD_MAP_STATION_INFO = {
    'StationDesc'      : 'StationDesc',
    'StationCode'      : 'StationCode',
    'StationType'      : 'StationType',
    'StationId'        : 'StationId',
    'StationAlias'     : 'StationAlias',
    'StationLatitude'  : 'StationLatitude',
    'StationLongitude' : 'StationLongitude',
    'updated_at'       : 'updated_at'
}

###  Train Movements 
URL_TRAIN_MOVEMENTS = "http://api.irishrail.ie/realtime/realtime.asmx/getTrainMovementsXML"
FIELD_MAP_TRAIN_MOVEMENTS = {
    'TrainCode'         : 'TrainCode',
    'TrainDate'         : 'TrainDate',
    'LocationCode'      : 'LocationCode',
    'LocationFullName'  : 'LocationFullName',
    'LocationOrder'     : 'LocationOrder',
    'LocationType'      : 'LocationType',
    'TrainOrigin'       : 'TrainOrigin',
    'TrainDestination'  : 'TrainDestination',
    'ScheduledArrival'  : 'ScheduledArrival',
    'ScheduledDeparture': 'ScheduledDeparture',
    'arrival_actual'    : 'arrival_actual',
    'departure_actual'  : 'departure_actual',
    'StopType'          : 'StopType',
    'fetched_at'        : 'fetched_at',
    # Additional columns from helper_functions.py
    'delay_minutes'        : 'delay_minutes',
    'train_category'       : 'train_category',
    'route_classification' : 'route_classification',
    'train_type_code'      : 'train_type_code',
    'enhanced_at'          : 'enhanced_at',
    'route_type'           : 'route_type',
    'train_type'           : 'train_type'
}

### Station Stops Data by Station Code (with timeframe) ###
URL_STATION_DATA_BY_CODE_WITH_MINUTES = "http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins"
FIELD_MAP_STATION_DATA_BY_CODE_WITH_MINUTES = {
    'ServerTime'        : 'ServerTime',
    'TrainCode'         : 'TrainCode',
    'StationFullName'   : 'StationFullName',
    'StationCode'       : 'StationCode',
    'QueryTime'         : 'QueryTime',
    'TrainDate'         : 'TrainDate',
    'Origin'            : 'Origin',
    'Destination'       : 'Destination',
    'OriginTime'        : 'OriginTime',
    'DestinationTime'   : 'DestinationTime',
    'Status'            : 'Status',
    'LastLocation'      : 'LastLocation',
    'DueIn'             : 'DueIn',
    'Late'              : 'Late',
    'ExpArrival'        : 'ExpArrival',
    'ExpDepart'         : 'ExpDepart',
    'SchArrival'        : 'SchArrival',
    'SchDepart'         : 'SchDepart',
    'Direction'         : 'Direction',
    'TrainType'         : 'TrainType',
    'LocationType'      : 'LocationType'
}

### Current trains with type filter 
URL_CURRENT_TRAINS_WITH_TYPE = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType"
FIELD_MAP_CURRENT_TRAINS_WITH_TYPE = FIELD_MAP_CURRENT_TRAINS

### Stations with type filter 
URL_STATIONS_WITH_TYPE = "http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType"
FIELD_MAP_STATIONS_WITH_TYPE = FIELD_MAP_STATION_INFO
