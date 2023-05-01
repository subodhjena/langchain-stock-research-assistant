# Stock Research Assistant

Langchain stock market research assistant

## How to run

1. Make a copy of .env.example file as .env and popualte the environment variables

2. Open app.py and change the symbol

   ```python
   # note: the assistant currently only support indian indices
   symbol = 'SYMBOL'
   run(symbol)
   ```

3. It should be noted that initial laod will take some time and consecuteive load should be much faster
