
import os
import glob

target_dir = r"c:/Users/SEOP/Desktop/seop architecture/docs"
print(f"Listing {target_dir}:")
for f in os.listdir(target_dir):
    print(f"File: {repr(f)}")
    full_path = os.path.join(target_dir, f)
    print(f"  Exists? {os.path.exists(full_path)}")
    
target_file = r"c:/Users/SEOP/Desktop/seop architecture/docs/eunma_schematic_plan.png"
print(f"Checking specific target: {target_file}")
print(f"Exists? {os.path.exists(target_file)}")

target_file_back = r"c:\Users\SEOP\Desktop\seop architecture\docs\eunma_schematic_plan.png"
print(f"Checking specific target (BS): {target_file_back}")
print(f"Exists? {os.path.exists(target_file_back)}")
