from __future__ import annotations

from base64 import b64decode
import logging

import cv2
import numpy as np


logger = logging.getLogger(__name__)


class ImageDecoder:
    def decode_image(self, image_base64: str):
        try:
            image_bytes = b64decode(image_base64)
        except Exception:
            logger.warning("Failed to decode base64 image payload.")
            return None

        buffer = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        if image is None:
            logger.warning("OpenCV failed to decode the uploaded image.")
        return image


class TagImageExtractor:
    def extract_tag_regions(self, image) -> list:
        height, width = image.shape[0], image.shape[1]
        new_width = int(width / height * 1080)
        resized = cv2.resize(image, (new_width, 1080))

        offset = int(new_width / 20)
        y1 = int(new_width / 2 * 1 / 2) - offset
        y2 = new_width - y1 - offset
        cropped = resized[270:810, y1:y2]

        gray_image = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 80, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        tag_contours = []
        for contour in contours:
            length = cv2.arcLength(contour, True)
            area = cv2.contourArea(contour)
            contour = cv2.approxPolyDP(contour, 0.025 * length, True)
            if len(contour) == 4 and cv2.isContourConvex(contour) and area > 7000:
                tag_contours.append(contour)

        tags: list = []
        for contour in tag_contours[4::-1]:
            x, y, w, h = cv2.boundingRect(contour)
            tags.append(cropped[y : y + h, x : x + w])

        return tags


class TagImagePreprocessor:
    def preprocess_tag_image(self, image):
        normalized = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        normalized = cv2.resize(normalized, (320, 100))

        gray_image = cv2.cvtColor(normalized, cv2.COLOR_BGR2GRAY)
        _, binary_white = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)
        _, binary_foreground = cv2.threshold(gray_image, 120, 255, cv2.THRESH_TOZERO)

        kernel = np.ones((1, 11), np.uint8)
        dilation = cv2.dilate(binary_white, kernel, iterations=1)
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            logger.warning("No OCR text area contour detected.")
            return binary_foreground

        text_area = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(text_area)

        box = cv2.boxPoints(rect)
        box = np.intp(box)
        stencil = np.zeros(binary_foreground.shape).astype(binary_foreground.dtype)
        cv2.fillPoly(stencil, [box], 255)
        return cv2.bitwise_and(binary_foreground, stencil)
