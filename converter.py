import os
import glob
import sys
from io import StringIO
from functools import partial
from copy import deepcopy

import fitz
from PIL import Image
from pipeline import Pipeline
from pipeline.decorators import coroutine
from pipeline.utils import StopPipeline

from imgproc import soura_handler, ayat_handler, layout_handler, DATA_DIRECTORY
from datatypes import PipelineItem
from formats import fitz2numpy, numpy2fitz, fitz2pil, pil2fitz

def generate_pages(source_doc, distination_doc):
    index = 0
    for page in source_doc:
        pix = page.getPixmap(alpha = False)
        orig_image = fitz2pil(pix)
        modified_image = orig_image.copy()
        yield PipelineItem(orig_image=orig_image, index=index, modified_image=modified_image, distination_doc=distination_doc)
        index +=1 

def pipeline_driver(page_generator):
    try:
        return next(page_generator), page_generator
    except:
        raise StopPipeline("file ended")


def pipeline_validator(pipeline_item: PipelineItem):
    '''
    return False for pages that should not be processed, else return True
    '''
    if pipeline_item.index > 4 and pipeline_item.index < 607:
        return True
    else:
        return False


def pipeline_consumer(pipeline_item: PipelineItem):
    image = pil2fitz(pipeline_item.modified_image)
    page = pipeline_item.distination_doc.newPage(pipeline_item.index, width=image.width, height=image.height)
    page.insertImage(image.irect, pixmap=image, overlay=True)
    return


def main(input_file_path,output_file_path):
    source_doc = fitz.open(input_file_path)
    distination_doc = fitz.open()

    pre_processed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "pre-processed"))
    for filename in sorted(glob.glob(pre_processed_dir+"/*.jpg", recursive=False)):
        image = fitz.Pixmap(filename)
        page = distination_doc.newPage(width=image.width, height=image.height)
        page.insertImage(image.irect, pixmap=image, overlay=True)


    image_processor = Pipeline(
        producer_func=pipeline_driver,
        stages=[layout_handler, ayat_handler, soura_handler],
        consumer_func=pipeline_consumer,
        validator=pipeline_validator
        )
    image_processor.follow(generate_pages(source_doc, distination_doc))
    distination_doc.save(output_file_path)
    print('success')


if __name__ == '__main__':
    try:
        input_file_path = sys.argv[1]
    except IndexError:
        print("please enter the pdf file path")
        input_file_path = input()

    output_file_path = input_file_path.split('/')
    output_file_path[-1] = "output_" + output_file_path[-1]
    output_file_path = '/'.join(output_file_path)
    
    
    main(input_file_path, output_file_path)
