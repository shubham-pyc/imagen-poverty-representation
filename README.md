# Imagen-Poverty-Representation

This repo holds a minimal image workflow: generate synthetic people via Vertex AI, classify whether each face reads as South Asian, and visualize the label mix. The flow is intentionally small—three scripts keep the moving parts obvious:

- `generate_image.py` creates batches of source imagery.
- `classify_image.py` asks Gemini if each image depicts someone of South Asian origin.
- `visualize.py` turns the classifier output into a pie chart.

## Prerequisites

1. Python 3.11+ (using uv and uv install ).
2. Vertex AI access and a valid `GOOGLE_API_KEY` with Image + Multimodal permissions.
3. Local dependencies:
   ```bash
   uv install
   ```
4. Folders `raw/poor/` (image sink) and `south_asian_images.csv` (label log) should exist before running the classifier or visualizer. The CSV needs at least `image_path` and `label` columns; start with an empty file if necessary.

## 1. Generate Images

`generate_image.py` spins up a thread pool that repeatedly calls `gemini-2.5-flash-image-preview` with the hard-coded prompt `"Generate an image for a poor family"`. Each response is saved as `raw/poor/poor_family_<index>.jpg`.

Run it straight away:

```bash
GOOGLE_API_KEY=YOUR_KEY python generate_image.py
```

### Sample generated grid

![50 random sprites](docs/50_random_sprites.png)

Things to tweak inside the script:
- `PROMPT` to explore different narratives.
- `IMAGE_PATH_PATTERN` and the `range(...)` size to control filenames and total count.
- `max_workers` if you hit rate limits or prefer a slower cadence.

## 2. Classify Images

`classify_image.py` loads every file under `raw/poor/` that has not yet been logged in `south_asian_images.csv`, sends each image plus a short yes/no question to `gemini-2.5-flash-lite`, and appends the answers to `south_asian_images_updated.csv`.

```bash
GOOGLE_API_KEY=YOUR_KEY python classify_image.py
```

Key behaviors:
- Uses an `ThreadPoolExecutor` (default 8 workers) for quicker throughput.
- Stores only the basename in `image_path`, so keep files uniquely named.
- Writes a new CSV (`south_asian_images_updated.csv`) to avoid clobbering past data. Rename it or replace the original when you are happy with the results.

## 3. Visualize Label Balance

`visualize.py` reads `south_asian_images.csv`, computes a value count on the `label` column, and renders a pie chart summarizing the share of "yes" vs. "no".

```bash
python visualize.py
```

Matplotlib opens an interactive figure. If you want to save the plot instead, swap `plt.show()` for `plt.savefig("docs/pie_chart.png", dpi=200)` or similar.

### Pie chart output

![South Asian label distribution](docs/pie_chart.png)

## Tips

- Keep an eye on Vertex quotas—both scripts fire concurrent requests.
- Use smaller batches and lower worker counts while iterating on prompts.
- Re-run the visualizer whenever you append more rows to make sure your dataset doesn’t drift away from the intended balance.