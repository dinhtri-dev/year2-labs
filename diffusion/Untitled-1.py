# ============================================
# Exercise 1: Using a Pretrained Generative Model (Diffusion)
# Model: google/ddpm-cifar10-32 (pretrained DDPM on CIFAR-10)
# Tasks:
#  - Load a pretrained model
#  - Generate images
#  - Adjust generation parameters
#  - Discuss quality vs diversity and computational cost
# ============================================

import time
import torch
from PIL import Image
import matplotlib.pyplot as plt

# 1) Install dependencies (run once)
# If you're on Colab, uncomment these:
# !pip -q install diffusers==0.30.3 transformers==4.44.2 accelerate==0.34.2 safetensors==0.4.5

from diffusers import DDPMPipeline

# 2) Device
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)

# 3) Load pretrained diffusion pipeline
model_id = "google/ddpm-cifar10-32"
pipe = DDPMPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

# Optional speed/memory tweaks (safe defaults)
# torch.backends.cuda.matmul.allow_tf32 = True  # if cuda
# pipe.unet.to(memory_format=torch.channels_last)  # if cuda

def make_grid(images, nrow=4, scale=4):
    """Create a grid plot from PIL images."""
    n = len(images)
    ncol = (n + nrow - 1) // nrow
    fig, axes = plt.subplots(ncol, nrow, figsize=(nrow*scale, ncol*scale))
    if ncol == 1:
        axes = [axes]
    for idx in range(ncol*nrow):
        r = idx // nrow
        c = idx % nrow
        ax = axes[r][c] if ncol > 1 else axes[c]
        ax.axis("off")
        if idx < n:
            ax.imshow(images[idx])
    plt.tight_layout()
    plt.show()

# 4) Generate images with adjustable parameters
def generate_batch(
    seed=0,
    batch_size=8,
    num_inference_steps=50,
):
    """
    DDPM generation parameters:
    - seed controls randomness/diversity
    - batch_size controls how many images to sample
    - num_inference_steps controls quality/cost trade-off (more steps = slower, often better)
    """
    g = torch.Generator(device=device).manual_seed(seed)

    t0 = time.perf_counter()
    out = pipe(
        batch_size=batch_size,
        num_inference_steps=num_inference_steps,
        generator=g
    )
    dt = time.perf_counter() - t0

    return out.images, dt

# =========================
# A) Base generation
# =========================
images, dt = generate_batch(seed=42, batch_size=8, num_inference_steps=50)
print(f"Generated 8 images in {dt:.2f}s with steps=50, seed=42")
make_grid(images, nrow=4)

# =========================
# B) Adjust generation parameters (steps)
# Compare: 10 vs 25 vs 50 vs 100 steps
# =========================
steps_list = [10, 25, 50, 100]
all_rows = []
timings = []

for steps in steps_list:
    imgs, t = generate_batch(seed=42, batch_size=8, num_inference_steps=steps)
    all_rows.append(imgs)
    timings.append((steps, t))

print("\nTiming by steps:")
for steps, t in timings:
    print(f"  steps={steps:3d} -> {t:.2f}s")

# Show 1 grid per steps
for steps, imgs in zip(steps_list, all_rows):
    print(f"\nResults with num_inference_steps={steps}")
    make_grid(imgs, nrow=4)

# =========================
# C) Diversity experiment (change seeds)
# Keep steps fixed, vary seed
# =========================
fixed_steps = 50
seeds = [0, 1, 2, 3]
diverse_imgs = []
diverse_times = []

for s in seeds:
    imgs, t = generate_batch(seed=s, batch_size=4, num_inference_steps=fixed_steps)
    diverse_imgs.extend(imgs)
    diverse_times.append((s, t))

print("\nDiversity timings (4 images each):")
for s, t in diverse_times:
    print(f"  seed={s} -> {t:.2f}s (steps={fixed_steps})")

print("\nDiversity samples (different seeds, same steps):")
make_grid(diverse_imgs, nrow=4)
