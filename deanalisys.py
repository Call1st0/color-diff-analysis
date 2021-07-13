""" script for calculating mean color difference between two images
        author: Ante Poljicak
        email: ante.poljicak@gmail.com
        version: 0.2 
        date: 13.7.2021
"""

# NOTE directory structure should be the same as stucture of the original dir

# Needed imports
from skimage import io, color
import numpy as np
import pandas as pd
import os

# read directory
root = "slike"

# original directory
dir_original = "slike/ORIGINAL"
dirlist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
print(dirlist)

# Open excel file for writing
with pd.ExcelWriter("rezultati.xlsx") as writer:

    for dir_num in range(25):  # Number of directories with images
        # set current dir
        current_dir = os.path.abspath(root + "/" + dirlist[dir_num])
        print(os.path.abspath(current_dir))
        print(os.path.abspath(dir_original))

        orig_file_list = [
            item
            for item in os.listdir(dir_original)
            if os.path.isfile(os.path.join(dir_original, item))
        ]
        # print(orig_file_list)

        img_file_list = [
            item
            for item in os.listdir(current_dir)
            if os.path.isfile(os.path.join(current_dir, item))
        ]
        # print(img_file_list)

        def compare_images(str_img_orig, str_img_edit):
            arr_results = np.zeros(7)
            # read images
            im_orig = io.imread(str_img_orig)
            im_edit = io.imread(str_img_edit)

            # convert to lab
            lab_orig = color.rgb2lab(im_orig)
            lab_edit = color.rgb2lab(im_edit)
            lch_orig = color.lab2lch(lab_orig)
            lch_edit = color.lab2lch(lab_edit)

            # calculate difference
            de_diff = color.deltaE_cie76(lab_orig, lab_edit)
            de2000_diff = color.deltaE_ciede2000(lab_orig, lab_edit)
            lab_diff = lab_orig - lab_edit
            chroma_diff = lch_orig[:, :, 1] - lch_edit[:, :, 1]
            hue_diff = lch_orig[:, :, 2] - lch_edit[:, :, 2]

            # mean values
            arr_results[0] = np.mean(de_diff)  # de76 difference
            arr_results[1] = np.mean(de2000_diff)  # de76 difference
            arr_results[2] = np.mean(lab_diff[:, :, 0])  # L difference
            arr_results[3] = np.mean(lab_diff[:, :, 1])  # a difference
            arr_results[4] = np.mean(lab_diff[:, :, 2])  # b difference
            arr_results[5] = np.mean(chroma_diff)  # Croma difference
            arr_results[6] = np.mean(hue_diff)  # Hue difference
            print(arr_results)
            return arr_results

        all_result = np.empty((1, 7))
        # print(all_result)

        for img_num in range(14):  # num of images
            print(orig_file_list[img_num])
            print(img_file_list[img_num])

            # add path
            orig_img = os.path.join(dir_original, orig_file_list[img_num])
            edit_img = os.path.join(current_dir, img_file_list[img_num])
            temp_result = compare_images(orig_img, edit_img)
            # temp_result.reshape(1,4)
            all_result = np.vstack((all_result, temp_result))

        # #add to datafram
        # all_result.reshape(13,4)
        all_result = np.delete(all_result, obj=0, axis=0)
        # print(all_result)

        # create dataframe
        metrics = ["dE", "dE2000", "dL", "da", "db", "dC", "dH"]
        df = pd.DataFrame(all_result.tolist(), index=orig_file_list, columns=metrics)
        print(df)

        df.to_excel(writer, sheet_name=dirlist[dir_num])

