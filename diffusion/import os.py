import os
import time
import torch
import pandas as pd
from diffusers import DDPMPipeline

# =============================
# CONFIG
# =============================
OUTPUT_DIR = "outputs_diffusion"
os.makedirs(OUTPUT_DIR, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "google/ddpm-cifar10-32"

pipe = DDPMPipeline.from_pretrained(model_id).to(device)

# =============================
# FUNCTION: generate + export
# =============================
def generate_and_save(seed, steps, batch_size=8):
    generator = torch.Generator(device=device).manual_seed(seed)

    start = time.perf_counter()
    result = pipe(
        batch_size=batch_size,
        num_inference_steps=steps,
        generator=generator
    )
    elapsed = time.perf_counter() - start

    run_id = f"seed{seed}_steps{steps}"
    run_dir = os.path.join(OUTPUT_DIR, run_id)
    os.makedirs(run_dir, exist_ok=True)

    for i, img in enumerate(result.images):
        img.save(os.path.join(run_dir, f"img_{i}.png"))

    return {
        "seed": seed,
        "steps": steps,
        "batch_size": batch_size,
        "time_sec": round(elapsed, 3),
        "device": device
    }

# =============================
# RUN EXPORT EXPERIMENTS
# =============================
records = []

experiments = [
    (42, 10),
    (42, 25),
    (42, 50),
    (42, 100),
    (1, 50),
    (2, 50),
]

for seed, steps in experiments:
    print(f"Running seed={seed}, steps={steps}")
    rec = generate_and_save(seed, steps)
    records.append(rec)

df = pd.DataFrame(records)
df.to_csv(os.path.join(OUTPUT_DIR, "generation_metrics.csv"), index=False)
df.to_excel(os.path.join(OUTPUT_DIR, "generation_metrics.xlsx"), index=False)

print("\nDONE. Results saved to outputs_diffusion/")
print(df)
