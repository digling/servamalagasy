from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import Language, FormSpec
from pylexibank import progressbar

from clldutils.misc import slug
import attr
