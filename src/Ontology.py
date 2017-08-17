import sys
from queue import Queue

__author__ = "Pierre Monnin"


class Ontology:
    def __init__(self, class_to_index, index_to_class, class_parents, class_children):
        self._class_to_index = class_to_index
        self._index_to_class = index_to_class
        self._class_parents = class_parents
        self._class_children = class_children

    def get_statistics(self, cycles_computation):
        statistics = dict()

        # Number of classes
        statistics["classes-number"] = len(self._class_to_index)
        print("\rComputing number of classes 100%\t\t")

        # Number of top level classes
        statistics["top-level-classes"] = 0
        top_level_classes = []
        for i in range(0, len(self._class_to_index)):
            sys.stdout.write("\rComputing top level classes %i %%\t\t" % (i * 100.0 / len(self._class_to_index)))
            sys.stdout.flush()
            if len(self._class_parents[i]) == 0:
                statistics["top-level-classes"] += 1
                top_level_classes.append(i)

        print("\rComputing top level classes 100 %\t\t")

        # Number of asserted subsumptions
        statistics["asserted-subsumptions-number"] = 0
        for i in range(0, len(self._class_to_index)):
            sys.stdout.write("\rComputing asserted subsumptions %i %%\t\t" % (i * 100.0 / len(self._class_to_index)))
            sys.stdout.flush()
            statistics["asserted-subsumptions-number"] += len(self._class_parents[i])

        print("\rComputing asserted subsumptions 100 %\t\t")

        # Number of inferred subsumptions (and classes in cycles at the same time)
        statistics["inferred-subsumptions-number"] = 0
        classes_seen_in_cycles = [False]*len(self._class_to_index)
        for i in range(0, len(self._class_to_index)):
            sys.stdout.write("\rComputing inferred subsumptions %i %%\t\t" % (i * 100.0 / len(self._class_to_index)))
            sys.stdout.flush()

            seen = [False]*len(self._class_to_index)

            q = Queue()
            q.put(i)
            seen[i] = True

            # Ancestors traversal
            while not q.empty():
                class_index = q.get()

                for j in self._class_parents[class_index]:
                    if j == i:
                        classes_seen_in_cycles[i] = True

                    if not seen[j]:
                        seen[j] = True
                        q.put(j)

            # Adding ancestors count
            statistics["inferred-subsumptions-number"] += seen.count(True) - 1 - len(self._class_parents[i])

        print("\rComputing inferred subsumptions 100 %\t\t")
        print(str(classes_seen_in_cycles.count(True)) + " classes were detected in cycles")

        # This variable indicates whether the depth algorithm can make multiple passes. Default is false
        # It can be set to true only if cycles have been computed and none were found
        depth_multiple_passes = False

        # Cycles computation (only from classes in cycles)
        if cycles_computation:
            # First, we save the number of classes in cycles
            statistics["classes-in-cycles"] = classes_seen_in_cycles.count(True)

            # Then, cycles are computed
            index_cycles = []
            classes_in_cycles = [i for i, t in enumerate(classes_seen_in_cycles) if t]
            for i in range(0, len(classes_in_cycles)):
                sys.stdout.write("\rComputing cycles %i %%\t\t" % (i * 100.0 / len(classes_in_cycles)))
                sys.stdout.flush()

                q = Queue()
                classes_seen = [False]*len(self._class_to_index)
                classes_seen[classes_in_cycles[i]] = True
                q.put((classes_seen, classes_in_cycles[i]))

                # Paths discovery
                while not q.empty():
                    current = q.get()

                    for j in self._class_parents[current[1]]:
                        if classes_seen_in_cycles[j]:
                            # Cycle detected
                            if j == classes_in_cycles[i]:
                                cycle = {i for i, t in enumerate(current[0]) if t}

                                if not self._existing_cycle(cycle, index_cycles):
                                    index_cycles.append(cycle)

                            # Else, exploration
                            elif not current[0][j]:
                                new_classes_seen = list(current[0])
                                new_classes_seen[j] = True
                                q.put((new_classes_seen, j))

            statistics["cycles"] = []
            for i_cycle in index_cycles:
                c_cycle = []
                for k in i_cycle:
                    c_cycle.append(self._index_to_class[k])
                statistics["cycles"].append(c_cycle)

            statistics["cycles-number"] = len(statistics["cycles"])
            depth_multiple_passes = statistics["cycles-number"] == 0  # If there are cycles, 1 pass can only for depth
            print("\rComputing cycles 100 %\t\t")

        # Depth (one traversal if cycles exist in the ontology)
        depths = {}
        q = Queue()
        statistics["depth"] = 0

        for i in top_level_classes:
            q.put(i)
            depths[i] = 0

        while not q.empty():
            sys.stdout.write("\rComputing depth %i %%\t\t" % (len(depths) * 100.0 / len(self._class_to_index)))
            sys.stdout.flush()

            class_index = q.get()

            for child in self._class_children[class_index]:
                if child not in depths or (depth_multiple_passes and depths[child] < depths[class_index] + 1):
                    depths[child] = depths[class_index] + 1
                    q.put(child)

                    if depths[child] > statistics["depth"]:
                        statistics["depth"] = depths[child]

        print("\rComputing depth 100 %\t\t")
        print(str(len(self._index_to_class) - len(depths)) + " classes weren't considered during depth computation")

        return statistics

    @staticmethod
    def _existing_cycle(cycle, cycles):
        for c in cycles:
            if len(c) == len(cycle) and cycle == c:
                return True

        return False
