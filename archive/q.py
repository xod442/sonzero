import logging    # first of all import the module


logging.basicConfig(filename="zero.log",
					format='%(asctime)s %(message)s',
					filemode='a')


logging.info('This message will get logged on to a file')
logging.debug("This is just a harmless debug message")
logging.info("This is just an information for you")
logging.warning("OOPS!!!Its a Warning")
logging.error("Have you try to divide a number by zero")
logging.critical("The Internet is not working....")
