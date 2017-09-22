import datetime


MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 30
SMALL_CHAR_LENGTH = 50
MEDIUM_CHAR_LENGTH = 200
MAX_CHAR_LENGTH = 1000
MAX_INVOICE_NUMBER_LENGTH = 8

#DELIVERY_COST = 50


DEFAULT_LAST_ORDER_RECEIVING_TIME = datetime.datetime.strptime('8:00 pm', "%I:%M %p").time()
DEFAULT_STORE_OPENING_TIME = datetime.datetime.strptime('8:00 am', "%I:%M %p").time()
DEFAULT_STORE_CLOSING_TIME = datetime.datetime.strptime('8:00 pm', "%I:%M %p").time()

TIME_CHOICES = (
        (datetime.datetime.strptime('7:00 am', "%I:%M %p").time(), '7:00 am'),
        (datetime.datetime.strptime('8:00 am', "%I:%M %p").time(), '8:00 am'),
        (datetime.datetime.strptime('9:00 am', "%I:%M %p").time(), '9:00 am'),
        (datetime.datetime.strptime('6:00 pm', "%I:%M %p").time(), '6:00 pm'),
        (datetime.datetime.strptime('7:00 pm', "%I:%M %p").time(), '7:00 pm'),
        (datetime.datetime.strptime('8:00 pm', "%I:%M %p").time(), '8:00 pm'),
        (datetime.datetime.strptime('9:00 pm', "%I:%M %p").time(), '9:00 pm'),

    )

ADMIN = 1
VENUE_MANAGER = 2
GENERAL_USER = 3
USER_TYPE_CHOICES = [(ADMIN, 'Admin'), (VENUE_MANAGER, 'Venue Manager'), (GENERAL_USER, 'General User')]

TIME_SLOT_1 = 1
TIME_SLOT_2 = 2
TIME_SLOT_3 = 3
TIME_SLOT_4 = 4

DELIVERY_TIME_SLOTS = [(TIME_SLOT_1, '8AM - 12PM'), (TIME_SLOT_2, '12PM - 4PM'), (TIME_SLOT_3, '4PM - 10PM'), (TIME_SLOT_4, 'Now')]

PENDING = 1
DELIVERED = 2
DELIVERY_STATUS = [(PENDING, 'Pending'),(DELIVERED, 'Delivered')]


MALE = 1
FEMALE = 2
GENDER_CHOICES = [(MALE, 'Male'), (FEMALE, 'Female')]