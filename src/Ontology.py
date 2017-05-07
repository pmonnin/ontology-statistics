import sys
from queue import Queue

__author__ = "Pierre Monnin"


class Ontology:
    def __init__(self, class_to_index, index_to_class, class_parents, class_children):
        self._class_to_index = class_to_index
        self._index_to_class = index_to_class
        self._class_parents = class_parents
        self._class_children = class_children

    def get_statistics(self):
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

        # Number of inferred subsumptions
        statistics["inferred-subsumptions-number"] = 0
        for i in range(0, len(self._class_to_index)):
            sys.stdout.write("\rComputing inferred subsumptions %i %%\t\t" % (i * 100.0 / len(self._class_to_index)))
            sys.stdout.flush()

            seen = [False]*len(self._class_to_index)

            seen[i] = True
            q = Queue()
            for j in self._class_parents[i]:
                q.put(j)
                seen[j] = True

            # Ancestors traversal
            while not q.empty():
                class_index = q.get()

                for j in self._class_parents[class_index]:
                    if not seen[j]:
                        seen[j] = True
                        q.put(j)

            # Adding ancestors count
            statistics["inferred-subsumptions-number"] += seen.count(True) - 1 - len(self._class_parents[i])

        print("\rComputing inferred subsumptions 100 %\t\t")

        # Cycles
        index_cycles = []
        for i in range(0, len(self._class_to_index)):
            sys.stdout.write("\rComputing cycles %i %%\t\t" % (i * 100.0 / len(self._class_to_index)))
            sys.stdout.flush()

            seen = {}
            q = Queue()
            q.put([i])
            seen[str([i])] = True

            # Paths discovery
            while not q.empty():
                current_path = q.get()

                for j in self._class_children[current_path[len(current_path) - 1]]:
                    # Cycle detected
                    if j == i:
                        cycle = list(current_path)
                        cycle.append(j)

                        if str(cycle) not in seen:
                            seen[str(cycle)] = True

                            if not self._existing_cycle(cycle, index_cycles):
                                index_cycles.append(cycle)

                    # Else, exploration
                    elif j not in current_path:
                        new_path = list(current_path)
                        new_path.append(j)

                        if str(new_path) not in seen:
                            seen[str(new_path)] = True
                            q.put(new_path)

        statistics["cycles"] = []
        for i_cycle in index_cycles:
            c_cycle = []
            for k in i_cycle:
                c_cycle.append(self._index_to_class[k])
            statistics["cycles"].append(c_cycle)

        statistics["cycles-number"] = len(statistics["cycles"])
        existing_cycles = statistics["cycles-number"] > 0
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
                if child not in depths or (not existing_cycles and depths[child] < depths[class_index] + 1):
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
            if len(c) == len(cycle):
                # Remove last component (same as first one)
                short_cycle = cycle[0:len(cycle) - 1]
                short_c = c[0:len(c) - 1]

                # Find where the first element of short_cycle is in short_c
                start_index = 0
                while start_index < len(short_c) and short_c[start_index] != short_cycle[0]:
                    start_index += 1

                # Compare rest of cycle
                if start_index < len(short_c):
                    i = 1
                    similar = True
                    while i < len(short_cycle) and similar:
                        short_c_index = start_index + i

                        if short_c_index >= len(short_c):
                            short_c_index -= len(short_c)

                        if short_c[short_c_index] != short_cycle[i]:
                            similar = False

                        i += 1

                    if similar:
                        return True

        return False
