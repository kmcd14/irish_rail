from scripts.x_pipeline import *
from .updated_current_trains_test import *
from .updated_dart_test import *
from .updated_train_type import *
from .everything_test import *
from scripts.scheduler import *

#trains = fetch_current_trains()
#print(f"Got {len(trains)} trains")


#all_data = collect_all_data_once()

# Check what you got
#print("Current trains columns:", list(all_data['current_trains'].columns))
#print("Movements columns:", list(all_data['movements'].columns))



run_once_for_testing()