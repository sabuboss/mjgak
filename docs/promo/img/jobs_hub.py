# 대학별 면접 글 모음(허브) 썸네일. python jobs_hub.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, make_thumb

make_thumb(HERE / "thumb-hub.png", "대학별 면접", line2="면접일 순 21개 대학", line3="글 모음 · 목차")
