# GROUP_12
A repository for 24/25 ADPRO's group project (Group 12)

**STUDENTS**:
 - Wale Doura: 57555@novasbe.pt
 - João Filipe Zhou Jin: 63631@novasbe.pt
 - Zhanshuo Guo: 64412@novasbe.pt
 - Léon Philipp Klingele: 67163@novasbe.pt

**HOW TO RUN THE PROGRAM**
  - The final part (2025/16/3) is stored on the main branch, please clone or pull the repository to your local machine.
  - Switch to the local folder of the program, Use command `pip install -r requirements.txt` to get necessary libraries.
  - One of the pages is based on library Ollama and need model "llama 3.2" to run, use command `ollama run llama3.2` to install it
  - Run the program/website using the command "streamlit run main.py".

**SPECIFICATION**
  - The program is built on Streamlit version 1.42.2.
  - If you already have streamlit installed, follow these steps to verify:
      - Check the installed Streamlit version by entering "pip list" in the terminal.
      - If Streamlit 1.42.2 is not installed, run "pip install --upgrade streamlit==1.42.2".
  - After completing these steps, you should be able to run main.py without any issues.

**ABOUT THE TEXT CLASSIFICATION**

We consider the text classification part of this project might help on SDG #9 Industry, Innovation and Infrastructure. The LLM shows a potential of functioning as intended with certain prompt. However, we find it is very hard to guarantee it generates proper format of text everytime it runs. If a large model is hold on cloud to complete this task, probably it will have higher accuracy. This project let us reflect on the potential of using large and mature LLM to complete certain automated tasks with outputs in a certain format, helping on the industrialization.
