
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import random
import os

# Paths
source_image_path = r"C:/Users/SEOP/.gemini/antigravity/brain/5cc77354-e533-4d7b-a6df-f0bce07e2472/uploaded_media_1769493046292.jpg"
output_image_path = r"c:/Users/SEOP/Desktop/seop architecture/eunma_schematic_plan.png"

def create_schematic():
    if not os.path.exists(source_image_path):
        print(f"Error: Source image not found at {source_image_path}")
        return

    try:
        img = Image.open(source_image_path)
        width, height = img.size
        
        # Create figure and axes
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.imshow(img)
        
        # Target Building Coverage Ratio (BCR) = 27.73% (approx 28%)
        target_bcr = 0.2773
        
        # We will simulate approx 30 towers (high-rise)
        num_towers = 30
        
        # Total image area
        total_pixels = width * height
        
        # Target building footprint area in pixels
        target_footprint_total = total_pixels * target_bcr
        
        # Area per tower (assuming equal size for schematic)
        area_per_tower = target_footprint_total / num_towers
        
        # Dimension of one tower (square root of area)
        tower_dim = area_per_tower ** 0.5
        
        # Define grid for placement (just to distribute them, then jitter)
        rows = 5
        cols = 6
        
        # Margins to keep away from the very edge
        margin_x = width * 0.1
        margin_y = height * 0.1
        
        usable_width = width - 2 * margin_x
        usable_height = height - 2 * margin_y
        
        step_x = usable_width / cols
        step_y = usable_height / rows
        
        towers_placed = 0
        
        print(f"Generating schematic with {num_towers} towers...")
        print(f"Target BCR: {target_bcr*100:.2f}%")
        
        for r in range(rows):
            for c in range(cols):
                if towers_placed >= num_towers:
                    break
                
                # Center of this grid cell
                cx = margin_x + c * step_x + step_x/2
                cy = margin_y + r * step_y + step_y/2
                
                # Random jitter offset
                jitter_x = random.uniform(-step_x * 0.3, step_x * 0.3)
                jitter_y = random.uniform(-step_y * 0.3, step_y * 0.3)
                
                # Top-left of the rectangle
                x0 = cx + jitter_x - tower_dim/2
                y0 = cy + jitter_y - tower_dim/2
                
                # Create a shadow (offset)
                shadow_offset = tower_dim * 0.2
                shadow = patches.Rectangle(
                    (x0 + shadow_offset, y0 + shadow_offset), 
                    tower_dim, tower_dim, 
                    linewidth=0, 
                    edgecolor='none', 
                    facecolor='black', 
                    alpha=0.5
                )
                ax.add_patch(shadow)
                
                # Create the building footprint (Blue)
                # We use a slightly transparent blue to see underlying vaguely, but opaque enough to be distinct
                rect = patches.Rectangle(
                    (x0, y0), 
                    tower_dim, tower_dim, 
                    linewidth=1, 
                    edgecolor='white', 
                    facecolor='#007acc', 
                    alpha=0.8
                )
                ax.add_patch(rect)
                
                towers_placed += 1

        # Add Legend / Info Box
        info_text = (
            f"EUNMA REDEVELOPMENT SCHEMATIC\n"
            f"Site Area: {width}x{height} px\n"
            f"Target BCR: {target_bcr*100:.2f}%\n"
            f"Green/Open Space: {(1-target_bcr)*100:.2f}%\n"
            f"Estimated Towers: {num_towers} (Variable)"
        )
        
        props = dict(boxstyle='round', facecolor='white', alpha=0.8)
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)

        # Hide axes
        ax.axis('off')
        
        # Save output
        plt.savefig(output_image_path, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Successfully saved schematic to {output_image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_schematic()
