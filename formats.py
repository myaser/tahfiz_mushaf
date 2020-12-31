from PIL import Image
from cv2 import cv2
import numpy
import fitz

def pil2cv(pil_im):
    cv_im = cv2.CreateImageHeader(pil_im.size, cv2.IPL_DEPTH_8U, 3)
    cv2.SetData(cv_im, pil_im.tostring())
    return cv_im


def pil2numpy(pil_im):
    num_im = numpy.array(pil_im)
    return num_im


def cv2pil(cv_im):
    pil_im = Image.fromstring("L", cv2.GetSize(cv_im), cv_im.tostring())
    return pil_im


def cv2numpy(cv_im):
    num_im = numpy.array(cv2pil(cv_im))
    return num_im


def numpy2cv(num_im):
    cv_im = cv2.fromarray(num_im)
    return cv_im


def numpy2pil(num_im):
    pil_im = Image.fromarray(num_im)
    return pil_im

def fitz2numpy(fitz_im: fitz.Pixmap):
    return numpy.array(fitz_im.samples)


def numpy2fitz(num_im: numpy.ndarray):
    return fitz.Pixmap(fitz.csRGB, num_im.width, num_im.height, bytearray(num_im.tostring()))

def fitz2pil(pix: fitz.Pixmap):
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

def pil2fitz(pil_img: Image):
    return fitz.Pixmap(fitz.csRGB, pil_img.size[0], pil_img.size[1], pil_img.tobytes())