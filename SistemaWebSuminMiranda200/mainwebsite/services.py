from .models import Orden, Inventario, Cliente, Proveedor, Destino


class OrdenServ(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(OrdenServ, cls).__new__(cls)
    return cls.instance
  
  @staticmethod
  def getAll():
    return Orden.objects.all()
  
  @staticmethod
  def get(pk):
    return Orden.objects.get(id_orden=pk)

  @staticmethod
  def insert(num_orden, fecha_emision, estado, num_factura, desc_requisicion, 
             fecha_requisicion, fecha_entrega, solicitado, tlf_solicitado, num_lote, 
             id_cliente, id_destino, id_usuario):
    nueva_orden = Orden(num_orden=num_orden, fecha_emision =fecha_emision, estado=estado, 
                        num_factura=num_factura, desc_requisicion=desc_requisicion, 
                        fecha_requisicion=fecha_requisicion, fecha_entrega=fecha_entrega, 
                        solicitado=solicitado,tlf_solicitado=tlf_solicitado, num_lote=num_lote,
                        id_cliente=id_cliente, id_destino=id_destino, id_usuario=id_usuario)
    nueva_orden.save()
  
   