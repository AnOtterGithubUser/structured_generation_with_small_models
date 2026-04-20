import os
from pathlib import Path
from openai import AsyncOpenAI
import base64
from typing import Dict
from pydantic import ValidationError
import instructor
import logging

from schemas.baseline import Invoice as Invoice_baseline
from schemas.step_2 import Invoice as Invoice_step_2
from schemas.step_3 import Invoice as Invoice_step_3
from schemas.step_4 import Invoice as Invoice_step_4
from prompts.baseline import PROMPT as prompt_baseline
from prompts.step_1 import RESPONSE_FORMAT as response_format_step_1
from prompts.step_2 import RESPONSE_FORMAT as response_format_step_2
from prompts.step_3 import RESPONSE_FORMAT as response_format_step_3
from prompts.step_2 import PROMPT as prompt_step_2
from prompts.step_3 import PROMPT as prompt_step_3


def baseline_message(img_url: str):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_baseline},
                {"type": "image_url", "image_url": {"url": img_url}},
            ],
        }
    ]

def step_1_message(img_url: str):
    return baseline_message(img_url)

def step_2_message(img_url: str):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_step_2},
                {"type": "image_url", "image_url": {"url": img_url}},
            ],
        }
    ]

def step_3_message(img_url: str):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_step_3},
                {"type": "image_url", "image_url": {"url": img_url}},
            ],
        }
    ]

def get_data_url_from_image_path(img_path: Path) -> str:
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    img_data_url = f"data:image/jpeg;base64,{img_b64}"

    return img_data_url


async def invoice_ocr_baseline() -> Dict[str, Invoice_baseline]:
    client = AsyncOpenAI(
        base_url=os.getenv("LM_STUDIO_SERVER_URL"),
        api_key="lm-studio"
    )
    models = await client.models.list()
    model = models.data[0].id

    data_folder = Path(os.getenv("DATA_FOLDER"))
    jpg_files = list(data_folder.glob("*.jpg"))

    invoice_results = {}

    for img_path in jpg_files:
        print(f"\n-------------------\nIMG_PATH: {img_path}")
        img_data_url = get_data_url_from_image_path(img_path)
        response = await client.chat.completions.create(
            model=model,
            messages=baseline_message(img_data_url)
        )
        content = response.choices[0].message.content
        print(f"Raw content: {content}")

        try:
            invoice_content = Invoice_baseline.model_validate_json(content)
            invoice_results[img_path] = invoice_content
        except ValidationError:
            print(f"Output parsing failed")
    
    return invoice_results


async def invoice_ocr_step_1() -> Dict[str, Invoice_baseline]:
    client = AsyncOpenAI(
        base_url=os.getenv("LM_STUDIO_SERVER_URL"),
        api_key="lm-studio"
    )
    models = await client.models.list()
    model = models.data[0].id

    data_folder = Path(os.getenv("DATA_FOLDER"))
    jpg_files = list(data_folder.glob("*.jpg"))

    invoice_results = {}

    for img_path in jpg_files:
        print(f"\n-------------------\nIMG_PATH: {img_path}")
        img_data_url = get_data_url_from_image_path(img_path)
        response = await client.chat.completions.create(
            model=model,
            response_format=response_format_step_1,
            messages=step_1_message(img_data_url),
        )
        content = response.choices[0].message.content
        print(f"Raw content: {content}")

        try:
            invoice_content = Invoice_baseline.model_validate_json(content)
            print("Parsing succeeded!")
            invoice_results[img_path] = invoice_content
        except ValidationError:
            print(f"Parsing failed!")
    
    return invoice_results


async def invoice_ocr_step_2() -> Dict[str, Invoice_step_2]:
    client = AsyncOpenAI(
        base_url=os.getenv("LM_STUDIO_SERVER_URL"),
        api_key="lm-studio"
    )
    models = await client.models.list()
    model = models.data[0].id

    data_folder = Path(os.getenv("DATA_FOLDER"))
    jpg_files = list(data_folder.glob("*.jpg"))

    invoice_results = {}

    for img_path in jpg_files:
        print(f"\n-------------------\nIMG_PATH: {img_path}")
        img_data_url = get_data_url_from_image_path(img_path)
        response = await client.chat.completions.create(
            model=model,
            response_format=response_format_step_2,
            messages=step_2_message(img_data_url),
        )
        content = response.choices[0].message.content
        print(f"Raw content: {content}")

        try:
            invoice_content = Invoice_step_2.model_validate_json(content)
            print("Parsing succeeded!")
            invoice_results[img_path] = invoice_content
        except ValidationError:
            print(f"Parsing failed!")
    
    return invoice_results

async def invoice_ocr_step_3() -> Dict[str, Invoice_step_3]:
    client = AsyncOpenAI(
        base_url=os.getenv("LM_STUDIO_SERVER_URL"),
        api_key="lm-studio"
    )
    models = await client.models.list()
    model = models.data[0].id

    data_folder = Path(os.getenv("DATA_FOLDER"))
    jpg_files = list(data_folder.glob("*.jpg"))

    invoice_results = {}

    for img_path in jpg_files:
        print(f"\n-------------------\nIMG_PATH: {img_path}")
        img_data_url = get_data_url_from_image_path(img_path)
        response = await client.chat.completions.create(
            model=model,
            response_format=response_format_step_3,
            messages=step_3_message(img_data_url),
        )
        content = response.choices[0].message.content
        print(f"Raw content: {content}")

        try:
            invoice_content = Invoice_step_3.model_validate_json(content)
            print("Parsing succeeded!")
            invoice_results[img_path] = invoice_content
        except ValidationError:
            print(f"Parsing failed!")
    
    return invoice_results

async def invoice_ocr_step_4() -> Dict[str, Invoice_step_3]:
    client = AsyncOpenAI(
        base_url=os.getenv("LM_STUDIO_SERVER_URL"),
        api_key="lm-studio"
    )
    models = await client.models.list()
    model = models.data[0].id

    data_folder = Path(os.getenv("DATA_FOLDER"))
    jpg_files = list(data_folder.glob("*.jpg"))

    invoice_results = {}

    for img_path in jpg_files:
        print(f"\n-------------------\nIMG_PATH: {img_path}")
        img_data_url = get_data_url_from_image_path(img_path)
        response = await client.chat.completions.create(
            model=model,
            response_format=response_format_step_3,
            messages=step_3_message(img_data_url),
        )
        content = response.choices[0].message.content
        print(f"Raw content: {content}")

        try:
            invoice_content = Invoice_step_3.model_validate_json(content)
            print("Parsing succeeded!")
        except ValidationError:
            print(f"Parsing failed!")

        try:
            invoice_content = Invoice_step_4.model_validate_json(content)  # run pydantic validators
            invoice_results[img_path] = invoice_content
            print("Validation succeeded!")
        except ValidationError as e:
            print(f"Validation failed!\nMessage: {e}")
    
    return invoice_results

async def invoice_ocr_step_5(n_retries: int, debug: bool) -> Dict[str, Invoice_step_3]:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    client = AsyncOpenAI(
        base_url=os.getenv("LM_STUDIO_SERVER_URL"),
        api_key="lm-studio"
    )
    models = await client.models.list()
    model = models.data[0].id

    data_folder = Path(os.getenv("DATA_FOLDER"))
    jpg_files = list(data_folder.glob("*.jpg"))

    invoice_results = {}

    for img_path in jpg_files:
        print(f"\n-------------------\nIMG_PATH: {img_path}")
        img_data_url = get_data_url_from_image_path(img_path)

        retry_client = instructor.from_openai(
            client,
            mode=instructor.Mode.JSON_SCHEMA
        )
        try:
            invoice_content = await retry_client.chat.completions.create(
                model=model,
                response_model=Invoice_step_4,
                max_retries=n_retries,
                messages=step_3_message(img_data_url)
            )
        except instructor.core.exceptions.InstructorRetryException:
            print("Invoice extraction failed!")

        print(f"Invoice: {invoice_content}")
        invoice_results[img_path] = invoice_content
    
    return invoice_results
