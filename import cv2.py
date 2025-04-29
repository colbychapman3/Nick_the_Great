import cv2
import numpy as np

def create_animated_video(image_path, output_path, duration=10, fps=30):
    """
    Create an animated video from the image with pan and zoom effects
    
    Parameters:
    - image_path: Path to input image
    - output_path: Path for output video
    - duration: Length of video in seconds
    - fps: Frames per second
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not load image")
    
    # Get dimensions
    height, width = img.shape[:2]
    
    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration * fps
    
    for frame in range(total_frames):
        progress = frame / total_frames
        
        # Create zoom effect
        scale = 1 + 0.2 * np.sin(progress * np.pi)
        
        # Create matrix for transformation
        matrix = cv2.getRotationMatrix2D((width/2, height/2), 0, scale)
        
        # Apply transformation
        frame_image = cv2.warpAffine(
            img, matrix, (width, height),
            borderMode=cv2.BORDER_REFLECT
        )
        
        # Add subtle horizontal pan
        pan_offset = int(50 * np.sin(progress * 2 * np.pi))
        matrix_pan = np.float32([[1, 0, pan_offset], [0, 1, 0]])
        frame_image = cv2.warpAffine(
            frame_image, matrix_pan, (width, height),
            borderMode=cv2.BORDER_REFLECT
        )
        
        out.write(frame_image)
    
    out.release()
    print(f"Video saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    create_animated_video(
        image_path="path/to/your/animated_characters.jpg",
        output_path="animated_scene.mp4",
        duration=10,
        fps=30
    )