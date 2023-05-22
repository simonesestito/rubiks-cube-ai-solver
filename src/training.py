from model import CubeModel
import torch
import torch.nn as nn
from progressbar import progressbar

PYTORCH_DEVICE = 'cuda'

assert torch.cuda.is_available(), 'CUDA is not available'

model = CubeModel().to(PYTORCH_DEVICE)

# Hyper-parameters
LEARNING_RATE = 0.001
EPOCHS = 3

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Train the model
def train_loop(dataloader, model, loss_fn, optimizer):
    batch = 0
    for batch, (X, y) in range():
        # Move tensors to the configured device
        X = X.to(PYTORCH_DEVICE)
        # Compute prediction and loss
        pred = model(X)
        y = torch.tensor(y, device=PYTORCH_DEVICE)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 1000 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

for epoch in progressbar(range(EPOCHS)):
    print(f"Epoch {epoch+1}\n-------------------------------")
    train_loop(dataloader, model, criterion, optimizer)