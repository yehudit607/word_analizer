# Word Analizer

Overview
The Word Counter API is a RESTful API designed to count the occurrences of words in various types of inputs, such as plain text, files, and URLs. The API processes input data asynchronously using Celery and stores the word count in a database.


Tech Stack:

Python 3.9
Django and Django Rest Framework for the API
Celery for asynchronous task processing
Redis as the message broker for Celery
PostgreSQL as the database for storing word count
aiohttp for processing URLs
Requirements
Docker
Docker Compose
Python 3.9

Getting Started

Clone the repository
Run docker-compose up to build and start the required services
The API will be accessible at http://localhost:8000/
API Endpoints
POST /api/wordcounter/
This endpoint accepts the following inputs:

text: Plain text
file: A file containing text
url: A URL containing text
Input Assumptions
Only one of the three inputs should be provided at a time. If multiple inputs are provided, the API will return an error.
The input data should be in a readable text format (e.g., UTF-8 encoded).

Output
The API returns a JSON response containing the following information:

detail: A message indicating the completion status of the word counting task

POST /api/wordstatistics/?word=word

output:
 count of times the word appeared so far 
 
 See more in: /docs/
  
Design Considerations

The API is designed to be scalable and can handle a large number of simultaneous requests.
Asynchronous processing is used to handle time-consuming tasks, such as counting words in large files or downloading content from URLs.
The API uses a database to store the word count, allowing for persistence and easy retrieval of results.

Review

The Word Counter API is a powerful tool for counting word occurrences in various types of inputs. It is designed to be scalable and can handle a large number of requests simultaneously. The asynchronous processing and use of a database for storing results make it suitable for use in various applications, such as data analysis, natural language processing, and search engine optimization.
