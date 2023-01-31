from zone_count_generator import *
from settings_golden_mile import *

"""
API sample output
{
    "CAMERA_A": {
        "raw_frame": [..img..],
        "labelled_frame": [..img..],
        "total_people_count": 10,
        "zone_people_count": [2, 2, 0, 0],
        "zone_mapping": [1, 3, 2, 5]
    },
    "CAMERA_B": {
        ...
    }
}

zone_mapping indicates the id of the object (e.g. a table, a stall) that the zone is supposed to track.
What these ids represent should be made clear through a labelled floor plan. 
"""


def run_API():
    generators = {camera_id:count_human_gen(INPUT_PATHS[camera_id], ZONES[camera_id], RESOLUTION, MAPPINGS[camera_id]) for camera_id in CAMERA_IDS}
    while True:
        yield {camera_id:next(generators[camera_id]) for camera_id in CAMERA_IDS}

# API = run_API()
# for _ in range(100):
#     next(API)