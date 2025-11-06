from api.models.pet import Pet
from api.models.statusPet import StatusPet, Status
from api.models.preferenciaAdotante import PreferenciaAdotante
from api.models.adotante import Adotante
from django.db.models import Case, When, Value, F
from django.db.models.fields import IntegerField


class HeuristicaService:
    def aplicar_heuristica(self, id_adotante):
        try:
            adotante = Adotante.objects.get(id=id_adotante)
        except Adotante.DoesNotExist:
            print("Adotante não encontrado.")
            return []

        preferencias = PreferenciaAdotante.objects.filter(
            adotante=adotante, preferencia_ativa=True
        ).first()

        if not preferencias:
            print("Preferências do adotante não encontradas ou inativas.")
            return []
        
        status_pet_disponivel = StatusPet.objects.get(status=Status.DISPONIVEL)

        filtros = {"especie": preferencias.preferencia_especie, "status_pet": status_pet_disponivel}

        max_score = 150

        if not preferencias.possui_tempo:
            filtros["cuidados_constantes"] = False
            max_score -= 10
            print("Filtro de cuidados constantes aplicado.")

        if not preferencias.aceita_doenca_cronica:
            filtros["doenca_cronica"] = False
            max_score -= 10
            print("Filtro de doença crônica aplicado.")

        if preferencias.possui_outros_animais:
            filtros["amigavel_outros_animais"] = True
            print("Filtro de amigável com outros animais aplicado.")

        if not preferencias.aceita_necessidades_especiais:
            filtros["necessidades_especiais"] = False
            max_score -= 10
            print("Filtro de necessidades especiais aplicado.")

        print(f"Filtros aplicados: {filtros}")

        pets_filtrados = Pet.objects.filter(**filtros)
        
        
        pets_pontuados = []
        for pet in pets_filtrados:
            score = 0
            
            if preferencias.preferencia_porte == pet.porte:
                score += 40
            elif preferencias.preferencia_porte == 'Médio' and pet.porte in ['Pequeno', 'Grande']:
                score += 15
            elif preferencias.preferencia_porte in ['Pequeno', 'Grande'] and pet.porte == 'Médio':
                score += 15
            elif preferencias.preferencia_porte == 'Muito Grande' and pet.porte == 'Grande':
                score += 15

            if preferencias.preferencia_idade == pet.idade:
                score += 40
            if preferencias.preferencia_idade == 2 and pet.idade in [1, 3]:
                score += 15
            if preferencias.preferencia_idade in [1, 3] and pet.idade == 2:
                score += 15
            
            if preferencias.preferencia_sexo == pet.sexo:
                score += 20
            
            if preferencias.preferencia_raca == pet.raca: # Precisa melhorar essa parte para considerar raças similares
                score += 20
            
            # Boost para pets com necessidades especiais ou doenças crônicas quando o adotante aceita
            if pet.necessidades_especiais:
                score += 10
            if pet.doenca_cronica:
                score += 10
            if pet.cuidados_constantes:
                score += 10

            # normaliza a pontuação
            score = score / max_score * 100

            pets_pontuados.append({"pet": pet, "score": score})
        
        pets_ordenados = sorted(pets_pontuados, key=lambda p: p['score'], reverse=True)
        
        return pets_ordenados