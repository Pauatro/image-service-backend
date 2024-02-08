import pytest
import images.services.images as services
import images.services.exceptions as exceptions

mock_image_db_dir = "src/tests/mocks/data/images_db"
mock_empty_image_db_dir = "src/tests/mocks/data/empty_images_db"
mock_first_set_folder_name = "SE000001"
mock_first_slice_name = "MR000001"


def test_get_image_dir_by_position_happy_path():

    def return_first_position(image_set_length: int):
        return 0

    path = services.get_image_dir_by_position(
        return_first_position, 0, mock_image_db_dir
    )

    assert (
        path
        == f"{mock_image_db_dir}/{mock_first_set_folder_name}/{mock_first_slice_name}"
    )

    def return_third_position(image_set_length: int):
        return 2

    path = services.get_image_dir_by_position(
        return_third_position, 0, mock_image_db_dir
    )

    assert path == f"{mock_image_db_dir}/{mock_first_set_folder_name}/MR000003"


def test_get_image_dir_by_position_failures():

    def return_first_position(image_set_length: int):
        return 0

    # Fails when the image db has not set folders
    with pytest.raises(exceptions.ImageNotFoundException):
        services.get_image_dir_by_position(
            return_first_position, 0, mock_empty_image_db_dir
        )

    # Fails when the set folder has not images in it
    with pytest.raises(exceptions.ImageNotFoundException):
        services.get_image_dir_by_position(return_first_position, 1, mock_image_db_dir)


def test_get_patient_name_happy_path():
    mock_image_path = (
        f"{mock_image_db_dir}/{mock_first_set_folder_name}/{mock_first_slice_name}"
    )
    patient_name = services.get_patient_name(mock_image_path)
    assert patient_name == "PatientName"


def test_get_patient_name_fails():
    mock_image_path = (
        f"{mock_image_db_dir}/{mock_empty_image_db_dir}/{mock_first_slice_name}"
    )

    with pytest.raises(exceptions.ImageNotFoundException):
        services.get_patient_name(mock_image_path)


def test_get_image_pixel_array_happy_path():
    mock_image_path = (
        f"{mock_image_db_dir}/{mock_first_set_folder_name}/{mock_first_slice_name}"
    )
    pixel_array = services.get_image_pixel_array(mock_image_path)
    assert pixel_array


def test_get_image_pixel_array_fails():
    mock_image_path = (
        f"{mock_image_db_dir}/{mock_empty_image_db_dir}/{mock_first_slice_name}"
    )

    with pytest.raises(exceptions.ImageNotFoundException):
        services.get_image_pixel_array(mock_image_path)
