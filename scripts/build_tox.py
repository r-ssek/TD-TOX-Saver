import asyncio
import subprocess
import shutil
import os
import json
import socket

import gitVersion
import build_settings
import env_var_utils

dist_dir_name = "release"
artifact_dir_name = "artifacts"
targets_dir_name = "targets"
dist_info_name = "dist_info.json"

dist_info: dict = {}
project_file = build_settings.project_file


def main():
    print('> verifying output directories are created...')
    # Verify dist directory exists
    dist_dir = dist_dir_name+"/"
    if not os.path.isdir(dist_dir):
        os.mkdir(dist_dir)

    print("Starting deploy process...")

    print("---> Finding Version Info...")
    dist_info = gitVersion.GetVersioningInfo()

    print(f"---> Creating build {dist_info.get('major_minor')}")

    # set up env vars
    env_var_utils.set_env_vars(
        build_settings=build_settings, dist_info=dist_info)

    # run td project
    print("---> Starting TouchDesigner")
    td_version = f"C:/Program Files/Derivative/TouchDesigner.{build_settings.td_version}/bin/TouchDesigner.exe"
    subprocess.call([td_version, project_file])

    # cleanup environment variable keys
    env_var_utils.clear_env_vars(build_settings=build_settings)


if __name__ == "__main__":
    main()
