import logging

FORMAT: str = "%(levelname)s [%(asctime)s - %(name)s] :  %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logger = logging.getLogger()
