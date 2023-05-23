from model import CubeModel
import torch
import torch.nn as nn
import cubes_dataset
import os

PYTORCH_DEVICE = os.getenv('PYTORCH_DEVICE', 'cuda')
print('[pytorch] Using device:', PYTORCH_DEVICE)

assert torch.cuda.is_available(), 'CUDA is not available'

# Load model, if present
if os.path.isfile('model.ckpt'):
    print('[pytorch] Loading model from checkpoint...')
    model = torch.load('model.ckpt')
else:
    print('[pytorch] Creating new model from SCRATCH...')
    model = CubeModel()
model = model.to(PYTORCH_DEVICE)
print(model)

# Hyper-parameters
LEARNING_RATE = 0.01
BATCH_SIZE = 500
EPOCHS = 10

print('[pytorch] Using hyper-parameters:')
print('[pytorch] LEARNING_RATE:', LEARNING_RATE)
print('[pytorch] BATCH_SIZE:', BATCH_SIZE)
print('[pytorch] EPOCHS:', EPOCHS)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Train the model
def train_loop(model, loss_fn, optimizer):
    batch = 0
    X, y = cubes_dataset.load_cubes_dataset_as_tensor(batch, BATCH_SIZE)

    total_samples, correct_samples = 0, 0

    while len(X) > 0:
        batch += BATCH_SIZE

        # Move tensors to the configured device
        X = X.to(PYTORCH_DEVICE)
        # Compute prediction and loss
        pred = model(X)
        y = y.to(PYTORCH_DEVICE)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Compute accuracy
        _, predicted = torch.max(pred.data, 1)
        total_samples += y.size(0)
        correct_samples += (predicted == y).sum().item()

        if batch % 1000 == 0 or BATCH_SIZE > 1000:
            loss = loss.item()
            print(f"loss: {loss:>7f}  [batch={batch}] - Batch accuracy: {correct_samples/total_samples*100:.4f}% ({correct_samples}/{total_samples})")
            total_samples, correct_samples = 0, 0
        
        # Load next batch
        X, y = cubes_dataset.load_cubes_dataset_as_tensor(batch, BATCH_SIZE)

if __name__ == '__main__':
    for epoch in range(EPOCHS):
        print('-------------------------------')
        print(f'Epoch {epoch+1}')
        train_loop(model, criterion, optimizer)

    # Save the model checkpoint
    torch.save(model, 'model.ckpt')