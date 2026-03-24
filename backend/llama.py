from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import OllamaLLM

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


def llama_model(word, relation):
      keyword = word.replace("_", " ")
      words = relation.split()

      inputword = words[0]
      
      llm = OllamaLLM(base_url="http://crai-04.dei.uc.pt:8080",
            model="llama3.3:latest",
            temperature=0.6,
            top_p=0.95)

      output = llm.invoke(f"Give me, in British English, a brief explanation of how the word “{inputword}” is related to the word “{keyword}”, following the definition of the word “{keyword}”. Do not answer with questions; if you cannot come up with an answer, just say that you do not know how to answer that.")

      return output
