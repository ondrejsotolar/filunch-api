from datetime import datetime
from pathlib import Path
import openai
import requests
from lxml import html, etree
from lxml.cssselect import CSSSelector
import re
import ast
openai.api_key = Path('key1.txt').read_text()  # what security LOL?


def get_todays_name():
    return datetime.today().strftime('%A')


def get_menu_u_drevaka(day="", restaurant_name=""):
    drevak_xpath = '//*[@id="menu"]'
    url = "https://udrevaka.cz/denni-menu/"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    content_elements = tree.xpath(drevak_xpath)
    pr = "".join([re.sub(r'\s{2,}', ' ', ''
                         .join(element.xpath(".//text()")).strip())
                  for element in content_elements])
    return pr


def get_menu_diva_bara(day="", restaurant_name=""):
    url = "https://www.restauracedivabara.cz/menu/"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    selector = CSSSelector('.daily-menu')
    content_elements = selector(tree)
    pr = "".join([re.sub(r'\s{2,}', ' ', ''
                         .join(element.xpath(".//text()[not(ancestor::div[contains(@id, 'tab-2')])]")).strip())
                  for element in content_elements])
    return pr


def getlunch(opening_prompt: str):
    # limitation: only one function call - cannot do routing
    # statement: https://community.openai.com/t/trigger-multiple-functions-simultaneously-with-function-calling/328103
    # possible solution: https://community.openai.com/t/emulated-multi-function-calls-within-one-request/269582
    # TODO: auto calling
    # TODO: message history
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        max_tokens=2048,
        temperature=0,
        messages=[
            {"role": "user", "content": opening_prompt}
        ],
        functions=[
            {
                "name": "get_menu_diva_bara",
                "description": "Get the daily menu in the restaurant Divá Bára in Brno",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "restaurant_name": {
                            "type": "string",
                            "description": "name of the restaurant."
                        },
                        "day": {
                            "type": "string",
                            "description": "name of the day of week."
                        }
                    },
                    "required": ["restaurant_name"]
                }
            },
            {
                "name": "get_menu_u_drevaka",
                "description": "Get the daily menu in the restaurant U Dřeváka in Brno",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "restaurant_name": {
                            "type": "string",
                            "description": "name of the restaurant."
                        },
                        "day": {
                            "type": "string",
                            "description": "name of the day of week."
                        }
                    },
                    "required": ["restaurant_name"]
                }
            }
        ]
    )
    # call the generated functions
    jr = completion.to_dict()
    print(f'Suggested call: {jr["choices"][0]["message"]["function_call"]["name"]}')
    if not (any(ch["message"]["function_call"]["name"] == "get_menu_diva_bara" for ch in jr["choices"]) or
            any(ch["message"]["function_call"]["name"] == "get_menu_u_drevaka" for ch in jr["choices"])):
        print("No menu functions suggested.")
        return
        # today = get_name_of_day()
        # print("get_name_of_day not detected in suggested functions - setting today.")


    func = jr["choices"][0]["message"]["function_call"]["name"]
    arguments = ast.literal_eval(jr["choices"][0]["message"]["function_call"]["arguments"])
    func_res = eval(func + "(" + ", ".join(f"{key}='{value}'" for key, value in arguments.items()) + ")")
    # func_res = eval(func)

    # prompt GPT again for the result
    menu_prompt = (f"You're a helpful assistant. Answer the question based on the given context: {opening_prompt}. The context:\n"
                   f"The lunch menu of the restaurant named {arguments['restaurant_name']} for each day of this week: {func_res} \n"
                   f"Today is {get_todays_name()} \n"
                   f"I want the menu for this day: {arguments['day']}.")
    print(f"Prompt: {menu_prompt}")
    menu_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        max_tokens=2048,
        temperature=0.5,
        messages=[
            {"role": "user", "content": menu_prompt}
        ]
    )
    res_dict = menu_completion.to_dict()
    print(res_dict["choices"][0]["message"]["content"])
    # return menu_completion

# result = getlunch("Which dishes contain chicken at the restaurant U Dřeváka on tomorrow's menu?")
# res_dict = result.to_dict()
# print(res_dict["choices"][0]["message"]["content"])
