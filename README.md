# использование

```
import asyncio
import os
import aiohttp
from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageChops
import base64
from io import BytesIO
import random


async def add_warn_to_img(img: Image.Image, text_list: list[str], icon: Image.Image) -> Image.Image:
    pass

result = asyncio.run(
    add_warn_to_img(
        Image.open('clip-vit-large_images/normal_test_1.png'),
        ['обнаружено порно', 'просьба сохранять спакойствие'],
        Image.open('smiley_face.png')
    )
)
result.show()
```

`img` - ну тут понятно

`text_list` - список строк, будут рапсположены по порядку по вертикали

`icon` - иконка к тексту для красоты, желательно квадратная и пнг

# результаты

![result_1](https://github.com/user-attachments/assets/5502458f-fb75-450d-b5f9-2beaaac18362)

![result_2](https://github.com/user-attachments/assets/f5fc31a9-3f2c-4968-9de2-b9f08ecd42f3)
