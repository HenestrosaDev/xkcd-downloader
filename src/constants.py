import sys
from pathlib import Path

XKCD_URL = "https://xkcd.com/{}/info.0.json"
XKCD_IMAGE_URL = "https://imgs.xkcd.com/comics/"
XKCD_EXPLAIN_URL = "https://www.explainxkcd.com/wiki/index.php/{}"

XKCD_SUBDIRECTORY_NAMES = ["xkcd-vignettes", "xkcd-explanations"]
if getattr(sys, "frozen", False):
    # The script is frozen
    ROOT_PATH = Path(sys._MEIPASS)
else:
    ROOT_PATH = Path(__file__).parent.parent
