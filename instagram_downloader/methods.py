import uuid
import requests
from telegram import InputFile, Update


def generate_random_filename():
    """Takrorlanmas matn qaytaruvchi funksiya"""
    random_uuid = uuid.uuid4()
    file_name = str(random_uuid)
    return file_name


async def download(url: str, update: Update):
    """Videoning urlini kiritsangiz xotijaga saqlaydigan funksiya"""
    ext = str(url).split("?")[0].split(".")[-1]
    # file_name = generate_random_filename()
    response = requests.get(url)
    if response.status_code == 200:  # Check if the request was successful
        file_content = response.content
        await update._bot.send_document(chat_id=update.effective_message.chat_id, document=InputFile(file_content, filename=f"file.{ext}"))
        # file_size = len(file_content) / (4**10)
        # with open(f"{file_name}.{ext}", 'wb') as file:
        #     file.write(file_content)
        #     print("File downloaded successfully.")
        #     print(f"File size: {file_size} MB")
    else:
        print("Error downloading file. Status code:", response.status_code)
