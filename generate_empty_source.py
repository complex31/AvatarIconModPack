import os

os.makedirs(f"resources", exist_ok=True)
original_names = os.listdir("original")

for name in original_names:
    os.makedirs(f"source/{name}", exist_ok=True)

print(f"generated {len(original_names)} folders")
