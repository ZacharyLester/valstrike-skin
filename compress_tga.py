from PIL import Image
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

exts = {".bmp", ".tga"}

files = [f for f in ROOT.rglob("*") if f.suffix.lower() in exts]

if not files:
	print("No BMP/TGA files found.")
	sys.exit(0)

print(f"Found {len(files)} file(s)...\n")

total_before = 0
total_after = 0

for src in files:
	try:
		before = src.stat().st_size
		img = Image.open(src)

		if src.suffix.lower() == ".bmp":
			# BMP has no compression — save as compressed BMP (limited gain)
			# Best option: re-save, Pillow will strip unused metadata
			img.save(src, format="BMP")
		elif src.suffix.lower() == ".tga":
			# TGA supports RLE compression
			img.save(src, format="TGA", compression="tga_rle")

		img.close()

		after = src.stat().st_size
		total_before += before
		total_after += after

		diff = before - after
		saved = 100 - after * 100 // before if before else 0
		print(f"  {src}  {before//1024}KB → {after//1024}KB  (-{saved}%)")

	except Exception as e:
		print(f"  SKIP {src}: {e}")

if total_before:
	print(f"\nDone. Total: {total_before//1024}KB → {total_after//1024}KB "
	      f"({100 - total_after*100//total_before}% saved)")