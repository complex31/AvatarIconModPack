import sys
import os
import subprocess
from PIL import Image

def generate_dds(input_path, output_path, output_index):
    try:
        output_file_png = output_path + "/" + str(output_index) + ".png"
        output_file_dds = output_path + "/" + str(output_index) + ".dds"
        output_file_dds = output_file_dds.replace('/', '\\')
        img = Image.open(input_path)
        img = resize(img)
        img.save(output_file_png, 'PNG', srgb=False)
        subprocess.run(["texconv.exe", "-f", "BC7_UNORM", "-y", "-sepalpha", "-srgb", "-m", "1", "-o", ".", output_file_png], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.remove(output_file_png)
    except Exception as e:
        print(e)
        return
    return

def resize(image):
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    imageBox = image.getbbox()
    image = image.crop(imageBox)
    width, height = image.size
    target_width, target_height = 256, 256
    # aspect_ratio = width / height
    side = int(max(width, height))
    bg = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    box = [0,0]
    if (width>height):
        box[1] = 0 # int((width - height)*0.5)
    else:
        box[0] = int((height-width)*0.5)
    bg.paste(image, box=box)
    padded = int(side * 1.05)
    bg2 = Image.new("RGBA", (padded, padded), (0, 0, 0, 0))
    box2 = [int((padded-side)*0.5), 0]
    bg2.paste(bg, box=box2)

    # if aspect_ratio > 1:
    #     # Then crop the left and right edges:
    #     new_width = height
    #     offset = (width - new_width) / 2
    #     resize = (offset, 0, width - offset, height)
    # else:
    #     # ... crop the top and bottom:
    #     new_height = width
    #     offset = (height - new_height) / 2
    #     resize = (0, offset, width, height - offset)

    thumb = bg2.resize((target_width, target_height), Image.LANCZOS)
    return thumb


os.makedirs(f"resources", exist_ok=True)
original_names = os.listdir("original")
args = sys.argv
force = args[1:]
if (len(force) > 0):
    print(f"selective for {force}")
    original_names = force


for name in original_names:
    os.makedirs(f"resources/{name}", exist_ok=True)
    input_files = os.listdir(f"source/{name}")
    output_files = os.listdir(f"resources/{name}")
    if len(input_files) == 0:
        continue
    index = 0
    #if len(input_files) <= len(output_files) and name not in force:
    #    continue
    print(f"generating resources for {name}: {len(input_files)}")
    for filename in input_files:
        generate_dds(
            input_path=f"source/{name}/{filename}",
            output_path=f"resources/{name}",
            output_index=str(index)
            )
        index += 1
