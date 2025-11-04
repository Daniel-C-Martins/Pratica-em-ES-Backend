from api.models.pet import Pet
from api.models.preferenciaAdotante import PreferenciaAdotante
from api.models.adotante import Adotante
from django.db.models import Case, When, Value, F
from django.db.models.fields import IntegerField


class HeuristicaService:
    def aplicar_heuristica(self, id_adotante):
        try:
            adotante = Adotante.objects.get(id=id_adotante)
        except Adotante.DoesNotExist:
            return []

        preferencias = PreferenciaAdotante.objects.filter(
            adotante=adotante, preferencia_ativa=True
        ).first()

        if not preferencias:
            return []

        filtros = {"especie": preferencias.preferencia_especie, "status_pet": 1}

        max_score = 150

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
        if preferencias.preferencia_porte == "Médio":
            porte.append(When(porte__in=["Pequeno", "Grande"], then=Value(15)))
        elif preferencias.preferencia_porte in ["Pequeno", "Grande"]:
            porte.append(When(porte="Médio", then=Value(15)))
        elif preferencias.preferencia_porte == "Muito Grande":
            porte.append(When(porte="Grande", then=Value(15)))

        porte_score = Case(*porte, default=Value(0), output_field=IntegerField())

        idade = [
            When(idade=preferencias.preferencia_idade, then=Value(40)),
        ]
        if preferencias.preferencia_idade == 2:
            idade.append(When(idade__in=[1, 3], then=Value(15)))
        elif preferencias.preferencia_idade in [1, 3]:
            idade.append(When(idade=2, then=Value(15)))

        idade_score = Case(*idade, default=Value(0), output_field=IntegerField())

        sexo_score = Value(0, output_field=IntegerField())
        if hasattr(Pet, "sexo"):
            sexo_score = Case(
                When(sexo=preferencias.preferencia_sexo, then=Value(20)),
                default=Value(0),
                output_field=IntegerField(),
            )

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

        top_pets = pets_query[:50]

        pets_pontuados = []
        for pet in top_pets:
            print(f"Pet ID: {pet.id_pet}, Score: {pet.score}")
            pets_pontuados.append({"pet": pet, "score": round(pet.score, 2)})

        return pets_pontuados
