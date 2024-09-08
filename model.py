"""
author:         Tola Shobande
name:           model.py
date:           4/09/2024
description:
"""

import torch
import args
import torch.nn as nn
from torchvision import models


class Classifier(nn.Module):
    """
    This is a custom image classification model built upon a pre-trained ResNet-50 architecture.
    The model allows for fine-tuning of the final fully connected layers while freezing the earlier layers.

    Attributes:
    ----
    model : torchvision.models.resnet.ResNet
        The pre-trained ResNet-50 model from torchvision with a modified fully connected layer.
    freeze_weights : bool
        Determines whether to freeze the pre-trained weights of ResNet-50.
    num_classes : int
        The number of classes for the classification task.
    """

    def __init__(self, num_classes, freeze_weights=True):
        super(Classifier, self).__init__()
        self.model = models.resnet50(weights="IMAGENET1K_V2")

        if freeze_weights:
            for param in self.model.parameters():
                param.requires_grad = False

        self.model.fc = nn.Sequential(
            nn.Linear(self.model.fc.in_features, 512),
            nn.ReLU(),
            nn.Dropout(args.dropout),
            nn.Linear(512, num_classes),
            nn.LogSoftmax(dim=1),
        )

    def forward(self, x):
        """
        Defines the forward pass of the model, passing input through the modified ResNet-50 architecture.
        :param x: torch.Tensor :
            The input tensor to be passed through the network.
        :returns: torch.Tensor :
            The log probabilities for each class, returned as an output of the LogSoftmax layer.
        """
        return self.model(x)


def get_model(num_classes, freeze_weights=True):
    """
    Creates and returns a classifier model with the specified number of output classes.
    :param num_classes: int:
        The number of output classes for the classifier.
    :param freeze_weights: bool:
        If True, the model's pre-trained weights will be frozen, meaning they will not
        be updated during training.
    :return:
        A Classifier object initialized with `num_classes` and `freeze_weights` arguments.
    """
    return Classifier(num_classes=num_classes, freeze_weights=freeze_weights)


def load_model(num_classes, path):
    """
    Loads a pre-trained model's saved weights from a specified path and initializes
    it with a given number of classes.
    :param num_classes: int:
        The number of classes for the classification task.
    :param path: str:
        The path models saved weights.
    :returns: torch.nn.Module:
        The loaded pre-trained model.
    """
    model = get_model(num_classes)
    model.load_state_dict(torch.load(path))
    return model


def save_model(model, path):
    """
    Saves the state of a given model to the specified file path.
    :param model: torch.nn.Module:
        The PyTorch model whose state will be saved.
    :param path: str:
        The file path where the model's state dictionary will be saved. The path should
        include the file name and extension, e.g., 'model.pth'.
    """
    torch.save(model.state_dict(), path)
