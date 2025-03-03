import subprocess
import os
import shutil

import project_settings
import td_builder.build_settings
import td_builder.env_var_utils
import td_builder.gitVersion
import td_builder.read_td_log

artifact_dir_name = "artifacts"
targets_dir_name = "targets"
dist_info_name = "dist_info.json"

dist_info: dict = {}
project_file = project_settings.PROJECT_FILE


def get_touchdesigner_path():
    """Get the path to the TouchDesigner executable."""
    # If TD_PATH is explicitly set in settings, use it directly
    if project_settings.TD_PATH and os.path.isfile(project_settings.TD_PATH):
        print(f"--> Using configured TouchDesigner path: {project_settings.TD_PATH}")
        return project_settings.TD_PATH

    # Otherwise try version-specific path
    version_specific_path = f"C:/Program Files/Derivative/TouchDesigner.{project_settings.TD_VERSION}/bin/TouchDesigner.exe"
    if os.path.isfile(version_specific_path):
        print(f"--> Using TouchDesigner version {project_settings.TD_VERSION}")
        return version_specific_path

    # Error if no valid path found
    raise FileNotFoundError(
        "TouchDesigner executable not found. Please set TD_PATH in project_settings.py"
    )


def main():
    print("> creating release...")
    # Verify dist directory exists
    dist_dir = f"{td_builder.build_settings.dest_dir}/"
    print("> verifying output directories are created...")
    if not os.path.isdir(dist_dir):
        print("-> creating directories...")
        os.makedirs(dist_dir, exist_ok=True)

    print("> Starting deploy process...")

    print("-> Finding Version Info...")
    dist_info = td_builder.gitVersion.GetVersioningInfo()

    print(f"--> Creating build {dist_info.get('major_minor')}")

    # set up env vars
    td_builder.env_var_utils.set_env_vars(
        build_settings=td_builder.build_settings, dist_info=dist_info
    )

    # Get TouchDesigner path with fallback support
    try:
        td_path = get_touchdesigner_path()

        # run td project
        print("--> Starting TouchDesigner")
        subprocess.call([td_path, project_file])

        td_builder.read_td_log.write_log_to_cloud(td_builder.build_settings.log_file)

        print("--> Zipping package")
        shutil.make_archive(
            td_builder.build_settings.package_dir,
            "zip",
            root_dir=td_builder.build_settings.package_dir,
        )
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return

    # cleanup environment variable keys
    td_builder.env_var_utils.clear_env_vars(build_settings=td_builder.build_settings)


if __name__ == "__main__":
    main()
