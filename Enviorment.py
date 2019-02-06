from Genome import *

class Enviorment():
    def __init__(self, input, output, top, cut, randomness, inno=0, carry = 1):

        self.randomness = randomness
        self.top = top
        self.population = []
        self.global_inno = inno
        self.input = input # Shape of original genome
        self.output = output
        self.prev_innovation = [[], []]
        self.cut = cut
        self.species = []
        self.carry = carry

    def create(self, nr):
        new = []
        for i in range(nr):
            new.append(Genome(self.input, self.output, [identity], self.get_innovation))
        return self.speciate(new)

    def generation(self):
        species_new = []
        species_surv = []
        averages = []
        # Raw scoring
        for s in self.species:
            for g in s:
                g.score = (g.score * random.gauss(1, self.randomness))/len(s)
            s.sort(key=Genome.get_score())
            species_new.append(s[:self.carry])
            species_surv.append(s[:int(self.top * len(s))])
            averages.append(sum(g.score for g in s))

        self.species = species_new
        # Allocating and creating offspring
        total = sum(averages)
        new_genome_nr = sum(len(s) for s in self.species) - (self.carry * len(self.species))
        for a, s in zip(averages, species_surv):
            allocated = round((a/total) * new_genome_nr)
            new_genome = self._repop(s, allocated)
            self.speciate(new_genome)
        return self.species

    def speciate(self, new):
        for g in new:
            found = False
            for s in self.species:
                g2 = s[0]
                if self.distance(g, g2) < self.cut:
                    s.append(g)
                    found = True
                    break
            if not found:
                self.species.append([g])
        return self.species

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
                exess_disjoint += 1 # TODO currently only getting disjoint and exess genes of g1
        return c1 * (exess_disjoint/max(len(g1.genes), len(g2.genes))) + c2 * (sum(weights)/len(weights))

    def _repop(self, s, nr):
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



