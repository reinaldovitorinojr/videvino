import os
import logging as log
import requests
import mysql.connector
from datetime import datetime, timedelta, date, timezone


log.getLogger().setLevel(log.getLevelName(os.environ.get("LOG_LEVEL", "INFO")))

def hello_world():
	log.info("Hello world!")
	
def main():
	hello_world()
	
def lambda_handler(event, context):
	hello_world()
	
	return {'statusCode': 200, 'body': "Success!"}
	
if __name__ == "__main__":
	main()