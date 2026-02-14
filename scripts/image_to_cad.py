
import argparse
import sys
import os
import cv2
import numpy as np
import ezdxf
from skimage.morphology import skeletonize

def main():
    parser = argparse.ArgumentParser(description="Convert an architectural image to a layered DXF file.")
    parser.add_argument("--input", required=True, help="Path to the source image file.")
    parser.add_argument("--output", required=True, help="Path to the destination DXF file.")
    parser.add_argument("--epsilon", type=float, default=1.0, help="Approximation accuracy for polyline simplification (default: 1.0).")
    parser.add_argument("--mode", choices=['bw', 'color'], default='bw', help="Processing mode: 'bw' for line drawings, 'color' for rendered plans.")
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
        
    print(f"Processing {input_path} in [{args.mode}] mode...")
    
    def log(msg):
        print(f"[Info] {msg}")

    try:
        img_color = cv2.imread(input_path)
        if img_color is None:
            print("Error: Could not read image.")
            sys.exit(1)
        
        height, width = img_color.shape[:2]
        
        # Initialize DXF
        doc = ezdxf.new()
        msp = doc.modelspace()
        doc.layers.new(name='A-WALL', dxfattribs={'color': 1}) # Red (Thick/Primary)
        doc.layers.new(name='A-DETAIL', dxfattribs={'color': 2}) # Yellow (Thin/Secondary) - Renamed from FURN for generic use

        def trace_contours(mask, layer_name, min_area=10, epsilon_factor=0.002):
            contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            count = 0
            for cnt in contours:
                if cv2.contourArea(cnt) < min_area: continue
                epsilon = epsilon_factor * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                points = [(float(p[0][0]), float(height - p[0][1])) for p in approx]
                if len(points) > 2:
                    points.append(points[0]) 
                    msp.add_lwpolyline(points, dxfattribs={'layer': layer_name})
                    count += 1
            return count

        def process_color(img):
            # HSV Segmentation strategy (from previous iteration)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Walls (Black)
            lower_black = np.array([0, 0, 0])
            upper_black = np.array([180, 255, 90])
            mask_walls_raw = cv2.inRange(hsv, lower_black, upper_black)
            mask_walls_clean = cv2.morphologyEx(mask_walls_raw, cv2.MORPH_OPEN, np.ones((2,2), np.uint8))
            mask_walls_solid = cv2.morphologyEx(mask_walls_clean, cv2.MORPH_CLOSE, np.ones((3,3), np.uint8))
            
            # Floor (Wood/Orange)
            lower_wood = np.array([5, 30, 50])
            upper_wood = np.array([45, 255, 255])
            mask_floor = cv2.inRange(hsv, lower_wood, upper_wood)
            
            # Furniture = Not Wall AND Not Floor
            mask_walls_floor = cv2.bitwise_or(mask_walls_solid, mask_floor)
            mask_furn_raw = cv2.bitwise_not(mask_walls_floor)
            
            # Smooth Furniture
            kernel_large = np.ones((5,5), np.uint8)
            mask_furn_solid = cv2.morphologyEx(mask_furn_raw, cv2.MORPH_CLOSE, kernel_large, iterations=2)
            mask_furn_clean = cv2.morphologyEx(mask_furn_solid, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=1)
            
            # Subtract walls
            mask_walls_dilated = cv2.dilate(mask_walls_solid, np.ones((3,3), np.uint8), iterations=1)
            mask_furn_final = cv2.subtract(mask_furn_clean, mask_walls_dilated)
            
            log("Tracing Wall Outlines...")
            n_walls = trace_contours(mask_walls_solid, 'A-WALL', min_area=50, epsilon_factor=0.001)
            log(f"Added {n_walls} wall boundaries.")
            
            log("Tracing Furniture Outlines...")
            n_furn = trace_contours(mask_furn_final, 'A-DETAIL', min_area=30, epsilon_factor=0.004)
            log(f"Added {n_furn} furniture boundaries.")

        def process_bw(img):
            # B&W Line Drawing Strategy (Thick vs Thin separation)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 1. Binarize (Adaptive for robustness)
            # Invert: Lines become White, Background Black
            mask_lines = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                             cv2.THRESH_BINARY_INV, 21, 10)
            
            # Clean noise
            mask_lines = cv2.morphologyEx(mask_lines, cv2.MORPH_OPEN, np.ones((2,2), np.uint8))
            
            # 2. Separate Thick Lines (Structures/Walls)
            # Erode to kill thin lines, keep thick ones
            kernel_thick = np.ones((3,3), np.uint8)
            mask_thick = cv2.erode(mask_lines, kernel_thick, iterations=1)
            # Restore thickness
            mask_thick = cv2.dilate(mask_thick, kernel_thick, iterations=1)
            
            # 3. Separate Thin Lines (Details/Hatch/Roads)
            # Thin = All Lines - Thick Lines
            mask_thick_dilated = cv2.dilate(mask_thick, np.ones((3,3), np.uint8), iterations=1)
            mask_thin = cv2.subtract(mask_lines, mask_thick_dilated)
            
            log("Tracing Thick Lines (A-WALL)...")
            n_thick = trace_contours(mask_thick, 'A-WALL', min_area=20, epsilon_factor=0.001)
            log(f"Added {n_thick} thick segments.")
            
            log("Tracing Thin Lines (A-DETAIL)...")
            n_thin = trace_contours(mask_thin, 'A-DETAIL', min_area=10, epsilon_factor=0.001)
            log(f"Added {n_thin} thin segments.")

        # Execute selected mode
        if args.mode == 'color':
            process_color(img_color)
        else:
            process_bw(img_color)
            
        doc.saveas(output_path)
        print(f"Success! DXF saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
