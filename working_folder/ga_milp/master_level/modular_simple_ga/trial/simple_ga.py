from fuzzywuzzy import fuzz
import random 
import string as st

##Representatioon an individual (Agent)
class Agent:
    def __init__(self, length):
        ##string.letters returns a list of letters from english alphabet
        ##randomly pick alphabets until the 'length is matched'
        self.string = ''.join(random.choice(st.ascii_letters) for _ in range(length))
        ##-1 as evaluation has not yet taken place in the object
        self.fitness = -1 
        
    def  __str__(self):
        
        return 'String: ' + str(self.string) + ' Fitness: ' + str(self.fitness)

##Storing global data 
in_str = None 
in_str_len = None 
population = 20 
generations = 1000000

def ga():
    
    ##initialize the population 
    agents = init_agents(population, in_str_len)
    
    for generation in range(generations):
        
        print('Generation: ' + str(generation))
        agents = fitness(agents)
        agents = selection(agents)
        agents = crossover(agents)
        agents = mutation(agents)
        
        ##Stopping criterion 
#        if any(agent.fitness >= 99 for agent in agents):
#            print('Treshold met!')
#            exit(0)

##Functions
def init_agents(population, length):
    return [Agent(length) for _ in range(population)]
            
def fitness(agents):
    for agent in agents:
        agent.fitness = fuzz.ratio(agent.string, in_str)
    return agents
    
def selection(agents):
    ##Sorted by the fitness values in reverse order 
    agents = sorted(agents, key = lambda agent: agent.fitness, reverse = True)
    print ('\n'.join(map(str, agents)))
    ##use array slicing, taking only the top 20 percent, the top 
    agents = agents[:int(0.2 * len(agents))]

    return agents
                    
def crossover(agents):
    offspring = []
    print(len(agents))
    print(int((population - len(agents)) / 2))
    
    for _ in range(int((population - len(agents)) / 2)):
        
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        child1 = Agent(in_str_len)
        child2 = Agent(in_str_len)
        split = random.randint(0, in_str_len)
        child1.string = parent1.string[0:split] + parent2.string[split:in_str_len]
        child2.string = parent2.string[0:split] + parent1.string[split:in_str_len]

        offspring.append(child1)
        offspring.append(child2)
    
    agents.extend(offspring)
    print(len(offspring))
    print(len(agents))
    return agents 

##To add diversity, crossover will end up converging onto a solution 
def mutation(agents):
    
    for agent in agents:
        
        for idx, param in enumerate(agent.string):
            if random.uniform(0.0, 1.0) <= 0.1:
                agent.string = agent.string[0:idx] + random.choice(st.ascii_letters) + agent.string[idx+1 : in_str_len]

    return agents

##refering to the module we are in, the file itself 
from datetime import datetime
startTime = datetime.now()

if __name__ == '__main__':
    in_str = 'TroySquillaci'
    in_str_len = len(in_str)
    ga()
    
    print(datetime.now() - startTime)
    
        
        