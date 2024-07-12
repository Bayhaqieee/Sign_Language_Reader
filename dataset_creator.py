import cv2
import os

def capture_images(label, num_images, save_dir='dataset'):
    """
    Capture images using the webcam and save them to the specified directory.
    """
    cap = cv2.VideoCapture(0)
    count = 0

    # Create a directory for the label if it doesn't exist
    label_dir = os.path.join(save_dir, label)
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            break

        # Display the frame
        cv2.imshow('frame', frame)

        # Save the image
        image_path = os.path.join(label_dir, f'{label}_{count}.jpg')
        cv2.imwrite(image_path, frame)
        count += 1

        # Print status to terminal
        print(f'Captured {count}/{num_images} for label: {label}')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Define labels for numbers 0-9 and alphabet A-Z
labels = [str(i) for i in range(10)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]

# Number of images per label
num_images_per_label = 100

# Capture images for each label
for label in labels:
    print(f'Start capturing images for label: {label}')
    capture_images(label, num_images_per_label)
    print(f'Finished capturing images for label: {label}')