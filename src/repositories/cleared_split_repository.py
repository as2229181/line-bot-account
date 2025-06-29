from database import db
from models.cleared_split import ClearedSplit
from repositories.repo import Repo


class ClearedSplitRepository(Repo):
    @staticmethod
    def create(
        uuid,
        from_whom_uuid,
        to_whom_uuid,
        do_commit=True,
        do_flush=False,
    ):
        cleared_split = ClearedSplit(
            uuid=uuid,
            from_whom_uuid=from_whom_uuid,
            to_whom_uuid=to_whom_uuid,
        )
        db.session.add(cleared_split)
        if do_commit:
            db.session.commit()
        if do_flush:
            db.session.flush(cleared_split)
        return cleared_split

    @staticmethod
    def get(uuid):
        split = db.session.query(
            ClearedSplit,
        ).filter(
            uuid=uuid,
        )
        return split
