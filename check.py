import operator
from config import tprint


class Satisfiability:
    def __init__(self, scc, clauses, no_variables):
        self.scc = scc
        self.clauses = clauses
        self.variables = {str(variable): 0 for variable in range(1, int(no_variables)+1)}

    def run(self):
        negate = self.negation()
        print("By negation: {}".format(negate))
        self.scc = dict(sorted(self.scc.items(), reverse=True))
        for key, value in self.scc.items():
            value = [self.abs_variable(raw_var) for raw_var in value]
            value = self.check_validity(value)
            if not value:
                tprint("Failed in assignment of SCC, last assignment: {}".format(str(self.variables)))
                break
            else:
                for var in value:
                    self.variables[var[0]] = var[1]
        boo = self.bool()
        print("By assignment of SCC: {}".format(boo))
        if negate and boo:
            print("FORMULA SATISFIABLE")
            print(self.variables)
        else:
            print("FORMULA UNSATISFIABLE")

    def check_validity(self, abs_scc):
        done = True
        tprint("Trying...{}".format(abs_scc))
        for scc in abs_scc:
            if self.variables[scc[0]] == 0:
                pass
            elif self.variables[scc[0]] == operator.not_(scc[1]):            # Opposites
                done = False
                break
            else:
                pass
        if not done:
            tprint("Trying opposite...")
            for scc in abs_scc:
                if self.variables[scc[0]] == 0:
                    pass
                elif self.variables[scc[0]] == operator.not_(scc[1]):  # Opposites
                    idx = abs_scc.index(scc)
                    scc[1] = operator.not_(scc[1])
                    abs_scc[idx] = scc
                else:
                    done = False
                    break
        if done:
            return abs_scc
        else:
            return False

    def negation(self):
        sat = 0
        for components in self.scc.values():
            if sat != 0:
                break
            else:
                for component in components:
                    if str(-int(component)) in components:
                        sat = False
                        break
        if sat == 0:
            sat = True
        return sat

    def abs_variable(self, var):
        return [str(abs(int(var))), int(var) > 0]

    def clause_bool(self, clause, unit=False):
        if not unit:                            # 2-SAT
            [v1, v2] = clause.split(" ")
            return [[str(abs(int(v1))), int(v1) > 0], [str(abs(int(v2))), int(v2) > 0]]
        else:                                   # Unit clause
            return [str(abs(int(clause))), int(clause) > 0]

    def bool(self):
        default = True
        for clause in self.clauses:
            if len(clause) > 2:
                [v1, v2] = self.clause_bool(clause, unit=False)
                if v1[1] == self.variables[v1[0]] or v2[1] == self.variables[v2[0]]:
                    pass
                else:
                    default = False
            else:
                v1 = self.clause_bool(clause, unit=True)
                if not v1[1] == self.variables[v1[0]]:
                    default = False
        return default
