# Post Rating System Backend

## Features

- **Post Listing with Ratings:** Retrieve a list of posts along with their aggregated ratings.
- **Submit Ratings:** Users can submit ratings for individual posts.
- **High Traffic Handling:** Utilizes Kafka and Celery to manage and process high-throughput rating data efficiently.
- **Performance Optimization:** Implements caching strategies to reduce latency and improve response times.
- **Security Measures:** Protects against rating manipulations and ensures secure data transactions. (whenever a malisiouce behaviour gets detected it discounts their impact on the average)


## Technologies Used

- **Django Rest Framework (DRF):** For building robust RESTful APIs.
- **Kafka:** Handles real-time data streams and high-throughput messaging.
- **Celery:** Manages asynchronous task processing.
- **Redis:** Serves as the message broker and caching layer.


## Usage

- **List Posts with Ratings:**
  - `GET /api/posts/`
- **Submit a Rating:**
  - `POST /api/posts/{post_id}/rate/`
  - Payload:
    ```json
    {
      "post_id": 1,
      "user_id": 1,
      "rating": 5
    }
    ```
