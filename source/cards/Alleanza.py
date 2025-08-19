class Alleanza:
    def __init__(self, nome, bonus, restrizioni=None):
        self.nome = nome
        self.bonus = bonus  # dict o descrizione di bonus dati
        self.restrizioni = restrizioni or []
