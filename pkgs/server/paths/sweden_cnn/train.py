import numpy as np
import cv2
from torch import classes

import os

from enum import Enum
from typing import Union


if __name__ == "__main__":
    import remoter

    print("hello")
    result = remoter.run(lambda x: x + 1, 1)
    print("rr", result)


class SwedenYoloV8Class(Enum):
    # class_id, class_name, signs part of the class
    E19 = (0, "e19")
    E20_1 = (1, "e20-1")
    E30 = (2, "e30")
    T11_1 = (3, "t11-1")
    T11_4 = (
        4,
        "t11-4",
    )
    T11_5 = (
        5,
        "t11-5",
    )
    BLUE_WITH_TEXT = (
        6,
        "blue-with-text",
    )
    T17 = (
        7,
        "t17",
    )
    T24_1 = (
        8,
        "t24-1",
    )

    @staticmethod
    def get_by_name(name: str) -> Union["SwedenYoloV8Class", None]:
        for member in SwedenYoloV8Class:
            if member.value[1] == name:
                return member
        return None

    @staticmethod
    def get_by_id(id: int) -> Union["SwedenYoloV8Class", None]:
        for member in SwedenYoloV8Class:
            if member.value[0] == id:
                return member
        return None


class YoloV8BoxLabel:
    def __init__(self, x: float, y: float, w: float, h: float, class_id: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.class_id = class_id

    @staticmethod
    def from_pixel_coords(
        x_min: float,
        y_min: float,
        w_box: float,
        h_box: float,
        img_w: float,
        img_h: float,
        class_id,
    ):
        x_center = (x_min + w_box / 2) / img_w
        y_center = (y_min + h_box / 2) / img_h
        w_rel = w_box / img_w
        h_rel = h_box / img_h
        return YoloV8BoxLabel(x_center, y_center, w_rel, h_rel, class_id)

    def __iter__(self):
        return iter((self.class_id, self.x, self.y, self.w, self.h))

    def shift(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    @staticmethod
    def from_file(file_path: str) -> list["YoloV8BoxLabel"]:
        boxes = []
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 5:
                    raise ValueError("Not enough parts in file")
                class_id = int(parts[0])
                # Parse bounding box parameters.
                x_center, y_center, bbox_width, bbox_height = map(float, parts[1:5])
                boxes.append(
                    YoloV8BoxLabel(
                        x_center, y_center, bbox_width, bbox_height, class_id
                    )
                )
        return boxes


def crop_yolo_box(image: np.ndarray, box: YoloV8BoxLabel) -> np.ndarray:
    img_h, img_w = image.shape[:2]

    # Unpack YOLO bounding box (center x, center y, width, height) in relative values.
    _, x_center_rel, y_center_rel, width_rel, height_rel = box

    # Convert relative coordinates to absolute pixel values
    x_center = int(x_center_rel * img_w)
    y_center = int(y_center_rel * img_h)
    width_abs = int(width_rel * img_w)
    height_abs = int(height_rel * img_h)

    # Compute the top-left corner of the bounding box
    x1 = max(0, x_center - width_abs // 2)
    y1 = max(0, y_center - height_abs // 2)

    # Compute the bottom-right corner of the bounding box
    x2 = min(img_w, x_center + width_abs // 2)
    y2 = min(img_h, y_center + height_abs // 2)

    # Crop the image using array slicing
    cropped_image = image[y1:y2, x1:x2]
    return cropped_image


processed_labels_dir = os.path.join("data/labels")
processed_images_dir = os.path.join("data/images")
output_dir = os.path.join("data/classes")
processed_labels = sorted(os.listdir(processed_labels_dir))
processed_images = sorted(os.listdir(processed_images_dir))
classes_images: dict[SwedenYoloV8Class, list[np.ndarray]] = {}
for img_file_name, labels_file_name in zip(processed_images, processed_labels):
    img_file_path = os.path.join(processed_images_dir, img_file_name)
    image = cv2.imread(img_file_path)
    labels_file_path = os.path.join(processed_labels_dir, labels_file_name)
    bboxes = YoloV8BoxLabel.from_file(labels_file_path)
    for bbox in bboxes:
        box_image = crop_yolo_box(image, bbox)
        yolo_class = SwedenYoloV8Class.get_by_id(bbox.class_id)
        if yolo_class is None:
            print(f"Unknown class id {bbox.class_id}")
            continue
        if yolo_class not in classes_images:
            classes_images[yolo_class] = []
        classes_images[yolo_class].append(box_image)
for yolo_class, images in classes_images.items():
    print(f"Class: {yolo_class}")
    yolo_class_dir = os.path.join(output_dir, str(yolo_class.value[0]))
    os.makedirs(yolo_class_dir, exist_ok=True)
    for i, image in enumerate(images):
        image_file_path = os.path.join(yolo_class_dir, f"{i}.jpg")
        cv2.imwrite(image_file_path, image)
        print(f"Saved {image_file_path}")


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms, models

# --- 1. Data Preparation ---

# Define transforms with data augmentation for training
train_transforms = transforms.Compose(
    [
        transforms.RandomResizedCrop(224),  # Random crop and resize to 224x224
        transforms.RandomHorizontalFlip(),  # Random horizontal flip
        transforms.RandomRotation(15),  # Random rotation up to 15 degrees
        transforms.ColorJitter(
            brightness=0.2, contrast=0.2, saturation=0.2
        ),  # Vary brightness/contrast
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[
                0.485,
                0.456,
                0.406,
            ],  # Standard normalization values for pre-trained models
            std=[0.229, 0.224, 0.225],
        ),
    ]
)

# Define transforms for validation (minimal augmentation)
val_transforms = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)
data_path = os.path.join("data/classes")
full_dataset = datasets.ImageFolder(root=data_path, transform=None)
# Create a list of indices and shuffle them for a random split
num_samples = len(full_dataset)
indices = list(range(num_samples))
np.random.seed(42)  # for reproducibility
np.random.shuffle(indices)

# Define the train/validation split: e.g., 80% train, 20% validation
split = int(0.8 * num_samples)
train_indices, val_indices = indices[:split], indices[split:]

# Now create two separate datasets with the appropriate transforms using Subset.
train_dataset = Subset(
    datasets.ImageFolder(root=data_path, transform=train_transforms), train_indices
)
val_dataset = Subset(
    datasets.ImageFolder(root=data_path, transform=val_transforms), val_indices
)


train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)

# Determine the number of classes from your dataset
num_classes = len(full_dataset.classes)
print("Detected classes:", full_dataset.classes)
print("Number of classes:", num_classes)

# --- 2. Model Setup ---

# Load a pre-trained ResNet18 model and modify the final fully connected layer
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# --- 3. Training Loop ---


def train_model(num_epochs=25):
    best_acc = 0.0
    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")
        model.train()
        running_loss = 0.0
        running_corrects = 0

        # Training phase
        count = 0
        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()  # Zero the parameter gradients

            outputs = model(inputs)  # Forward pass
            count += 1
            loss = criterion(outputs, labels)
            loss.backward()  # Backpropagation
            optimizer.step()  # Optimize weights

            # Statistics
            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        epoch_loss = running_loss / len(train_dataset)
        epoch_acc = running_corrects.double() / len(train_dataset)
        print(f"Training Loss: {epoch_loss:.4f}  Acc: {epoch_acc:.4f}")

        # Validation phase
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                _, preds = torch.max(outputs, 1)
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)

        val_loss = val_loss / len(val_dataset)
        val_acc = val_corrects.double() / len(val_dataset)
        print(f"Validation Loss: {val_loss:.4f}  Acc: {val_acc:.4f}\n")

        # Save the model if it has the best accuracy so far
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), "best_sign_classifier.pth")
            print("Best model saved with accuracy: {:.4f}".format(best_acc))

    print("Training complete. Best validation accuracy: {:.4f}".format(best_acc))
