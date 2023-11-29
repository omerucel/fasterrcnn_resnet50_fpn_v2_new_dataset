import os
import argparse
import json
import shutil


def labelme_to_xml(labelme_path, output_label_path):
    with open(labelme_path, 'r') as f:
        data = json.load(f)

    object_lines = []

    for shape in data['shapes']:
        label = shape['label']
        points = shape['points']

        x_min, y_min = float("inf"), float("inf")
        x_max, y_max = float("-inf"), float("-inf")

        for x, y in points:
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

        object_line = f"<object><name>{label}</name><bndbox><xmin>{x_min}</xmin><xmax>{x_max}</xmax><ymin>{y_min}</ymin><ymax>{y_max}</ymax></bndbox></object>"
        object_lines.append(object_line)

    with open(output_label_path, 'w') as f:
        f.writelines(["<annotation>"])
        f.writelines(object_lines)
        f.writelines(["</annotation>"])


def main():
    parser = argparse.ArgumentParser(description="Convert LabelMe to XML format")
    parser.add_argument("--input-dir", required=True, help="Input folder containing image and LabelMe JSON files")
    parser.add_argument("--output-dir", required=True, help="Output folder for XML format data")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    image_dir = os.path.join(output_dir, "train", "images")
    label_dir = os.path.join(output_dir, "train", "labels")

    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            labelme_path = os.path.join(input_dir, filename)
            output_image_path = os.path.join(image_dir, filename.replace(".json", ".png"))
            output_label_path = os.path.join(label_dir, filename.replace(".json", ".xml"))
            shutil.copyfile(os.path.join(input_dir, filename.replace(".json", ".png")), output_image_path)
            labelme_to_xml(labelme_path, output_label_path)


if __name__ == "__main__":
    main()
