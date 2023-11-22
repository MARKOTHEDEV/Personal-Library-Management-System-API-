
from typing import Dict, Union, List
from rest_framework.response import Response




def response_data(
    status: int, message: str, data: Union[None, Dict, List] = None
) -> Dict:
    """
    data response function
    :param status
    :param message:
    :param data:
    :return:
    """
    payload = {
        "status": status,
        "message": message,
    }
    if data is not None:
        payload.update(
            {"error": data}
        ) if 400 <= status <= 600 else payload.update({"data": data})
    return payload



def Res(status: int, message: str, data: Union[None, Dict, List] = None):
    'this is a helper class that helps return structured  response style to the frontend'
    resp = response_data(status=status,data=data,message=message)
    return Response(data=resp,status=status)    

