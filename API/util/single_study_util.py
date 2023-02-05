import numpy as np
import pydicom
import cv2
import torch
import util
import zipfile
import io
import os


async def dicom_2_npy(zipped_input_study):
    dcm_slices = []

    # convert UploadedFile to io.BytesIO
    input_zip_bytes = io.BytesIO(await zipped_input_study.read())

    zip_file = zipfile.ZipFile(input_zip_bytes)

    # extract all dicom files from zip
    zip_file.extractall()
    files = [f for f in zip_file.namelist() if f.endswith(".dcm")]

    if len(files) == 0:
        raise Exception("No dicom files in zip")

    # read in all dcm slices
    for dicom_file in files:
        try:
            dcm = pydicom.dcmread(dicom_file)
            # arr = dcm.pixel_array
        except:
            print("error reading dicom")
            continue
        # skip dicom types that we don't want
        # if dcm.SeriesDescription != series_description:
        #     continue
        dcm_slices.append(dcm)

    # check if dicoms are succesfully retrived
    if len(dcm_slices) == 0:
        raise Exception("no dicom files retrived")

    # sort slices
    # test using image patient location instead
    # dcm_slices_sorted = sorted(dcm_slices, key=lambda dcm: int(dcm.InstanceNumber))
    dcm_slices_sorted = sorted(
        dcm_slices, key=lambda dcm: int(dcm.ImagePositionPatient[-1]))
    # save as npy_volume
    npy_volume = np.array([dcm.pixel_array for dcm in dcm_slices_sorted])

    # reverse volumne if patient position defer from standard
    # test using image patient location instead
    # if dcm.PatientPosition == "FFS":
    #    npy_volume = npy_volume[::-1]

    # remove extracted files
    for f in files:
        os.remove(f)

    return npy_volume


def normalize(img):

    img = img.astype(np.float32)
    # img = (img - CONTRAST_HU_MIN) / (CONTRAST_HU_MAX - CONTRAST_HU_MIN)
    img = np.clip(img, 0., 1.)  # - CONTRAST_HU_MEAN
    return img


def format_img(img):
    """reshape, normalize image and convert to tensor"""

    num_slices = img.shape[0]
    num_windows = num_slices - 24 + 1

    # rescale
    interpolation = cv2.INTER_AREA
    img = util.resize_slice_wise(img, (208, 208), interpolation)

    # crop
    row = (img.shape[-2] - 192) // 2
    col = (img.shape[-1] - 192) // 2
    img = img[:, row: row + 192, col: col + 192]

    # noramlize Hounsfield Units
    img_normalized = normalize(img)

    # expand dimention for tensor
    img_split = np.array([img_normalized[i:i+24] for i in range(num_windows)])
    img_expand = [np.expand_dims(np.expand_dims(
        split, axis=0), axis=0) for split in img_split]

    # create torch tensor
    study_windows = [torch.from_numpy(np.array(window))
                     for window in img_expand]

    return study_windows
