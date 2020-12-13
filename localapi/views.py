import time

from app.utils import log_webservice
from shop.models import Product
from shop.models import SizeProductStock
from shop.utils import split_reference

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class UpdateInventoryView(APIView):
    """Para consumir este servicio en una máquina tipo UNIX puede invocar
    algo como:

    curl -X POST -d '{"inventory_list": [{"reference": "ABC", \
    "quantity": 10}, {"reference": "DEF", "quantity": 20}]}' \
    -H 'Content-Type: application/json; indent=4; Accept: application/json'\
     https://gecolsa.com/api/update_inventory/SU_LLAVE_DE_INVENTARIO/

     SU_LLAVE_DE_INVENTARIO debe coincidir tanto en la configuración del
     portal como desde su cliente o programa para hacer la actualización del
     inventario, se espera que únicamente envíe aquellos items que hayan
     cambiado recientemente en cuanto a su inventario.
     """

    def post(self, request, key):
        from constance import config
        start_time = time.time()
        category = 'actualización de inventario'
        result = {
            "updated_objects": [],
            "errors": [],
        }

        if key != config.WEBSERVICE_KEY:
            result['errors'].append('No authorized')
            log_webservice(
                request,
                start_time,
                request.data,
                category,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        if 'inventory_list' not in request.data:
            result['errors'].append(
                'make sure you use a string like '
                '{"inventory_list":[{"quantity":10,'
                '"reference":"7SV 715325-EAS"}]}'
            )
            log_webservice(
                request,
                start_time,
                request.data,
                category,
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                answer=result,
            )
            return Response(result, status=status.HTTP_412_PRECONDITION_FAILED)

        line_no = 1
        for item in request.data['inventory_list']:
            if 'quantity' not in item or 'reference' not in item:
                result['errors'].append(
                    '{0}: {1} -> Nonconforming'.format(
                        line_no,
                        item,
                    )
                )
                line_no += 1
                continue
            reference, size = split_reference(item['reference'])
            if size is None:
                updated = Product.objects.filter(
                    reference=reference
                ).update(
                    quantity=item['quantity']
                )
                if updated:
                    result['updated_objects'].append({
                        'reference': item['reference'],
                        'quantity': item['quantity'],
                    })
                else:
                    result['errors'].append(
                        '{0}: There is no product with reference {1}'.format(
                            line_no,
                            item['reference'],
                        )
                    )
            else:
                updated = SizeProductStock.objects.filter(
                    product__reference=reference,
                    name=size,
                ).update(
                    quantity=item['quantity']
                )
                if updated:
                    result['updated_objects'].append({
                        'reference': item['reference'],
                        'quantity': item['quantity'],
                    })
                else:
                    result['errors'].append(
                        '{0}: There is no product with reference {1}'.format(
                            line_no,
                            item['reference'],
                        )
                    )
            line_no += 1

        # We make sure that a product with sizes only have quantity in the
        # sizes
        Product.objects.filter(sizestock__isnull=False).update(quantity=0)

        # Deactivating products with no photograph
        Product.objects.filter(
            gallery__isnull=True,
        ).update(is_active=False)

        # Deactivating products with no stock
        Product.objects.filter(
            sizestock__isnull=True,
            quantity=0
        ).update(is_active=False)

        # Deactivating sized products with no stock
        Product.objects.filter(
            sizestock__isnull=False,
        ).exclude(sizestock__quantity__gt=0).distinct().update(is_active=False)

        # Activating nonsized products with stock
        Product.objects.filter(
            sizestock__isnull=True,
            gallery__isnull=False,
            quantity__gt=0,
            is_active=False,
        ).update(is_active=True)

        # Activating sized products with stock and gallery
        Product.objects.filter(
            gallery__is_active=True,
            sizestock__quantity__gt=0,
            is_active=False,
        ).distinct().update(is_active=True)

        nactive = Product.objects.filter(is_active=True).count()

        to_record = result.copy()
        to_record['active_products'] = nactive

        log_webservice(
            request,
            start_time,
            request.data,
            category,
            status_code=status.HTTP_200_OK,
            answer=to_record,
        )
        return Response(result)
