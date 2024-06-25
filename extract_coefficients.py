from matrixbuilder import MatrixBuilding

def buildDatasets(path: str, matrices: MatrixBuilding):
    dataset_human = []
    dataset_machine = []

    with open(path) as file:
        dataset = file.read()
           
    for line in dataset.split("\n"):
        line_list = line.split(" ")
        dataset_human.append(line_list[2])
        dataset_machine.append(matrices.findCoefficient(line_list[0], line_list[1], "N"))

    return dataset_human, dataset_machine


	
	 
