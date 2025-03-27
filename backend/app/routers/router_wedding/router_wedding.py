from sqlalchemy.orm import Session

class RouterWedding:
    def __init__(self, session: Session):
        self.db = session

    def create_wedding(self, wedding: Wedding):
        self.db.add(wedding)
        self.db.commit()
