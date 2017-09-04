from handlers.rewards_handler import RewardsHandler
from handlers.endpoint1_handler import Endpoint1Handler
from handlers.endpoint2_handler import Endpoint2Handler
from handlers.endpoint3_handler import Endpoint3Handler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/endpoint1', Endpoint1Handler),
    (r'/endpoint2', Endpoint2Handler),
    (r'/endpoint3', Endpoint3Handler),
]
