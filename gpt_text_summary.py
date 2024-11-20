from openai import AzureOpenAI
import os

client = AzureOpenAI(
  azure_endpoint = "https://textsumary.openai.azure.com/", 
  api_key="CT5DoE2HwGbeTBe0Zhs7vQuXAxnSnIRl0ooOMMY82Tq51sDGVBfuJQQJ99AKACYeBjFXJ3w3AAABACOGJNvB",  
  api_version="2024-09-01-preview"
)

def ai_text_response(path,files_to_summarize):
  file_path = os.path.join(path, files_to_summarize)

  with open(file_path, "r") as file:
    content = file.read()

  if len(content) > 50:
    content = content[:50]


  global response
  response = client.chat.completions.create(
  model="gpt-4-summary", # replace with the model deployment name of your o1-preview, or o1-mini model
  messages=[
        {"role": "user", "content": f"Please tell me in no more than 5 words what the following is about:\n{content}"},
  ],
  max_tokens = 500,
  )
  return (response.choices[0].message.content)


def main():
   ai_text_response()

if __name__ == "__main__":
    main()
#print(response.model_dump_json(indent=2))


