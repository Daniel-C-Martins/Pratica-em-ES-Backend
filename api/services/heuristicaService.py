from api.models.pet import Pet
from api.models.statusPet import StatusPet, Status
from api.models.preferenciaAdotante import (
    PreferenciaAdotante,
    PortePet,
    IdadePet,
    SexoPet,
)
from api.models.adotante import Adotante
from api.models.adocao import Adocao, StatusAdocao
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

        filtros = {
            "especie": preferencias.preferencia_especie,
            "status_pet": status_pet_disponivel,
        }

        max_score = 130

        if not preferencias.possui_tempo:
            filtros["cuidados_constantes"] = False
            max_score -= 10

        if not preferencias.aceita_doenca_cronica:
            filtros["doenca_cronica"] = False
            max_score -= 10

        if preferencias.possui_outros_animais:
            filtros["amigavel_outros_animais"] = True

        if not preferencias.aceita_necessidades_especiais:
            filtros["necessidades_especiais"] = False
            max_score -= 10

        porte = [
            When(porte=preferencias.preferencia_porte, then=Value(40)),
        ]
        if preferencias.preferencia_porte == PortePet.MEDIO:
            porte.append(
                When(porte__in=[PortePet.PEQUENO, PortePet.GRANDE], then=Value(15))
            )
        elif preferencias.preferencia_porte in [PortePet.PEQUENO, PortePet.GRANDE]:
            porte.append(When(porte=PortePet.MEDIO, then=Value(15)))
        elif preferencias.preferencia_porte == PortePet.MUITO_GRANDE:
            porte.append(When(porte=PortePet.GRANDE, then=Value(15)))
        elif preferencias.preferencia_porte == PortePet.INDIFERENTE:
            porte.append(
                When(
                    porte__in=[
                        PortePet.PEQUENO,
                        PortePet.MEDIO,
                        PortePet.GRANDE,
                        PortePet.MUITO_GRANDE,
                    ],
                    then=Value(20),
                )
            )

        porte_score = Case(*porte, default=Value(0), output_field=IntegerField())

        idade = [
            When(idade=preferencias.preferencia_idade, then=Value(40)),
        ]
        if preferencias.preferencia_idade == IdadePet.ADULTO:
            idade.append(
                When(idade__in=[IdadePet.FILHOTE, IdadePet.IDOSO], then=Value(15))
            )
        elif preferencias.preferencia_idade in [IdadePet.FILHOTE, IdadePet.IDOSO]:
            idade.append(When(idade=IdadePet.ADULTO, then=Value(15)))
        elif preferencias.preferencia_idade == IdadePet.INDIFERENTE:
            idade.append(
                When(
                    idade__in=[IdadePet.FILHOTE, IdadePet.ADULTO, IdadePet.IDOSO],
                    then=Value(20),
                )
            )

        idade_score = Case(*idade, default=Value(0), output_field=IntegerField())

        sexo = [
            When(sexo=preferencias.preferencia_sexo, then=Value(30)),
        ]
        if preferencias.preferencia_sexo == SexoPet.INDIFERENTE:
            sexo.append(When(sexo__in=[SexoPet.M, SexoPet.F], then=Value(15)))

        sexo_score = Case(*sexo, default=Value(0), output_field=IntegerField())

        raca_score = Value(0, output_field=IntegerField())
        if hasattr(Pet, "raca"):
            raca_score = Case(
                When(raca=preferencias.preferencia_raca, then=Value(20)),
                default=Value(0),
                output_field=IntegerField(),
            )

        boost_score = Value(0)
        boost_score += Case(
            When(necessidades_especiais=True, then=Value(10)),
            default=Value(0),
            output_field=IntegerField(),
        )
        boost_score += Case(
            When(doenca_cronica=True, then=Value(10)),
            default=Value(0),
            output_field=IntegerField(),
        )
        boost_score += Case(
            When(cuidados_constantes=True, then=Value(10)),
            default=Value(0),
            output_field=IntegerField(),
        )

        pets_query = (
            Pet.objects.filter(**filtros)
            .annotate(
                score_bruto=(
                    porte_score + idade_score + sexo_score + raca_score + boost_score
                ),
                score=(F("score_bruto") * 100.0 / Value(max_score)),
            )
            .order_by("-score")
        )

        top_pets = pets_query[:10]
        pets_pontuados = []
        for pet in top_pets:
            # garante que o score já venha arredondado pro serializer
            pet.score = round(pet.score, 0)
            if pet.score > 100:
                pet.score = 100
            print(f"Pet ID: {pet.id_pet}, Nome: {pet.nome}, Score: {pet.score}")
            pets_pontuados.append(pet)

        return pets_pontuados
