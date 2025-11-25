import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.db import connection

# Cliente a eliminar
cliente_id = 1

try:
    with connection.cursor() as cursor:
        # Verificar cliente
        cursor.execute("SELECT nombre, email FROM clientes WHERE idCliente = %s", [cliente_id])
        cliente = cursor.fetchone()
        
        if not cliente:
            print(f"Cliente con ID {cliente_id} no existe")
            sys.exit()
        
        print(f"Cliente encontrado: {cliente[0]} - {cliente[1]}")
        
        # Obtener pedidos del cliente
        cursor.execute("SELECT idPedido FROM pedidos WHERE idCliente = %s", [cliente_id])
        pedidos = cursor.fetchall()
        pedido_ids = [p[0] for p in pedidos]
        print(f"Pedidos encontrados: {len(pedido_ids)}")
        
        if pedido_ids:
            placeholders = ','.join(['%s']*len(pedido_ids))
            
            # Eliminar notificaciones de problema
            cursor.execute(f"DELETE FROM notificaciones_problema WHERE idPedido IN ({placeholders})", pedido_ids)
            print(f"Notificaciones problema eliminadas: {cursor.rowcount}")
            
            # Eliminar facturas
            cursor.execute(f"DELETE FROM facturas WHERE idPedido IN ({placeholders})", pedido_ids)
            print(f"Facturas eliminadas: {cursor.rowcount}")
            
            # Eliminar detalles de pedidos
            cursor.execute(f"DELETE FROM detallepedido WHERE idPedido IN ({placeholders})", pedido_ids)
            print(f"Detalles de pedidos eliminados: {cursor.rowcount}")
            
            # Eliminar pedidos
            cursor.execute("DELETE FROM pedidos WHERE idCliente = %s", [cliente_id])
            print(f"Pedidos eliminados: {cursor.rowcount}")
        
        # Eliminar usuario asociado
        cursor.execute("DELETE FROM usuarios WHERE idCliente = %s", [cliente_id])
        print(f"Usuarios eliminados: {cursor.rowcount}")
        
        # Eliminar cliente
        cursor.execute("DELETE FROM clientes WHERE idCliente = %s", [cliente_id])
        print(f"Cliente {cliente_id} eliminado exitosamente")
        
except Exception as e:
    print(f"Error: {str(e)}")
