# LogisticsInventory
## About the project
This project was created for the Shopify intern challenge. It is a inventory management web app for a theoretical logistics company. It has basic CRUD functionality, and also allows deletion comments and restoration as per one of the prescribed challenges.

## Built with
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Mongodb](https://www.mongodb.com/)
- [BootStrap](https://getbootstrap.com/)

## Getting Started

### Prerequisites
- MongoDB: Create an account on [Mongodb](https://www.mongodb.com/), and download MongoDB compass and connect to a localhost (follow the [guide](https://docs.mongodb.com/compass/current/connect/))
- Python: Install the most recent version of [python](https://www.python.org/) and pip (pip comes with python)

### Installation
1. Clone the repo
```sh
   git clone https://github.com/JeffeyL/LogisticsInventory.git
```
2. Navigate to requirements.txt and install the required packages
```sh
   pip install -r requirements.txt
```

### Usage
1. Open and run the project
```sh
   python run.py
```
2. Access the localhost web URL, then enter a userID, which will be stored in cookies
3. Click create to create a new item in the inventory
4. The created item will be shown in the inventory page, and individual items can be updated or deleted by clicking on the links on each item.
5. After deleting an item, it can be seen in the deleted page, and can be restored or permanently deleted.
