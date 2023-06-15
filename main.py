import openai
import json
import os
os.environ["http_proxy"]="127.0.0.1:10809"
os.environ["https_proxy"]="127.0.0.1:10809"
openai.organization = "org-WH4aE1ZoUknRcCTSul3MH8JJ"
openai.api_key = "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"
def askChatGPT(messages):
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages = messages,
        temperature=1)
    return response['choices'][0]['message']['content']
def audioToEnglish(filename):
    MODEL = "whisper-1"
    with open(filename,"rb") as file:
        response = openai.Audio.transcribe(model=MODEL,file=file)
    print(response["text"])
def beATeacher():
    return [{"role": "system","content":"假设你是一位知识渊博的教授，我是你的学生。由于我的无知，你需要尽可能地用简单易懂的语言传授给我知识。"}]
def oneWord():
    return [{"role": "system","content":"假设你是一个输入法软件，我打入拼音，你输出最可能的中文"}]
def main():
    messages = oneWord()
    print('你前面是一位教授，他将传授给你知识。当你输入 quit 时，将终止程序\n')
    remember = ""
    while 1:
        try:
            text = input('你：')
            if text == 'quit':
                break
            remember+='你：'+text+'\n'
            d = {"role":"user","content":text}
            messages.append(d)

            text = askChatGPT(messages)
            d = {"role":"assistant","content":text}
            print('教师：'+text+'\n')
            remember +='教师：'+text+'\n'
            messages.append(d)
        except Exception as e:
            print(e)
            messages.pop()
            print('教授：等等，你太着急了，让我想想\n')
    with open('./venv/params.json', 'r') as f:
        loaded_params = json.load(f)
    # 打开文件以写入模式打开

    with open('./record/'+str(loaded_params['fileCount'])+'.txt', 'w') as f:
       # 写入字符串到文件中
        f.write(remember)

    # 修改参数
    loaded_params['fileCount'] += 1
    # 将修改后的参数保存回 JSON 文件
    with open('./venv/params.json', 'w') as f:
        json.dump(loaded_params, f)

if __name__ == '__main__':
    audioToEnglish("text.mp3")