import sys
import cv2
import numpy as np
# Fix for TensorFlow typing issue in Python 3.9
if sys.version_info < (3, 10):
    from typing import List, Optional, Union
import tensorflow as tf
from tensorflow.keras import models, layers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
import tempfile
import shutil
import os
import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define class labels
classes = {
    'cover': 0, 
    'defense': 1, 
    'flick': 2, 
    'hook': 3, 
    'late_cut': 4, 
    'lofted': 5, 
    'pull': 6, 
    'square_cut': 7, 
    'straight': 8, 
    'sweep': 9
}

# Global variable to hold the model
model = None
model_weights_path = 'model_weights.h5'

# Function to load the model
def load_model(weights_path):
    global model
    base_model = EfficientNetB0(include_top=False, weights='imagenet', input_shape=(224, 224, 3))

    # Set the base model as non-trainable
    base_model.trainable = False

    # Define the full model using a Sequential model - matching the original saved weights (5 layers)
    model = models.Sequential([
        # Apply EfficientNetB0 to each frame of the video
        layers.TimeDistributed(base_model, input_shape=(None, 224, 224, 3)),
        layers.TimeDistributed(layers.GlobalAveragePooling2D()),

        # Use GRU layers to capture temporal relationships
        layers.GRU(256, return_sequences=True),
        layers.GRU(128),

        # Dense layers for classification
        layers.Dense(1024, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    
    model.load_weights(weights_path)
    return model

def format_frames(frame, output_size):
    """
    Pad and resize an image from a video and apply proper preprocessing.

    Args:
      frame: Image that needs to resized and padded.
      output_size: Pixel size of the output frame image.

    Return:
      Formatted frame with padding of specified output size, properly preprocessed.
    """
    # Convert to float32 for processing
    frame = tf.image.convert_image_dtype(frame, tf.float32)
    # Resize with padding
    frame = tf.image.resize_with_pad(frame, *output_size)
    # Scale to [0, 255] range (EfficientNetB0 expects this)
    frame = frame * 255.0
    # Apply EfficientNetB0 preprocessing
    frame = preprocess_input(frame)
    return frame.numpy()

def frames_from_video_file(video_path, n_frames, output_size=(224, 224), frame_step=1):
    """
    Extracts frames sequentially from the start of the video file, with a specified step between frames.

    Args:
      video_path: File path to the video.
      n_frames: Number of frames to be created per video file.
      output_size: Pixel size of the output frame image (height, width).
      frame_step: Number of frames to skip between extracted frames.

    Returns:
      A NumPy array of frames in the shape of (n_frames, height, width, channels).
    """
    result = []
    src = cv2.VideoCapture(str(video_path))

    src.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Start from the first frame

    # Attempt to read the first frame
    ret, frame = src.read()
    if ret:
        frame = format_frames(frame, output_size)
        result.append(frame)
    else:
        # If the first frame can't be read, append a zero frame and exit
        result.append(np.zeros((output_size[0], output_size[1], 3), dtype=np.uint8))

    # Read subsequent frames with the specified frame_step
    for _ in range(n_frames - 1):
        for _ in range(frame_step):
            ret, frame = src.read()
        if ret:
            frame = format_frames(frame, output_size)
            result.append(frame)
        else:
            # Append a zero-like frame if no more frames can be read
            result.append(np.zeros_like(result[0]))

    src.release()

    # Convert the list of frames to a NumPy array and adjust color channels from BGR to RGB
    result = np.array(result)[..., [2, 1, 0]]

    return result

# Function to classify video
def classify_video(video_path, model, frame_count, class_labels):
    # Process the video file to get the frames
    frames = frames_from_video_file(video_path, frame_count)
    print(f"Frames shape: {frames.shape}")
    print(f"Frames dtype: {frames.dtype}")
    print(f"Frames min: {frames.min()}, max: {frames.max()}")

    # Add batch dimension if the model expects it
    frames = np.expand_dims(frames, axis=0)
    print(f"Batch frames shape: {frames.shape}")

    # Use the model to predict the class probabilities
    predictions = model.predict(frames)
    print("Raw predictions:", predictions)

    # Convert predictions to class labels
    predicted_class_idx = np.argmax(predictions, axis=1)[0]  # Get the index of the max class score
    print("Predicted class index:", predicted_class_idx)
    
    # Get the class name using the predicted index
    predicted_class_name = list(class_labels.keys())[list(class_labels.values()).index(predicted_class_idx)]
    
    # Calculate the confidence percentage of the predicted class
    confidence = predictions[0][predicted_class_idx] * 100  # Assuming softmax output, multiply by 100 for percentage
    print("Confidence (%): {:.2f}%".format(confidence))
    
    # Get top 3 predictions
    top_3_indices = np.argsort(predictions[0])[-3:][::-1]  # Get indices of top 3 in descending order
    top_3_predictions = []
    print("\nTop 3 Predictions:")
    for idx in top_3_indices:
        class_name = list(class_labels.keys())[list(class_labels.values()).index(idx)]
        confidence_score = predictions[0][idx] * 100
        top_3_predictions.append({
            'shotType': class_name,
            'confidence': round(float(confidence_score), 2)
        })
        print(f"  {class_name}: {confidence_score:.4f}%")
    
    # Print all class probabilities
    print("\nAll class predictions:")
    for class_name, class_idx in sorted(class_labels.items(), key=lambda x: x[1]):
        print(f"  {class_name}: {predictions[0][class_idx]*100:.4f}%")

    return predicted_class_name, confidence, top_3_predictions

@app.on_event("startup")
async def startup_event():
    logger.info("Cricket Shot Classification API started")
    logger.info(f"Model weights path: {model_weights_path}")
    logger.info("Model will be loaded on each /classify-video/ request")

@app.get("/")
async def root():
    return {"message": "Cricket Shot Classification API"}

@app.post("/classify-video/")
async def classify_video_endpoint(file: UploadFile = File(...)):
    # Log file information
    logger.info(f"Received file: {file.filename}")
    logger.info(f"File content type: {file.content_type}")
    
    # Load the model for this request
    logger.info("Loading model...")
    request_model = load_model(model_weights_path)
    logger.info("Model loaded successfully")
    
    # Save the uploaded file temporarily
    # Preserve original file extension
    file_extension = '.mp4'  # default
    if file.filename:
        ext = file.filename.split('.')[-1].lower()
        if ext in ['mp4', 'avi', 'mov']:
            file_extension = '.' + ext
            logger.info(f"Using file extension: {file_extension}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmpfile:
        shutil.copyfileobj(file.file, tmpfile)
        tmp_path = tmpfile.name
        logger.info(f"Saved file to temporary path: {tmp_path}")

    try:
        # Classify the video using the loaded model
        class_name, confidence, top_3_predictions = classify_video(tmp_path, request_model, 30, classes)
        
        # Map class names to more readable formats
        class_display_names = {
            'cover': 'Cover Drive',
            'defense': 'Defense',
            'flick': 'Flick Shot',
            'hook': 'Hook Shot',
            'late_cut': 'Late Cut',
            'lofted': 'Lofted Shot',
            'pull': 'Pull Shot',
            'square_cut': 'Square Cut',
            'straight': 'Straight Drive',
            'sweep': 'Sweep Shot'
        }
        
        # Convert top 3 predictions to display names
        top_3_with_display_names = [
            {
                'shotType': class_display_names.get(pred['shotType'], pred['shotType']),
                'confidence': pred['confidence']
            }
            for pred in top_3_predictions
        ]
        
        # Prepare response data
        result = {
            "shotType": class_display_names.get(class_name, class_name),
            "confidence": round(float(confidence), 2),
            "top3Predictions": top_3_with_display_names,
            "shotsDetected": [class_display_names.get(class_name, class_name)],
            "footworkQuality": 85,  # This would be calculated in a full implementation
            "timingClassification": "Excellent",  # This would be calculated in a full implementation
            "shotTypeRecognition": [f"{class_display_names.get(class_name, class_name)}: 100%"],
            "balanceAnalysis": 78,  # This would be calculated in a full implementation
            "keyFrames": ["/placeholder.svg"] * 6,  # Placeholder for key frames
            "recommendations": [
                f"Focus on improving your {class_display_names.get(class_name, class_name).lower()} technique",
                "Maintain proper body alignment during shots",
                "Practice consistent footwork for better balance"
            ]
        }
        
        logger.info(f"Classification complete: {class_name} with confidence {confidence:.2f}%")
        logger.info(f"Top 3 predictions: {top_3_with_display_names}")
        return result
    except Exception as e:
        logger.error(f"Error processing video file: {str(e)}")
        # Re-raise the exception so the client gets an error response
        raise e
    finally:
        # Clean up the temporary file
        try:
            os.unlink(tmp_path)
            logger.info(f"Cleaned up temporary file: {tmp_path}")
        except Exception as e:
            logger.warning(f"Failed to delete temporary file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)