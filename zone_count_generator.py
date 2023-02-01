from pathlib import Path

from peekingduck.pipeline.nodes.dabble import zone_count, bbox_count, bbox_to_btm_midpoint
from peekingduck.pipeline.nodes.draw import bbox, legend, zones
from peekingduck.pipeline.nodes.input import visual
from peekingduck.pipeline.nodes.model import yolox, yolo
from peekingduck.pipeline.nodes.output import media_writer, screen


def count_human_gen(path_to_file, zone_split, resolution, mapping):
    # input
    visual_node = visual.Node(source=path_to_file)

    # Model
    yolo_node = yolo.Node(detect=["person"])

    # Dabble
    bbox_count_node = bbox_count.Node()
    bbox_to_btm_midpoint_node = bbox_to_btm_midpoint.Node()  # Convert to btm_midpoint to feed into zone_count_node
    zone_count_node = zone_count.Node(zones=zone_split, resolution=resolution)

    # Draw
    bbox_node = bbox.Node(show_labels=True)
    zones_node = zones.Node()
    legend_node = legend.Node(show=["bbox_count","zone_count"])

    # Output
    media_writer_node = media_writer.Node(output_dir=str(Path.cwd() / "output"))

    # Manually run the pipeline
    while True:
        visual_output = visual_node.run({})
        raw_frame = visual_output["img"].copy()
        if visual_output["pipeline_end"]: break  # Video has no more frames

        yolo_output = yolo_node.run({"img":visual_output["img"]})
        bbox_count_output = bbox_count_node.run({"bboxes": yolo_output["bboxes"]})
        bbox_to_btm_midpoint_output = bbox_to_btm_midpoint_node.run({"img": visual_output["img"], "bboxes": yolo_output["bboxes"]})
        zone_count_output = zone_count_node.run({"btm_midpoint": bbox_to_btm_midpoint_output["btm_midpoint"]})

        bbox_node.run({"img": visual_output["img"],
                       "bboxes": yolo_output["bboxes"],
                       "bbox_labels": yolo_output["bbox_labels"]})
        zones_node.run({"img": visual_output["img"],
                        "zones": zone_count_output["zones"]})
        legend_output = legend_node.run({"img": visual_output["img"],
                                         "bbox_count": bbox_count_output["count"],
                                         "zone_count":zone_count_output["zone_count"]})
        # media_writer_node.run({"img":legend_output["img"],
        #                        "filename":visual_output["filename"],
        #                        "saved_video_fps":visual_output["saved_video_fps"],
        #                        "pipeline_end":visual_output["pipeline_end"]})

        # zone_people_count indicates the number of bboxes with bottom midpoint lying in the zone boundary
        yield {"raw_frame": raw_frame,
               "labelled_frame": legend_output["img"],
               "total_people_count": bbox_count_output["count"],
               "zone_people_count": zone_count_output["zone_count"],
               "zone_mapping": mapping}


# Code for testing
# from settings_golden_mile import *
# generator = count_human_gen("videos/GoldenMile/A.mp4",CAMERA_A_ZONES, RESOLUTION, CAMERA_A_MAPPING)
# while True:
#     try:
#         res = next(generator)
#         print(res["total_people_count"])
#         cv2.imshow("img", res["raw_frame"])
#         cv2.waitKey(0)
#         break
#     except Exception as e:
#         print(e)
#         print("End of Processing")
#         break