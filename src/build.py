"""CLI entry point: build the blood-report visualization."""

from .html_builder import build


def main() -> None:
    out = build()
    print(f"Visualization written to: {out}")
    print("Open it in a browser to view.")


if __name__ == "__main__":
    main()
