from fastapi import APIRouter, Depends
from images.services.images import (
    get_first_image_dir,
    get_patient_name,
    get_middle_image_dir,
    get_image_pixel_array,
)
from images.services.exceptions import ImageNotFoundException
from images.endpoints.schemas import (
    ImagePatientNameResponseBody,
    ImagePixelArrayResponseBody,
)
from shared.settings import Settings
from shared.endpoints.exceptions import (
    ResourceNotFoundHttpException,
    InternalServerHttpException,
)
from users.services.users import get_current_user

router = APIRouter(prefix="/images")
app_settings = Settings()


@router.get("/patient")
async def image_patient_name(
    user: str = Depends(get_current_user),
) -> ImagePatientNameResponseBody:
    try:
        patient_name = get_patient_name(get_first_image_dir())
        return ImagePatientNameResponseBody(name=patient_name)
    except ImageNotFoundException:
        raise ResourceNotFoundHttpException()
    except:
        raise InternalServerHttpException()


@router.get("/pixel-array")
async def image_pixel_array(
    user: str = Depends(get_current_user),
) -> ImagePixelArrayResponseBody:
    try:
        pixel_array = get_image_pixel_array(get_middle_image_dir())
        return ImagePixelArrayResponseBody(pixel_array=pixel_array)
    except ImageNotFoundException:
        raise ResourceNotFoundHttpException()
    except Exception:
        raise InternalServerHttpException()
