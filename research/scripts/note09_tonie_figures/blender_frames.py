"""Extract still frames from a video with Blender's sequencer (no ffmpeg CLI on this machine).

Usage: blender --background --factory-startup --python blender_frames.py -- VIDEO OUTDIR STEP [MAXSIDE]
The video is untrusted data: it is only decoded, nothing in it is executed.
"""
import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
video, outdir, step = argv[0], argv[1], int(argv[2])
os.makedirs(outdir, exist_ok=True)
scene = bpy.context.scene
if not scene.sequence_editor:
    scene.sequence_editor_create()
se = scene.sequence_editor
coll = se.strips if hasattr(se, "strips") else se.sequences
strip = coll.new_movie(name="v", filepath=video, channel=1, frame_start=1)
n = strip.frame_final_duration
el = strip.elements[0]
scene.render.resolution_x = el.orig_width
scene.render.resolution_y = el.orig_height
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "JPEG"
scene.render.image_settings.quality = 92
scene.render.use_sequencer = True
scene.view_settings.view_transform = "Standard"
scene.frame_start, scene.frame_end = 1, n
print("VIDEO", os.path.basename(video), "frames", n, "size", el.orig_width, el.orig_height, "fps", strip.fps)
for f in range(1, n + 1, step):
    scene.frame_set(f)
    scene.render.filepath = os.path.join(outdir, f"frame_{f:04d}.jpg")
    bpy.ops.render.render(write_still=True)
print("DONE")
