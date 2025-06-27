from .cleared_spilt import ClearedSpilt
from .payment import Payment
from .split import Spilt
from .user import User

print(
    f' loading model {User.__tablename__}'
    f'loading model {ClearedSpilt.__tablename__}'
    f'loading model {Payment.__tablename__}'
    f'loading model {Spilt.__tablename__}'
)
