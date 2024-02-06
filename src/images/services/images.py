from pydicom import dcmread
import os
from typing import Callable
from images.services.exceptions import ImageNotFoundException
from shared.settings import Settings
from shared.logging import get_logger, Logger

settings = Settings()

def get_patient_name(path: str, logger: Logger = get_logger()) -> str:
    try: 
        patient_name = str(dcmread(path).PatientName)

        logger.log(f'Image in {path} was accessed succesfully and the patient name was retrieved')
        return patient_name
    except Exception as error:
        logger.error(f'Failed to access image in {path} or its patient name: {error}')
        raise ImageNotFoundException()
   

def get_image_pixel_array(path: str, logger: Logger = get_logger()):
    try:
        pixel_array = dcmread(path).pixel_array.tolist()

        logger.log(f'Image in {path} was accessed succesfully and the image pixel data was retrieved')
        return pixel_array
    except Exception as error:
        logger.error(f'Failed to access image in {path} or its patient name: {error}')
        raise ImageNotFoundException()

## This assumes that the name of the slices follows the proper slice number.
## Accounting for potential mismatches there would require either a different function or renaming the files according to the slice number when uploaded
def get_image_dir_by_position(position_getter: Callable[[int], int], logger: Logger = get_logger()):
    image_set_folders = os.listdir(settings.image_db_directory)

    if (not image_set_folders) | len(image_set_folders) == 0:
        logger.error(f'Failed to access the image db directory {settings.image_db_directory} or it was empty')
        raise ImageNotFoundException()
    
    image_folder_dir = f'{settings.image_db_directory}/{image_set_folders[0]}'
    sorted_image_folders = sorted(os.listdir(image_folder_dir))
 
    if len(sorted_image_folders) == 0:
        logger.error(f'Failed to find images in the requested image folder {image_folder_dir}')
        raise ImageNotFoundException()
    
    ## If the number of slices is even, it rounds up (would take the 3rd out of 4)
    file_name = sorted_image_folders[position_getter(len(sorted_image_folders))]
    image_dir = f'{image_folder_dir}/{file_name}'

    logger.info(f'Retrieved the image directory {image_dir}')
    return image_dir

def get_first_image_dir():
    def return_first(length: int):
        return 0

    return get_image_dir_by_position(return_first)

def get_middle_image_dir():
    def return_middle(length: int):
        return length//2
    return get_image_dir_by_position(return_middle)
