import fitz
from PIL import Image
from dataclasses import dataclass
from numpy import ndarray

@dataclass
class PipelineItem:
    orig_image : ndarray
    index : int
    modified_image: ndarray
    distination_doc: fitz.Document