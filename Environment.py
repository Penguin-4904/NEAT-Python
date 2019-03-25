import math

from Genome import *


class Environment:
    def __init__(self, game, fun=sig, keep=(1/2), dist=None, randomness=0, inno=0, carry=1,
                 mutation_rates=None, species_nr=10):
        if dist is None:
            dist = [1 / 2, 1, 1]
        if mutation_rates is None:
            mutation_rates = [0.8, 0.05, 0.01]
        self.game = game
        self.function = fun
        self.randomness = randomness
        self.keep = keep
        self.population = 0
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
        self.species_nr = species_nr
        self.largest_dist = 0
        self.large_genome_size = 20  # the size at which a genome is considered "large"

        self.staleness = []
        self.max_staleness = 40
        self.max_score = []

    def create(self, nr):
        new = []
        for i in range(nr):
            new.append(Genome(self.input, self.output, self.function, self.get_innovation))
            new[-1].complete_connect()
        self.species = self.speciate(new, [new[-1]])
        self.population = nr
        return True

    def generation(self, replay=None):
        if replay is None:
            replay = [0, 0]
        species_champ = []
        species_surv = []
        averages = []
        old_species = []
        # Raw scoring
        self.staleness += ((len(self.species) - len(self.staleness)) * [0])
        self.max_score += ((len(self.species) - len(self.max_score)) * [0])
        for s in self.species:
            i = self.species.index(s)
            for g in s:
                g.score = (self.score_genome(g) * random.gauss(1, self.randomness)) / len(s)
            s.sort(key=lambda x: x.score, reverse=True)
            old_species.append(copy.deepcopy(s))
            # species_champ.append(s[:self.carry])
            # species_surv.append(s[:math.ceil(self.keep * len(s))])
            # averages.append(sum(g.score for g in s))

            if s[0].score >= self.max_score[i]:
                self.staleness[i] = 0
                self.max_score[i] = s[0].score
            else:
                self.staleness[i] += 1

            if (not (self.staleness[i] > self.max_staleness)) or len(self.species) <= 1:
                species_champ.append(s[:self.carry])
                species_surv.append(s[:math.ceil(self.keep * len(s))])
                averages.append(sum(g.score for g in s))
            else:
                self.max_score.pop(i)
                self.staleness.pop(i)
                self.species.pop(i)

        # Checking "Staleness"

        # Allocating and creating offspring
        new_population = []
        self.prev_innovation = [[], []]
        total = sum(averages)
        new_genome_nr = self.population
        for i in range(len(species_surv)):
            allocated = round((averages[i] / total) * new_genome_nr)
            # if allocated is less than 1 then the species does not get added to the next generation
            new_genome = self._repop(species_surv[i], allocated - len(species_champ[i]))
            new_population += (species_champ[i][:allocated] + new_genome)

        self.species = self.speciate(new_population, [s[0] for s in species_surv])
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

    def speciate(self, new, reps):
        new_species = [[] for _ in range(len(reps))]
        for g in new:
            found = False
            for i in range(len(reps)):
                if self.distance(g, reps[i]) < self.dist:
                    new_species[i].append(g)
                    found = True
                    break
            if not found:
                new_species.append([g])

        return list(filter(lambda x: False if len(x) < 1 else True, new_species))

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
        return self.c1 * (exess_disjoint / max(len(g1.genes) - self.large_genome_size,
                                               len(g2.genes) - self.large_genome_size, 1)) \
               + self.c2 * (sum(weights) / len(weights))

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

        for g in fit[0].genes:
            if g.innovation not in innovation_nrs and random.random() < fit_ratio:
                new_genes.append(copy.copy(g))
                innovation_nrs.append(g.innovation)

        new_genome._insert_layer(1, [])
        for g in new_genes:
            while g.in_node > len(new_genome.nodes) - 1:
                new_genome.nodes.append(Node(self.function))
                new_genome.layers[1].append(new_genome.nodes[-1])
            while g.out_node > len(new_genome.nodes) - 1:
                new_genome.nodes.append(Node(self.function))
                new_genome.layers[1].append(new_genome.nodes[-1])
            if not g.enabled and random.random() > .75:
                g.enable()
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
