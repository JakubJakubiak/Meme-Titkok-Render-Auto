import cv2
import os
import numpy as np


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            filepath = os.path.join(folder, filename)
            img = cv2.imread(filepath)
            if img is not None:
                images.append(img)
            else:
                print(f"Warning: Could not read image {filepath}")
    return images


image_up_folder = 'image_up'
image_down_folder = 'image_down'


if not os.path.exists(image_up_folder):
    raise FileNotFoundError(f"Folder '{image_up_folder}' does not exist.")
if not os.path.exists(image_down_folder):
    raise FileNotFoundError(f"Folder '{image_down_folder}' does not exist.")


fps = 30
duration_per_image = 5  # duration of one picture in seconds
total_frames_per_image = fps * duration_per_image


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

images_up = load_images_from_folder(image_up_folder)
images_down = load_images_from_folder(image_down_folder)


height_up, width_up, _ = images_up[0].shape
height_down, width_down, _ = images_down[0].shape
width = min(width_up, width_down)
height = height_up + height_down

counter = 1
for img_up, img_down in zip(images_up, images_down):
    img_up_resized = cv2.resize(img_up, (width, height_up))
    img_down_resized = cv2.resize(img_down, (width, height_down))

    combined_image = np.vstack((img_up_resized, img_down_resized))

    video_name = f'output/output_video_{counter}.mp4'
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for _ in range(total_frames_per_image):
        video.write(combined_image)

    video.release()

    print(f"The video was saved as  '{video_name}'")
    counter += 1

print("The video recording process is complete.")
