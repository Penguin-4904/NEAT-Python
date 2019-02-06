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
        species_champ = []
        species_surv = []
        averages = []
        # Raw scoring
        for s in self.species: # TODO add method to update score of each genome
            for g in s:
                g.score = (g.score * random.gauss(1, self.randomness))/len(s)
            s.sort(key=Genome.get_score(), reverse=True)
            species_champ.append(s[:self.carry])
            species_surv.append(s[:int(self.top * len(s))])
            averages.append(sum(g.score for g in s))
        # Allocating and creating offspring
        new_population = []
        total = sum(averages)
        new_genome_nr = sum(len(s) for s in self.species)
        for i in range(len(species_surv)):
            allocated = round((averages[i]/total) * new_genome_nr)
            # if allocated is less than 1 then the species does not get added to the next generation
            new_genome = self._repop(species_surv[i], allocated - len(species_champ[i]))
            new_population += (species_champ[:allocated][i] + new_genome)
        self.species = []
        self.speciate(new_population) # TODO reset innovation tracker
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

    def distance(self, g1, g2, c1=1, c2=1): # TODO implement proper handling of c1 and c2
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
        if nr < 1:
            return []
        genome = []
        for i in range(nr):
            genome.append(self.crossover(random.choice(s), random.choice(s)))
        return genome

    def crossover(self, g1, g2):
        fit = sorted([g1, g2], key=Genome.get_score())
        fit_ratio = fit[0]/fit[1]

        return None

    def _value(self, g):
        return 0

    def get_innovation(self, in_node, out_node):

        if [in_node, out_node] not in self.prev_innovation[0]:
            self.prev_innovation[0].append([in_node, out_node])
            self.global_inno += 1
            self.prev_innovation[1].append(self.global_inno)
            return self.global_inno
        else:
            return self.prev_innovation[1][self.prev_innovation[0].index([in_node, out_node])]



