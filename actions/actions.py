# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
class ActionSaleForm(Action):

    def name(self) -> Text:
         return "action_sale_form"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text')

        buttons = []

        #append the response of API in the form of title and payload

        buttons.append({"title": "Đúng" , "payload": "Xác nhận thông tin đúng. Cảm ơn"})
        buttons.append({"title": "Sai" , "payload": tracker.events[-3].get('text')})

        #then display it using dispatcher


        if "-" not in user_message:
            dispatcher.utter_message(text="Sorry, try again")
        else:
            try:
                name, phone_num, product_ID = user_message.split("-")
                dispatcher.utter_message(text=f"Xác nhận lại thông tin\nTên:{name}\nSdt:{phone_num}\nsản phẩn:{product_ID}",  buttons = buttons)
            except:
                dispatcher.utter_message(text="Vui lòng nhập lại")

        return []
    
class ActionFindProduct(Action):

    def name(self) -> Text:
         return "action_find_product"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text')


    # def get_chatgpt_response(self, message):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer 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',
            'Content-Type': 'application/json'
        }
        data = {
            'model': "gpt-3.5-turbo",
            'messages': [   {'role': 'system', 'content': 'Hãy xác định món hàng mà khách hàng muốn mua và trả lời trong dấu. Chỉ trả lời món hàng đó, không dài dòng.'},
                            {'role': 'user', 'content': user_message}
                            ],
            'max_tokens': 30
        }

        

        response = requests.post(url, headers=headers, json=data)
                # response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            chatgpt_response = response.json()
            message = chatgpt_response['choices'][0]['message']['content']
            #product_name = message.split('"')[-2]
            res = f"dưới đây là danh sách {message} phù hợp (link, ảnh, mã)"

            buttons = []

            buttons.append({"title": "Đặt" + message + "mã 01" , "payload": "tôi muốn mua" + message + "mã 01"})
            buttons.append({"title": "Đặt" + message + "mã 02" , "payload": "tôi muốn mua" + message + "mã 02"})

            dispatcher.utter_message(text = res, buttons = buttons)
        else:
            # Handle error
            dispatcher.utter_message("Vui lòng nhập lại")
        
        return []
     
class ActionHello(Action):

     def name(self) -> Text:
         return "action_greet"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Xin chào, Tớ là Cá Ngừ - chatbot tự động. Tớ có thể giúp gì cho cậu khum?")

         return []
     
class ActionFallBack(Action):
    def name(self) -> Text:
        return "action_chatgpt_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
    # Get user message from Rasa tracker
        user_message = tracker.latest_message.get('text')
        print(user_message)

    # def get_chatgpt_response(self, message):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer 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',
            'Content-Type': 'application/json'
        }
        data = {
            'model': "gpt-3.5-turbo",
            'messages': [   {'role': 'system', 'content': 'Bạn là một trợ lý ảo. Hãy trả lời ngắn gọn 2, 3 câu.'},
                            {'role': 'user', 'content': user_message}
                            ],
            'max_tokens': 300
        }
        response = requests.post(url, headers=headers, json=data)
                # response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            chatgpt_response = response.json()
            message = chatgpt_response['choices'][0]['message']['content']
            dispatcher.utter_message(message)
        else:
            # Handle error
            return "Sorry, I couldn't generate a response at the moment. Please try again later."
        
                # Revert user message which led to fallback.
        return []
