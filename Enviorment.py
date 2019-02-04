from Genome import *

class Enviorment():
    def __init__(self, input, output, top, cut, randomness, inno=0):

        self.randomness = randomness
        self.top = top
        self.population = []
        self.global_inno = inno
        self.input = input # Shape of original genome
        self.output = output
        self.prev_innovation = [[], []]
        self.cut = cut
        self.species = []

    def create(self, nr):
        for i in range(nr):
            self.population.append(Genome(self.input, self.output, [identity], self.get_innovation))
        return self.population

    def generation(self):
        for s in self.species:
            self._score_species(s)
            for g in s:
                g.score = g.score * random.gauss(1, self.randomness) # TODO This does not actually follow the Paper. Fix or decide to not follow paper.

        self.population.sort(key=Genome.get_score())
        survive = self.population[:self.top]
        return survive

    def speciate(self):
        for g in self.population:
            for s in self.species:
                g2 = s[0]
                if self.distance(g, g2) < self.cut:
                    s.append(g)
                    break

    def distance(self, g1, g2, c1=1, c2=1): # TODO implement proper handeling of c1 and c2
        weights = []
        exess_disjoint = 0
        for gene1 in g1.genes:
            yes = False
            for gene2 in g2.genes:
                if gene1.innovation == gene2.innovation:
                    weights.append(gene1.weight - gene2.weight)
                    yes = True
                    break
            if not yes:
                exess_disjoint += 1
        return c1 * (exess_disjoint/max(len(g1.genes), len(g2.genes))) + c2 * (sum(weights)/len(weights))
    def _repop(self):
        return None

    def _score_species(self, s):
        return None

    def _value(self):
        return 0

    def get_innovation(self, in_node, out_node):

        if [in_node, out_node] not in self.prev_innovation[0]:
            self.prev_innovation[0].append([in_node, out_node])
            self.global_inno += 1
            self.prev_innovation[1].append(self.global_inno)
            return self.global_inno
        else:
            return self.prev_innovation[1][self.prev_innovation[0].index([in_node, out_node])]



