import os


class CNFReader:
    def __init__(self, filename):
        self.filename = filename
        self.file_loc = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_files", filename))
        self.parsed = {"parsed": False,
                       "comments": [],
                       "parameters": {"format": None,
                                      "variables": None,
                                      "clauses": None
                                      },
                       "clauses": []
                       }
        self.section = (25 * "=")

    def read(self):
        try:
            with open(self.file_loc, 'r') as infile:
                lines = infile.readlines()
            return lines
        except FileNotFoundError:
            raise Exception("The file {} is not found. Please upload in the test_files folder and try again".format(self.filename))

    def parse(self):                # TODO throw errors for 3-SAT or invalid variable/clause numbers?
        if not self.parsed['parsed']:
            clauses = ""
            for line in self.read():
                if line[0] == "c":                          # If it is a comment
                    self.parsed['comments'].append(line.strip('c ').replace("\n", ""))
                elif line[0] == "p":                        # If stating the problem parameters
                    problem = line.replace("\n", "").split(" ")
                    [__,
                     self.parsed['parameters']['format'],
                     self.parsed['parameters']['variables'],
                     self.parsed['parameters']['clauses']] = problem
                else:
                    clauses += line
            self.parsed["clauses"] = [clause.replace("\n", "").strip(" ") for clause in clauses.split("0") if clause.replace("\n", "").strip(" ") != ""]
            self.parsed['parsed'] = True

    def visualise(self, parsed):
        print(self.section)
        if len(parsed['comments']) != 0:
            print("Comments: {}".format(" | ".join(parsed['comments'])))
        else:
            print("Comments: None")
        print("Format: {txt_format}\n"
              "Number of Variables: {variables}\n"
              "Number of Clauses: {clauses}".format(txt_format=parsed['parameters']['format'],
                                                    variables=parsed['parameters']['variables'],
                                                    clauses=parsed['parameters']['clauses']))
        print(self.section)
        for clause in parsed['clauses']:
            print(clause)
        print(self.section)
