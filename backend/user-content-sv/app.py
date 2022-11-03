import sys  
from pathlib import Path  
file = Path(__file__).resolve()
package_root_directory = file.parents [1]  
sys.path.append(str(package_root_directory))  

from common_lib.get_user_data import GetUserData
import os, multiprocessing
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_HOST=os.environ['RABBITMQ_HOST']
LINE_WEBHOOK_EXCHANE=os.environ['LINE_WEBHOOK_EXCHANE']
LINE_WEBHOOK_ROUTING_KEY=os.environ['LINE_WEBHOOK_ROUTING_KEY']
LINE_WEBHOOK_QUEUE=os.environ['LINE_WEBHOOK_QUEUE']
LINE_CAT=os.environ['LINE_CAT']

if __name__ == '__main__':
    gud = GetUserData(RABBITMQ_HOST, LINE_WEBHOOK_EXCHANE, 'topic', LINE_WEBHOOK_QUEUE, LINE_WEBHOOK_ROUTING_KEY, LINE_CAT)
    gud_proc = multiprocessing.Process(target=gud.run)
    gud_proc.start()