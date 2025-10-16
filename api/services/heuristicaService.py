from api.models.pet import Pet
from api.models.preferenciaAdotante import PreferenciaAdotante
from api.models.adotante import Adotante

class HeuristicaService:
    def aplicar_heuristica(self, id_adotante):
        adotante = Adotante.objects.get(id=id_adotante)

        preferencias = PreferenciaAdotante.objects.filter(adotante=adotante, preferencia_ativa=True).first()

        aceita_doenca_cronica = preferencias.aceita_doenca_cronica
        aceita_necessidades_especiais = preferencias.aceita_necessidades_especiais
        possui_outros_animais = preferencias.possui_outros_animais
        possui_tempo = preferencias.possui_tempo

        pets_recomendados = Pet.objects.filter(especie__in=preferencias.values_list("especie", flat=True))

        return pets_recomendados