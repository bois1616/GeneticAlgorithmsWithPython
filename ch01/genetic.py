# File: genetic.py
#    from chapter 1 of _Genetic Algorithms with Python_
#
# Author: Clinton Sheppard <fluentcoder@gmail.com>
# Copyright (c) 2016 Clinton Sheppard
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.

import random
import statistics
import sys
import time

class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness
        
        
def _generate_parent(length: int, geneSet: str, fnGetFitness: "function") -> Chromosome:
    genes = []
    while len(genes) < length:
        # Since the target might be longer than geneSet, we need to 
        # determine the largest chunk we can create with one call to
        # random.sample. Obviously, this sample size  becomes smaller as 
        # genes becomes larger
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    genes = ''.join(genes)
    fitness = fnGetFitness(genes)
    return Chromosome(genes, fitness)


def _mutate(parent: str, geneSet: str, fnGetFitness: "function") -> Chromosome:
    index = random.randrange(0, len(parent.Genes))
    childGenes = list(parent.Genes)
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    genes = ''.join(childGenes)
    fitness = fnGetFitness(genes)
    return Chromosome(genes, fitness)


def get_best(fnGetFitness, targetLen, optimalFitness, geneSet, fnDisplay):
    random.seed()
    bestParent = _generate_parent(targetLen, geneSet, fnGetFitness)
    fnDisplay(bestParent)
    # accidentially hit the target with first try?
    if bestParent.Fitness >= optimalFitness:
        return bestParent
    
    while True:
        child = _mutate(bestParent, geneSet, fnGetFitness)
        if bestParent.Fitness >= child.Fitness:
            continue
        fnDisplay(child)
        if child.Fitness >= optimalFitness:
            return child
        bestParent = child


class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = None
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print(f"{i+1} {mean:3.2f} {statistics.stdev(timings, mean) if i > 1 else 0:3.2f}")
 