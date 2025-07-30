# Perplexity CLI - Submission Details

## How I Spent My Time

My time was primarily focused on building a robust and user-friendly application that successfully replicates Perplexity's core value. The breakdown was roughly:

1.  **Core Functionality (50%):** The highest priority was ensuring the main workflow was solid: fetching search results, passing them to an LLM, and generating a useful, cited answer. This involved integrating the SerpAPI and OpenAI libraries and ensuring the data flowed correctly between them.

2.  **User Experience (40%):** A tool like this lives or dies by its interface. I invested significant time using the `rich` library to create a polished and intuitive CLI experience. This includes the live streaming of AI responses, formatted tables for search results, and clear, color-coded text that makes the output easy to read.

3.  **Key Feature Enhancement (10%):** To more closely mimic Perplexity and demonstrate a deeper use of AI, I added the "follow-up questions" feature. This required a second, distinct call to the AI with a different prompt, adding more intelligence to the tool.

## Technical Decisions & AI Techniques

### Architecture
I chose a modular design to separate concerns, making the code cleaner and easier to maintain. The key modules are:
-   `cli.py`: The main entry point and orchestrator, responsible for the user interface and coordinating the other modules.
-   `search_engine.py`: Handles all communication with the SerpAPI.
-   `ai_processor.py`: Manages all interactions with the OpenAI API, including prompt construction.
-   `cache_manager.py`: Implements a simple file-based cache to improve performance and reduce costs.

### AI Techniques Employed

My focus was on effective **Prompt Engineering** to get the desired behavior from the LLM.

1.  **Cited Synthesis:** The core of the application. The system prompt strictly instructs the AI to synthesize an answer *based only on the provided search results* and to cite sources using the `[index]` format. This makes the output trustworthy and verifiable.

2.  **Streaming Responses:** By setting `stream=True` in the API call and using `rich.live` in the front end, the application provides immediate feedback to the user, creating a much better experience than waiting for the full response to generate.

3.  **Follow-up Question Generation:** This is a separate, secondary AI call. After the main answer is generated, a different prompt is sent to the model, asking it to generate relevant follow-up questions. This demonstrates the ability to use an LLM for multiple, distinct tasks within a single workflow.

## What I Would Do With More Time

Given more time, I would focus on these areas:

1.  **Comprehensive Testing:** I would build out a full test suite with `pytest`, using mocks to simulate API calls. This would allow for rigorous testing of the `SearchEngine` and `AIProcessor` logic without incurring API costs.

2.  **More Advanced Caching:** The current file-based cache is simple. I would upgrade it to a more robust solution like a local SQLite database, which would allow for more complex caching logic (e.g., caching based on the model used, setting expiration times).

3.  **Error Handling and Resilience:** I would make the error handling more granular. For instance, if a single search result fails to load, the system could gracefully ignore it and proceed with the rest, rather than potentially failing the entire query.

4.  **Configuration File:** Instead of relying solely on command-line arguments, I would add a configuration file (e.g., `config.yaml`) to allow users to set their default model, number of results, and other preferences.
