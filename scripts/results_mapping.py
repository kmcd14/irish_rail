# scripts/config.py

### Get current trains ###
URL_CURRENT_TRAINS = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML"
FIELD_MAP_CURRENT_TRAINS = {
    'TrainCode': 'TrainCode',
    'Direction': 'Direction',
    'TrainStatus': 'TrainStatus',
    'TrainDate': 'TrainDate',
    'PublicMessage': 'PublicMessage',
    'TrainLatitude': 'TrainLatitude',
    'TrainLongitude': 'TrainLongitude',
    'TrainType': 'TrainType'
}

### Station information ###
URL_STATION_INFO = "http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML"
FIELD_MAP_STATION_INFO = {
    'StationDesc': 'StationDesc',
    'StationCode': 'StationCode',
    'StationType': 'StationType',
    'StationId': 'StationId',
    'StationAlias': 'StationAlias',
    'StationLatitude': 'StationLatitude',
    'StationLongitude': 'StationLongitude'
}


### Train Movements ###
URL_TRAIN_MOVEMENTS = "http://api.irishrail.ie/realtime/realtime.asmx/getTrainMovementsXML"
FIELD_MAP_TRAIN_MOVEMENTS = {
    'TrainCode': 'TrainCode',
    'TrainDate': 'TrainDate',
    'LocationCode': 'LocationCode',
    'LocationFullName': 'LocationFullName',
    'LocationOrder': 'LocationOrder',
    'LocationType': 'LocationType',
    'TrainOrigin': 'TrainOrigin',
    'TrainDestination': 'TrainDestination',
    'ScheduledArrival': 'ScheduledArrival',
    'ScheduledDeparture': 'ScheduledDeparture',
    'arrival_actual': 'arrival_actual',
    'departure_actual': 'departure_actual',
    'StopType': 'StopType',
    'fetched_at': 'fetched_at'
}

### Station Stop Data by Station Code (with timeframe) ###
URL_STATION_DATA_BY_CODE_WITH_MINUTES = ("http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins")
FIELD_MAP_STATION_DATA_BY_CODE_WITH_MINUTES = {
    'ServerTime': 'ServerTime',
    'TrainCode': 'TrainCode',
    'StationFullName': 'StationFullName',
    'StationCode': 'StationCode',
    'QueryTime': 'QueryTime',
    'TrainDate': 'TrainDate',
    'Origin': 'Origin',
    'Destination': 'Destination',
    'OriginTime': 'OriginTime',
    'DestinationTime': 'DestinationTime',
    'Status': 'Status',
    'LastLocation': 'LastLocation',
    'DueIn': 'DueIn',
    'Late': 'Late',
    'ExpArrival': 'ExpArrival',
    'ExpDepart': 'ExpDepart',
    'SchArrival': 'SchArrival',
    'SchDepart': 'SchDepart',
    'Direction': 'Direction',
    'TrainType': 'TrainType',
    'LocationType': 'LocationType'
}

