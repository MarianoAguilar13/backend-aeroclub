from app.models.transacciones import Transacciones
from app.models.tipo_pago import TipoPago
from app import db
from flask import jsonify

# Una Cuenta Corriente no se deberá deshabilitar, a su vez tampoco se podrá crear, se inicializará con el valor de una transacción...

class TransaccionesController:

    def _init_(self):
        pass

    def __chequearTipoPago(self,tipoPago):

        tipos=["Cheque","Efectivo", "Transferencia"] 

        print(f"__chequearTipoPago tipoPago entro: {tipoPago}")

        resultado = [x for x in tipos if x==tipoPago]

        if resultado:
            return True

        else:
            return False
        
    
    def crearTransaccion(self, monto, fecha, motivo,tipoPago,idCuentaCorriente):

            try:
                #chequeando el tipo de pago 
                if self.__chequearTipoPago(self.__chequearTipoPago,tipoPago):

                    #aca me traigo el tipoPago para obtener su id    
                    tipoPagoDictionary = db.session.query(TipoPago).filter_by(tipo=tipoPago).first()

                    transaccion = Transacciones(None,monto,fecha,motivo,tipoPagoDictionary.id_tipo_pago,idCuentaCorriente)
                    
                    db.session.add(transaccion)
                    db.session.commit()

                    return transaccion

                else:
                    return False  
              
            except Exception as ex:
                print(ex)
                return False

    #Esta es solo de prueba para ver si funciona lo de borrar en cascada
    def eliminarTransaccion(self, id):

            try:
                    #chequeando el tipo de pago 
              
                    transaccion = db.session.query(Transacciones).filter_by(id_transacciones=id).first()
                    
                    db.session.delete(transaccion)
                    db.session.commit()

                    return True 
              
            except Exception as ex:
                print(ex)
                return False
            
    def obtenerTransacciones(self):

        try:
            transacciones = Transacciones.query.all()
            transaccion_list = []

            for transaccion in transacciones:
                
                transaccion_data = {
                    'id_transacciones': transaccion.id_transacciones,
                    'monto': transaccion.monto,
                    'fecha': transaccion.fecha,
                    'motivo': transaccion.motivo,
                    'tipo_pago_id': transaccion.tipo_pago_id,
                    'cuenta_corriente_id': transaccion.cuenta_corriente_id,
                }
                transaccion_list.append(transaccion_data)
            return transaccion_list
        
        except Exception as ex:
                print(ex)
                return False