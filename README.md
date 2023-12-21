# ETechShop - Navigating the Digital World of Electronics.

ETechShop is a web application that allows users to explore the digital world of electronics. This README provides information on deploying the application and using some key features.

## Table of Contents
- [Deployment](#deployment)
- [API Endpoints](#api-endpoints)
- [Docker Commands](#docker-commands)
- [Management Commands](#management-commands)

## Deployment

To deploy ETechShop locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/etechshop.git
   cd etechshop
   ```
2. **Set Up Environment Variables:**
   Create a .env file in the project root and configure the required environment variables. You can use the provided .env.example as a templat

## Docker Commands
3. **Build and Run Docker Containers:**
   ```bash
   docker compose build
   ``` 
   > NOTE: for that you need to install docker on you computer https://docs.docker.com/engine/install/

   
4. **Initialize the Database:**
   ```bash
   docker compose exec etechshop-web-1 python manage.py migrate
   docker compose exec etechshop-web-1 python manage.py initial_fill_database
   # for clean tables
   docker compose exec etechshop-web-1 python manage.py clean_tables
   ```

5. **Management Commands**
   ```bash
   docker compose up
   docker compse down
   ```

## API Endpoints

Get token by username and password
http://127.0.0.1:8010/api/auth/

Next you need to set up headers with `Authorzation: Token <some_token>`  

CRUD for networknode model
http://127.0.0.1:8010/api/networknodes/  
http://127.0.0.1:8010/api/networknodes/1/  
filter by `product_id`  
http://127.0.0.1:8010/api/networknodes?product_id=1  
get statistic by debts
http://127.0.0.1:8010/api/networknodes/debt_statistics/  
sending contact email info  
http://127.0.0.1:8010/api/networknodes/5/send_netwoknode_info_email/  
CRUD for product model  
http://127.0.0.1:8010/api/products/  

>for more  information go to swagger auto generated documentation for all existing endpoints
http://127.0.0.1:8010/api/swagger/  
or redoc  
http://127.0.0.1:8010/api/redoc/
