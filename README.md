**Project Documentation: AI Document Summarizer Summarify (Project_n9)**

**1. Introduction**

This document provides a comprehensive overview of the AI Document Summarizer application, codenamed "Project_n9". Developed as a full-stack web application, Summarify allows users to generate concise summaries of large text inputs using advanced AI models. It supports various summarization types tailored for different document formats like research papers, financial reports, technical documentation, and more. The platform includes user authentication, enabling users to save and revisit their generated summaries.

This project addresses the core requirements of the assignment by providing a functional web interface, a robust backend API, secure user authentication, integration with a NoSQL database, and utilization of a Large Language Model (LLM) for the summarization task.

**2. Features**

Summarify implements the following key features:

*   **User Authentication:** Secure signup and login process to manage user accounts.
*   **Text Summarization:** Allows users to input text and select a specific summarization type.
*   **Multiple Summary Types:** Provides predefined templates for summarizing research papers, financial reports, technical documents, meeting minutes, generating UML diagrams (via Mermaid code), and a general custom summary.
*   **AI Model Integration:** Leverages a Large Language Model (LLM) via the Groq API to perform the summarization.
*   **Summary History:** Users can view a list of their previously generated summaries on a personalized dashboard.
*   **Detailed Summary View:** Users can access a dedicated page to view the generated summary alongside the original text, with separate tabs for easy comparison.
*   **Markdown Rendering:** Summaries are displayed using Markdown formatting for readability, with syntax highlighting for code blocks (relevant for technical or UML summaries).
*   **Client-Side API Key Management:** For convenience, the Groq API key is handled on the client side and can be saved in local storage (browser-specific).
*   **Responsive User Interface:** The frontend is designed to be accessible on various device sizes.

**3. Technology Stack**

The project was developed using the following technologies, demonstrating proficiency across the full stack and alignment with the assignment's recommendations where applicable:

| Assignment Requirement           | Technology Used         | How It Was Used                                                                                                | Alignment                                  |
| :------------------------------- | :---------------------- | :------------------------------------------------------------------------------------------------------------- | :----------------------------------------- |
| **Frontend** (React or Vue.js) | Jinja2, HTML, CSS, JS | Server-side rendering with Jinja2 templates via FastAPI; custom CSS for styling; plain JavaScript for client-side interactions (API calls, markdown rendering, tab switching). | **Deviation:** Used server-side rendering & plain JS instead of a modern JS framework. This approach provides a functional and responsive UI using standard web technologies. |
| **Backend** (Node.js or FastAPI) | Python (FastAPI)        | Built a RESTful API to handle user authentication, summary requests, and data retrieval. FastAPI's performance and asynchronous capabilities are utilized. | **Match:** Utilized the recommended Python/FastAPI stack. |
| **Authentication** (JWT)         | JWT (via `python-jose`) | Implemented JWT-based authentication for securing API endpoints and managing user sessions via cookies and Authorization headers. Password hashing uses `passlib` (bcrypt). | **Match:** Implemented JWT authentication. |
| **Database** (PostgreSQL or MongoDB) | MongoDB (via `motor`)   | Used MongoDB as a NoSQL database to store user credentials and summary data (`users` and `summaries` collections). `motor` provides asynchronous MongoDB drivers for FastAPI. | **Match:** Utilized the recommended MongoDB database. |
| **AI Integration** (Hugging Face or OpenAI) | Groq (via `langchain-groq`) | Integrated with the Groq API to access high-performance LLMs (specifically `llama-3.3-70b-versatile`) for generating summaries based on prompt templates defined in the backend. `langchain-core` is used for building the prompt chain. | **Deviation:** Used Groq, another leading LLM provider, which fulfills the core requirement of integrating with an LLM API for text generation. |
| **Deployment** (AWS, GCP, Heroku) | AWS EC2 (Ubuntu)        | Deployed the application on an Ubuntu Server instance on Amazon Web Services (AWS) EC2. | **Match:** Deployed on a recommended cloud platform. |

**Additional Technologies Used:**

*   **`python-dotenv`:** For managing environment variables (`.env` file).
*   **`uvicorn` / `gunicorn`:** Asynchronous server gateway interface for running the FastAPI application in production.
*   **`uuid`:** For generating unique IDs for summaries.
*   **`datetime`:** For handling timestamps.
*   **`marked.js`:** (Frontend JS) For rendering Markdown in the browser.
*   **`Prism.js`:** (Frontend JS) For syntax highlighting code blocks within Markdown.
*   **`Font Awesome`:** (Frontend CSS/Icons) For icons in the UI.
*   **Nginx:** (Deployment) Used as a reverse proxy to serve the application and static files.

**4. Architecture**

The application follows a standard client-server architecture with distinct layers:

1.  **Frontend (Browser):**
    *   Static HTML pages rendered using Jinja2 templates.
    *   Client-side CSS (`static/css/`) for styling.
    *   Plain JavaScript (`static/js/`) for handling user interactions, making API calls to the backend, rendering Markdown (`marked.js`), and syntax highlighting (`Prism.js`).
    *   Manages user-side API key input and local storage persistence.

2.  **Backend (FastAPI Application):**
    *   Built with Python and the FastAPI framework (`main.py`).
    *   Handles routing, request/response processing, and serving templates/static files.
    *   Uses `AuthMiddleware` (`middleware/auth.py`) as a dependency to secure routes, verifying JWT tokens from cookies or headers.
    *   Interacts with the `SummarizerService` (`services/summarizer.py`) to perform summarization logic.
    *   Communicates with the MongoDB database using the asynchronous `motor` driver.
    *   Defines Pydantic schemas (`models/schemas.py`) for API data validation.
    *   Includes a logging utility (`utils/logger.py`).

3.  **Database (MongoDB):**
    *   Stores user information (username, hashed password) in the `users` collection.
    *   Stores generated summary data (original text, summary, type, username, timestamps, ID) in the `summaries` collection.
    *   Also includes a `sessions` collection, primarily for backward compatibility checks within the auth middleware.

4.  **AI Model (Groq API):**
    *   Called by the `SummarizerService` in the backend.
    *   Receives the user's text and a prompt template.
    *   Processes the text using the `llama-3.3-70b-versatile` LLM.
    *   Returns the generated summary text to the backend.

**Interaction Flow Example (Summarization):**

1.  User logs in via the Frontend, receives JWT token (stored in a cookie).
2.  User navigates to the `/summarize` page. The browser sends the JWT cookie with the request.
3.  FastAPI backend uses `auth.verify_session` dependency to validate the token and authenticate the user before serving the `summarize.html` template.
4.  On the `/summarize` page, the user enters text, selects a type, inputs their Groq API key, and clicks "Generate Summary".
5.  Client-side JS (`summarizer.js`) retrieves the inputs (including the API key), saves the API key to local storage, and makes an AJAX POST request to `/api/summarize` with the text, type, and API key in the request body (as defined by `TextInput` schema). The JWT cookie is automatically sent by the browser.
6.  FastAPI receives the request. `auth.verify_session` dependency validates the JWT cookie again.
7.  The `/api/summarize` endpoint function extracts the data, including the API key, and passes it to `summarizer_service.summarize_text`.
8.  `summarizer_service` initializes the `ChatGroq` client with the user-provided API key, fetches the correct prompt template, builds a Langchain chain, and calls the Groq API asynchronously.
9.  Upon receiving the summary from Groq, `summarizer_service` stores the original text, summary, type, and user information in MongoDB, generating a unique `summary_id`.
10. The `summarize` endpoint returns a JSON response containing the generated summary text and the `summary_id`.
11. Client-side JS receives the response, renders the summary using `marked.js`, applies `Prism.js` for highlighting, displays a success message, and shows the "Save Summary" button, storing the `summary_id`.
12. If the user clicks "Save Summary", client-side JS makes a POST request to `/api/save_summary/{summary_id}`. This endpoint calls the service to set a `saved: True` flag (though this flag isn't currently used for filtering in the dashboard) and then the JS redirects the user to the `/summary/{summary_id}` page.

**5. Setup and Installation (Local Development)**

To set up and run the project locally:

**Prerequisites:**

*   Python 3.7+ and `pip`
*   MongoDB server running or a MongoDB Atlas connection string
*   Git

**Steps:**

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd ninadw25-project_n9
    ```
    *(Replace `<repository_url>` with the actual URL)*

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables:**
    Create a `.env` file in the project root directory with the following variables:
    ```dotenv
    MONGO_URL="mongodb://localhost:27017/" # Or your MongoDB Atlas connection string
    JWT_SECRET="YOUR_SUPER_SECRET_JWT_KEY" # Replace with a strong, random secret key
    ```
    *(Note: For local testing, you can use a local MongoDB instance. For a full setup matching production, use a cloud-hosted DB like MongoDB Atlas)*

5.  **Run the Application:**
    Use `uvicorn` to run the FastAPI application. The `--reload` flag is useful for development.
    ```bash
    uvicorn main:app --reload
    ```
    The application should start and be accessible at `http://127.0.0.1:8000`.

**6. Usage**

1.  **Access the Application:** Open your web browser and go to `http://127.0.0.1:8000`. You will be redirected to the login page.
2.  **Sign Up:** If you don't have an account, click the "Sign up here" link on the login page, fill in the desired username and password, and click "Sign Up". You will be redirected back to the login page.
3.  **Login:** Enter your username and password on the login page and click "Login". You will be redirected to the dashboard.
4.  **Dashboard:** The dashboard (`/dashboard`) shows a welcome message and lists your recent summaries. You can navigate to the "Features" or "History" sections.
5.  **Generate Summary:**
    *   Click on a specific summary type link (e.g., "Summarize →" under Research Paper) or the "Try Custom" button (which also goes to `/summarize`).
    *   You will be taken to the summarizer page (`/summarize`).
    *   Enter your Groq API key in the "Groq API Key" field. (Note: This key is saved in your browser's local storage for convenience).
    *   Select the desired "Summary Type" from the dropdown.
    *   Paste the text you want to summarize into the "Text to Summarize" area.
    *   Click the "Generate Summary" button.
    *   Wait for the summary to appear in the "Summary" section. Status messages will indicate progress.
6.  **Save Summary:** After a summary is generated, a "Save Summary" button appears. Clicking this button redirects you to the detail page for that summary.
7.  **View Summary Detail:**
    *   From the dashboard history list, click the "View Summary" button for a specific summary.
    *   You will be taken to the detail page (`/summary/{summary_id}`).
    *   Use the tabs ("Summary", "Original Text") to switch between viewing the generated summary and the original input text.
