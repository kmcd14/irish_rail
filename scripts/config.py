# scripts/config.py

### Get current trains ###
URL_CURRENT_TRAINS = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML"
FIELD_MAP_CURRENT_TRAINS = {
    'train_code': 'TrainCode',
    'direction': 'Direction',
    'status': 'TrainStatus',
    'date': 'TrainDate',
    'message': 'PublicMessage',
    'latitude': 'TrainLatitude',
    'longitude': 'TrainLongitude'
}

### Sttation information ###
URL_STATION_INFO = "http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML "
FIELD_MAP_STATION_INFO = {
    'station_desc': 'StationDesc',
    'station_code': 'StationCode',
    'station_id': 'StationId',
    'alias': 'StationAlias',
    'latitude': 'StationLatitude',
    'longitude': 'StationLongitude',
}


### Train Movements ###
URL_TRAIN_MOVEMENTS = "http://api.irishrail.ie/realtime/realtime.asmx/getTrainMovementsXML"
FIELD_MAP_TRAIN_MOVEMENTS = {
    'train_code': 'TrainCode',  
    'train_date': 'TrainDate',
    'location_code': 'LocationCode',
    'LocationFullName': 'LocationFullName',
    'LocationOrder': 'LocationOrder',
    'LocationType': 'LocationType',  # O= Origin, S= Stop, T= TimingPoint (non stopping location) D = Destination
    'TrainOrgin': 'TrainOrigin',
    'TrainDestination': 'TrainDestination',
    'ScheduledArrival': 'ScheduledArrival',
    'ScheduledDeparture': 'ScheduledDeparture',
    'Arrival (actual)': 'ArrivalActual',
    'Departure (actual)': 'DepartureActual',
    'StopType': 'StopType',  # C= Current N = Next
}


### Station Stop Data by Station Code (with timeframe) ###
URL_STATION_DATA_BY_CODE_WITH_MINUTES = ("http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins")
FIELD_MAP_STATION_DATA_BY_CODE_WITH_MINUTES = {
    'server_time': 'ServerTime',
    'train_code': 'TrainCode',
    'station_name': 'StationFullName',
    'station_code': 'StationCode',
    'query_time': 'QueryTime',
    'train_date': 'TrainDate',
    'origin': 'Origin',
    'destination': 'Destination',
    'origin_time': 'OriginTime',
    'destination_time': 'DestinationTime',
    'status': 'Status',
    'last_location': 'LastLocation',
    'due_in': 'DueIn',
    'late': 'Late',
    'expected_arrival': 'ExpArrival',
    'expected_departure': 'ExpDepart',
    'scheduled_arrival': 'SchArrival',
    'scheduled_departure': 'SchDepart',
    'direction': 'Direction',
    'train_type': 'TrainType',
    'location_type': 'LocationType',  # O= Origin, S= Stop, D = Destination
}
