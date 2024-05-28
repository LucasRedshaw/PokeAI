import csv
from PIL import Image, ImageDraw
from collections import defaultdict

# Define base coordinates for each map ID
base_coordinates = {
    0: (1519, 3903),
    12: (1519, 3327),
    # Add other map IDs and their base coordinates here
    # Example: 1: (2000, 3000)
}

def read_coordinates(csv_path, map_ids):
    coordinates = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            map_id = int(row[1])
            if map_id in map_ids:  # Only process coordinates with specified map IDs
                x = int(row[2])
                y = int(row[3])
                coordinates.append((map_id, x, y))
    return coordinates

def calculate_frequencies(coordinates):
    freq = defaultdict(int)
    for coord in coordinates:
        freq[coord] += 1
    return freq

def create_heatmap(image_path, coordinates, output_path, base_coordinates, tile_size=16):
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))  # Create an overlay with full transparency
    draw = ImageDraw.Draw(overlay, "RGBA")

    # Calculate frequencies of visits
    freq = calculate_frequencies(coordinates)

    # Determine maximum frequency for normalization
    if len(freq) == 0:
        return
    max_freq = max(freq.values())

    for (map_id, x, y), count in freq.items():
        # Get the base coordinates for the current map ID
        basex_0, basey_0 = base_coordinates[map_id]
        
        # Calculate the top-left and bottom-right coordinates of the tile
        x1 = basex_0 + x * tile_size
        x2 = x1 + tile_size
        y1 = basey_0 + y * tile_size
        y2 = y1 + tile_size

        # Normalize the frequency to get the shade of red and transparency
        min_shade = 200  # Minimum shade value for light red
        max_shade = 255  # Maximum shade value for dark red
        min_alpha = 50   # Minimum transparency for very pale red
        max_alpha = 220  # Maximum transparency for dark red

        shade = int(min_shade + (count / max_freq) * (max_shade - min_shade))
        alpha = int(min_alpha + (count / max_freq) * (max_alpha - min_alpha))
        color = (shade, 0, 0, alpha)  # Red color with varying intensity and transparency

        # Fill the tile with the shaded color
        draw.rectangle([x1, y1, x2, y2], fill=color)

    # Composite the overlay onto the original image
    combined = Image.alpha_composite(img, overlay)
    combined.save(output_path)
    print(f"Heatmap saved to {output_path}")

