# Stock Research Assistant

Langchain stock market research assistant

## How to run

1. Make a copy of .env.example file as .env and popualte the environment variables

2. Install the dependencies

   ```bash
   # install dependencies
   poetry install
   ```

3. Open app.py and change the symbol

   ```python
   # note: the assistant currently only support indian indices
   symbol = 'SYMBOL'
   run(symbol)
   ```

4. Run the following command to start the app

   ```bash
   # run the app
   streamlit run app.py
   ```

5. It should be noted that initial load will take some time and consecuteive load should be much faster
