from datetime import datetime

import pydicom
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
import numpy as np
from PIL import Image
from io import BytesIO

# def image_to_dcm(image_bytes, patient_id="Anon001", patient_name="Anonymous^Patient"):
#     pixel_array = np.array(Image.open(BytesIO(image_bytes)))
#
#     ds = pydicom.Dataset()
#
#     # File Meta Information (required for valid DICOM)
#     ds.file_meta = pydicom.FileMetaDataset()
#     ds.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7' # Secondary Capture Image Storage
#     ds.file_meta.MediaStorageSOPInstanceUID = generate_uid()
#     ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian # Or ExplicitVRLittleEndian
#     ds.file_meta.ImplementationClassUID = generate_uid()
#
#     # General Study, Series, and Patient Information
#     ds.PatientID = patient_id
#     ds.PatientName = patient_name
#     ds.StudyInstanceUID = generate_uid()
#     ds.SeriesInstanceUID = generate_uid()
#     ds.SOPInstanceUID = ds.file_meta.MediaStorageSOPInstanceUID
#     ds.SOPClassUID = ds.file_meta.MediaStorageSOPClassUID
#
#     # Image Pixel Module
#     ds.Rows, ds.Columns = pixel_array.shape[:2]
#     if pixel_array.ndim == 3:  # Color image
#         ds.SamplesPerPixel = 3
#         ds.PhotometricInterpretation = "RGB"
#         ds.PlanarConfiguration = 0  # 0 for interleaved, 1 for separated planes
#     else:  # Grayscale image
#         ds.SamplesPerPixel = 1
#         ds.PhotometricInterpretation = "MONOCHROME2" # Or MONOCHROME1
#     ds.BitsAllocated = 8
#     ds.BitsStored = 8
#     ds.HighBit = 7
#     ds.PixelRepresentation = 0  # 0 for unsigned integer, 1 for signed integer
#
#     # Pixel Data
#     ds.PixelData = pixel_array.tobytes()
#
#     with BytesIO() as buffer:
#         ds.save_as(buffer, write_like_original=False)
#         return buffer.getvalue()


# def image_bytes_to_dicom_bytes(image_bytes: bytes) -> bytes:
#     """
#     Converts image bytes (JPEG, PNG, etc.) to DICOM bytes.
#
#     Args:
#         image_bytes: Bytes of the input image.
#
#     Returns:
#         DICOM file bytes.
#     """
#     # Open image and convert to numpy array
#     with Image.open(BytesIO(image_bytes)) as img:
#         img_array = np.array(img)
#
#     # Create in-memory DICOM file
#     file_meta = pydicom.Dataset()
#     file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'  # Secondary Capture
#     file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
#     file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
#
#     ds = pydicom.FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
#
#     # Set required DICOM attributes
#     ds.PatientName = "Unknown"
#     ds.PatientID = "Unknown"
#     ds.StudyInstanceUID = pydicom.uid.generate_uid()
#     ds.SeriesInstanceUID = pydicom.uid.generate_uid()
#     ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
#     ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
#     ds.Modality = "OT"  # Other
#     ds.StudyDescription = "Generated from Image"
#     ds.SeriesDescription = "Converted Series"
#
#     # Set image dimensions and color space
#     ds.Rows, ds.Columns = img_array.shape[:2]
#     ds.SamplesPerPixel = 1 if len(img_array.shape) == 2 else img_array.shape[2]
#     ds.PhotometricInterpretation = "MONOCHROME2" if ds.SamplesPerPixel == 1 else "RGB"
#     ds.BitsAllocated = 8
#     ds.BitsStored = 8
#     ds.HighBit = 7
#     ds.PixelRepresentation = 0
#
#     # Handle pixel data
#     if ds.SamplesPerPixel > 1:
#         ds.PlanarConfiguration = 0
#
#     ds.PixelData = img_array.tobytes()
#
#     # Save to bytes buffer
#     buffer = BytesIO()
#     ds.save_as(buffer, write_like_original=False)
#     return buffer.getvalue()

def image_to_dcm(image_bytes: bytes) -> bytes:
    """
    Converts PNG or JPG image bytes into DICOM format bytes.

    Parameters:
        image_bytes (bytes): Input image bytes in PNG or JPG format.

    Returns:
        bytes: DICOM encoded bytes.
    """
    # Open image and convert to grayscale numpy array
    with Image.open(BytesIO(image_bytes)) as img:
        img = img.convert('L')  # Convert to 8-bit grayscale
        pixel_array = np.array(img)

    # Create in-memory DICOM file
    suffix = '.dcm'
    file_meta = pydicom.Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'  # Secondary Capture Image Storage
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid() # Random UID
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian  # Encoding format

    # Create dataset
    ds = pydicom.FileDataset(None, {}, file_meta=file_meta, preamble=b'\0' * 128)
    ds.PatientName = "Unknown"
    ds.PatientID = "Unknown"
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.Modality = 'OT'  # Other
    ds.StudyDescription = 'Generated from Image'
    ds.SeriesDescription = 'Converted Image'
    ds.StudyDate = datetime.now().strftime('%Y%m%d')
    ds.StudyTime = datetime.now().strftime('%H%M%S')
    ds.Rows, ds.Columns = pixel_array.shape
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = 'MONOCHROME2'
    ds.PixelRepresentation = 0
    ds.HighBit = 7
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.PixelData = pixel_array.tobytes()

    # Save to bytes buffer
    buffer = BytesIO()
    ds.save_as(buffer, write_like_original=False)
    return buffer.getvalue()

def dcm_to_png(dicom_data_bytes):
    try:
        ds = pydicom.dcmread(BytesIO(dicom_data_bytes))

        pixel_array = ds.pixel_array

        if 'PhotometricInterpretation' in ds and ds.PhotometricInterpretation == "MONOCHROME1":
            pixel_array = np.amax(pixel_array) - pixel_array

        if pixel_array.dtype != np.uint8:
            pixel_array = pixel_array - np.min(pixel_array)
            if np.max(pixel_array) > 0:
                pixel_array = pixel_array / np.max(pixel_array) * 255
            pixel_array = pixel_array.astype(np.uint8)

        img = Image.fromarray(pixel_array)

        png_output = BytesIO()
        img.save(png_output, format="PNG")
        png_bytes = png_output.getvalue()

        return png_bytes

    except Exception as e:
        print(f"Error converting DICOM to PNG: {e}")
        return None

def jpg_to_png(jpg_bytes):
    jpg_stream = BytesIO(jpg_bytes)
    img = Image.open(jpg_stream)

    png_stream = BytesIO()
    img.save(png_stream, format="PNG")

    png_bytes = png_stream.getvalue()
    return png_bytes