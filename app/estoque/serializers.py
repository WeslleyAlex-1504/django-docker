from .models import Fruta


class FrutaSerializer:
    @staticmethod
    def to_dict(fruta: Fruta):
        return {
            'id': str(fruta.id),
            'nome': fruta.nome,
            'tipo': fruta.tipo,
            'data_validade': fruta.data_validade.isoformat(),
            'quantidade_estoque': fruta.quantidade_estoque,
            'status': fruta.status,
            'is_vencida': fruta.is_vencida(),
            'created_at': fruta.created_at.isoformat(),
            'updated_at': fruta.updated_at.isoformat(),
        }
