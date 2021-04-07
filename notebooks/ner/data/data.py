import pandas as pd

# diretorios = ['AnatEM-IOB', 'BC2GM-IOB', 'BC4CHEMD', 'BC5CDR-chem-IOB', 'BC5CDR-disease-IOB', 'BC5CDR-IOB', 'BioNLP09-IOB', 'BioNLP11EPI-IOB', 'BioNLP11ID-chem-IOB', 'BioNLP11ID-ggp-IOB', 'BioNLP11ID-IOB', 'BioNLP11ID-species-IOB', 'BioNLP13CG-cc-IOB', 'BioNLP13CG-cell-IOB', 'BioNLP13CG-chem-IOB', 'BioNLP13CG-ggp-IOB', 'BioNLP13CG-IOB', 'BioNLP13CG-species-IOB', 'BioNLP13GE-IOB', 'BioNLP13PC-cc-IOB', 'BioNLP13PC-chem-IOB', 'BioNLP13PC-ggp-IOB', 'BioNLP13PC-IOB', 'CRAFT-cc-IOB', 'CRAFT-cell-IOB', 'CRAFT-chem-IOB', 'CRAFT-ggp-IOB', 'CRAFT-IOB', 'CRAFT-species-IOB', 'Ex-PTM-IOB', 'linnaeus-IOB', 'linnaeus-IOB']

# diretorios = ['AnatEM-IOB', 'BC2GM-IOB', 'BC4CHEMD', 'BC5CDR-chem-IOB', 'BC5CDR-disease-IOB', 'BC5CDR-IOB', 'BioNLP09-IOB', 'BioNLP11EPI-IOB', 'BioNLP11ID-chem-IOB', 'BioNLP11ID-ggp-IOB', 'BioNLP11ID-IOB', 'BioNLP11ID-species-IOB', 'BioNLP13CG-cc-IOB', 'BioNLP13CG-cell-IOB']

diretorios = ['AnatEM-IOB', 'BC5CDR-IOB']

train = pd.DataFrame({'word': [], 'label': []})
test = pd.DataFrame({'word': [], 'label': []})
devel = pd.DataFrame({'word': [], 'label': []})

train = train.reindex(columns=['word', 'label'])
test = test.reindex(columns=['word', 'label'])
devel = devel.reindex(columns=['word', 'label'])


Anatomy = ['Anatomy', 'Anatomical_system', 'Developing_anatomical_structure', 'Immaterial_anatomical_entity']
Gene = ['Gene', 'Regulon-operon', 'Gene_or_gene_product', 'SO', 'GGP', 'GENE']
Chemical = ['Chemical', 'Simple_chemical', 'CHEBI']
Disease = ['Disease']
Protein = ['Protein', 'Amino_acid']
Organism = ['Organism', 'Organism_subdivision', 'Organism_substance']
Cancer = ['Cancer']
Organ = ['Organ']
Cell = ['Cell', 'Cellular_component', 'Complex', 'CL', 'GO']
Tissue = ['Tissue', 'Multi-tissue_structure']
Pathology = ['Pathology', 'Pathological_formation']

Tags = [Anatomy, Gene, Chemical, Disease, Protein, Organism, Cancer, Organ, Cell, Tissue, Pathology]

for diretorio in diretorios:
    local_train = pd.read_csv('sources/' + diretorio+'/train.tsv', delimiter='\t', names=['word', 'label'], quoting=3, error_bad_lines=False)
    local_test = pd.read_csv('sources/' + diretorio+'/test.tsv', delimiter='\t', names=['word', 'label'], quoting=3, error_bad_lines=False)
    local_devel = pd.read_csv('sources/' + diretorio+'/devel.tsv', delimiter='\t', names=['word', 'label'], quoting=3, error_bad_lines=False)

    #print(diretorio, ':', sorted(list(set(df['label'].values))))

    train = train.append(local_train, ignore_index=True, sort=False)
    test = test.append(local_test, ignore_index=True, sort=False)
    devel = devel.append(local_devel, ignore_index=True, sort=False)

print(train.head())
#print(sorted(list(set(train['label'].values))))
train = train.dropna()
test = test.dropna()
devel = devel.dropna()
# for tag in Tags:
# 	for string in tag:
# 		train = train.replace(regex = r'{}'.format(string), value = tag[0])	
# 		test = test.replace(regex = r'{}'.format(string), value = tag[0])
# 		devel = devel.replace(regex = r'{}'.format(string), value = tag[0])


# print(sorted(list(set(train['label'].values))))
# print(train.head())
print('aquiiiiiiiiii')
train.to_csv('tratados/train-AnatEM-BC5CDR.tsv', sep='\t', index=False, header=False)
test.to_csv('tratados/test-AnatEM-BC5CDR.tsv', sep='\t', index=False, header=False)
devel.to_csv('tratados/devel-AnatEM-BC5CDR.tsv', sep='\t', index=False, header=False)
#print(df.loc[df['label'] == 'B-Taxon'])


