"""Detect text in a local video."""
from google.cloud import videointelligence
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.TEXT_DETECTION]
video_context = videointelligence.types.VideoContext()

with io.open('Can_You_See_It.mp4', "rb") as file:
    input_content = file.read()

operation = video_client.annotate_video(
    input_content=input_content,  # the bytes of the video file
    features=features,
    video_context=video_context,
)

print("\nProcessing video for text detection.")
result = operation.result(timeout=300)

# The first result is retrieved because a single video was processed.
annotation_result = result.annotation_results[0]

for text_annotation in annotation_result.text_annotations:
    print("\nText: {}".format(text_annotation.text))

    # Get the first text segment
    text_segment = text_annotation.segments[0]
    start_time = text_segment.segment.start_time_offset
    end_time = text_segment.segment.end_time_offset
    print(
        "start_time: {}, end_time: {}".format(
            start_time.seconds + start_time.nanos * 1e-9,
            end_time.seconds + end_time.nanos * 1e-9,
        )
    )

    print("Confidence: {}".format(text_segment.confidence))

    # Show the result for the first frame in this segment.
    frame = text_segment.frames[0]
    time_offset = frame.time_offset
    print(
        "Time offset for the first frame: {}".format(
            time_offset.seconds + time_offset.nanos * 1e-9
        )
    )
    print("Rotated Bounding Box Vertices:")
    for vertex in frame.rotated_bounding_box.vertices:
        print("\tVertex.x: {}, Vertex.y: {}".format(vertex.x, vertex.y))