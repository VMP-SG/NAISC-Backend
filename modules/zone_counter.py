from pathlib import Path

from peekingduck.pipeline.nodes.dabble import fps, zone_count, bbox_count, bbox_to_btm_midpoint
from peekingduck.pipeline.nodes.draw import bbox, legend, zones
from peekingduck.pipeline.nodes.input import visual
from peekingduck.pipeline.nodes.model import yolo
from peekingduck.pipeline.nodes.output import media_writer, screen
from peekingduck.runner import Runner

def count_human_gen(path_to_file):
  # input
  visual_node = visual.Node(source=path_to_file)

  # Model
  # yolo_node = yolo.Node(detect=["person", "cup", "dining table", "chair", "fork", "knife", "spoon", "bowl", "banana", "wine glass", "bird"])
  yolo_node = yolo.Node(detect=["person"])

  # Dabble
  bbox_count_node = bbox_count.Node()

  # Draw
  # bbox_node = bbox.Node(show_labels=True)
  # legend_node = legend.Node(show=["bbox_count"])

  # Output
  # screen_node = screen.Node()
  # media_writer_node = media_writer.Node(output_dir=str(Path.cwd() / "output"))

  # Manually run the pipeline
  while True:  # Need to loop through all the frames for video input
    try:
      visual_output = visual_node.run({})  # No inputs required
      yolo_output = yolo_node.run({"img":visual_output["img"]})
    except KeyboardInterrupt:
      exit()
    except:
      visual_node = visual.Node(source=path_to_file)
      visual_output = visual_node.run({})  # No inputs required
      yolo_output = yolo_node.run({"img":visual_output["img"]})
    bbox_count_output = bbox_count_node.run({"bboxes": yolo_output["bboxes"]})

    # # Uncomment this to generate video output
    # bbox_node.run({"img": visual_output["img"], "bboxes": yolo_output["bboxes"], "bbox_labels": yolo_output["bbox_labels"]})
    # legend_output = legend_node.run({"img": visual_output["img"], "bbox_count": bbox_count_output["count"]})
    # media_writer_node.run({"img":legend_output["img"],
    #                         "filename":visual_output["filename"],
    #                         "saved_video_fps":visual_output["saved_video_fps"],
    #                         "pipeline_end":visual_output["pipeline_end"]})
    yield "data: %s\n\n" % (bbox_count_output)

if __name__ == "__main__":
  generator = count_human_gen(str(Path.cwd() / "videos" / "GoldenMile" / "GoldenMile_1.mp4"))
  while True:
    print(next(generator))
