from sqlalchemy.orm import Session
from app.schemas.wedding import Wedding, WeddingCreate, WeddingUpdate
from app.models.models import Wedding as WeddingModel, User
from fastapi import HTTPException, status

class CreateWeddingController:
    def __init__(self, session: Session, wedding: WeddingCreate, current_user: User):
        self.db = session
        self.wedding = wedding
        self.current_user = current_user
        self.db_wedding: WeddingModel | None = None

    def execute(self) -> Wedding:
        try:
            if self.db.query(WeddingModel).filter(WeddingModel.w_fiance_id == self.current_user.id).first():
                raise HTTPException(status_code=400, detail="User already has a wedding")
            self.create_wedding()
            self.db.commit()
            return Wedding.from_orm(self.db_wedding)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, 
                detail=str(e)
            )

    def create_wedding(self) -> None:
        self.db_wedding = WeddingModel(
            w_fiance_id = self.current_user.id,
            w_date=self.wedding.w_date,
            w_location=self.wedding.w_location,
            w_description=self.wedding.w_description,
            w_status=self.wedding.w_status
        )
        self.db.add(self.db_wedding)
        self.db.flush()


class GetWeddingController:
    def __init__(self, session: Session, wedding_id: int):
        self.db = session
        self.wedding_id = wedding_id

    def execute(self) -> Wedding:
        wedding = self.db.query(WeddingModel).filter(WeddingModel.id == self.wedding_id).first()    
        if not wedding:
            raise HTTPException(status_code=404, detail="Wedding not found")
        return Wedding.from_orm(wedding)

class GetWeddingsByFianceController:
    def __init__(self, session: Session, fiance_id: int):
        self.db = session
        self.fiance_id = fiance_id
        self.db_weddings: list[WeddingModel] | None = None

    def execute(self) -> list[Wedding]:
        self.db_weddings = self.db.query(WeddingModel).filter(WeddingModel.w_fiance_id == self.fiance_id).all()
        return [Wedding.from_orm(wedding) for wedding in self.db_weddings]  


class UpdateWeddingController:
    def __init__(self, session: Session, wedding_id: int, wedding: WeddingUpdate):
        self.db = session
        self.wedding_id = wedding_id
        self.wedding = wedding

    def execute(self) -> Wedding:
        try:
            db_wedding = self.db.query(WeddingModel).filter(WeddingModel.id == self.wedding_id).first()
            if not db_wedding:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wedding not found"
            )
            update_data = self.wedding.dict(exclude_unset=True)

            for field, value in update_data.items():
                setattr(db_wedding, field, value)

            self.db.commit()
            self.db.refresh(db_wedding)
            return Wedding.from_orm(db_wedding)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

class DeleteWeddingController:
    def __init__(self, session: Session, wedding_id: int):
        self.db = session
        self.wedding_id = wedding_id

    def execute(self) -> None:
        try:
            db_wedding = self.db.query(WeddingModel).filter(WeddingModel.id == self.wedding_id).first()
            if not db_wedding:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Wedding not found"
                )
            self.db.delete(db_wedding)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
