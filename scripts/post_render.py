"""Move the rendered deck to docs/index.html for GitHub Pages and add .nojekyll."""
import pathlib, shutil

docs = pathlib.Path("docs")
deck = docs / "products" / "folien" / "index.html"
if deck.exists():
    shutil.move(str(deck), docs / "index.html")
    shutil.rmtree(docs / "products")
(docs / ".nojekyll").touch()
