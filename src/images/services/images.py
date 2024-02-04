from pydicom import dcmread
import os
from typing import Callable
from images.services.exceptions import ImageNotFoundException
from shared.settings import Settings

settings = Settings()

def get_patient_name(path: str) -> str:
    try: 
        return str(dcmread(path).PatientName)
    except:
        raise ImageNotFoundException()
   

def get_image_pixel_array(path: str):
    try:
        return dcmread(path).pixel_array.tolist()
    except Exception:
        raise ImageNotFoundException()

## This assumes that the name of the slices follows the proper slice number.
## Accounting for potential mismatches there would require either a different function or renaming the files according to the slice number when uploaded
def get_image_dir_by_position(position_getter: Callable[[int], int]):
    folders = os.listdir(settings.image_db_directory)

    if not folders:
        raise ImageNotFoundException()
    
    folder_name = folders[0]
    sorted_files = sorted(os.listdir(f'{settings.image_db_directory}/{folder_name}'))

    ## If the number of slices is even, it rounds up (would take the 3rd out of 4)
    try:
        file_name = sorted_files[position_getter(len(sorted_files))] 
    except:
        raise ImageNotFoundException()
    
    return f'{settings.image_db_directory}/{folder_name}/{file_name}'

def get_first_image_dir():
    def return_first(length: int):
        return 0

    return get_image_dir_by_position(return_first)

def get_middle_image_dir():
    def return_middle(length: int):
        return length//2
    return get_image_dir_by_position(return_middle)
