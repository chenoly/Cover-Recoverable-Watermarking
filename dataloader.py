import os
import glob
import torch
from PIL import Image, ImageOps
from torch.utils.data import Dataset
import torchvision.transforms as transforms


class HideImage(Dataset):
    def __init__(self, root_path, im_size, bit_length, channel_dim, mode="center"):
        self.cover = None
        self.im_size = im_size
        self.root_path = root_path
        self.bit_length = bit_length
        self.channel_dim = channel_dim
        self.transform = transforms.Compose([
            transforms.ToTensor()
        ])
        self.load_images()

    def load_images(self):
        file_modes = ('*.png', '*.tif', '*.tiff', '*.bmp', '*.jpg', '*.jpeg', '*.gif', '*.webp')
        img_paths = []
        for mode in file_modes:
            for img_path in glob.glob(os.path.join(self.root_path, '**', mode), recursive=True):
                with Image.open(img_path) as img:
                    # if img.size[0] >= self.im_size and img.size[1] >= self.im_size:
                    img_paths.append(img_path)
        self.cover = img_paths

    def __len__(self):
        return len(self.cover)

    def __getitem__(self, idx):
        cover_path = self.cover[idx]
        if self.channel_dim == 3:
            cover = Image.open(cover_path).convert('RGB')
        else:
            cover = Image.open(cover_path).convert('L')
        cover = ImageOps.fit(cover, (self.im_size, self.im_size))
        cover_tensor = self.transform(cover)
        secret_tensor = torch.randint(0, 2, size=(self.bit_length,))
        return cover_tensor / 1., secret_tensor / 1.


# if __name__ == "__main__":
#     root_path = r"/data/chenjiale/datasets/MiniVOCAL2012"
#     im_size = 256
#     dataset = HideImage(root_path, im_size, 1)
#     dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
#     for x_img_tensor, y_img_tensor in dataloader:
#         print(x_img_tensor)
