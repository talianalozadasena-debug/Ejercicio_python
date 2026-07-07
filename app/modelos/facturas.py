from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship
from .clientes import Cliente, ClienteLeer
from .transacciones import Transaccion
from datetime import datetime


class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def vr_total(self) -> float:
        total_factura = 0.0

        # Si el modelo no tiene la relación transacciones
        # (por ejemplo FacturaCrear o FacturaEditar),
        # simplemente retorna 0.
        if not hasattr(self, "transacciones"):
            return total_factura

        if self.transacciones is None:
            return total_factura

        for transaccion in self.transacciones:
            total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")

    cliente: Cliente = Relationship(back_populates="factura")
    transacciones: list[Transaccion] = Relationship(back_populates="factura")


class FacturaLeer(FacturaBase):
    id: int
    cliente: ClienteLeer


class FacturaLeerCompuesta(FacturaLeer):
    transacciones: list[Transaccion] = []