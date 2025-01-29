import json
import numpy as np
from PIL import Image
from utils.perlin_noise import generate_perlin_noise

def save_image(noise, filename, color_config):
    if not color_config.get('use', True):
        noise = (noise * 255).astype(np.uint8)
        img = Image.fromarray(noise)
        img.save(filename)
        return
    
    height, width = noise.shape
    color_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            value = noise[y, x]
            for layer in color_config['layers']:
                if layer['use'] and value <= layer['height']:
                    color = np.array(layer['color'])
                    # Adjust the blending logic to ensure proper scaling
                    blended_color = color * (value / layer['height'])
                    color_image[y, x] = blended_color.astype(np.uint8)
                    break
    
    img = Image.fromarray(color_image)
    img.save(filename)

def smooth_edges(noise, smoothing_percentage=0.25, inflation_factor=1.1):
    height, width = noise.shape
    
    # Smooth the top
    top_value = min(np.mean(noise[0, :]) * inflation_factor, 1.0)
    noise[0, :] = top_value  # Set the top line to the average value
    top_smoothing_height = int(height * smoothing_percentage)
    for y in range(1, top_smoothing_height):
        blend_factor = y / top_smoothing_height
        noise[y, :] = blend_factor * noise[y, :] + (1 - blend_factor) * top_value
    
    # Smooth the bottom
    bottom_value = np.mean(noise[-1, :])  # Calculate the average value of the last line
    noise[-1, :] = bottom_value  # Set the bottom line to the average value
    bottom_smoothing_height = int(height * smoothing_percentage)
    for y in range(1, bottom_smoothing_height):
        blend_factor = y / bottom_smoothing_height
        noise[-y-1, :] = blend_factor * noise[-y-1, :] + (1 - blend_factor) * bottom_value
    
    # Smooth the left and right
    left_smoothing_width = int(width * (smoothing_percentage / 2))
    for y in range(height):
        left_value = noise[y, 0]
        right_value = noise[y, -1]
        avg_value = (left_value + right_value) / 2  # Average value for the current row
        noise[y, 0] = avg_value  # Set the left column to the average value
        noise[y, -1] = avg_value  # Set the right column to the average value
        for x in range(1, left_smoothing_width):
            blend_factor = x / left_smoothing_width
            noise[y, x] = blend_factor * noise[y, x] + (1 - blend_factor) * avg_value
            noise[y, -x-1] = blend_factor * noise[y, -x-1] + (1 - blend_factor) * avg_value
    
    return noise

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    image_config = config.get('image', {})
    size_config = image_config.get('size', {})
    global_scale = image_config.get('global_scale', 1.0)
    color_config = config.get('colors', {})
    
    width = int(size_config.get('width', 720) * global_scale)
    height = int(size_config.get('height', 320) * global_scale)
    save_path = image_config.get('save_path', '../maps/map1.png')
    
    layers = config.get('layers', [])
    
    final_noise = np.zeros((height, width))
    total_weight = 0
    
    for layer in layers:
        if not layer.get('use', True):
            continue
        
        seed = layer.get('seed', 0)
        scale = layer.get('scale', 10.0)
        octaves = layer.get('octaves', 1)
        persistence = layer.get('persistence', 0.5)
        lacunarity = layer.get('lacunarity', 2.0)
        invert = layer.get('invert', False)
        weight = layer.get('weight', 1.0)
        
        noise = generate_perlin_noise(width, height, seed, scale * global_scale, octaves, persistence, lacunarity)
        
        if invert:
            noise = 1 - noise
        
        final_noise += noise * weight
        total_weight += weight
    
    final_noise = smooth_edges(final_noise)

    if total_weight > 0:
        final_noise /= total_weight
    
    save_image(final_noise, save_path, color_config)
    print("Image generation complete.")