from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

# Create ENUM types
usertype = ENUM('noivo', 'convidado', name='usertype', create_type=False)
weddingstatus = ENUM('ativo', 'adiado', 'cancelado', name='weddingstatus', create_type=False)
phototype = ENUM('noivos', 'convidados', name='phototype', create_type=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(Text, nullable=False)
    telefone = Column(String(20))
    tipo = Column(usertype, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    casamentos_noivo = relationship("Casamento", foreign_keys="[Casamento.noivo_id]", back_populates="noivo")
    casamentos_noiva = relationship("Casamento", foreign_keys="[Casamento.noiva_id]", back_populates="noiva")
    fotos = relationship("Foto", back_populates="usuario")

class Casamento(Base):
    __tablename__ = "casamentos"

    id = Column(Integer, primary_key=True, index=True)
    noivo_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    noiva_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    data = Column(Date, nullable=False)
    local = Column(String(255), nullable=False)
    descricao = Column(Text)
    status = Column(weddingstatus, default='ativo')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    noivo = relationship("Usuario", foreign_keys=[noivo_id], back_populates="casamentos_noivo")
    noiva = relationship("Usuario", foreign_keys=[noiva_id], back_populates="casamentos_noiva")
    convidados = relationship("Convidado", back_populates="casamento")
    grupos = relationship("GrupoConvidados", back_populates="casamento")
    lembretes = relationship("Lembrete", back_populates="casamento")
    fotos = relationship("Foto", back_populates="casamento")
    orcamentos = relationship("Orcamento", back_populates="casamento")

class GrupoConvidados(Base):
    __tablename__ = "grupos_convidados"

    id = Column(Integer, primary_key=True, index=True)
    casamento_id = Column(Integer, ForeignKey("casamentos.id", ondelete="CASCADE"))
    nome_grupo = Column(String(100), nullable=False)
    responsavel_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    confirmado = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    casamento = relationship("Casamento", back_populates="grupos")
    convidados = relationship("Convidado", back_populates="grupo")
    responsavel = relationship("Usuario")

class Convidado(Base):
    __tablename__ = "convidados"

    id = Column(Integer, primary_key=True, index=True)
    casamento_id = Column(Integer, ForeignKey("casamentos.id", ondelete="CASCADE"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=True)
    grupo_id = Column(Integer, ForeignKey("grupos_convidados.id", ondelete="CASCADE"), nullable=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    email = Column(String(100))
    qr_code = Column(String(255), unique=True)
    confirmado = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    casamento = relationship("Casamento", back_populates="convidados")
    usuario = relationship("Usuario")
    grupo = relationship("GrupoConvidados", back_populates="convidados")

class Lembrete(Base):
    __tablename__ = "lembretes"

    id = Column(Integer, primary_key=True, index=True)
    casamento_id = Column(Integer, ForeignKey("casamentos.id", ondelete="CASCADE"))
    descricao = Column(Text, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    casamento = relationship("Casamento", back_populates="lembretes")

class Foto(Base):
    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True, index=True)
    casamento_id = Column(Integer, ForeignKey("casamentos.id", ondelete="CASCADE"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    url_foto = Column(Text, nullable=False)
    tipo = Column(phototype, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    casamento = relationship("Casamento", back_populates="fotos")
    usuario = relationship("Usuario", back_populates="fotos")

class Orcamento(Base):
    __tablename__ = "orcamento"

    id = Column(Integer, primary_key=True, index=True)
    casamento_id = Column(Integer, ForeignKey("casamentos.id", ondelete="CASCADE"))
    descricao = Column(String(255), nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    pago = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    casamento = relationship("Casamento", back_populates="orcamentos") 