import pandas as pd
import torch
import torchvision
from PIL import Image

def remove_noise(image):
    alpha = image[3, :, :] > 50
    alpha = alpha.type(torch.uint8)
    noise_filtered = torch.mul(alpha, image)
    return noise_filtered[:3, :, :]

def read_images_from_csv(csv_path, n=-1):
    """Read images from paths in CSV and apply noise removal."""

    # Load the CSV that contains the image paths
    data = pd.read_csv(csv_path)

    # Initialize lists to store features and labels
    features, labels = [], []

    # Loop through rows in the CSV and process the images
    for i, row in data.iterrows():
        if i == n:
            break

        image_path = row['image_path']  # Get the image path from the 'image_path' column

        try:
            # Open the image using torchvision.io.read_image (or PIL Image)
            img = torchvision.io.read_image(image_path)

            # Apply noise removal
            img = remove_noise(img)

            # Append the processed image and the label to the lists
            features.append(img)
            labels.append(int(row['idnumber']))  # Assuming 'idnumber' column holds labels
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            continue

    return features, labels

import torchvision
class affectnetDataset(torch.utils.data.Dataset):
    def __init__(self):
        super(affectnetDataset, self).__init__()
        self.data = pd.read_csv("/content/filtered_data_fix2_withimages.csv")

        f,l = read_images_from_csv("/content/filtered_data_fix2_withimages.csv", n=-1)


        names = list(self.data["Name"])




        self.img_list = f

        self.names = names
        self.transform = torchvision.transforms.Resize((64,64))

    def __len__(self):
        return len(self.names)

    def __getitem__(self, idx):
        img = self.img_list[idx]/255.0

        n  = self.names[idx]
        return self.transform(img.type(torch.float32)), n

affect = affectnetDataset()
batch_size = 32
data_iter = torch.utils.data.DataLoader(
    affect, batch_size=batch_size,
    shuffle=True, num_workers=2)

import torch
import torch.nn as nn
import torch.nn.functional as F

class AUG_block(nn.Module):
    def __init__(self, out_channels, in_channels=3, kernel_size=4, strides=2,
                 padding=1, **kwargs):
      #inserte su código aquí
        super(AUG_block, self).__init__(**kwargs)
        self.conv2d_trans = nn.ConvTranspose2d(in_channels, out_channels,
                                kernel_size, strides, padding, bias=False)
        self.batch_norm = nn.BatchNorm2d(out_channels)
        self.activation = nn.ReLU()

    def forward(self, X):
      #inserte su código aquí
        return self.activation(self.batch_norm(self.conv2d_trans(X)))
class DEC_block(nn.Module):
    def __init__(self, out_channels, in_channels=3, kernel_size=4, strides=2,
                padding=1, alpha=0.2, **kwargs):
      #inserte su código aquí
        super(DEC_block, self).__init__(**kwargs)
        self.conv2d = nn.Conv2d(in_channels, out_channels, kernel_size,
                                strides, padding, bias=False)
        self.batch_norm = nn.BatchNorm2d(out_channels)
        self.activation = nn.LeakyReLU(alpha, inplace=True)

    def forward(self, X):
      #inserte su código aquí
        return self.activation(self.batch_norm(self.conv2d(X)))

n_G = 48

class Variational_Encoder(nn.Module):
    def __init__(self, latent_dims):
        super(Variational_Encoder, self).__init__()
        self.conv_seq = nn.Sequential(
            DEC_block(in_channels=3,out_channels=n_G),
            DEC_block(in_channels=n_G, out_channels=n_G*2),
            DEC_block(in_channels=n_G*2, out_channels=n_G*4),
            DEC_block(in_channels=n_G*4, out_channels=n_G*8),
            DEC_block(in_channels=n_G*8, out_channels=n_G*16),
            nn.AdaptiveMaxPool2d((1,1)),
            nn.Flatten(),
            nn.LazyLinear(latent_dims)

        )

        self.linear3 = nn.LazyLinear(latent_dims)
        self.linear4 = nn.LazyLinear(latent_dims)
    def forward(self, x):
      #inserte su código aquí
        z = self.conv_seq(x)
        media = self.linear3(z)
        log_var = F.relu(self.linear4(z))
        # Calcula la desviación estándar (std) a partir del logaritmo de la varianza.
        std = torch.exp(0.5*log_var)

        eps = torch.randn_like(std)
        latente = eps.mul(std).add_(media)
        return (latente, media, log_var)


class Decoder(nn.Module):
    def __init__(self, latent_dims):
        super(Decoder, self).__init__()
        self.seq = nn.Sequential(
          AUG_block(in_channels=latent_dims, out_channels=n_G*8,
                  strides=1, padding=0),
          AUG_block(in_channels=n_G*8, out_channels=n_G*4),
          AUG_block(in_channels=n_G*4, out_channels=n_G*2),
          AUG_block(in_channels=n_G*2, out_channels=n_G),
          nn.ConvTranspose2d(in_channels=n_G, out_channels=3,
                            kernel_size=4, stride=2, padding=1, bias=False),
          nn.Sigmoid()

        )


    def forward(self, z):
      #inserte su código aquí
        return self.seq(z)

class Variational_Autoencoder(nn.Module):
    def __init__(self, latent_dims):
        super(Variational_Autoencoder, self).__init__()
        self.encoder = Variational_Encoder(latent_dims)
        self.decoder = Decoder(latent_dims)

    def forward(self, x):
        z, media, log_var = self.encoder(x)
        z = z.unsqueeze(2).unsqueeze(3)
        return self.decoder(z), media, log_var

import torch.nn.functional as F
reconstruction_weight = 20000
latent_weight = 1

def vae_loss(x, x_hat, media, log_var):
    reconstruction_loss = F.binary_cross_entropy(x_hat, x, reduction='sum')
    latent_loss = -0.5 * torch.sum(1 + log_var - log_var.exp() - media.pow(2))
    return reconstruction_weight * reconstruction_loss + latent_weight * latent_loss
