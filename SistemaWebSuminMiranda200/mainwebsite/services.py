from .models import Orden, Inventario, Cliente, Proveedor, Destino


class OrdenServ(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(OrdenServ, cls).__new__(cls)
    return cls.instance
  
  @staticmethod
  def getAll():
    return Orden.objects.all()
  
   