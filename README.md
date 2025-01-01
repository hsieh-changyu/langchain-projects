# Langchain-Projects
There are two projects developed by LangChain in this repo
1. Pinecone Documentation Bot
2. Python Code Interpreter


## Pinecone Documentation Bot through LangChain 
folder: documentation-bot-helper

The goal of this project is to utilize RAG technique to have a private bot, utilizing the LLM to answer the relevant pinecone information which we have fed to the pinecone vector database beforehand.

The specifications are:
Embeddings: OpenAI text-embedding-3-small
LLM model: gpt-3.5-turbo
Vector Database: Pinecone
Client-Server: Streamlit
Memory: Chat History (Buffer Memory)
Web Crawl: Firecrawl service (to convert the pinecone documentational web page to markdown and feed to the pinecone database)

The disadvantage of using buffer memory is that as conversations grow longer, the token limit of the LLM can be exceeded, truncating older parts of the chat.

input this command to get the bot running
```console
streamlit run main.py
```
**Result:**
![DocumentRAGBotResult](https://drive.google.com/uc?id=1IQ-vRkGo-vGQ3u3h9tMn5A8ZANKTRIV9)
Fig. A bot has been specialized to answer the pinecore relevant information. 

<br />
<br />

## Python Code Interpreter (LangChain) 
Folder: slim-code-interpreter

The goal of this project is to utilize the capabilities of the ReAct agent and functional calling based on the LangChain with OpenAI model.

*   Python agent: Generate the QR codes with corresponding URL and save in the hard drive.
    
*   CSV agent: Analyze a csv data, given user prompts, e.g. find the number of books published for each author, and sort in the ascending order.
    
*   Functional calling of Tavily search api.
    

A single composite agent is capable of selecting between the tools using a high-level description or logic. Use LangChain’s AgentExecutor to integrate the tools and provide an interface for the unified system. The agent prompt is taken from [langchain-ai/react-agent-template](https://smith.langchain.com/hub/langchain-ai/react-agent-template?organizationId=3320254e-9799-441d-a995-d4f43283424e)


**Result:**
![LangSmithResult](https://drive.google.com/uc?id=1KHczxgELdI9u0POiLNfAmx0Us8tpWfGK)
Fig. After two consecutive Tavily api searches, the current weather is shown as illustrated in LangSmith

<br />

![csvReActAgentResult](https://drive.google.com/uc?id=1tJXsFBxmHXKOqCTjG0lyJyF-wdUox_Cf)
Fig. The inference process shown in console to analyze the csv file

<br />

![pythonReActAgentResult](https://drive.google.com/uc?id=1QjvHhaydLf57IBG4czNnY0z4PXzo7Kic)
Fig. The inference process shown in console to generate QR code and save in the disk.