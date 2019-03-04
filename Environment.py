from Genome import *


class Environment:
    def __init__(self, game, fun=sig, keep=1, dist=None, randomness=0, inno=0, carry=1,
                 mutation_rates=None):
        if dist is None:
            dist = [1 / 2, 1, 1]
        if mutation_rates is None:
            mutation_rates = [0.8, 0.05, 0.01]
        self.game = game
        self.function = fun
        self.randomness = randomness
        self.keep = keep
        self.population = []
        self.global_inno = inno
        self.input = game.input_size
        self.output = game.output_size
        self.prev_innovation = [[], []]
        self.dist = dist[0]
        self.c1 = dist[1]
        self.c2 = dist[2]
        self.species = []
        self.carry = carry
        self.mutation_rates = mutation_rates
        self.generation_num = 0

    def create(self, nr):
        new = []
        for i in range(nr):
            new.append(Genome(self.input, self.output, self.function, self.get_innovation))
            new[-1].complete_connect()
        return self.speciate(new)

    def generation(self, replay=None):
        if replay is None:
            replay = [0, 0]
        species_champ = []
        species_surv = []
        averages = []
        # Raw scoring
        for s in self.species:
            for g in s:
                g.score = (self.score_genome(g) * random.gauss(1, self.randomness)) / len(s)
            s.sort(key=lambda x: x.score, reverse=True)
            species_champ.append(s[:self.carry])
            species_surv.append(s[:int(self.keep * len(s))])
            averages.append(sum(g.score for g in s))
        # Allocating and creating offspring
        new_population = []
        self.prev_innovation = [[], []]
        old_species = self.species
        total = sum(averages)
        new_genome_nr = sum(len(s) for s in self.species)
        for i in range(len(species_surv)):
            allocated = round((averages[i] / total) * new_genome_nr)
            # if allocated is less than 1 then the species does not get added to the next generation
            new_genome = self._repop(species_surv[i], allocated - len(species_champ[i]))
            new_population += (species_champ[:allocated][i] + new_genome)
        self.species = []
        self.speciate(new_population)
        self.generation_num += 1
        # Returning things for replay.
        if replay[0] == 0:  # return only top species
            if replay[1] == 0:  # Only top player
                return sorted(species_champ, key=lambda x: x[0].score, reverse=True)[0][0]
            if replay[1] == 1:  # all Champions
                return sorted(species_champ, key=lambda x: x[0].score, reverse=True)[0]
            if replay[1] == 2:  # all survivors
                return sorted(species_surv, key=lambda x: x[0].score, reverse=True)[0]
            if replay[1] == 3:  # whole species
                return sorted(old_species, key=lambda x: x[0].score, reverse=True)[0]

        if replay[0] == 1:  # all species
            if replay[1] == 0:  # Only top player
                return [s[0] for s in sorted(species_champ, key=lambda x: x[0].score, reverse=True)]
            if replay[1] == 1:  # all Champions
                return sorted(species_champ, key=lambda x: x[0].score, reverse=True)
            if replay[1] == 2:  # all survivors
                return sorted(species_surv, key=lambda x: x[0].score, reverse=True)
            if replay[1] == 3:  # whole species
                return sorted(old_species, key=lambda x: x[0].score, reverse=True)
        else:
            return None

    def score_genome(self, g):
        score, frames = self.game.run_genome(g, save_replay=True)
        g.last_play = frames
        return score

    def speciate(self, new):
        for g in new:
            found = False
            for s in self.species:
                g2 = s[0]
                if self.distance(g, g2) < self.dist:
                    s.append(g)
                    found = True
                    break
            if not found:
                self.species.append([g])
        return self.species

    def distance(self, g1, g2):
        weights = []
        exess_disjoint = 0
        for inno1 in g1.innovation_nrs:
            if inno1 in g2.innovation_nrs:
                weights.append(abs(
                    g1.genes[g1.innovation_nrs.index(inno1)].weight - g2.genes[g2.innovation_nrs.index(inno1)].weight))
            else:
                exess_disjoint += 1
        for inno2 in g2.innovation_nrs:
            if inno2 not in g1.innovation_nrs:
                exess_disjoint += 1
        if len(weights) == 0:
            return self.c1 * (exess_disjoint / max(len(g1.genes), len(g2.genes)))
        return self.c1 * (exess_disjoint / max(len(g1.genes), len(g2.genes))) + self.c2 * (sum(weights) / len(weights))

    def _repop(self, s, nr):
        if nr < 1:
            return []
        genome = []
        for i in range(nr):
            genome.append(self.crossover(random.choice(s), random.choice(s)))
        return genome

    def crossover(self, g1, g2):
        fit = sorted([g1, g2], key=lambda genome: genome.score)
        fit_ratio = fit[0].score / (fit[1].score + fit[0].score)
        new_genome = Genome(self.input, self.output, self.function, self.get_innovation)
        # lining up genes

        genome_pairs = []
        for i1, g1 in enumerate(fit[0].genes):
            for i2, g2 in enumerate(fit[1].genes):
                if g1.innovation == g2.innovation:
                    genome_pairs.append([i1, i2])
                    break

        new_genes = []
        innovation_nrs = []
        for p in genome_pairs:
            if random.random() > fit_ratio:
                new_genes.append(copy.copy(fit[1].genes[p[1]]))
                innovation_nrs.append(fit[1].genes[p[1]].innovation)
            else:
                new_genes.append(copy.copy(fit[0].genes[p[0]]))
                innovation_nrs.append(fit[0].genes[p[0]].innovation)

        for g in fit[1].genes:
            if g.innovation not in innovation_nrs and random.random() > fit_ratio:
                new_genes.append(copy.copy(g))
                innovation_nrs.append(g.innovation)

        new_genome._insert_layer(1, [])
        for g in fit[0].genes:
            if g.innovation not in innovation_nrs and random.random() < fit_ratio:
                new_genes.append(copy.copy(g))
                innovation_nrs.append(g.innovation)

        for g in new_genes:
            while g.in_node > len(new_genome.nodes) - 1:
                new_genome.nodes.append(Node(self.function))
                new_genome.layers[1].append(new_genome.nodes[-1])
            while g.out_node > len(new_genome.nodes) - 1:
                new_genome.nodes.append(Node(self.function))
                new_genome.layers[1].append(new_genome.nodes[-1])
            new_genome._add_gene(g)
        new_genome.relayer()
        new_genome.mutate(self.mutation_rates[0], self.mutation_rates[1], self.mutation_rates[2])
        return new_genome

    def get_innovation(self, in_node, out_node):

        if [in_node, out_node] not in self.prev_innovation[0]:
            self.prev_innovation[0].append([in_node, out_node])
            self.global_inno += 1
            self.prev_innovation[1].append(self.global_inno)
            return self.global_inno
        else:
            return self.prev_innovation[1][self.prev_innovation[0].index([in_node, out_node])]
