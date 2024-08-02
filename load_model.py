import torch
import re
import os

# Define your model architecture
from net.refinement import Refinement

def parse_performance_file(performance_file):
    """
    Parse the performance file to extract mAP, total_loss, mIoU, and epoch information.

    Parameters:
    - performance_file (str): The path to the performance results file

    Returns:
    - epochs_data (list of dict): A list of dictionaries with epoch, mAP, total_loss, mIoU, and other metrics
    """
    epochs_data = []

    with open(performance_file, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "Epoch" in line and "training completed" in line:
                epoch_match = re.search(r'Epoch (\d+)', line)
                if epoch_match:
                    epoch = int(epoch_match.group(1))
                    total_loss_match = re.search(r'total_loss: ([\d\.]+)', line)
                    total_loss = float(total_loss_match.group(1)) if total_loss_match else None
                    
                    mAP_line = lines[i + 2].strip()
                    mAP_match = re.search(r'mAP: ([\d\.]+)', mAP_line)
                    mAP = float(mAP_match.group(1)) if mAP_match else None

                    eval_line = lines[i + 6].strip()
                    mIoU_match = re.search(r'mIoU: ([\d\.]+)', eval_line)
                    mIoU = float(mIoU_match.group(1)) if mIoU_match else None

                    if epoch and mAP and total_loss and mIoU:
                        epochs_data.append({
                            'epoch': epoch,
                            'mAP': mAP,
                            'total_loss': total_loss,
                            'mIoU': mIoU
                        })

    return epochs_data

def load_model(model_path_format, performance_file, epoch=None):
    """
    Load the model from a specific epoch or the best performing epoch.

    Parameters:
    - model_path_format (str): The format of the model file path, e.g., './models/epoch_{}.pth'
    - performance_file (str): The path to the performance results file
    - epoch (int, optional): The epoch number to load. If None, load the best performing model.

    Returns:
    - model (torch.nn.Module): The loaded model
    - epoch (int): The epoch number of the loaded model
    - best_record (dict): The best performance record
    """
    # Initialize the model
    model = Refinement(k=7)

    # Parse the performance results
    epochs_data = parse_performance_file(performance_file)
    print("epochs_data")
    print(epochs_data)
    
    if not epochs_data:
        raise ValueError("No epoch data found in the performance file.")

    if epoch is None:
        # Find the best performing epoch based on mAP, total_loss, and mIoU
        best_record = {'mAP': 0, 'total_loss': float('inf'), 'mIoU': 0, 'epoch': None}
        for data in epochs_data:
            if data['mAP'] > best_record['mAP']:
                best_record = data
            elif data['mAP'] == best_record['mAP']:
                if data['total_loss'] < best_record['total_loss']:
                    best_record = data
                elif data['total_loss'] == best_record['total_loss'] and data['mIoU'] > best_record['mIoU']:
                    best_record = data

        epoch = best_record['epoch']
        print(f"Loading model from the best performing epoch: {epoch} with mAP: {best_record['mAP']}, total_loss: {best_record['total_loss']}, mIoU: {best_record['mIoU']}")
    else:
        print(f"Loading model from epoch: {epoch}")

    # Load the model weights
    model_path = model_path_format.format(epoch)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = torch.load(model_path)

    # Ensure the model is in evaluation mode
    model.eval()

    print(f"Model from epoch {epoch} loaded successfully.")
    return model, epoch, best_record

# Example usage
model_path_format = "./models/epoch_{}.pth"
performance_file = "./test_performance.txt"

# To load the model from the best performing epoch
model, best_epoch, best_record = load_model(model_path_format, performance_file)

# To load the model from a specific epoch (e.g., epoch 300)
# model, specific_epoch, _ = load_model(model_path_format, performance_file, epoch=300)
