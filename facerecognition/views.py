
import cv2
import face_recognition
import os
import glob
from django.http import JsonResponse,StreamingHttpResponse ,HttpRequest
from PIL import Image
import json
import base64

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def handle_request(request):
    if request.method == 'POST':
        default_camera = int(request.POST.get('defaultCameraIndex').strip("'"))

        return default_camera
    
    
    elif request.method == 'GET':
        default_camera = 0
        return default_camera
    
    else:
        # Code to handle other types of requests
        return None

    
@csrf_exempt
def generate_frames(request):
    # Load known faces from folder
    known_faces = []
    known_labels = []
    for filename in glob.glob('faces/*.*'):
        # Load face image and extract label from filename
        image = face_recognition.load_image_file(filename)
        label = os.path.splitext(os.path.basename(filename))[0]

        # Append face image and label to lists
        known_faces.append(image)
        known_labels.append(label)

    # Encode known faces
    known_encodings = [face_recognition.face_encodings(face)[0] for face in known_faces]
    
    cam=handle_request(request)
    # Start video capture from camera
    cap = cv2.VideoCapture(cam)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Find all faces in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Recognize each face
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare face encoding with known encodings
            matches = face_recognition.compare_faces(known_encodings, face_encoding)

            # Find best match
            match_index = matches.index(True) if True in matches else -1

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Print name of recognized face
            if match_index >= 0:
                name = known_labels[match_index]
                print(name)
            else:
                name = 'unknown'
                print(name)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            # Encode the frame as JPEG image
            _, jpeg_frame = cv2.imencode('.jpg', frame)
            jpeg_bytes = jpeg_frame.tobytes()
            jpeg_base64 = base64.b64encode(jpeg_bytes).decode('utf-8')

            # Yield JPEG-encoded frame
            response = {
                'name': name,
                'frame': jpeg_base64
            }

            # Yield the response as JSON
            yield json.dumps(response) + '\n'
        
    # Release video capture and close window
    cap.release()
    cv2.destroyAllWindows()
    
@csrf_exempt
def face_recognition_api(request):
    return StreamingHttpResponse(generate_frames(request), content_type='text/event-stream')



@csrf_exempt
def capture_and_save_image(request: HttpRequest) -> JsonResponse:
    # Get the camera device ID from the request data
    cam=handle_request(request)
    # Access the camera device
    cap = cv2.VideoCapture(cam)

    # Initialize the filename variable
    filename = None

    # Capture an image
    ret, frame = cap.read()

    # Check if the image was captured successfully
    if not ret:
        return JsonResponse({'status': 'error', 'message': 'Image not captured'})

    # Get the filename from the request data
    filename_without_ext = request.POST.get('Name')

    # Check if the filename is empty or includes an extension
    if not filename_without_ext:
        return JsonResponse({'status': 'error', 'message': 'name not provided'})
    if '.' in filename_without_ext:
        return JsonResponse({'status': 'error', 'message': 'name should not include extension'})

    # Add the ".jpg" extension to the filename
    filename = f"{filename_without_ext}.jpg"

    # Save the image in the "faces" folder
    path = os.path.join(os.getcwd(), 'faces', filename)
    image = Image.fromarray(frame)
    image.save(path)

    # Encode the captured image as a base64 string
    _, buffer = cv2.imencode('.jpg', frame)
    image_data = base64.b64encode(buffer).decode('utf-8')

    # Return the response with the filename and image
    response_data = {'status': 'success', 'filename': filename, 'image': image_data}
    return JsonResponse(response_data)

