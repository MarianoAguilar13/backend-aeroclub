from flask import Blueprint, request, jsonify
from app.utils.Security import Security
from app.controllers.transacciones import TransaccionesController
from app.controllers.cuentaCorrienteController import cuentaCorrienteController


transacciones_bp = Blueprint('transacciones', __name__)

@transacciones_bp.route('/', methods=['GET'])
def get_transacciones(): 
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:

            transaccion_controller = TransaccionesController()
            transacciones = transaccion_controller.obtenerTransacciones()
            if transacciones:
                return jsonify({'response': transacciones, 'success': True})
            else:
                return jsonify({'message': 'ERROR', 'success': False})
                  
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ERROR', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401      

@transacciones_bp.route('/', methods=['POST'])
def create_transaccion():
    try:

        data = request.get_json()
        monto=data.get("monto")
        idUsuario=data.get("idUsuario") 
        motivo=data.get("motivo")
        tipoPago=data.get("tipoPago")
        fecha=data.get("fecha")
      
        cuentaController = cuentaCorrienteController()
        idCuenta=cuentaController.obtenerCuentaCorriente(idUsuario)
        if idCuenta:
            
            respuesta =  cuentaController.actualizar_saldo(idUsuario,monto,fecha,motivo,tipoPago)
            ## respuesta = transaccion_controller.crearTransaccion(monto, fecha, motivo,tipoPago,idCuentaCorriente)
            if respuesta:
                return jsonify({'message': 'Transaccion created successfully','success': True})
            else:
                return jsonify({'message': 'Some data is invalid','success': False})
        else:
            return jsonify({'message': 'El usuario no posee una cuenta', 'success': False})
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'An error occurred', 'success': False})

