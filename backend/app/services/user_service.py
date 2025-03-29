from sqlalchemy.orm import Session
from app.models.models import User as UserModel

def get_user_by_email(db: Session, email: str) -> UserModel | None:
    """
    Busca um usuário pelo email.
    
    Args:
        db: Sessão do banco de dados
        email: Email do usuário
        
    Returns:
        Usuário encontrado ou None
    """
    return db.query(UserModel).filter(UserModel.u_email == email).first() 