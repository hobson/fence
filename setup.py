# setup.py for Fence
from distutils.core import setup
import os

VERSION = '0.0.2'
setup(
    name = "fence",
    # packages = ["fence"],
    version = "0.0.2",
    description = "BitCoin trending and trading bot",
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    author = "Hobson Lane",
    author_email = "hobson@totalgood.com",
    url = "http://github/hobsonlane.com/fence/",
    # download_url = "https://github.com/hobsonlane.com/fence/archive/v%s.tar.gz" % VERSION,
    keywords = ["bitcoin", "agent", "bot", "ai", "finance", "trend", "trade"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        # "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Office/Business :: Financial :: Investment",
        ],
)
