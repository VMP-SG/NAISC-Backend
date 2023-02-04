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


def adjust_zone_split(original_res, new_res, zones):  # Adjust zone split if resolution is shrunk
    if original_res[0] == new_res[0] and original_res[1] == new_res[1]:
        return zones
    ratio_w, ratio_h = new_res[0] / original_res[0], new_res[1] / original_res[1]
    adjusted_zones = {}
    for camera_id,zone in zones.items():
        new_zone = []
        for box in zone:
            new_box = []
            for x,y in box:
                new_box.append([int(x*ratio_w), int(y*ratio_h)])
            new_zone.append(new_box)
        adjusted_zones[camera_id] = new_zone
    return adjusted_zones


def run_API():
    ADJUSTED_ZONES = adjust_zone_split(ORIGINAL_RESOLUTION, RESOLUTION, ZONES)
    generators = {camera_id:count_human_gen(INPUT_PATHS[camera_id], ADJUSTED_ZONES[camera_id], RESOLUTION, MAPPINGS[camera_id]) for camera_id in CAMERA_IDS}
    while True:
        yield {camera_id:next(generators[camera_id]) for camera_id in CAMERA_IDS}


if __name__ == "__main__":
    API = run_API()
    for _ in range(100):
        next(API)
