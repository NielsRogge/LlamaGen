import argparse
from huggingface_hub import hf_hub_download
import torch
from tokenizer.tokenizer_image.vq_model import VQ_models


model2ckpt = {
    "GPT-XL": ("vq_ds16_c2i.pt", "c2i_XL_384.pt", 384),
    "GPT-B": ("vq_ds16_c2i.pt", "c2i_B_256.pt", 256),
}

def load_model(args):
    ckpt_folder = "./"
    vq_ckpt, gpt_ckpt, _ = model2ckpt[args.gpt_model]
    hf_hub_download(repo_id="FoundationVision/LlamaGen", filename=vq_ckpt, local_dir=ckpt_folder)
    hf_hub_download(repo_id="FoundationVision/LlamaGen", filename=gpt_ckpt, local_dir=ckpt_folder)
    # create and load model
    vq_model = VQ_models[args.vq_model](
        codebook_size=args.codebook_size,
        codebook_embed_dim=args.codebook_embed_dim)
    vq_model.eval()
    checkpoint = torch.load(f"{ckpt_folder}{vq_ckpt}", map_location="cpu")
    vq_model.load_state_dict(checkpoint["model"])
    del checkpoint
    print(f"image tokenizer is loaded")
    return vq_model




parser = argparse.ArgumentParser()
parser.add_argument("--gpt-model", type=str, default="GPT-XL")
parser.add_argument("--vq-model", type=str, choices=list(VQ_models.keys()), default="VQ-16")
parser.add_argument("--codebook-size", type=int, default=16384, help="codebook size for vector quantization")
parser.add_argument("--codebook-embed-dim", type=int, default=8, help="codebook dimension for vector quantization")
args = parser.parse_args()

vq_model = load_model(args)
vq_model.push_to_hub("nielsr/vq-ds16-c2i")