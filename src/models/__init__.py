from .cleared_split import ClearedSplit
from .payment import Payment
from .split import Split
from .user import User

print(
    f' loading model {User.__tablename__}'
    f'loading model {ClearedSplit.__tablename__}'
    f'loading model {Payment.__tablename__}'
    f'loading model {Split.__tablename__}'
)
