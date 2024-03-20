import blendersynth as bsyn
import numpy as np
import os

bsyn.run_this_script()

monkey = bsyn.Mesh.from_primitive("monkey")
# TODO: load a mesh from file

bsyn.render.set_resolution(640, 480)
bsyn.render.set_cycles_samples(10)

comp = bsyn.Compositor()
obj_pass_idx = monkey.assign_pass_index(
    1
)  # To show masking, we assign a pass index to the first object

# we will create 4 cameras, one from each side of the monkey, facing the monkey
# TODO: increase camera numbers
cameras = []
camera_radius = 5
for i in range(4):
    camera = bsyn.Camera.create(
        name=f"Cam{i}",
        location=(
            camera_radius * np.cos(i * np.pi / 2),
            camera_radius * np.sin(i * np.pi / 2),
            0,
        ),
    )
    camera.look_at_object(monkey)
    cameras.append(camera)

    # we'll add a point light at each camera too
    light = bsyn.Light.create("POINT", location=camera.location, intensity=250)

bsyn.render.render_depth()  # Enable standard Blender depth pass
depth_vis = comp.get_depth_visual(max_depth=20)  # Create a visual of the depth pass
rgb_mask = comp.get_mask(
    obj_pass_idx, "Image"
)  # create an RGB mask (i.e. only render monkey)
bounding_box_visual = comp.get_bounding_box_visual()
# keypoints_visual = comp.get_keypoints_visual()  # Create a visual of keypoints


# we'll render RGB, normals, and bounding boxes
normal_aov = bsyn.aov.NormalsAOV(polarity=[-1, 1, -1])
instancing_aov = bsyn.aov.InstanceRGBAOV()
class_aov = bsyn.aov.ClassRGBAOV()
UVAOV = bsyn.aov.UVAOV()  # UV Coordinates
NOCAOV = bsyn.aov.GeneratedAOV()  # Normalized Object Coordinates (NOC)

for aov in [normal_aov, instancing_aov, class_aov, UVAOV, NOCAOV]:
    monkey.assign_aov(aov)

output_folder = "data/multiview"
os.makedirs(output_folder, exist_ok=True)

# All of the following will have Blender's Filmic colour correction by default
comp.define_output("Image", file_name="rgb", directory=output_folder + "/rgb")
comp.define_output(
    rgb_mask, name="rgb_masked", directory=output_folder + "/rgb_masked"
)  # render RGB layer masked by monkey
comp.define_output(
    bounding_box_visual, output_folder + "/bounding_box", name="bounding_box_visual"
)
# comp.define_output(keypoints_visual, output_folder, name='keypoints')

# All of the following will not have any colour correction
comp.define_output(
    normal_aov, file_name="normals", directory=output_folder + "/normals"
)
comp.define_output(
    depth_vis, output_folder + "/depth_vis"
)  # render visual of depth layer
comp.define_output(instancing_aov, output_folder + "/instancing", name="instancing")
comp.define_output(class_aov, output_folder + "/semantic", name="semantic")
comp.define_output(UVAOV, output_folder + "/UV", name="UV")
comp.define_output(NOCAOV, output_folder + "/NOC", name="NOC")
comp.define_output("Depth", output_folder + "/depth", file_format="OPEN_EXR")

bounding_boxes = bsyn.annotations.bounding_boxes([monkey], cameras)
# keypoints = bsyn.annotations.keypoints.project_keypoints(cube_vertices)

comp.render(camera=cameras, annotations=bounding_boxes)
