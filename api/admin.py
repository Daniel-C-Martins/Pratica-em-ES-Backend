from django.contrib import admin

from .models.preferenciaAdotante import PreferenciaAdotante
from .models.adocao import Adocao
from .models.adotante import Adotante
from .models.ong import Ong
from .models.pet import Pet
from .models.especiePet import EspeciePet
from .models.statusPet import StatusPet
from .models.tutor import Tutor
from .models.evento import Evento
from .models.racasPet import RacasPet

admin.site.register(Adocao)
admin.site.register(Adotante)
admin.site.register(Ong)
admin.site.register(Pet)
admin.site.register(EspeciePet)
admin.site.register(StatusPet)
admin.site.register(Tutor)
admin.site.register(Evento)
admin.site.register(RacasPet)
admin.site.register(PreferenciaAdotante)
