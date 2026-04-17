import open3d as o3d
import numpy as np
import json
from pathlib import Path


def visualize_pcd_with_keypoints(pcd_path: str, json_path: str = None):
    """
    Visualize point cloud with annotated keypoints

    Args:
        pcd_path: Path to the PCD file
        json_path: Path to the annotation JSON file (defaults to same name as PCD)
    """
    # Auto-detect JSON path
    if json_path is None:
        json_path = str(Path(pcd_path).with_suffix('.json'))

    # 1. Load point cloud
    print(f"Loading point cloud: {pcd_path}")
    pcd = o3d.io.read_point_cloud(pcd_path)
    if not pcd.has_points():
        print("Error: Point cloud is empty or failed to load")
        return

    # Set color (gray if no original color)
    if not pcd.has_colors():
        pcd.paint_uniform_color([0.5, 0.5, 0.5])

    # 2. Load annotation JSON
    print(f"Loading annotation: {json_path}")
    try:
        with open(json_path, 'r') as f:
            annotations = json.load(f)
    except FileNotFoundError:
        print(f"Error: Annotation file not found: {json_path}")
        return

    # 3. Extract keypoint coordinates
    keypoints_xyz = []
    class_id = None
    model_id = None

    # Annotation file is a list, each element contains class_id, model_id, keypoints
    for ann in annotations:
        class_id = ann.get("class_id")
        model_id = ann.get("model_id")
        for kp in ann.get("keypoints", []):
            xyz = kp.get("xyz")
            if xyz is not None and len(xyz) == 3:
                keypoints_xyz.append(xyz)

    print(f"Class ID: {class_id}")
    print(f"Model ID: {model_id}")
    print(f"Number of keypoints: {len(keypoints_xyz)}")

    # 4. Create sphere markers for keypoints
    geometries = [pcd]
    for i, xyz in enumerate(keypoints_xyz):
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
        sphere.translate(xyz)
        sphere.paint_uniform_color([1.0, 0.0, 0.0])  # Red
        geometries.append(sphere)
        print(f"Keypoint {i}: {xyz}")

    # 5. Display visualization window
    print("\nLaunching visualization window...")
    print("Controls: Drag to rotate/pan, scroll to zoom, press 'h' for help")
    o3d.visualization.draw_geometries(
        geometries,
        window_name=f"Point Cloud Annotation Viewer - {Path(pcd_path).name}",
        width=1024,
        height=768,
        point_show_normal=False,
        mesh_show_wireframe=False,
        mesh_show_back_face=False,
    )


if __name__ == "__main__":
    # Modify to your actual file path
    PCD_FILE = r"E:\BaiduNetdiskDownload\shapenetcorev2_hdf5_2048\bus_pcds\02924116\3ff98b31a921fd0f51dc8a1ad94841b7.pcd"
    # JSON file defaults to same name as PCD; can also be specified manually
    JSON_FILE = None  # If None, auto-matches same-name JSON

    visualize_pcd_with_keypoints(PCD_FILE, JSON_FILE)