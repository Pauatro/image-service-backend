from pydicom import dcmread
import os
from typing import Callable
from images.services.exceptions import ImageNotFoundException
from shared.settings import Settings
from shared.logging import get_logger, Logger


def get_patient_name(path: str, logger: Logger = get_logger()) -> str:
    try:
        patient_name = str(dcmread(path).PatientName)
        logger.info(
            f"Image in {path} was accessed successfully and the patient name was retrieved"
        )
        return patient_name
    except Exception as error:
        logger.error(f"Failed to access image in {path} or its patient name: {error}")
        raise ImageNotFoundException(error)


def get_image_pixel_array(path: str, logger: Logger = get_logger()):
    try:
        pixel_array = dcmread(path).pixel_array.tolist()

        logger.info(
            f"Image in {path} was accessed successfully and the image pixel data was retrieved"
        )
        return pixel_array
    except Exception as error:
        logger.error(f"Failed to access image in {path} or its pixel data: {error}")
        raise ImageNotFoundException()


## This assumes that the name of the slices follows the proper slice number.
## Accounting for potential mismatches there would require either a different function or renaming the files according to the slice number when uploaded
def get_image_dir_by_position(
    slice_position_getter: Callable[[int], int],
    folder_position: int = 0,
    db_dir=Settings().image_db_directory,
    logger: Logger = get_logger(),
):
    image_set_folders = os.listdir(db_dir)

    if not image_set_folders:
        logger.error(
            f"Failed to access the image db directory {db_dir} or it was empty"
        )
        raise ImageNotFoundException()

    image_folder_dir = f"{db_dir}/{image_set_folders[folder_position]}"
    sorted_image_folders = sorted(os.listdir(image_folder_dir))

    if not sorted_image_folders:
        logger.error(
            f"Failed to find images in the requested image folder {image_folder_dir}"
        )
        raise ImageNotFoundException()

    ## If the number of slices is even, it rounds up (would take the 3rd out of 4)
    file_name = sorted_image_folders[slice_position_getter(len(sorted_image_folders))]
    image_dir = f"{image_folder_dir}/{file_name}"

    logger.info(f"Retrieved the image directory {image_dir}")
    return image_dir


def get_first_image_dir():
    def return_first_position(image_set_length: int):
        return 0

    return get_image_dir_by_position(return_first_position)


def get_middle_image_dir():
    def return_middle_position(image_set_length: int):
        return image_set_length // 2

    return get_image_dir_by_position(return_middle_position)
