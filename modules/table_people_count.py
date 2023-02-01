def is_table(obj_id):
    return obj_id>=100

def table_people_count(records):
    # Note that a table can be captured by multiple cameras. Take average
    compiled = {}  # table_id: [people counts]
    for record in records:
        for v in record.values():
            for i in range(len(v["zone_people_count"])):
                if v["zone_mapping"][i] in compiled:
                    compiled[v["zone_mapping"][i]].append(v["zone_people_count"][i])
                else:
                    compiled[v["zone_mapping"][i]] = [v["zone_people_count"][i]]
    compiled = dict(filter(lambda x:is_table(x[0]), compiled.items()))  # Keep only ids corresponding to tables
    for table_id in compiled:  # Compute mean. Table is considered occupied if mean greater than some threshold
        compiled[table_id] = sum(compiled[table_id])//len(compiled[table_id])
    return compiled
