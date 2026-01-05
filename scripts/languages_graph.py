import json
import math
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    data_path = Path("assets/languages.json")
    out_path = Path("assets/languages.png")
    plt.savefig(out_path, dpi=150)

    data = json.loads(data_path.read_text(encoding="utf-8"))

    # data is dict: language -> bytes
    items = sorted(data.items(), key=lambda x: x[1], reverse=True)

    # Keep top N languages, group the rest into "Other"
    TOP_N = 10
    top = items[:TOP_N]
    rest = items[TOP_N:]
    other_bytes = sum(v for _, v in rest)

    labels = [k for k, _ in top]
    values = [v for _, v in top]
    if other_bytes > 0:
        labels.append("Other")
        values.append(other_bytes)

    total = sum(values)
    if total == 0:
        raise SystemExit("No language data to plot (total bytes is 0).")

    # Make a simple horizontal bar chart (readable in README)
    # No hardcoded colors needed: matplotlib will auto-color each bar.
    plt.figure(figsize=(10, 6))
    y = list(range(len(labels)))[::-1]
    labels_rev = labels[::-1]
    values_rev = values[::-1]

    plt.barh(y, values_rev)
    plt.yticks(y, labels_rev)

    # Show percentages on the right of bars
    for yi, v in zip(y, values_rev):
        pct = (v / total) * 100
        plt.text(v * 1.01, yi, f"{pct:.1f}%", va="center", fontsize=9)

    plt.xlabel("Bytes (GitHub Linguist)")
    plt.title("Languages (overall across repositories)")
    plt.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
