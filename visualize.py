#!/usr/bin/env python3

from __future__ import annotations

import rerun as rr
import argparse
import numpy as np
import os
from pathlib import Path
from rerun_loader_urdf import URDFLogger
import scipy.spatial.transform as st

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow_datasets as tfds


def path_to_link(link: int) -> str:
    return "/".join(f"panda_link{i}" for i in range(link + 1))


def log_angle_rot(urdf_logger: URDFLogger, link: int, angle_rad: int) -> None:
    entity_path = path_to_link(link)
    start_translation, start_rotation_mat = urdf_logger.entity_to_transform[entity_path]

    link_to_rot_axis = np.array([
        [1, 0, 0],

        [0, 0, 1], # 1
        [0, 1, 0], # 2
        [0, 1, 0], # 3
        [0, 1, 0], # 4
        [0, 1, 0], # 5
        [0, 0, 1], # 6
        [0, 0, 1], # 7
        [0, 0, 1], # 8
    ])
    vec = np.array(link_to_rot_axis[link]*angle_rad)
    rot = st.Rotation.from_rotvec(vec).as_matrix()
    rotation_mat = rot @ start_rotation_mat
    rr.log(
        entity_path, rr.Transform3D(translation=start_translation, mat3x3=rotation_mat)
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Visualizes the DROID dataset using Rerun."
    )
    parser.add_argument("--data-dir", type=Path, default=Path("droid_100") / "1.0.0")
    parser.add_argument("--urdf-path", type=Path, default=Path("Panda") / "panda.urdf")
    args = parser.parse_args()

    rr.init("droid", spawn=True)

    data_dir = args.data_dir
    rr.set_time_sequence("step", 0)
    urdf_logger = URDFLogger(args.urdf_path)
    urdf_logger.log()

    builder = tfds.builder_from_directory(builder_dir=args.data_dir)
    print(builder.info.features)

    dataset = builder.as_dataset()["train"]

    elems = [element for element in dataset]
    for i, step in enumerate(elems[0]["steps"]):
        rr.set_time_sequence("step", i+1)

        joint_positions = step["observation"]["joint_position"]
        for (joint_idx, angle) in enumerate(joint_positions):
            log_angle_rot(urdf_logger, joint_idx+2, angle)


if __name__ == "__main__":
    main()
