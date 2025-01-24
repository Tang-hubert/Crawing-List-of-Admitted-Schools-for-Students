# --- START OF FILE get_side_rank.py ---
import glob
from pathlib import Path
from bs4 import BeautifulSoup
import base64
import pandas as pd
from pytesseract import pytesseract
from PIL import Image
import cv2
import numpy as np

class SideRankProcessor:
    def __init__(self, input_dir, result_dir, tesseract_path):
        self.input_dir = Path(input_dir)
        self.result_dir = Path(result_dir)
        self.result_dir.mkdir(parents=True, exist_ok=True)
        pytesseract.tesseract_cmd = Path(tesseract_path)

    def thresholding_(self, png):
        image = cv2.imread(png)
        gray = self.get_grayscale(image)
        thresh_ = self.thresholding(gray)
        return thresh_

    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def thresholding(self, image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def img_detect(self, item_scope2, img, language, oem_psm):
        try:
            base64_str = item_scope2.find_all('img')[0]['src'].split(',')[1]
        except IndexError:
            return "None"
        else:
            with open(img, "wb") as fh:
                fh.write(base64.decodebytes(bytes(base64_str, 'utf-8')))
            path_to_image = img
            cv2.imwrite(img, self.thresholding_(path_to_image))
            return pytesseract.image_to_string(Image.open(path_to_image), lang=language, config=oem_psm)

    def img_detect_crop(self, img_, i):
        basic_width = 4
        digit_width = 9
        crop_initial = digit_width * (i - 1) + basic_width
        crop_end = digit_width * i + basic_width
        crop_img = img_[0: 20, crop_initial:crop_end]
        cv2.imwrite(f'data/crop_img{i}.png', crop_img)
        image = f'data/crop_img{i}.png'
        path_to_image = image
        cv2.imwrite(f'data/crop_img{i}.png', self.thresholding_(image))
        return pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

    def dept_img_detect_crop(self, img, i):
        basic_width = 48
        digit_width = 28
        crop_initial = digit_width * (i - 1) + basic_width
        crop_end = digit_width * i + basic_width
        crop_img = img[0: 48, crop_initial:crop_end]
        cv2.imwrite(f'data/dept_crop_img{i}.png', crop_img)
        image = f'data/dept_crop_img{i}.png'
        path_to_image = image
        cv2.imwrite(f'data/dept_crop_img{i}.png', self.thresholding_(image))
        return pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

    def processing_list(self, univ, year, color_list, df, department_name, select, dept_rank):
        rank = ''
        stuno = ''
        print(univ)
        for item in color_list:
            color_list_item_scope1 = item.children
            count_item = 0
            exam_location = ""
            for item_scope2 in color_list_item_scope1:
                if count_item == 3:
                    try:
                        base64_str = item.find_all('img')[0]['src'].split(',')[1]
                    except IndexError:
                        rank = "None"
                    else:
                        rank = ''
                        img_chi = ''
                        img_digit = ''
                        img_digit_2 = ''
                        img_digit_3 = ''
                        with open(r'data/rank.png', "wb") as fh:
                            fh.write(base64.decodebytes(bytes(base64_str, 'utf-8')))

                        img_dept_rank_crop = cv2.imread(r'data/rank.png')
                        if img_dept_rank_crop.shape[0] < 51:
                            if img_dept_rank_crop.shape[1] < 100:
                                # only one digit
                                crop_img_chi = img_dept_rank_crop[0: 48, 0:48]
                                cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                path_to_image = f'data/dept_crop_img_chi.png'
                                cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                # first digit
                                crop_img_digit = img_dept_rank_crop[0:48, 48:76]
                                cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit.png'
                                cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                img_chi = img_chi.strip()
                                img_digit = img_digit.strip()
                                rank = f'{img_chi}{img_digit}'

                            elif 100 < img_dept_rank_crop.shape[1] < 120:
                                # two digits
                                crop_img_chi = img_dept_rank_crop[0: 48, 0:48]
                                cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                path_to_image = f'data/dept_crop_img_chi.png'
                                cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                # first digit
                                crop_img_digit = img_dept_rank_crop[0:48, 48:76]
                                cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit.png'
                                cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                # second digit
                                crop_img_digit = img_dept_rank_crop[0:48, 76:104]
                                cv2.imwrite(f'data/dept_crop_img_digit_2.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit_2.png'
                                cv2.imwrite(f'data/dept_crop_img_digit_2.png', self.thresholding_(path_to_image))
                                img_digit_2 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                img_chi = img_chi.strip()
                                img_digit = img_digit.strip()
                                img_digit_2 = img_digit_2.strip()
                                rank = f'{img_chi}{img_digit}{img_digit_2}'

                            elif img_dept_rank_crop.shape[1] > 120:
                                # three digits
                                crop_img_chi = img_dept_rank_crop[0: 48, 0:48]
                                cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                path_to_image = f'data/dept_crop_img_chi.png'
                                cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                # first digit
                                crop_img_digit = img_dept_rank_crop[0:48, 48:76]
                                cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit.png'
                                cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                # second digit
                                crop_img_digit = img_dept_rank_crop[0:48, 76:104]
                                cv2.imwrite(f'data/dept_crop_img_digit_2.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit_2.png'
                                cv2.imwrite(f'data/dept_crop_img_digit_2.png', self.thresholding_(path_to_image))
                                img_digit_2 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                # third digit
                                crop_img_digit = img_dept_rank_crop[0:48, 104:132]
                                cv2.imwrite(f'data/dept_crop_img_digit_3.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit_3.png'
                                cv2.imwrite(f'data/dept_crop_img_digit_3.png', self.thresholding_(path_to_image))
                                img_digit_3 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                img_chi = img_chi.strip()
                                img_digit = img_digit.strip()
                                img_digit_2 = img_digit_2.strip()
                                img_digit_3 = img_digit_3.strip()
                                rank = f'{img_chi}{img_digit}{img_digit_2}{img_digit_3}'

                        elif img_dept_rank_crop.shape[0] > 51:
                            if img_dept_rank_crop.shape[1] < 100:
                                # only one digit
                                crop_img_chi = img_dept_rank_crop[0: 52, 0:48]
                                cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                path_to_image = f'data/dept_crop_img_chi.png'
                                cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                # first digit
                                crop_img_digit = img_dept_rank_crop[0:52, 48:76]
                                cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit.png'
                                cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                img_chi = img_chi.strip()
                                img_digit = img_digit.strip()
                                rank = f'{img_chi}{img_digit}'

                            elif 100 < img_dept_rank_crop.shape[1] < 120:
                                # two digits
                                crop_img_chi = img_dept_rank_crop[0: 52, 0:48]
                                cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                path_to_image = f'data/dept_crop_img_chi.png'
                                cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                # first digit
                                crop_img_digit = img_dept_rank_crop[0:52, 48:76]
                                cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit.png'
                                cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                # second digit
                                crop_img_digit = img_dept_rank_crop[0:52, 76:104]
                                cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit_2.png'
                                cv2.imwrite(f'data/dept_crop_img_digi_2t.png', self.thresholding_(path_to_image))
                                img_digit_2 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                img_chi = img_chi.strip()
                                img_digit = img_digit.strip()
                                img_digit_2 = img_digit_2.strip()
                                rank = f'{img_chi}{img_digit}{img_digit_2}'

                            elif img_dept_rank_crop.shape[1] > 120:
                                # three digits
                                crop_img_chi = img_dept_rank_crop[0: 52, 0:48]
                                cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                path_to_image = f'data/dept_crop_img_chi.png'
                                cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                # first digit
                                crop_img_digit = img_dept_rank_crop[0:52, 48:76]
                                cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit.png'
                                cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                # second digit
                                crop_img_digit = img_dept_rank_crop[0:52, 76:104]
                                cv2.imwrite(f'data/dept_crop_img_digit_2.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit_2.png'
                                cv2.imwrite(f'data/dept_crop_img_digit_2.png', self.thresholding_(path_to_image))
                                img_digit_2 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                # third digit
                                crop_img_digit = img_dept_rank_crop[0:52, 104:132]
                                cv2.imwrite(f'data/dept_crop_img_digit_3.png', crop_img_digit)
                                path_to_image = f'data/dept_crop_img_digit_3.png'
                                cv2.imwrite(f'data/dept_crop_img_digit_3.png', self.thresholding_(path_to_image))
                                img_digit_3 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                img_chi = img_chi.strip()
                                img_digit = img_digit.strip()
                                img_digit_2 = img_digit_2.strip()
                                img_digit_3 = img_digit_3.strip()
                                rank = f'{img_chi}{img_digit}{img_digit_2}{img_digit_3}'

                elif count_item == 5:
                    stuno = 'temp'
                    x = item.find_all('a')
                    exam_location = x[0].text[6:-1]
                elif count_item == 9:
                    tr_scope3 = item_scope2.find_all('tr')
                    department_name_list = []
                    select_list = []
                    dept_rank_list = []
                    for item_scope4 in tr_scope3:
                        count_item_scope5 = 0
                        for item_scope5 in item_scope4:
                            if count_item_scope5 == 1:
                                img_tag = item_scope5.find('img')
                                if img_tag is not None:
                                    img_tag_ = True
                                else:
                                    img_tag_ = False
                                select_list.append(img_tag_)

                            elif count_item_scope5 == 3:
                                if item_scope5.text != "":
                                    department_name_list.append(item_scope5.text)
                                else:
                                    department_name_list.append(np.nan)

                            elif count_item_scope5 == 5:
                                try:
                                    base64_str = item_scope5.find_all('img')[0]['src'].split(',')[1]
                                except IndexError:
                                    dept_rank_list.append("None")
                                else:

                                    dept_rank_whole = ''
                                    img_chi = ''
                                    img_digit = ''
                                    img_digit_2 = ''
                                    img_digit_3 = ''
                                    with open(r'data/dept_rank_crop.png', "wb") as fh:
                                        fh.write(base64.decodebytes(bytes(base64_str, 'utf-8')))

                                    img_dept_rank_crop = cv2.imread(r'data/dept_rank_crop.png')
                                    if img_dept_rank_crop.shape[0] < 51:
                                        if img_dept_rank_crop.shape[1] < 100:
                                            # only one digit
                                            crop_img_chi = img_dept_rank_crop[0: 48, 0:48]
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                            path_to_image = f'data/dept_crop_img_chi.png'
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                            img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_sim', config='--oem 0 --psm 7')

                                            # first digit
                                            crop_img_digit = img_dept_rank_crop[0:48, 48:76]
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                            img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            img_chi = img_chi.strip()
                                            img_digit = img_digit.strip()
                                            dept_rank_whole = f'{img_chi}{img_digit}'
                                            dept_rank_list.append(dept_rank_whole)

                                        elif 100 < img_dept_rank_crop.shape[1] < 120:
                                            # two digits
                                            crop_img_chi = img_dept_rank_crop[0: 48, 0:48]
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                            path_to_image = f'data/dept_crop_img_chi.png'
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                            img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_sim', config='--oem 0 --psm 7')

                                            # first digit
                                            crop_img_digit = img_dept_rank_crop[0:48, 48:76]
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                            img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            # second digit
                                            crop_img_digit = img_dept_rank_crop[0:48, 76:104]
                                            cv2.imwrite(f'data/dept_crop_img_digit_2.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit_2.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit_2.png', self.thresholding_(path_to_image))
                                            img_digit_2 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            img_chi = img_chi.strip()
                                            img_digit = img_digit.strip()
                                            img_digit_2 = img_digit_2.strip()
                                            dept_rank_whole = f'{img_chi}{img_digit}{img_digit_2}'
                                            dept_rank_list.append(dept_rank_whole)

                                        elif img_dept_rank_crop.shape[1] > 120:
                                            # three digits
                                            crop_img_chi = img_dept_rank_crop[0: 48, 0:48]
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                            path_to_image = f'data/dept_crop_img_chi.png'
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                            img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_sim', config='--oem 0 --psm 7')

                                            # first digit
                                            crop_img_digit = img_dept_rank_crop[0:48, 48:76]
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                            img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            # second digit
                                            crop_img_digit = img_dept_rank_crop[0:48, 76:104]
                                            cv2.imwrite(f'data/dept_crop_img_digit_2.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit_2.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit_2.png', self.thresholding_(path_to_image))
                                            img_digit_2 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            # third digit
                                            crop_img_digit = img_dept_rank_crop[0:48, 104:132]
                                            cv2.imwrite(f'data/dept_crop_img_digit_3.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit_3.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit_3.png', self.thresholding_(path_to_image))
                                            img_digit_3 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            img_chi = img_chi.strip()
                                            img_digit = img_digit.strip()
                                            img_digit_2 = img_digit_2.strip()
                                            img_digit_3 = img_digit_3.strip()
                                            dept_rank_whole = f'{img_chi}{img_digit}{img_digit_2}{img_digit_3}'
                                            dept_rank_list.append(dept_rank_whole)

                                    elif img_dept_rank_crop.shape[0] > 51:
                                        if img_dept_rank_crop.shape[1] < 100:
                                            # only one digit
                                            crop_img_chi = img_dept_rank_crop[0: 52, 0:48]
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                            path_to_image = f'data/dept_crop_img_chi.png'
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                            img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                            # first digit
                                            crop_img_digit = img_dept_rank_crop[0:52, 48:76]
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                            img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            img_chi = img_chi.strip()
                                            img_digit = img_digit.strip()
                                            dept_rank_whole = f'{img_chi}{img_digit}'
                                            dept_rank_list.append(dept_rank_whole)

                                        elif 100 < img_dept_rank_crop.shape[1] < 120:
                                            # two digits
                                            crop_img_chi = img_dept_rank_crop[0: 52, 0:48]
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                            path_to_image = f'data/dept_crop_img_chi.png'
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                            img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                            # first digit
                                            crop_img_digit = img_dept_rank_crop[0:52, 48:76]
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                            img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            # second digit
                                            crop_img_digit = img_dept_rank_crop[0:52, 76:104]
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit_2.png'
                                            cv2.imwrite(f'data/dept_crop_img_digi_2t.png', self.thresholding_(path_to_image))
                                            img_digit_2 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            img_chi = img_chi.strip()
                                            img_digit = img_digit.strip()
                                            img_digit_2 = img_digit_2.strip()
                                            dept_rank_whole = f'{img_chi}{img_digit}{img_digit_2}'
                                            dept_rank_list.append(dept_rank_whole)

                                        elif img_dept_rank_crop.shape[1] > 120:
                                            # three digits
                                            crop_img_chi = img_dept_rank_crop[0: 52, 0:48]
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', crop_img_chi)
                                            path_to_image = f'data/dept_crop_img_chi.png'
                                            cv2.imwrite(f'data/dept_crop_img_chi.png', self.thresholding_(path_to_image))
                                            img_chi = pytesseract.image_to_string(Image.open(path_to_image), lang='chi_tra', config='--oem 0 --psm 7')

                                            # first digit
                                            crop_img_digit = img_dept_rank_crop[0:52, 48:76]
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit.png', self.thresholding_(path_to_image))
                                            img_digit = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            # second digit
                                            crop_img_digit = img_dept_rank_crop[0:52, 76:104]
                                            cv2.imwrite(f'data/dept_crop_img_digit_2.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit_2.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit_2.png', self.thresholding_(path_to_image))
                                            img_digit_2 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            # third digit
                                            crop_img_digit = img_dept_rank_crop[0:52, 104:132]
                                            cv2.imwrite(f'data/dept_crop_img_digit_3.png', crop_img_digit)
                                            path_to_image = f'data/dept_crop_img_digit_3.png'
                                            cv2.imwrite(f'data/dept_crop_img_digit_3.png', self.thresholding_(path_to_image))
                                            img_digit_3 = pytesseract.image_to_string(Image.open(path_to_image), lang='eng', config='--oem 1 --psm 7')

                                            img_chi = img_chi.strip()
                                            img_digit = img_digit.strip()
                                            img_digit_2 = img_digit_2.strip()
                                            img_digit_3 = img_digit_3.strip()
                                            dept_rank_whole = f'{img_chi}{img_digit}{img_digit_2}{img_digit_3}'
                                            dept_rank_list.append(dept_rank_whole)
                            count_item_scope5 += 1
                    department_name.append(department_name_list)
                    select.append(select_list)
                    dept_rank.append(dept_rank_list)

                count_item += 1

        data = {'rank': rank, 'exam_location': exam_location, 'stuno': stuno, 'univ': univ, 'year': year,
                'department_name': department_name, 'dept_rank': dept_rank, 'select': select}
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        return df

    @staticmethod
    def cross_interleave(df1, df2):
        df = pd.DataFrame()
        max_len = max(len(df1), len(df2))
        for line in range(max_len):
            if line < len(df1):
                df = pd.concat([df, df1.iloc[[line]]], ignore_index=True)
            if line < len(df2):
                df = pd.concat([df, df2.iloc[[line]]], ignore_index=True)
        return df

    def processing_department(self, filename):
        filepath = self.input_dir / filename
        with open(filepath, 'r', encoding="utf-8") as file:
            html = file.read()
            soup = BeautifulSoup(html, 'html.parser')

        fields = ['rank', 'exam_location', 'stuno', 'univ', 'year', 'department_name', 'select', 'dept_rank']
        df = pd.DataFrame(columns=fields)
        df1 = pd.DataFrame(columns=fields)
        df2 = pd.DataFrame(columns=fields)

        department_name = []
        select = []
        dept_rank = []

        title_str = soup.head.find_all('title')[0].text
        year_pos = title_str.find('年')
        year = title_str[year_pos - 3:year_pos]

        univ_pos = title_str.find('-')
        univ = title_str[:univ_pos].rstrip()

        dark_list = soup.body.find_all(bgcolor="#DEDEDC")  # 褐色
        df1 = self.processing_list(univ, year, dark_list, df, department_name, select, dept_rank)

        white_list = soup.body.find_all(bgcolor="#FFFFFF")  # 白色
        df2 = self.processing_list(univ, year, white_list, df, department_name, select, dept_rank)

        df_interleaved = self.cross_interleave(df1, df2)

        df_exploded = df_interleaved.explode(['department_name', 'select', 'dept_rank']).reset_index(drop=True)
        df_cleaned = df_exploded.dropna()

        output_csv_path = self.result_dir / f'{univ}.csv'
        df_cleaned.to_csv(output_csv_path, encoding='utf-8-sig', index=False)
        print(f"Processed and saved: {output_csv_path}")


    def run(self):
        department_dir = self.input_dir
        for file in glob.iglob(str(department_dir / '*交叉查榜*.html')):
            self.processing_department(Path(file).name)


if __name__ == "__main__":
    input_directory = 'data/department'  # Replace with your input directory
    result_directory = 'result'  # Replace with your result directory
    tesseract_exe_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Replace with your Tesseract path

    processor = SideRankProcessor(input_directory, result_directory, tesseract_exe_path)
    processor.run()