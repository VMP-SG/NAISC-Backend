def is_store(obj_id):
    return obj_id<100

def queue_count(record):
    # Note that the same store can be captured by multiple cameras
    compiled = {}
    for v in record.values():
        for i in range(len(v["zone_people_count"])):
            if v["zone_mapping"][i] in compiled:
                compiled[v["zone_mapping"][i]].append(v["zone_people_count"][i])
            else:
                compiled[v["zone_mapping"][i]] = [v["zone_people_count"][i]]
    compiled = dict(filter(lambda x: is_store(x[0]), compiled.items()))  # Keep only ids corresponding to stores
    for store_id in compiled:  # Compute mean. Table is considered occupied if mean greater than some threshold
        compiled[store_id] = sum(compiled[store_id])//len(compiled[store_id])
    return compiled
