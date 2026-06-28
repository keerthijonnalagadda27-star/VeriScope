import io
from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'




def extract_text_from_image(image_bytes:bytes)->dict:
    try:
        image=Image.open(io.BytesIO(image_bytes))

        #ikkada io.ByesIO() raw bytes ni file like obj ga convert chestai PIL ki ala kaavali kaabatti

        if image.mode!='RGB':
            image=image.convert('RGB')

        text=pytesseract.image_to_string(image,lang='eng')
        text=text.strip()

        if len(text)<20:
            return{
                "text":text,
                "success":False,
                "error":"Could not extract enough text from image-try a clearer image"
            }
        return{
            "text":text,
            "success":True
        }
    except Exception as e:
        return{
            "text":"",
            "success":False,
            "error":str(e)
        }
    



