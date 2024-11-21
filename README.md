# MyProducts

This is the backend for the MyProducts application.

## Access

The backend can be accessed [here](https://my-products-backend.vercel.app/).

The frontend can be accessed [here](https://my-products-frontend.vercel.app/).

## Built With

- [FastAPI](https://fastapi.tiangolo.com/)

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Python 3.7+

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/your_username/myproducts.git
    ```
2. Change to the project directory
    ```sh
    cd myproducts
    ```
3. Create a virtual environment
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment
    - On Windows
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux
        ```sh
        source venv/bin/activate
        ```
5. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. Run the FastAPI server
    ```sh
    uvicorn main:app --reload
    ```
2. Open your browser and navigate to `http://127.0.0.1:8000`

## License

Distributed under the MIT License. See `LICENSE` for more information.