from datetime import datetime
from typing import List

from backend.modules.subject.models import Subject
from backend.tests.integration.user.data import get_user_db

BASE_SUBJECT_ID = 1
BASE_SUBJECT_DATA = {
    "id": BASE_SUBJECT_ID,
    "name": "Subject 1",
}


def get_subject_data() -> List[Subject]:
    return [
        Subject(
            **BASE_SUBJECT_DATA,
            user_id=1,
            user=get_user_db()[0],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Subject(
            id=2,
            name="Subject 2",
            user_id=2,
            user=get_user_db()[1],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        Subject(
            id=3,
            name="Subject 3",
            user_id=1,
            user=get_user_db()[0],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
    ]
