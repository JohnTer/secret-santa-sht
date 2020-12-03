import time
import logging

import orjson
import aiohttp

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from secret_santa import settings
from .context import ContextManager


async def http_vk_handler(request) -> HttpResponse:
    current_time: float = time.time()
    ctx_manager = ContextManager()

    json_data: dict = orjson.loads(request.body)
    logging.info(f'The request was received {json_data}')

    if json_data["type"] == "confirmation":
        logging.info('A confirmation code was sent')
        return HttpResponse(settings.VK_CONFIRMATION_CODE, status=200)

    send_time: int = json_data['object']['message']['date']
    vk_id: int = json_data['object']['message']['from_id']
    text: str = json_data['object']['message']['text']
    if abs(time.time() - send_time) > settings.MESSAGE_TIMEOUT:  # ttl
        logging.warning(
            f'The message was rejected due to a timeout[vk_id={vk_id} text={text}]'
        )
        return HttpResponse('ok', status=200)

    logging.info(
        f'The message [text={text}] was received from [vk_id={vk_id}]')
    await ctx_manager.process(json_data)

    logging.info('the message \"%s\" by user %d was processed in %f ms', text,
                 vk_id, (time.time() - current_time) * 1000)

    return HttpResponse('ok', status=200)
