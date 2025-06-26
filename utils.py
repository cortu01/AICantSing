import os
import openai
import requests
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import random
import time

# Window position for image display
IMAGE_WINDOW_X = 50  # X coordinate
IMAGE_WINDOW_Y = 20 # Y coordinate
IMAGE_WIDTH = 1536
IMAGE_HEIGHT = 1536

#Local model parameters
LOCAL_ROUNDS = 5
LOCAL_SEED = random.randint(1, 1000000)
LOCAL_DIMS = (512, 512)

# Configurable options
persistentImage = True  # Set True for multiple images, False for only one active image
save_images = True  # Set True to save each image
save_folder = "generated_images"  # Folder where images are saved

# Ensure save folder exists
os.makedirs(save_folder, exist_ok=True)

# Track the latest window name (for single-image mode)
latest_window = None

def get_next_image_path():
    """Finds the next available filename in the save folder."""
    existing_files = [f for f in os.listdir(save_folder) if f.endswith(".png")]
    next_index = len(existing_files) + 1
    return os.path.join(save_folder, f"image_{next_index:04d}.png")

def generate_image(prompt, API_KEY, use_local_model=False):
    """Generates an image using either OpenAI DALL·E or local AIST model, saves it, and displays it in OpenCV."""
    global latest_window  # Track the last window name
    
    start_time = time.time()  # Start timing
    print(f"Starting image generation for: '{prompt}'")
    
    if use_local_model:
        print("Using local AIST model...")
        try:
            from aist import image
            
            # Generate with local model
            result = image.stable_diffusion(
                prompt,
                rounds=LOCAL_ROUNDS,  # Reduced for speed
                dims=LOCAL_DIMS,
                seed=LOCAL_SEED,
                accelerate=True
            )
            
            generation_time = time.time() - start_time
            print(f"Local image generation took: {generation_time:.2f} seconds")
            
            # Save the image
            if save_images:
                save_start = time.time()
                image_path = get_next_image_path()
                result.save(image_path)
                save_time = time.time() - save_start
                print(f"Image saved: {image_path} (took {save_time:.2f} seconds)")
            
            # Display the image
            display_start = time.time()
            image_cv = np.array(result)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
            
            # Close any existing "Generated Image" window
            cv2.destroyWindow("Generated Image")
            
            # Show the new image
            win_name = "Generated Image"
            image_cv = cv2.resize(image_cv, (IMAGE_WIDTH, IMAGE_HEIGHT))
            cv2.imshow(win_name, image_cv)
            cv2.moveWindow(win_name, IMAGE_WINDOW_X, IMAGE_WINDOW_Y)
            cv2.waitKey(1)  # Allow the window to refresh
            
            display_time = time.time() - display_start
            total_time = time.time() - start_time
            
            print(f"Display processing took: {display_time:.2f} seconds")
            print(f"Total local processing time: {total_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            print(f"⚠ Local generation failed: {e}")
            print("Falling back to OpenAI DALL-E...")
            # Continue to OpenAI fallback
    
    # OpenAI DALL-E generation (original code)
    print("Using OpenAI DALL-E...")
    openai.api_key = API_KEY
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt="A creative digital artwork of: " + prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response.data[0].url
        generation_time = time.time() - start_time  # Calculate generation time
        print(f"Generated Image URL: {image_url}")
        print(f"Image generation took: {generation_time:.2f} seconds")

        # Fetch the image
        fetch_start = time.time()
        image_data = requests.get(image_url).content
        fetch_time = time.time() - fetch_start
        print(f"Image download took: {fetch_time:.2f} seconds")
        
        image = Image.open(BytesIO(image_data))

        # Save image with sequential numbering
        if save_images:
            save_start = time.time()
            image_path = get_next_image_path()
            image.save(image_path)
            save_time = time.time() - save_start
            print(f"Image saved: {image_path} (took {save_time:.2f} seconds)")

        # Convert image for OpenCV
        display_start = time.time()
        image_cv = np.array(image)
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

        # Always close all previous windows before showing a new one
        #cv2.destroyAllWindows()
        cv2.destroyWindow("Generated Image")

        # Show the new image
        win_name = "Generated Image"
        image_cv = cv2.resize(image_cv, (IMAGE_WIDTH, IMAGE_HEIGHT))
        cv2.imshow(win_name, image_cv)
        cv2.moveWindow(win_name, IMAGE_WINDOW_X, IMAGE_WINDOW_Y)
        cv2.waitKey(1)  # Allow the window to refresh
        
        display_time = time.time() - display_start
        total_time = time.time() - start_time
        
        print(f"Display processing took: {display_time:.2f} seconds")
        print(f"Total image processing time: {total_time:.2f} seconds")

    except openai.OpenAIError as e:
        generation_time = time.time() - start_time
        print(f"Error generating image after {generation_time:.2f} seconds: {e}")

def load_starter_image():
    """Loads and displays starter.png from the root folder in the same window and location as generated images."""
    global latest_window
    
    starter_path = "starter.png"
    
    # Check if starter image exists
    if not os.path.exists(starter_path):
        print(f"Warning: {starter_path} not found in root folder")
        return False
    
    try:
        # Load the image using PIL first
        image = Image.open(starter_path)
        
        # Convert image for OpenCV
        image_cv = np.array(image)
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
        
        # Close any existing "Generated Image" window
        cv2.destroyWindow("Generated Image")
        
        # Show the starter image
        win_name = "Generated Image"
        image_cv = cv2.resize(image_cv, (IMAGE_WIDTH, IMAGE_HEIGHT))
        cv2.imshow(win_name, image_cv)
        cv2.moveWindow(win_name, IMAGE_WINDOW_X, IMAGE_WINDOW_Y)
        cv2.waitKey(1)  # Allow the window to refresh
        
        latest_window = win_name
        print(f"Starter image loaded and displayed: {starter_path}")
        return True
        
    except Exception as e:
        print(f"Error loading starter image: {e}")
        return False
